import os
import pandas as pd
import openai
import json
from openai import OpenAI
from datetime import datetime
from utils import load_api_key

csv_file = 'database/word_db.csv'

def search_word(word, category, df):
    api_key = load_api_key()

    client = OpenAI(
        api_key=api_key
    ) 

    if word in df['Word'].values:
        df.loc[df['Word'] == word, 'Search Count'] += 3
    else:
        new_row = pd.DataFrame({
            "Word": [word], 
            "Meaning": [""], 
            "Pronounce": [""], 
            "Example Sentence": [""], 
            "Translated Sentence": [""], 
            "Search Count": [3],
            "Add Date": [datetime.now().strftime('%Y-%m-%d')], 
            "Category": [category], 
            "Importance": ["0"]
        })
        df = pd.concat([df, new_row], ignore_index=True)
    
    request_data = {
                "meaning": "検索された単語の意味",
                "pronounce": "検索された単語の発音記号",
                "example_sentence": "検索された単語の例文の和訳",
                "translated_sentence" : "検索された単語の例文",
    }
    
    message = f"""
                {word}の意味と発音記号、その例文の和訳と例文を教えてください。
                発音記号はrʌnのようにお願いします。
                意味は日本語、例文は英語でお願いします。
                以下JSON形式で生成してください。
                {json.dumps(request_data, ensure_ascii=False)}
                """
    
    response = client.chat.completions.create(
                model="gpt-3.5-turbo",  #4o-minにする
                messages=[
                    {"role": "user", "content": f"/japanese {message}"}  
                ],
                max_tokens=100,  
                n=1, 
                stop=None,  
                temperature=0.5,  
                top_p=1,  
    )

    output = response.choices[0].message.content
    data_json = json.loads(output)
    # print(data_json)
    
    search_count = df.loc[df['Word'] == word, 'Search Count'].values[0]
    df.loc[df['Word'] == word, 'Meaning'] = data_json['meaning']
    df.loc[df['Word'] == word, 'Pronounce'] = data_json['pronounce']
    df.loc[df['Word'] == word, 'Example Sentence'] = data_json['example_sentence']
    df.loc[df['Word'] == word, 'Translated Sentence'] = data_json['translated_sentence']
    df.loc[df['Word'] == word, 'Add Date'] = datetime.now().strftime('%Y-%m-%d')

    df.to_csv(csv_file, index=False)

    return {
            "word": word,
            "meaning": data_json['meaning'],
            "pronounce": data_json['pronounce'],
            "example_sentence": data_json['example_sentence'],
            "translated_sentence": data_json['translated_sentence'],
            "data": df.loc[df['Word'] == word, 'Add Date'].values[0], 
            "search_count": search_count
    }

def main(word, category, df):
    # CSVファイルが存在しない場合は新規作成
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=[
            "Word", "Meaning", "Pronounce", "Example Sentence", 
            "Translated Sentence", "Search Count", "Add Date", 
            "Category", "Importance"
        ])
        df.to_csv(csv_file, index=False)

    df = pd.read_csv(csv_file)

    return search_word(word, category, df)