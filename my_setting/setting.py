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
        settings = {"FinalLogin": None, "Character": None, "Goal": None, "ContinueDays": None, 
                    "Gender": None, "Age": None, "HabitualSaying": None, "UserProfile": None, 
                    "UserInterest": None, "ColorPattern": None}

    # 列が存在しない場合は追加
    if "FinalLogin" not in df.columns:
        df["FinalLogin"] = None
    if "Character" not in df.columns:
        df["Character"] = None
    if "Goal" not in df.columns:
        df["Goal"] = None
    if "ContinueDays" not in df.columns:
        df["ContinueDays"] = None
    if "Gender" not in df.columns:
        df["Gender"] = None
    if "Age" not in df.columns:
        df["Age"] = None
    if "HabitualSaying" not in df.columns:  # HabitualSaying列が存在しない場合に追加
        df["HabitualSaying"] = None
    if "UserProfile" not in df.columns:
        df["UserProfile"] = None
    if "UserInterest" not in df.columns:
        df["UserInterest"] = None
    if "ColorPattern" not in df.columns:
        df["ColorPattern"] = None

    # settings を更新
    settings = df.iloc[0].to_dict()

    # setting.csv を更新
    df.to_csv(setting_csv_path, index=False)
else:
    settings = {"FinalLogin": None, "Character": None, "Goal": None, "ContinueDays": None, 
                "Gender": None, "Age": None, "HabitualSaying": None, "UserProfile": None, 
                "UserInterest": None, "ColorPattern": None}
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
st.markdown("---")
# 口調の入力欄を追加
habitual_saying = st.text_input("口調", value=settings["HabitualSaying"] if settings["HabitualSaying"] else "")

if st.button("キャラクター設定を更新する", key="update_character"):
    settings["Gender"] = gender
    settings["Age"] = age
    # 改行文字を削除してから保存
    settings["Character"] = character.replace("\n", "")
    settings["HabitualSaying"] = habitual_saying  # 口調をsettingsに保存

    # setting.csvファイルに設定を保存する
    df = pd.DataFrame([settings])
    df.to_csv(setting_csv_path, index=False)  # パスを変更
    st.success("キャラクター設定を更新しました！", icon="✅")

# ユーザー情報の設定
st.markdown("<hr style='border:3px solid gray'>", unsafe_allow_html=True)
st.subheader("ユーザー情報の設定")

# 自己紹介欄
user_profile = st.text_area("自己紹介：できるだけ詳細に記入してください", value=settings["UserProfile"] if settings["UserProfile"] else "", height=100)
st.markdown("---")
# 興味のある分野
user_interest = st.text_input("興味のある分野", value=settings["UserInterest"] if settings["UserInterest"] else "")

# 更新ボタン
if st.button("ユーザー情報を更新する", key="update_user_info"):
    # 改行文字を削除してから保存
    settings["UserProfile"] = user_profile.replace("\n", "")
    settings["UserInterest"] = user_interest

    # setting.csvファイルに設定を保存する
    df = pd.DataFrame([settings])
    df.to_csv(setting_csv_path, index=False)  # パスを変更
    st.success("ユーザー情報を更新しました！", icon="✅")

# テーマカラーの設定
st.markdown("<hr style='border:3px solid gray'>", unsafe_allow_html=True)
st.subheader("テーマカラーの設定")

# プルダウンメニュー
color_patterns = ["1 : Refreshing", "2 : Warm", "3 : Cool", "4 : Bright", "5 : Strange"]
selected_pattern = st.selectbox("テーマカラーを選択してください", color_patterns)

# 設定ボタン
if st.button("設定する", key="update_color_pattern"):
    # 選択されたテーマカラーの番号を取得
    pattern_number = int(selected_pattern.split(":")[0].strip())
    settings["ColorPattern"] = pattern_number

    # setting.csvファイルに設定を保存する
    df = pd.DataFrame([settings])
    df.to_csv(setting_csv_path, index=False)  # パスを変更
    st.success("テーマカラーを追加しました！", icon="✅")