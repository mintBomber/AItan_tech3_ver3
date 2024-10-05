import os
import openai
from openai import OpenAI
import pandas as pd
import json

from utils import load_api_key

def _load_csv(file_name):
    """csvファイルのの読み込み"""
    file_path = os.path.join('database', file_name)
    print(file_path)

    try:
        df = pd.read_csv(file_path)
        return df
    
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません。パスを確認してください。")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None


def decrease_search_count(word):
    """該当するWordのLearning Pointを-1する"""
    for file_name in ['word_db.csv', 'paper_db.csv']:
        file_path = os.path.join('database', file_name)
        df = pd.read_csv(file_path)
        
        # 該当するwordを確認
        if word in df['Word'].values:
            # 該当するWordのLearning Pointを-1する
            df.loc[df['Word'] == word, 'Learning Point'] -= 1
            df.loc[df['Learning Point'] < 0, 'Learning Point'] = 0
            
            # CSVファイルに上書き保存
            df.to_csv(file_path, index=False)


def _extraction_from_category(df_word, df_paper, n_word_test, quiz_category):
    """基本データと論文データを総合したテストの単語抽出"""
    try:
        # 共通するカラム抽出
        common_columns = ['Word', 'Meaning', 'Category', 'Learning Point', 'Add Date', 'Importance']

        # df_word と df_paper を共通のカラムでフィルタリング
        filtered_df_word = df_word[common_columns]
        filtered_df_paper = df_paper[common_columns]

        # df_word と df_paperを結合
        combined_df = pd.concat([filtered_df_word, filtered_df_paper], ignore_index=True)

        # 'Category'カラムがquiz_categoryと等しい行のみを抽出
        df_filtered = combined_df[combined_df['Category'] == quiz_category]
        
        if df_filtered.empty:
            print(f"カテゴリ '{quiz_category}' に一致するデータが見つかりませんでした。")
            return None
        
        # 'Learning Point'の値を10でcut編集
        df_filtered['Learning Point'] = df_filtered['Learning Point'].apply(lambda x: x if x <= 9 else 10)

        # 'Learning Point'カラムと'Importance'カラムの値を足し合わせた新しいカラムを作成
        df_filtered['Total Score'] = df_filtered['Learning Point'] + df_filtered['Importance']
        df_sorted = df_filtered.sort_values(by='Total Score', ascending=False)

        # 上位N件（例: 5件）の"単語"と"意味"を取得
        top_words = df_sorted[['Word', 'Meaning']].head(n_word_test)

        return top_words

    except Exception as e:
        print(f"データ処理中にエラーが発生しました: {e}")


def _extraction_from_basic(df, n_word_test, quiz_category):
    """基本データからテストする単語抽出"""
    try:
        # 'Category'カラムがquiz_categoryと等しい行のみを抽出
        df_filtered = df[df['Category'] == quiz_category]
        
        if df_filtered.empty:
            print(f"カテゴリ '{quiz_category}' に一致するデータが見つかりませんでした。")
            return None
        
        # 'Learning Point'の値を10でcut編集
        df_filtered['Learning Point'] = df_filtered['Learning Point'].apply(lambda x: x if x <= 9 else 10)

        # 'Learning Point'カラムと'Importance'カラムの値を足し合わせた新しいカラムを作成
        df_filtered['Total Score'] = df_filtered['Learning Point'] + df_filtered['Importance']
        
        # 'Total Score'カラムで降順ソート
        df_sorted = df_filtered.sort_values(by='Total Score', ascending=False)
        print(df_sorted)

        # 上位N件（例: 5件）の"単語"と"意味"を取得
        top_words = df_sorted[['Word', 'Meaning']].head(n_word_test)

        return top_words    

    except Exception as e:
        print(f"データ処理中にエラーが発生しました: {e}")


def process_csv(file_name, n_word_test, quiz_mode, quiz_category):
    """
    csvより、クイズを作成する対象の単語をリストアップする
    
    Args:
        file_path (str): 対象csv名 ---.csv
        n_word_teste (int): 問題数
        quiz_mode (str): "基本単語モード" or "論文モード"
        quiz_category (str): '認知科学' or '強化学習' or 'データ分析' or 'その他'

    Returns:
        top_words (dict): 問題とするWord,Meaning
    """

    try:
        # 選択肢したモード別に単語をピックアップする
        if quiz_mode in ['基本単語帳もーど', '論文もーど']:
            df = _load_csv(file_name)
            top_words = _extraction_from_basic(df, n_word_test, quiz_category)

        elif quiz_mode == 'ガッチャンコもーど':
            df_word = _load_csv(file_name[0])
            df_paper = _load_csv(file_name[1])
            top_words = _extraction_from_category(df_word, df_paper, n_word_test, quiz_category)

        return top_words

    except Exception as e:
        print("CSVファイルの読み込みに失敗したため、処理を中止します。")
        print(f"エラー内容: {e}")


def _prompt_quiz_type(quiz_type: str, row: dict) -> str: # あとでかっこ
        """出題タイプ別のpromptにする関数"""
        word = row['Word']
        meaning = row['Meaning']

        # JSONフォーマットでリクエストメッセージを構築
        request_data = {
            "question": "ここに問題文",
            "choice4": ["選択肢A", "選択肢B", "選択肢C", "選択肢D"],
            "correct_answer": "選択肢A"
        }

        system_message = f"""
                あなたは、4択単語テスト生成アシスタントです。
                以下JSON形式で問題、選択肢、答えを生成してください。
                選択肢は、似た意味を持つ選択肢を並べないでください。
                また、正解は提示する４択の中でランダムに配置してください。
                {json.dumps(request_data, ensure_ascii=False)}
                """

        if quiz_type == '4択単語問題：英→日':
            message = f"""
                次の英単語をもとに、正しい日本語の意味を選択する４択問題を作成してください。: {word}の意味は「{meaning}」です。
                問題文には英単語を提示し、選択肢は日本語の意味を提示してください。
                以下は、生成の例になります。
                問題文：『read』の意味はなんですか？ 選択肢：書く、読む、食べる
                """
            
        elif quiz_type == '4択単語問題：日→英':
            message = f"""
                次の単語の日本語の意味をもとに、正しい英単語を選択する４択問題を作成してください。: {word}の意味は「{meaning}」です。
                問題文には日本語の意味を提示し、選択肢は英単語を提示してください。
                以下は、生成の例になります。
                問題文：『読む』の英単語はなんですか？ 選択肢：eat、begin、search, read
                """
        
        return system_message, message


def generate_quiz(top_words, quiz_type):
    """
    gptのapiを使用し、問題を作成する

    Args:
        top_words (pd.DataFrame): 問題とするWord,Meaning
        quiz_type (str): '4択単語問題：日→英' or '4択単語問題：英→日'

    Returns:
        quiz_list (dict): 生成した辞書型クイズデータ question, choice4, correct_answer
    """

    api_key = load_api_key()

    client = OpenAI(
        api_key=api_key
    )  

    # クイズデータを保存するリスト
    quiz_list = []

    for index, row in top_words.iterrows():
        # 出題タイプ別のpromptを作成する
        system_message, message = _prompt_quiz_type(quiz_type, row)
        print(message)
        
        try:
            # print("APIリクエスト前")
            response = client.chat.completions.create(
                model="gpt-4o-mini", # "gpt-3.5-turbo",  # GPTのエンジン名を指定します
                messages=[
                    {"role": "system", "content": f"/japanese {system_message}"},
                    {"role": "user", "content": f"/japanese {message}"}  # ユーザーのメッセージ
                ],
                max_tokens=200,  # 生成するトークンの最大数
                n=1,  # 生成するレスポンスの数
                stop=None,  # 停止トークンの設定
                temperature=0.5,  # 生成時のランダム性の制御
                top_p=1,  # トークン選択時の確率閾値
            )

            # 生成されたコンテンツを取得
            quiz_data = response.choices[0].message.content
            # print(quiz_data)

            try:
                quiz_data_json = json.loads(quiz_data)
                quiz_data_json['word'] = row['Word']
                quiz_data_json['meaning'] = row['Meaning']

                quiz_list.append(quiz_data_json)
                print(quiz_list)

            except json.JSONDecodeError as e:
                print(f"JSONデコードエラー: {e}")

        except openai.RateLimitError as e:
            # APIリクエストがレート制限を超えたときのエラー
            print(f"レート制限に達しました。時間を置いて再試行してください: {e}")
        except openai.APITimeoutError as e:
            # リクエストに無効なパラメータが含まれていた場合のエラー
            print(f"リクエストがタイムアウトしました。: {e}")
        except openai.AuthenticationError as e:
            # APIキーの認証が失敗した場合のエラー
            print(f"APIキーの認証に失敗しました。キーを確認してください: {e}")
        except openai.APIConnectionError as e:
            # サーバーへの接続に問題があった場合のエラー
            print(f"APIサーバーへの接続に失敗しました。ネットワーク接続を確認してください: {e}")
        except openai.OpenAIError as e:
            # その他のOpenAI APIに関連するエラー
            print(f"OpenAI APIでエラーが発生しました: {e}")
        except Exception as e:
            # その他の汎用的なエラー
            print(f"不明なエラーが発生しました: {type(e).__name__}, {str(e)}")

    return quiz_list


if __name__ == '__main__':
    top_words = process_csv(file_name=["word_db.csv", "paper_db.csv"], n_word_test=2, quiz_mode="カテゴリ別もーど", quiz_category='認知科学')
    print(top_words)
