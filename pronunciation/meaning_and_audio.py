import os
import re
import csv
from openai import OpenAI
from google.cloud import texttospeech

client = OpenAI()

# Google Cloud Text-to-Speechの認証情報設定 (事前に設定済みであること)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret-key.json'
text_to_speech_client = texttospeech.TextToSpeechClient()

def get_word_meaning_and_ipa(word):
    """
    入力された単語の意味とIPA発音記号を取得する関数

    Args:
        word (str): 入力された単語

    Returns:
        dict: 単語の意味とIPA発音記号を辞書形式で返す
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{word} の意味,IPA発音記号,単語を使用した英語の例文,その和訳分を教えてください。出力形式は必ず「入力した単語」「単語の意味」「IPA発音記号」「単語を使用した例文」「その例文の和訳」の5つの順で、改行して箇条書きでお願いします。出力例は「- enter 」「- 入る、参加する 」「- （発音記号）」「You can enter from the back of the building.」「建物の裏から入れます。」で、「」の直前に絶対改行します。「単語の意味」については、カタカナ語はうまく日本語に訳してください。例えばschizophreniaの意味は「スキズフレニア」ではなく「統合失調症」と日本語で返してください。日本語の訳語が検索しても見つからない場合は、その単語の概念について、数10字で説明してください。"
            }
        ]
    )

    # レスポンスから意味と発音記号を抽出
    meaning_and_ipa = response.choices[0].message.content.strip()

    # 正規表現でIPA発音記号を抽出
    match = re.search(r"IPA発音記号:(.*)", meaning_and_ipa)
    if match:
        ipa = match.group(1).strip()
    else:
        ipa = None

    # 意味を抽出 (IPA以外の部分)
    meaning = meaning_and_ipa.replace(ipa, "").strip() if ipa else meaning_and_ipa

    return {
        "意味": meaning,
        "IPA": ipa
    }

if __name__ == "__main__":
    word = input("英単語を入力してください: ")

    result = get_word_meaning_and_ipa(word)
    print(f"{result['意味']}")

    # CSVファイルに保存
    with open("output.csv", "a", newline="") as csvfile:
        fieldnames = ["単語", "意味", "IPA"]
        writer = csv.writer(csvfile)
        # 意味を-で区切って、横一列に別々のセルに格納
        meaning_list = result["意味"].split('-')
        row = [word] + meaning_list + [result["IPA"]]
        writer.writerow(row)  
    
    #########################################  
    # クライアントをインスタンス化
    client2 = texttospeech.TextToSpeechClient()

    # 合成するテキスト入力を設定
    synthesis_input = texttospeech.SynthesisInput(text=word)

    # 声のリクエストを構築し、言語コード（「en-US」）と
    # SSML音声のジェンダー（「neutral」）を選択
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # 返されるオーディオファイルの種類を選択
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # 選択した音声パラメータとオーディオファイルタイプを使用して、
    # テキスト入力に対してテキストから音声に変換するリクエストを実行
    response2 = client2.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # responseのaudio_contentはバイナリ
    with open(f"{word}.wav", "wb") as out:
        out.write(response2.audio_content)
        print("Audio content written to file",f"{word}.wav",".") 
