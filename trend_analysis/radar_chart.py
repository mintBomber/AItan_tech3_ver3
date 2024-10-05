import streamlit as st
import matplotlib.pyplot as plt
from math import pi
import matplotlib.font_manager as fm

from trend_analysis.process_trend import analysis_trend

# 日本語フォントのパスを指定
jp_font_path = jp_font_path = 'trend_analysis/fonts/NotoSansJP-VariableFont_wght.ttf'   # フォントのパス


# レーダーチャート描画用の関数
def plot_radar_chart(categories, values):
    # 各カテゴリの角度を計算
    N = len(categories)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # 最後の角度を最初と同じにして閉じる
    values += values[:1]  # データを閉じるために再度最初の値を追加

    # レーダーチャートをプロット
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # ラベルをセット
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # 各カテゴリに対応する軸を設定
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontproperties=fm.FontProperties(fname=jp_font_path))

    # グラフを描画
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.3)

    # タイトルを設定
    plt.title('', fontproperties=fm.FontProperties(fname=jp_font_path))

    return fig


# メインのStreamlitアプリケーション
def main():

    # CSVファイルが既に存在する場合
    file_path_1 = 'database/word_db.csv'
    file_path_2 = 'database/paper_db.csv'

    # CSVからデータを分析してレーダーチャート用のデータを取得
    categories_1, values_1 = analysis_trend(file_path_1)
    categories_2, values_2 = analysis_trend(file_path_2)

    # レーダーチャートを作成
    fig_1 = plot_radar_chart(categories_1, values_1)
    fig_2 = plot_radar_chart(categories_2, values_2)

    # Streamlitでチャートを表示
    st.title("単語傾向の可視化")
    st.header("単語検索")
    st.pyplot(fig_1)

    st.header("論文")
    st.pyplot(fig_2)

    # レーダーチャートを横に並べて表示する
    # col1, col2 = st.columns(2)

    # with col1:
    #     st.header("単語検索")s
    #     st.pyplot(fig_1)
    # with col2:
    #     st.header("論文")
    #     st.pyplot(fig_2)


main()
    

if __name__ == "__main__":
    main()