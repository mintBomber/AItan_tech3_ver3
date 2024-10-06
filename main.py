import time
import streamlit as st
import pandas as pd
from datetime import datetime
import os


def main():
    st.set_page_config(
        page_title="AI単", 
        page_icon="images/icon.png",
    )

    if 'next_screen' not in st.session_state:
        st.markdown("<h1 style='text-align: center; color: black;'>&emsp;&emsp;&emsp;&emsp;AI単</h1>", unsafe_allow_html=True)
        # ホーム画面表示
        col1, col2, col3= st.columns([1,1,1]) # 中央寄せのためにカラムを追加
        with col2: # 中央のカラムにタイトルを表示
            st.image("images/icon.png", width=400)
            #st.markdown(f'<img src="images/nabe_popping.gif" width="300">', unsafe_allow_html=True)

        # setting.csvファイルのパスを指定
        setting_csv_path = "database/setting.csv"
            
        # setting.csvファイルから設定を読み込む
        if os.path.exists(setting_csv_path):
            df = pd.read_csv(setting_csv_path)
            if not df.empty:
                continue_days = df.at[0, 'ContinueDays']
                user_name = df.at[0, 'UserName']
    
                # メッセージを生成
                if continue_days < 4:
                    message = f"おかえりなさい、{user_name}"
                elif continue_days < 7:
                    message = f"最近頑張ってるね、{user_name}"
                elif continue_days < 14:
                    message = f"{user_name}、継続は力なりだね"
                else:
                    message = f"ログイン{continue_days}日目だね、すごいよ{user_name}！"
    
                # メッセージを表示
                st.markdown(f"<p style='text-align: center;'>st.markdown(f"<p style='text-align: center;'>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;{message}</p>", unsafe_allow_html=True)st.markdown(f"<p style='text-align: center;'>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;{message}</p>", unsafe_allow_html=True)&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;{message}</p>", unsafe_allow_html=True)

        # ページを読み込んだ瞬間にword_db.csvを更新
        update_word_db("database/word_db.csv")
        update_word_db("database/paper_db.csv")
        update_final_login()

        time.sleep(3)
        st.session_state['next_screen'] = True
        st.rerun()

    word_search = st.Page(page="word_search/display_word_search.py", title="単語検索", icon=":material/home:", default=True)
    word_quiz = st.Page(page="word_quiz/display_word_quiz.py", title="単語テスト", icon=":material/quiz:")
    pb_chart = st.Page(page="pb_chart/visualize_graph.py", title="Voca鍋", icon=":material/apps:")
    paper_upload = st.Page(page="paper_analysis/display_paper_analysis.py", title="論文登録", icon=":material/description:")
    my_data = st.Page(page="my_learning/learning_display.py", title="学習データ", icon=":material/monitoring:")
    trend_analysis = st.Page(page="trend_analysis/radar_chart.py", title="単語傾向", icon=":material/pentagon:")
    setting = st.Page(page="my_setting/setting.py", title="設定", icon=":material/settings:")
    
    # スピナーを表示しつつナビゲーションを実行
    with st.spinner('ページを読み込んでいます...'):
        pg = st.navigation([word_search, pb_chart, word_quiz, paper_upload, my_data, trend_analysis, setting])
        pg.run()


def update_word_db(file_name):
    """
    word_db.csvを読み込み、DuringとWeightを計算して更新する関数
    """
    try:
        df = pd.read_csv(file_name)

        # 単語が一つも登録されていない場合は処理をスキップ
        if df.empty:
            return

        # Add Date列が日付型であることを確認し、空欄を現在の日時で埋める
        df['Add Date'] = pd.to_datetime(df['Add Date'], errors='coerce').fillna(datetime.now().strftime('%Y-%m-%d'))

        now = datetime.now()
        df['During'] = abs((now - df['Add Date']).dt.days)  # 現在の日付との差を日数で計算

        # Weightを計算
        df['Importance'] = df['During'].apply(lambda x: 1 if x <= 7 else 2 if x <= 14 else 3 if x <= 21 else 4)

        # During列を削除
        df = df.drop('During', axis=1)

        df.to_csv(file_name, index=False)

    except Exception as e:
        st.error(f"word_db.csvの更新に失敗しました: {e}")

    except Exception as e:
        st.error(f"word_db.csvの更新に失敗しました: {e}")


def update_final_login():
    """
    "setting" フォルダ内の "setting.csv" の "FinalLogin" カラムを現在の日付で更新する関数
    """
    try:
        # setting.csvファイルのパスを指定
        setting_csv_path = "database/setting.csv"
        df = pd.read_csv(setting_csv_path)

        today = datetime.now().strftime('%Y-%m-%d')

        # 最初の行のFinalLoginとContinueDaysを更新する
        if not df.empty:
            final_login = df.at[0, 'FinalLogin']
            
            if final_login == today: # 今日が最終ログインなら何もしない
                return
            elif final_login == (datetime.now() - pd.Timedelta(days=1)).strftime('%Y-%m-%d'): # 最終ログインが昨日ならContinueDaysを1増やす
                df.at[0, 'ContinueDays'] += 1
            else: # それより前ならContinueDaysを1にリセット
                df.at[0, 'ContinueDays'] = 1
            
            # FinalLoginを今日の日付に更新
            df.at[0, 'FinalLogin'] = today

        # setting.csvファイルを上書き保存
        df.to_csv(setting_csv_path, index=False)

    except Exception as e:
        print(f"setting.csvの更新に失敗しました: {e}")

if __name__ == '__main__':
    main()
