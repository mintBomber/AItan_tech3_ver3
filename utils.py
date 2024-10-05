import streamlit as st
import os
import pandas as pd
import json


def load_csv(file_name):
    """csvファイルのの読み込み"""
    file_path = os.path.join('database', file_name)

    try:
        df = pd.read_csv(file_path)
        return df
    
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません。パスを確認してください。")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None


def load_api_key():
    """api_keyの取得"""
    with open('config.json', 'r') as file:
        config = json.load(file)

    api_key = config.get('api_key')

    return api_key
