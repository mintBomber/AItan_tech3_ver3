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
    client = OpenAI(api_key=api_key)


    spell_check_prompt = f"""
                あなたは英語のスペルチェッカーです。以下の単語のスペルを確認してください。
                単語: {word}
                この単語がスペルミスの場合、"正しいスペル: [正しい単語]" として正しいスペルを提案してください。
                正しいスペルがある場合、その単語を返してください。
                スペルミスがない場合は "正しいスペル: {word}" としてそのまま返してください。
                """

    spell_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": spell_check_prompt}
        ],
        max_tokens=100,
        temperature=0.5,
    )

    spell_check_output = spell_response.choices[0].message.content  

    if "正しいスペル" in spell_check_output:
        correct_spelling = spell_check_output.split("正しいスペル: ")[1].strip()
        word = correct_spelling  # word を正しいスペルに上書き

    if word in df['Word'].values:
        df.loc[df['Word'] == word, 'Search Count'] += 1
        df.loc[df['Word'] == word, 'Learning Point'] += 1
    else:
        new_row = pd.DataFrame({
                "Word": [word],
                "Meaning": [""],
                "Pronounce": [""],
                "Example Sentence": [""],
                "Translated Sentence": [""],
                "Search Count": [1],
                "Add Date": [datetime.now().strftime('%Y-%m-%d')],
                "Category": [category],
                "Importance": ["0"],
                "Done": [0],
                "Learning Point": [1]
        })
        df = pd.concat([df, new_row], ignore_index=True)

    request_data = {
                "word": word,
                "meaning": "検索された単語の意味",
                "pronounce": "検索された単語の発音記号",
                "example_sentence": "検索された単語の例文の和訳",
                "translated_sentence": "検索された単語の例文",
            }
    message = f"""
                あなたはベテランの英語教師です。
                {word}の意味と発音記号、その例文の和訳、そしてその例文(英語)を教えてください。
                意味は日本語で、発音記号はrʌnのようにお願いします。
                以下JSON形式で生成してください。
                {json.dumps(request_data, ensure_ascii=False)}
                """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ],
        max_tokens=200,
        temperature=0.5,
    )

    output = response.choices[0].message.content  
    data_json = json.loads(output)

    search_count = df.loc[df['Word'] == word, 'Search Count'].values[0]
    df.loc[df['Word'] == word, 'Meaning'] = data_json['meaning']
    df.loc[df['Word'] == word, 'Pronounce'] = data_json['pronounce']
    df.loc[df['Word'] == word, 'Example Sentence'] = data_json['example_sentence']
    df.loc[df['Word'] == word, 'Translated Sentence'] = data_json['translated_sentence']
    df.loc[df['Word'] == word, 'Add Date'] = datetime.now().strftime('%Y-%m-%d')

    df.to_csv(csv_file, index=False)

    return {
                "word": word,  # 正しいスペル
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
        df = pd.DataFrame(columns=["Word", "Meaning", "Pronounce", "Example Sentence", "Translated Sentence",
                                   "Search Count", "Add Date", "Category", "Importance", "Done", "Learning Point"
                                   ])
        df.to_csv(csv_file, index=False)
    df = pd.read_csv(csv_file)

    return search_word(word, category, df)