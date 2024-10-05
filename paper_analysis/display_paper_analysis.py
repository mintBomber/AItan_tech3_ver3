import streamlit as st
import pandas as pd
import spacy
from collections import Counter

from paper_analysis.process_papar_analysis import *


# SpaCyのモデルをロード（英語モデル）
nlp = spacy.load('en_core_web_sm')

# タイトル
st.title("英語論文から英単語を抽出する")

# ヘルプテキスト
help_text1 = '''
    ### 複合語の解析オプションの説明:
    | オプション名 | 説明 | 具体例 | 
    |:-----|:-----:|:-----|
    | **副詞修飾** | 副詞 + 形容詞, 動詞 | Highly accurate, Efficiently train |
    | **形容詞修飾** | 形容詞 + 名詞 | Neural Network | 
    | **複合名詞** | 名詞 + 名詞 | Data set | 
    | **分詞** | 名詞 + 動詞(V-ing, V-ed) | Machine learning, Trained model | 
    '''

# 品詞の選択オプション
pos_options = st.multiselect(
    "抽出したい品詞と複合語のオプションを選択してください:",
    options=['名詞', '動詞', '形容詞', '副詞', '形容詞修飾', '複合名詞', '分詞', '副詞修飾'],
    default=['名詞', '動詞', '形容詞', '副詞'],
    help=help_text1  # ヘルプテキストを追加
)

# 表示する単語数のスライダー
word_count_slider = st.slider("表示する単語数を選択してください:", min_value=10, max_value=200, value=100, step=10)

# PDFファイルのアップロード
uploaded_file = st.file_uploader("PDFファイルをアップロードしてください:", type="pdf")

# 分野タグの選択プルダウン
field_options = st.multiselect(
    "論文の分野を選択してください:",
    options=['強化学習', '認知科学', 'データ分析', 'その他'],
)

help_text2 = '''
    ### 翻訳モデルの選択オプションの説明:
    | オプション名 | 説明 | 和訳 | 
    |:-----|:-----:|:-----|
    | **Google** | Google翻訳を使用 | 精度の高い翻訳が可能である一方、専門用語には弱いです。|
    | **ChatGPT** | OpenAIのChatGPTを使用 | 翻訳の精度はやや低いものの、特定分野に適した訳を作ることができます。|
    '''

# 翻訳に使用するモデルの選択
translation_model = st.selectbox(
    "翻訳に使用するモデルを選択してください:",
    options=['Google', 'ChatGPT'],
    help = help_text2  # ヘルプテキストを追加
)

# プログレスバーの設定
st.write("解析の進行状況:")
process_status = st.empty()
progress_bar = st.progress(0)

# 初期ログの設定
if 'log' not in st.session_state:
    st.session_state['log'] = ""  # 初期化

# ログ表示用のテキストエリア（初期状態）
log_placeholder = st.empty()  # テキストエリアのための空の場所を確保
log_placeholder.text_area("解析ログ", st.session_state['log'], height=200)  # 初期のログを表示


# 解析ボタン
if st.button("解析開始"):
    log = st.session_state['log']  # セッションから現在のログを取得

    if uploaded_file is not None:
        log = update_log(log, "PDFファイルの読み込みを開始します。", log_placeholder)
        
        # PDFのテキストを抽出する
        log = update_log(log, "PDFからテキストを抽出中...", log_placeholder)
        
        text = extract_text_from_pdf(uploaded_file)
        process_status.write("20%")  # プログレスを20%に設定
        progress_bar.progress(20)  # プログレスを20%に設定

        if text:
            log = update_log(log, "テキストの抽出が完了しました！", log_placeholder)
            process_status.write("40%")  # プログレスを40%に設定
            progress_bar.progress(40)  # プログレスを40%に設定

            # テキストをトークン化（品詞分解）
            doc = nlp(text.lower())

            # 単語のフィルタリング
            
            log = update_log(log, "単語を解析中...", log_placeholder)
            
            filtered_words = filter_words(doc, pos_options)
            process_status.write("60%")  # プログレスを60%に設定
            progress_bar.progress(60)  # プログレスを60%に設定

            # 複合語の解析を行う（必要に応じて）
            classified_terms = classify_compound_terms(doc, pos_options)
            for category, terms in classified_terms.items():
                for term in terms:
                    filtered_words.append(term)

            log = update_log(log, "単語フィルタリングと複合語の解析が完了しました！", log_placeholder)
            process_status.write("70%")  # プログレスを70%に設定
            progress_bar.progress(70)  # プログレスを70%に設定

            # be動詞と不要な単語を削除
            be_verbs = ['is', 'are', 'am', 'was', 'were', 'be', 'being', 'been']
            unwanted_words = ['as', 'much', 'also', 'such']
            cleaned_words = clean_words(filtered_words, unwanted_words, be_verbs)

            # 単語の出現頻度をカウント
            word_freq = Counter(cleaned_words)
            most_common_words = word_freq.most_common(word_count_slider)
            progress_bar.progress(80)  # プログレスを80%に設定

            # Learning Pointの計算
            search_count = calculate_search_count(word_count_slider)
            
            # 翻訳部分の呼び出し（display_paper_analysis.pyで）
            log = update_log(log, "単語を翻訳中...", log_placeholder)
            word_list = [word for word, freq in most_common_words]
            translated_words = translate_word_list(word_list, field_options, translation_model)
            process_status.write("90%")  # プログレスを90%に設定
            progress_bar.progress(90)  # プログレスを90%に設定

            log = update_log(log, "単語の翻訳が完了しました！", log_placeholder)

            # 結果をデータフレームにまとめる
            df = pd.DataFrame(most_common_words, columns=['Word', 'Appearance Frequency'])
            df['Meaning'] = df['Word'].map(translated_words)
            df['Category'] = field_options[0] if field_options else "その他"  # 分野タグを追加, デフォルトは"その他"
            df['Learning Point'] = search_count  # Learning Pointを追加
            df['Add Date'] = pd.Timestamp('today').strftime('%Y-%m-%d')
            df['Importance'] = 0
            df['Done'] = 0

            # データフレームを表示
            st.write(df)

            # CSVダウンロード機能
            csv = save_and_update_csv(df, log, log_placeholder).to_csv(index=False, encoding='utf-8')
            
            # 保存が完了したことをユーザーに知らせる
            log = update_log(log, "単語リストの保存が完了しました！", log_placeholder)
            process_status.write("100%")
            progress_bar.progress(100)  # プログレスを100%に設定
            
            st.download_button("CSVファイルとしてダウンロード", csv, file_name="word_list.csv", mime="text/csv")

        else:
            log = update_log(log, "PDFからテキストを抽出できませんでした。", log_placeholder)

    else:
        log = update_log(log, "PDFファイルをアップロードしてください。", log_placeholder)
    
    
    # プログレスバーをリセット
    progress_bar.empty()
    
    # ログに改行を追加
    log += "\n"

    # ログをセッションに保存
    st.session_state['log'] = log