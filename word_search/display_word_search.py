import os
import pandas as pd
import streamlit as st
from openai import OpenAI

from word_search.process_word_search_EJ import main as main_EJ
from word_search.process_word_search_JE import main as main_JE
from utils import load_csv, load_api_key

# OpenAI APIキーの設定
api_key = load_api_key()
client = OpenAI(api_key=api_key)

def generate_audio(word2):
    """
    OpenAI APIを利用して単語の音声を生成し、audioフォルダに保存する関数

    Args:
        word2 (str): 単語
    """
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # 他の音声も選択可能
            input=word2  # ここを word2 に修正
        )

        # audioフォルダが存在しない場合は作成する
        if not os.path.exists("audio"):
            os.makedirs("audio")

        # 音声ファイル名を "{word2}_pronounce.wav" に変更
        file_name = f"audio/{word2}_pronounce.wav"
        with open(file_name, "wb") as f:
            f.write(response.content)

        # ファイルが生成されるまで待機
        while not os.path.exists(file_name):  # ファイル名を使用
            time.sleep(0.1)

    except Exception as e:
        st.error(f"音声の生成に失敗しました: {e}")


def main():

    csv_file = "word_db.csv"  
    df = load_csv(csv_file)

    st.title("単語検索")
    mode = st.radio("モードを選択してください:", ('和英もーど', '英和もーど'), horizontal=True) 
    word = st.text_input("単語入力:", key="word_input")
    category = st.selectbox('分野選択:', ['認知科学', '強化学習', 'データ分析', 'その他'], index=None, placeholder="登録する分野を選択してください", key="category_select")
    search_button = st.button("検索", key="search_button")

    if search_button and word:
        # 入力チェック
        # if mode == '和英もーど' and any(c.isalpha() for c in word):
        #    st.warning("日本語を入力して下さい")
        #    return
        if mode == '英和もーど' and any(c.isascii() == False for c in word):  # 日本語が含まれているかチェック
            st.warning("英語を入力して下さい")
            return

        if mode == '和英もーど':
            result = main_JE(word, category, df)     
        else:
            result = main_EJ(word, category, df)
            
        print(result)
        # OpenAI APIを利用して音声を生成
        # ここで result['word'] を使うように修正
        generate_audio(result['word'])

        if "error" in result:
            st.error(result["error"])
        else:
            st.info(f"Word:　{result['word']}")
            st.info(f"Meaning:　{result['meaning']}")
            st.info(f"Pronounce:　{result['pronounce']}")
            
            # 発音記号と再生ボタンを横に並べる
            if mode == '英和もーど' :
                try:
                    # 音声ファイル名を "{result['word']}_pronounce.wav" に変更
                    file_name = f"audio/{result['word']}_pronounce.wav"
                    with open(file_name, "rb") as f:
                        st.audio(f.read(), format="audio/wav")
                except FileNotFoundError:
                    st.warning(f"音声ファイルが見つかりませんでした: {file_name}")  # ファイル名を使用
                except Exception as e:
                    st.error(f"音声の再生に失敗しました: {e}")
            
            st.info(f"Example Sentence:　{result['example_sentence']}")
            st.info(f"Translated Sentence:　{result['translated_sentence']}")
            st.info(f"Search Count:　{result['search_count']}")
            st.info(f"Category:　{category}")

main()

if __name__ == '__main__':
    main()
