import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def analysis_trend(file_path):

    # クラスタの定義
    clusters = {
        "学び"      : ['knowledge', 'understand', 'curiously', 'explore', 'practice'],
        "食事"      : ['taste', 'delicious', 'chew', 'happily', 'savor'],
        "仕事"      : ['accomplish', 'efficiently', 'task', 'organize', 'diligently'],
        "娯楽"      : ['play', 'enjoyable', 'relax', 'laugh', 'excitedly'],
        "感情・思想" : ['reflect', 'hopeful', 'feel', 'deeply', 'express'],
    }

    # CSVファイルの読み込み
    data = pd.read_csv(file_path)

    # SentenceTransformer モデルをロード
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model.tokenizer.clean_up_tokenization_spaces = False  # 新しい設定に合わせる

    # クラスタの中心ベクトルを計算
    cluster_vectors = {}
    for cluster_name, words in clusters.items():
        word_vectors = model.encode(words)  # 各クラスタの単語をベクトル化
        cluster_center = np.mean(word_vectors, axis=0)  # 各クラスタの中心を計算
        cluster_vectors[cluster_name] = cluster_center

    # 単語をクラスタに割り当て
    assigned_clusters = []
    for word in data['Word']:
        word_vector = model.encode([word])[0]
        # 各クラスタの中心とのコサイン類似度を計算
        similarities = {cluster: cosine_similarity([word_vector], [center])[0][0] for cluster, center in cluster_vectors.items()}
        # 最も類似度が高いクラスタに割り当て
        best_cluster = max(similarities, key=similarities.get)
        assigned_clusters.append(best_cluster)

    # 割り当て結果をデータフレームに追加
    data['Cluster'] = assigned_clusters

    # 各クラスターに含まれる単語数をカウント
    cluster_counts = data['Cluster'].value_counts()

    # レーダーチャート用のデータを返す
    labels = list(clusters.keys())
    values = [cluster_counts.get(cluster, 0) for cluster in labels]

    return labels, values