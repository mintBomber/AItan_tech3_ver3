import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from my_learning.learning_process import process_data

# st.set_page_config(layout="wide")s

st.title("学習データ")

category = st.selectbox("期間を選択してください", ["1日", "1週間", "1ヶ月", "1年"])

data = process_data('database/word_db.csv', category)

filtered_df = data['filtered_df']
total_words_registered = data['total_words_registered']
consecutive_days = data['consecutive_days']
week_words_learned = data['week_words_learned']
achievement_level = data['achievement_level'] 

# 日付だけを抽出
filtered_df['Add Date'] = pd.to_datetime(filtered_df['Add Date']).dt.date

# 2列のレイアウトを作成
col1, col2 = st.columns([1.5, 1])

# 右側の列にメトリクスを常に表示
with col2:
    st.markdown(
"""
<style>
.custom-font {
    font-size:20px;
}
.custom-info {
    font-size:18px;
    color: #1C1C1C;
    background-color: #b0c4de;
    padding: 10px;
    border-radius: 10px;
}
.outline-achievement {
    font-size: 60px;
    color: transparent;
    -webkit-text-stroke: 5px black; 
    background-color: #b0c4de;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True
)
    
    st.title("英単語学習進捗")
    st.markdown('<p class="custom-font">1週間当たりに調べた英単語数:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="custom-info">　　　　　　{week_words_learned}語</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-font">連続日数:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="custom-info">　　　　　　{consecutive_days}日</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-font">累計登録単語数:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="custom-info">　　　　　　{total_words_registered}語</p>', unsafe_allow_html=True)
    st.markdown('<p class="custom-font">達成度:</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="outline-achievement">　　{achievement_level}</p>', unsafe_allow_html=True)

# 左側の列にグラフを表示 
with col1:
    st.write("## 学習データのグラフ")

    if not filtered_df.empty:
        # 日付ごとの単語数を集計
        word_counts_by_date = filtered_df.groupby('Add Date')['Word'].count()

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=word_counts_by_date.index, 
                                 y=word_counts_by_date.values, 
                                 mode='lines+markers', 
                                 name='学習単語数', 
                                 line=dict(color='red'),
                                 marker=dict(size=8)))

        fig.add_trace(go.Bar(x=word_counts_by_date.index, 
                             y=word_counts_by_date.values, 
                             name='学習単語数', 
                             marker_color='skyblue',
                             opacity=0.6))

        # レイアウト設定
        fig.update_layout(
            title="学習単語数の推移",
            xaxis_title="Date",
            yaxis_title="Word Count",
            yaxis_range=[0, word_counts_by_date.max() + 5], 
            xaxis_tickangle=-45,
            showlegend=False,
            height=500,
            width=700
        )

        st.plotly_chart(fig)
    else:
        st.write("選択したカテゴリーにはデータがありません。")