import os
import pandas as pd
import streamlit as st

from word_search.process_word_search_EJ import main as main_EJ
from word_search.process_word_search_JE import main as main_JE
# from word_search.audio import main as audio_main  # word_search.audio を使用

from utils import load_csv, load_api_key
from openai import OpenAI
api_key = load_api_key()
client = OpenAI(api_key=api_key)

def generate_audio(word):
    """
    OpenAI APIを利用して単語の音声を生成し、audioフォルダに保存する関数
    Args:
        word (str): 単語
    """
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",  # 他の音声も選択可能
            input=word
        )

        # audioフォルダが存在しない場合は作成する
        if not os.path.exists("audio"):
            os.makedirs("audio")

        # 音声ファイルを保存
        with open(f"audio/{word}.wav", "wb") as f:
            f.write(response.content)

    except Exception as e:
        # st.error(f"音声の生成に失敗しました: {e}")

def main():

    csv_file = "word_db.csv"  
    df = load_csv(csv_file)

    st.title("単語検索")
    mode = st.radio("モードを選択してください:", ('和英もーど', '英和もーど'), horizontal=True) 
    word = st.text_input("単語入力:",key="word_input")
    category = st.selectbox('分野選択:',['認知科学', '強化学習', 'データ分析','その他'],index = None,placeholder="登録する分野を選択してください",key="category_select")
    search_button = st.button("検索", key="search_button")

    if search_button and word:
        # 入力チェック
        if mode == '英和もーど' and any(c.isascii() == False for c in word):  # 日本語が含まれているかチェック
            st.warning("英語を入力して下さい")
            return

        if mode == '和英もーど':
            result = main_JE(word, category, df)     
        else:
            result = main_EJ(word, category, df) 
        
        ## audio.pyを呼び出して音声を生成
        ## audio_main(word)  # ここでaudio.pyのmain関数を呼び出す
        # OpenAI APIを利用して音声を生成
        # generate_audio(result['word'])
        
        print(result)

        if "error" in result:
            st.error(result["error"])
        else:
            st.info(f"Word:　{result['word']}")
            st.info(f"Meaning:　{result['meaning']}")
            st.info(f"Pronounce:　{result['pronounce']}")
             # 発音記号と再生ボタンを横に並べる
            # col1, col2 = st.columns([3, 1])  # カラムの比率を調整
            # with col1:
               # with open(f"audio/{word}.wav", "rb") as f:
                   # st.audio(f.read(), format="audio/wav")
           # with col2:
                # st.info()
            st.info(f"Example Sentence:　{result['example_sentence']}")
            st.info(f"Translated Sentence:　{result['translated_sentence']}")
            st.info(f"Search Count:　{result['search_count']}")
            st.info(f"Category:　{category}")

main()

if __name__ == '__main__':
    main()
