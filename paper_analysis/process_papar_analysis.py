import spacy
import re
import os
import pandas as pd
from unstructured.partition.pdf import partition_pdf
from deep_translator import GoogleTranslator
from openai import OpenAI   # OpenAI APIを使用するためのライブラリ
from utils import load_api_key

# SpaCyのモデルをロード（英語モデル）
nlp = spacy.load('en_core_web_sm')

# ログにメッセージを追加する関数
def update_log(log, new_message, log_placeholder):
    log += new_message + "\n"
    log_placeholder.text_area("解析ログ", log, height=200)  # テキストエリアにログを表示
    return log

# 単語を単数形（レンマ）に変換する関数
def convert_to_singular(word):
    # SpaCyの文書オブジェクトに変換
    doc = nlp(word)
    
    # トークンごとのlemma_属性を使って単数形を取得
    for token in doc:
        return token.lemma_  # レンマ（単数形）を返す

# PDFからテキストを抽出する関数
def extract_text_from_pdf(uploaded_file):
    elements = partition_pdf(file=uploaded_file)
    
    # テキストを結合
    text = ''.join([str(element) for element in elements])
    
    # ハイフンで分割された単語を結合
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    
    # 改行をスペースに置き換え
    text = text.replace('\n', ' ')
    
    # SpaCyでテキストをトークン化
    doc = nlp(text.lower())
    
    # 単数形に変換
    singular_words = [convert_to_singular(token.text) for token in doc]
    
    # 単数形の単語をスペースで結合して再びテキストに戻す
    singular_text = ' '.join(singular_words)
    
    # 「References」以降のテキストを削除
    if 'References' in text:
        text = text.split('References')[0]
        
    return singular_text

# OpenAI APIを使って翻訳する関数
def translate_word_list(words, field_options, translation_model):
    
    if translation_model == 'Google':
        translator = GoogleTranslator(source='en', target='ja')
        translated_words = {word: translator.translate(word) for word in words}

    else:  
        # APIキーをロード
        api_key = load_api_key()
        
        client = OpenAI(
            api_key=api_key
        ) 
        
        translated_words = {}
        
        for word in words:
            try:
                
                message = f"""
                {word}の翻訳をお願いします。
                翻訳は日本語にしてください。
                応答は、{word}に対して1つの日本語訳を提供してください。
                用語に関する説明は不要です。
                {field_options}の分野に適した翻訳を行ってください。
                {field_options}に関連しない単語は、通常の翻訳を行ってください。
                """
                
                # OpenAI APIを呼び出して翻訳
                response = client.chat.completions.create(
                    #model="gpt-3.5-turbo",
                    model = "gpt-4o-mini",
                    messages=[
                        #{"role": "system", "content": "You are a helpful assistant who translates English to Japanese."},
                        #{"role": "user", "content": f"Translate the following word to Japanese: {word}"}
                        {"role": "user", "content": f"/japanese {message}"}  
                    ],
                    temperature=0.3,
                    max_tokens=50,
                    n=1
                )
                
                # 翻訳結果の取得
                translation = response.choices[0].message.content
                translated_words[word] = translation

            except Exception as e:
                translated_words[word] = f"Error: {str(e)}"
                
    return translated_words

# 単語フィルタリング関数
def filter_words(doc, selected_pos_tags):
    filtered_words = []
    for token in doc:
        if (token.pos_ in ['NOUN'] and '名詞' in selected_pos_tags) or \
           (token.pos_ in ['VERB'] and '動詞' in selected_pos_tags) or \
           (token.pos_ in ['ADJ'] and '形容詞' in selected_pos_tags) or \
           (token.pos_ in ['ADV'] and '副詞' in selected_pos_tags):
            filtered_words.append(token.text)
    return filtered_words

# 複合語の解析関数
def classify_compound_terms(doc, pos_options):
    compounds = {'形容詞修飾': [], '複合名詞': [], '分詞': [], '副詞修飾': []}
    for token in doc:
        if token.pos_ == 'ADJ' and token.dep_ == 'amod' and '形容詞修飾' in pos_options:
            compounds['形容詞修飾'].append(f"{token.text} {token.head.text}")
        elif token.pos_ == 'NOUN' and token.dep_ == 'compound' and '複合名詞' in pos_options:
            compounds['複合名詞'].append(f"{token.head.text} {token.text}")
        elif token.tag_ in ['VBG', 'VBN'] and token.head.pos_ == 'NOUN' and '分詞' in pos_options:
            compounds['分詞'].append(f"{token.text} {token.head.text}")
        elif token.pos_ == 'ADV' and token.dep_ == 'advmod' and '副詞修飾' in pos_options:
            compounds['副詞修飾'].append(f"{token.text} {token.head.text}")
    return compounds

# 特定の単語を削除する関数
def clean_words(filtered_words, unwanted_words, be_verbs):
    return [word for word in filtered_words if 
            not re.search(r'\d', word) and  # 数字を含む単語を削除
            re.match(r'^[a-zA-Z ]+$', word) and  # A-Z,a-z,スペース以外の文字を含む単語を削除
            2 < len(word) and
            len(word) < 33 and  # 長すぎる単語を削除
            not any(be_verb in word for be_verb in be_verbs) and  # be動詞を削除
            not any(unwanted_word in word for unwanted_word in unwanted_words)]  # 特定の単語を削除
    
# Learning Pointを計算する関数
def calculate_search_count(word_count_slider):
    # Learning Pointを格納するリスト
    search_count = [] 
    
    # 抽出数の1割を計算(小数点は四捨五入)
    one_tenth = round(word_count_slider * 0.1)
    
    # 抽出数の2割を計算(小数点は四捨五入)
    two_tenths = round(word_count_slider * 0.2)
    
    # 1割の範囲で「5」を追加
    for i in range(one_tenth):
        search_count.append(5) 
    
    # 2割の範囲で「4」を追加
    for i in range(two_tenths):
        search_count.append(4)
    
    # 残りの範囲で「3」を追加
    for i in range(word_count_slider - one_tenth - two_tenths):
        search_count.append(3)
                            
    return search_count

# データをcsvファイルに保存し、タグが異なる場合に更新する関数
def save_and_update_csv(df, log, log_placeholder):
    
    csv_file_path = 'database/paper_db.csv'  # 必要に応じてファイルパスを指定
    current_date = pd.Timestamp('today').strftime('%Y-%m-%d')

    # paper_db.csv が存在するか確認
    if os.path.exists(csv_file_path):
        # 既存のデータを読み込む
        paper_db = pd.read_csv(csv_file_path)
        
        # ファイルが空の場合
        if paper_db.empty:
            log = update_log(log, f"{csv_file_path} は空です。新しいデータを挿入します。", log_placeholder)
            # 新しいデータフレーム df をそのまま保存
            paper_db = df
        else:
            log = update_log(log, f"{csv_file_path} にデータを確認しています...", log_placeholder)
            
            # 新しいデータをループ処理で確認
            for index, new_row in df.iterrows():
                # 既存のデータベースに同じ単語があるかを確認
                existing_row = paper_db[paper_db['Word'] == new_row['Word']]

                if not existing_row.empty:
                    # 既存のデータに対してタグが異なる場合、タグを更新
                    if existing_row['Category'].values[0] != new_row['Category']:
                        log = update_log(log, f"単語 '{new_row['Word']}' のタグを更新: {existing_row['Category'].values[0]} -> {new_row['Category']}", log_placeholder)
                        paper_db.loc[paper_db['Word'] == new_row['Word'], 'Category'] = new_row['Category']
                        paper_db.loc[paper_db['Word'] == new_row['Word'], 'Add Date'] = current_date  # 日付も更新
                        paper_db.loc[paper_db['Word'] == new_row['Word'], 'Importance'] = 0
                        paper_db.loc[paper_db['Word'] == new_row['Word'], 'Done'] = 0
                    else:
                        log = update_log(log, f"単語 '{new_row['Word']}' はすでに存在し、タグも同じです。", log_placeholder)
                else:
                    # 新しい単語の場合、データを追加
                    log = update_log(log, f"単語 '{new_row['Word']}' を新規追加します。", log_placeholder)
                    paper_db = paper_db._append(new_row, ignore_index=True)
    else:
        log = update_log(log, f"{csv_file_path} が存在しません。新しいファイルを作成し、データを保存します。", log_placeholder)
        # ファイルが存在しない場合、新しいデータフレームを保存
        paper_db = df

    # 更新または作成したデータを再度 paper_db.csv に保存
    paper_db.to_csv(csv_file_path, index=False, encoding='utf-8')
    
    return paper_db