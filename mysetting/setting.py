import streamlit as st
import pandas as pd
import os

st.title("設定")

# setting.csvファイルのパスを指定
setting_csv_path = "database/setting.csv"  # パスを変更

# setting.csvファイルから設定を読み込む
if os.path.exists(setting_csv_path):
    df = pd.read_csv(setting_csv_path)
    if len(df) > 0:
        settings = df.iloc[0].to_dict()
    else:
        settings = {"FinalLogin": None, "Character": None, "Goal": None, "ContinueDays": None, "Gender": None, "Age": None}
else:
    settings = {"FinalLogin": None, "Character": None, "Goal": None, "ContinueDays": None, "Gender": None, "Age": None}

# 学習目標
st.markdown("<hr style='border:3px solid gray'>", unsafe_allow_html=True)

st.subheader("目標設定")
col1, col2 = st.columns(2)
# ...

with col1:
    # Goalの値を取得
    if pd.isna(settings["Goal"]):  # settings["Goal"] が NaN かどうかを確認
        goal_value = 1  # NaN の場合はデフォルト値 1 を設定
    else:
        goal_value = int(settings["Goal"])
    goal = st.number_input("目標単語数 / week", min_value=1, max_value=100, value=goal_value)

with col2:
    if st.button("更新"):
        if goal:
            settings["Goal"] = goal  # Goalの値を更新
            # setting.csvファイルに設定を保存する
            # setting.csvファイルに設定を保存する
            df = pd.DataFrame([settings])
            df.to_csv(setting_csv_path, index=False)  # パスを変更
            with col1:
                st.success("✅目標を設定しました！")

# キャラクター設定
st.markdown("<hr style='border:3px solid gray'>", unsafe_allow_html=True)
st.subheader("キャラクター設定")

col1, col2 = st.columns([1, 2])
with col1:
    st.write("性別")
    gender_options = ["男性", "女性", "中性的", "どちらでもない"]
    if settings["Gender"] in gender_options:
        index = gender_options.index(settings["Gender"])
    else:
        index = 0
    gender = st.selectbox("", gender_options, index=index)

with col2:
    st.write("年齢")
    if pd.isna(settings["Age"]):
        age_value = 1
    else:
        age_value = int(settings["Age"])
    age = st.number_input("", min_value=1, max_value=100, value=age_value)

st.markdown("---")

# Characterの値を取得
character = st.text_area("性格：できるだけ詳細に設定してください", value=settings["Character"] if settings["Character"] else "", height=100)

# 例として文章を表示
st.markdown("<small>例：東京生まれの、優柔不断だが優しい青年。幼少期に両親を亡くし、祖父母に育てられた。彼の夢は、家族の愛情を受け継ぎ、誰かの支えになること。決断に時間がかかることもあるが、その分、相手の気持ちを深く考えることができる。困っている人を見過ごせず、いつも手を差し伸べる心優しい青年。</small>", unsafe_allow_html=True)

if st.button("キャラクター設定を更新する", key="update_character"):
    settings["Gender"] = gender
    settings["Age"] = age
    # 改行文字を削除してから保存
    settings["Character"] = character.replace("\n", "")
    # setting.csvファイルに設定を保存する
    df = pd.DataFrame([settings])
    df.to_csv(setting_csv_path, index=False)  # パスを変更
    st.success("キャラクター設定を更新しました！", icon="✅")