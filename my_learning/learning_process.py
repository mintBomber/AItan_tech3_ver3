import pandas as pd
from datetime import timedelta

df = pd.read_csv('database/word_db.csv')

def process_data(file_path, category):
    df = pd.read_csv(file_path)

    df['Add Date'] = pd.to_datetime(df['Add Date'], errors='coerce')

    # カテゴリーに基づいてデータをフィルタリング
    if category == "1日":
        filtered_df = df[df['Add Date'] == df['Add Date'].max()]
    elif category == "1週間":
        end_date = df['Add Date'].max()
        start_date = end_date - timedelta(days=6)
        filtered_df = df[(df['Add Date'] >= start_date) & (df['Add Date'] <= end_date)]
    elif category == "1ヶ月":
        end_date = df['Add Date'].max()
        start_date = end_date - pd.DateOffset(months=1)
        filtered_df = df[(df['Add Date'] >= start_date) & (df['Add Date'] <= end_date)]
    elif category == "1年":
        end_date = df['Add Date'].max()
        start_date = end_date - pd.DateOffset(years=1)
        filtered_df = df[(df['Add Date'] >= start_date) & (df['Add Date'] <= end_date)]
    
    # 累計学習語数
    total_words_learned = df['Word'].count()  

    # 連続学習日数を計算する関数
    def calculate_consecutive_days(df):
        consecutive_days = 0
        previous_date = None

        for index, row in df.iterrows():
            current_date = row['Add Date']  
            if previous_date is None or current_date == previous_date + timedelta(days=1):
                consecutive_days += 1
            previous_date = current_date
        return consecutive_days

    consecutive_days = calculate_consecutive_days(df)

    # 1週間で調べた単語数を計算
    end_date = filtered_df['Add Date'].max() if not filtered_df.empty else None
    if end_date:
        start_date = end_date - timedelta(days=6)  
        week_words_learned = filtered_df[(filtered_df['Add Date'] >= start_date) & (filtered_df['Add Date'] <= end_date)].shape[0]
    else:
        week_words_learned = 0

    setting_df = pd.read_csv('database/setting.csv') 
    goal_value = setting_df['Goal'].iloc[0] 

    # 達成度を計算
    remaining_words = goal_value - week_words_learned

    if remaining_words <= -20:
        achievement_level = "UR"
    elif remaining_words <= 20:
        achievement_level = "SS"
    elif remaining_words <= 40:
        achievement_level = "A"
    elif remaining_words <= 60:
        achievement_level = "B"
    else:
        achievement_level = "C"

    return {
            'filtered_df': filtered_df,
            'total_words_registered': total_words_learned,
            'consecutive_days': consecutive_days,
            'week_words_learned': week_words_learned,
            'achievement_level': achievement_level  
        }