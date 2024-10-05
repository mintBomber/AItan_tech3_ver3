# hacku2024_tech3

## 概要
- 2024年度電大ハッカソン「HackU」の、チーム「Tech3!」用レポジトリです

## 環境
- python
- OpenAI API使用
- Google Cloud text-to-speech API使用

## インストール
ライブラリをインストールします。

必要となるライブラリは、`requirements.txt`に的間ています。
```
pip3 install -r requirements.txt
```

論文の登録を動かす場合、以下のコードでモデルのインストールが必要かもです。(ちぐちぐに聞いてみてください)
```
python -m spacy download en_core_web_sm
```

## ファイル構造
あんまり、コード同士が干渉しないように、作成しました。
人のコードもあんまりいじらないように結合しました。
各個人が実装した機能を1ファイルに、`main.py`から呼び出しをかけています。

```txt 
.
├── README.md
├── __pycache__
├── database
│   ├── word_db.csv
│   ├── word_list_nltk_top100.csv
│   └── word_list_spacy_top100.csv
│
├── images
│   └── push.png
│
├── main.py
│
├── mysetting
│   ├── myprofile.py
│   └── setting.py
│
├── paper_analysis
│   ├── __pycache__
│   ├── display_paper_analysis.py
│   └── process_papar_analysis.py
│
├── pb_chart
│   ├── __pycache__
│   ├── bubble_UI.py
│   ├── move_bubbles.py
│   ├── visualize_graph.py
│   └── word_count_mean_jp.csv
│
├── pronunciation
│   └── meaning_and_audio.py
│
├── requirements.txt
├── utils.py
│
├── word_quiz
│   ├── __pycache__
│   ├── display_word_quiz.py
│   └── process_word_quiz.py
│
└── word_search
    ├── __pycache__
    ├── display_word_search.py
    └── process_word_search.py
```

## 更新時のお願い
- `requirement.txt`の更新
    - 必要ライブラリが増えた場合、書き加えてください。
- `main.py`の更新
    - 基本に呼び出して欲しいファイル名に変更がある場合は、の`st.Page(page=)`以降のパスを変更してください。
    - その他、機能追加を行った場合、他の行に倣い、新たに`st.Page`行を追加し、`st.navigation`の引数に加えてください。
    - ページアイコン参照
        - カラー： https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
        - モノクロ： https://fonts.google.com/icons?icon.size=24&icon.color=%23e8eaed
- import時の、パスの記載方法
    - main.pyをカレントディレクトリと見てください。
- csvファイルについて
    - 単語登録csvは`word_db.csv`です。
        - カラム名は`Word`,`Meaning`,`Pronounce`,`Example Sentence`,`Translated Sentence`,`Search Count`,`Add Date`,`Category`,`Importance`,`Done`です。
    - 論文用csvは`paper_db.csv`です。
        - カラム名は`Word`,`Meaning`,`Appearance Frequency`,`Add Date`,`Category`,`Search Count`,`Importance`,`Done`です。
    - 設定用csvは`setting.csv` 
        - カラム名は`FinalLogin`,`Character`,`Goal`,`ContinueDays`,`Gender`,`Age`,`UserProfile`,`UserInterest`,`ColorPattern`です
    - csvファイル新規作成や、読み込みは`database`ディレクトリ内にお願いします。
- 画像ファイルの保存先
    - 使用する画像は、`images`ディレクトリ内にお願いします。
