import os
import pandas as pd
import openai
import json
from openai import OpenAI
from datetime import datetime

from utils import load_api_key


csv_file = 'database/word_db.csv'

def search_word_JE(word, category, df):
    api_key = load_api_key()

    client = OpenAI(
        api_key=api_key
    )

    request_data = {
        "word": "日本語の単語の英語翻訳",
        "pronounce": "検索された単語の発音記号",
        "example_sentence": "検索された単語の例文の和訳",
        "translated_sentence" : "検索された単語の例文",
    }

    message = f"""
    日本語の単語 '{word}' を英語に翻訳し、その英単語を "word" フィールドに、発音記号を "pronounce" フィールドに、例文を "translated_sentence" フィールドに格納してください。
    意味は文章ではなく英単語でお願いします。
    発音記号は rʌn のように正しいフォーマットで返してください。
    例文の和訳も一緒に返してください。
    以下JSON形式で生成してください。
    {json.dumps(request_data, ensure_ascii=False)}
    """

    # ChatGPT API へのリクエストを送信
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ],
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.5,
        top_p=1,
    )

    #print("API Response: ", response)

    try:
        output = response.choices[0].message.content.strip()
        data_json = json.loads(output)  

        print("Parsed JSON: ", data_json)

        english_word = data_json.get('word', None)

        # 英単語が正しく取得されなかった場合
        if not english_word or english_word == word:  
            raise ValueError(f"Failed to retrieve English word from response: {english_word}")

    except json.JSONDecodeError:
        print("Error: Could not decode JSON from response. Check the response format.")
        return
    except Exception as e:
        print(f"Error: {e}")
        return

    # 単語が既存か新規かの判定: 既存している場合二つのカラムのカウントを+1
    if english_word in df['Word'].values:
        df.loc[df['Word'] == english_word, 'Search Count'] += 1
        df.loc[df['Word'] == english_word, 'Learning Point'] += 1
    else:

        new_row = pd.DataFrame({
            "Word": [english_word],  
            "Meaning": [word],  
            "Pronounce": [data_json.get('pronounce', '')],
            "Example Sentence": [data_json.get('example_sentence', '')],
            "Translated Sentence": [data_json.get('translated_sentence', '')],
            "Search Count": [1],
            "Add Date": [datetime.now().strftime('%Y-%m-%d')],
            "Category": [category],
            "Importance": ["0"],
            "Done": [0],
            "Learning Point": [1]
        })
        df = pd.concat([df, new_row], ignore_index=True)

    df.to_csv(csv_file, index=False)

    search_count = df.loc[df['Word'] == english_word, 'Search Count'].values[0]
    return {
        "word": english_word,
        "meaning": word,
        "pronounce": data_json.get('pronounce', ''),
        "example_sentence": data_json.get('example_sentence', ''),
        "translated_sentence": data_json.get('translated_sentence', ''),
        "data": df.loc[df['Word'] == english_word, 'Add Date'].values[0],
        "search_count": search_count
    }

def main(word, category, df):
    # CSVファイルが存在しない場合は新規作成
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=[
            "Word", "Meaning", "Pronounce", "Example Sentence", 
            "Translated Sentence", "Search Count", "Add Date", 
            "Category", "Importance", "Done", "Learning Point"
        ])
        df.to_csv(csv_file, index=False)
    df = pd.read_csv(csv_file)

    return search_word_JE(word, category, df)