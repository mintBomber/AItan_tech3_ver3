import streamlit as st

from word_quiz.process_word_quiz import process_csv, generate_quiz, decrease_search_count


def display_results(quiz_list): # 文字を大きく
    """クイズの結果を表示する"""
    st.write("## テスト結果")
    # 学習目標
    # st.markdown("<hr style='border:3px solid gray'>", unsafe_allow_html=True)
    
    # スコアに応じたメッセージの表示（中央揃え）
    if st.session_state.score == len(quiz_list):
        st.markdown("<h2 style='text-align: center; color: black;'>Excellent</h2>", unsafe_allow_html=True)
    elif st.session_state.score >= len(quiz_list) * 0.8:
        st.markdown("<h2 style='text-align: center; color: black;'>Great</h2>", unsafe_allow_html=True)
    elif st.session_state.score >= len(quiz_list) * 0.5:
        st.markdown("<h2 style='text-align: center; color: black;'>Nice</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: black;'>Oh my god...</h2>", unsafe_allow_html=True)

    # 学習目標
    st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)

    st.markdown(f"<h3 style='text-align: right; color: black;'>Score:　{st.session_state.score}/{len(quiz_list)}</h3>", unsafe_allow_html=True)
    # st.write(f"Score: {st.session_state.score}/{len(quiz_list)}")
    
    # 2列で結果を表示
    col1, col2 = st.columns(2)  

    for i, res in enumerate(st.session_state.results):
        with col1 if i % 2 == 0 else col2:  # 奇数はcol1、偶数はcol2に表示
            # 正解か不正解でアイコンを決定
            if res['result']:
                st.success(f"⚪︎　{res['word']} : {res['meaning']}")
            else:
                st.info(f"×　{res['word']} : {res['meaning']}")
                

def display_quiz(quiz_list):
    """生成したクイズのリストから、順に取り出し表示する"""
    if 'current_quiz_index' not in st.session_state:
        st.session_state.current_quiz_index = 0
        st.session_state.score = 0
        st.session_state.results = []  # クイズの結果を保存するリスト
        st.session_state.show_results = False  # 結果画面を表示するかどうかのフラグ
    
    # クイズが全て終了し、結果画面が表示される場合
    if st.session_state.show_results == True:
        display_results(quiz_list)  # 結果画面の表示を別の関数に分ける
        return  # 結果画面を表示後、関数を終了する

    # 今回のクイズを取得
    current_quiz = quiz_list[st.session_state.current_quiz_index]

    st.markdown("<hr style='border:1px solid gray'>", unsafe_allow_html=True)

    st.error(f"**問題:** {current_quiz['question']}")
    # st.markdown(f"""
    # <div style='font-size: 15px; font-weight: bold; margin-bottom: 20px;'>問題: {current_quiz['question']}</div>
    # """, unsafe_allow_html=True)

    # 選択肢の表示とユーザーの選択を取得
    user_choice = st.radio("選択肢:", current_quiz['choice4'])

    # 提出ボタン
    if st.button("回答"):
        result = {}  # 結果を保存するための辞書
        result['word'] = current_quiz['word']
        result['meaning'] = current_quiz['meaning']

        if user_choice == current_quiz['correct_answer']:
            st.session_state.score += 1
            result['result'] = True

            # search_countを-1する
            decrease_search_count(current_quiz['word'])
        else:
            result['result'] = False

        # 結果をリストに追加
        st.session_state.results.append(result)

        # 次のクイズに進む
        if st.session_state.current_quiz_index < len(quiz_list) - 1:
            st.session_state.current_quiz_index += 1
            st.rerun() # 画面を再描画して次のクイズを表示
        else:
            st.write(f"すべての問題が終了しました。正解数: {st.session_state.score}/{len(quiz_list)}")

            st.session_state.show_results = True

            # 結果画面の遷移
            if st.button("結果画面"):  
                st.rerun()  # 画面を再描画して結果画面を表示


def main():
    """クイズがスタートする画面表示"""
    st.title("単語テスト")
    
    if 'quiz_list' not in st.session_state:
        # 問題モードの選択
        quiz_mode = st.radio(
            "問題のタイプを選択してください:", 
            ('基本単語帳もーど', '論文もーど', 'ガッチャンコもーど'), 
            horizontal=True)
        
        # カテゴリの選択
        quiz_category = st.selectbox(
            "出題の方法を指定してください:",
            ['認知科学', '強化学習', 'データ分析', 'その他'],
            index = 0)
        
        # 出題方法の選択
        quiz_type = st.selectbox(
            "出題の方法を指定してください:",
            ['4択単語問題：日→英', '4択単語問題：英→日'],
            index = 0)
        
        # 出題方法からファイルパスを選ぶ
        if quiz_mode == "基本単語帳もーど":
            file_name="word_db.csv"
        elif quiz_mode == "論文もーど":
            file_name="paper_db.csv"
        elif quiz_mode == "ガッチャンコもーど":
            file_name=["word_db.csv", "paper_db.csv"]
        
        # 問題数を指定する
        n_word_test = st.selectbox(
            "問題数を指定してください:",
            [2, 5, 10, 20, 50],
            index = 1)
        
        if st.button("この設定で開始する"):
            top_words = process_csv(file_name, n_word_test, quiz_mode, quiz_category) # CSVの処理
            print(top_words)
            quiz_list = generate_quiz(top_words, quiz_type)  # クイズの生成
            st.session_state.quiz_list = quiz_list  # セッション状態に保存
            st.rerun()
    
    # クイズが生成されていれば問題の表示
    elif 'quiz_list' in st.session_state:
        display_quiz(st.session_state.quiz_list)


main()

if __name__ == '__main__':
    main()