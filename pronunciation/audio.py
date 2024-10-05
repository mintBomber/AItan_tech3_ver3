import os
from google.cloud import texttospeech


# Google Cloud Text-to-Speechの認証情報設定 (事前に設定済みであること)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'secret-key.json'
text_to_speech_client = texttospeech.TextToSpeechClient()

def main(word):
    # audioディレクトリが存在しない場合は作成
    if not os.path.exists("audio"):
        os.makedirs("audio")

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
    response2 = text_to_speech_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # responseのaudio_contentはバイナリ
    # audioディレクトリに保存
    with open(f"audio/{word}.wav", "wb") as out:
        out.write(response2.audio_content)
        print("Audio content written to file", f"audio/{word}.wav", ".") 

# if __name__ == "__main__":