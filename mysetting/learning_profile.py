import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# 学習データのサンプル（日付と覚えた語数）
df = pd.read_csv('database/word_db.csv')

# 日付のフォーマットを統一し、datetime型に変換
df['Add Date'] = pd.to_datetime(df['Add Date'], format='%Y-%m-%d')

# 累計学習語数
total_words_learned = len(df['Word'])

# 連続学習日数を計算する関数
def calculate_consecutive_days(df):
    consecutive_days = 0
    previous_date = None

    for index, row in df.iterrows():
        current_date = row['Add Date']  # 日付はすでにdatetime型になっている

        if previous_date is None or current_date == previous_date + timedelta(days=1):
            consecutive_days += 1
        # 連続が途切れたら終了

        previous_date = current_date

    return consecutive_days

consecutive_days = calculate_consecutive_days(df)

# 1週間で覚えた語数
week_words_learned = len(df['Word'])

# 1日当たりの平均語数
average_words_per_day = df['Search Count'].mean()

st.title("英単語学習の進捗")

# 2列のレイアウトを作成
col1, col2 = st.columns([1, 1])

# 左側の列に棒グラフを表示 (matplotlib使用)
with col1:
    st.write("### 学習データの棒グラフ")

    # matplotlibでグラフを描画
    fig, ax = plt.subplots()
    ax.bar(df['Add Date'], df['Word'], color='skyblue')

    ax.set_title('one day')
    ax.set_xlabel('date')
    ax.set_ylabel('number')
    ax.tick_params(axis='x', rotation=45)  # 日付を45度回転して表示
    ax.get_yaxis().set_visible(False)
    # Streamlitでmatplotlibのグラフを表示
    st.pyplot(fig)

# 右側の列にメトリクスを表示
with col2:
    st.write("#### 学習データの概要")
    st.metric("1週間当たりに覚えた英単語数", f"{week_words_learned}語")
    st.metric("連続日数", f"{consecutive_days}日")
    st.metric("累計学習語数", f"{total_words_learned}語")
    st.metric("1日当たりに調べた語数", f"{average_words_per_day:.2f}語")

    # 学習履歴のデータテーブル
    st.write("#### 学習履歴")
    st.dataframe(df)