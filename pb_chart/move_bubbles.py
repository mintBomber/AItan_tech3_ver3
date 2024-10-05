import math


def place_bubbles_on_circle(num_bubbles, center_x, center_y, radius):
    """
    バブルを円周上に均等に配置する関数。

    Parameters:
        num_bubbles (int): バブルの数
        center_x (float): 円の中心のx座標
        center_y (float): 円の中心のy座標
        radius (float): 円の半径

    Returns:
        List[float]: 各バブルのx座標のリスト
        List[float]: 各バブルのy座標のリスト
    """
    x_positions = []
    y_positions = []

    # バブルを円周上に均等に配置
    for i in range(num_bubbles):
        # 各バブルの角度を計算 (2πをnum_bubblesで等分)
        angle = (2 * math.pi / num_bubbles) * i

        # x, y座標を計算
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)

        # 計算したx, y座標をリストに追加
        x_positions.append(x)
        y_positions.append(y)

    return x_positions, y_positions

# 初期配置のバブルをいい感じの位置に動かす関数
def move_bubbles_towards_center(num_bubbles, x, y, center_x, center_y, radii, speed=1, iterations=1):

    for _ in range(iterations):  # 指定回数ループ
        for i in range(num_bubbles):
            # 中心に向かって移動
            direction_to_center = [center_x - x[i], center_y - y[i]]
            distance_to_center = math.sqrt(direction_to_center[0]**2 + direction_to_center[1]**2)

            if distance_to_center > 0:  # 中心にすでにいる場合を除外
                # 正規化して一定速度で中心に向かう
                direction_to_center = [d / distance_to_center for d in direction_to_center]
                x[i] += direction_to_center[0] * speed
                y[i] += direction_to_center[1] * speed

            # 衝突回避ロジック
            for j in range(num_bubbles):
                if i != j:
                    dx = x[i] - x[j]
                    dy = y[i] - y[j]
                    dist = math.sqrt(dx**2 + dy**2)
                    min_dist = radii[i] + radii[j]

                    if dist < min_dist:  # バブルが重なっている場合
                        # バブルを反発させる
                        overlap = (min_dist - dist) / 2
                        angle = math.atan2(dy, dx)
                        x[i] += math.cos(angle) * overlap
                        y[i] += math.sin(angle) * overlap
                        # x[j] -= math.cos(angle) * overlap
                        # y[j] -= math.sin(angle) * overlap
    return x, y


def mendo(df, done):
    color_list = ['#0000d0', '#E69F00', '#009E73', '#D52300']
    category_list = ['認知科学', '強化学習', 'データ分析', 'その他']
    df['tmp'] = df['Learning Point']
    df = df[df['Done'] == done]

    for i in range(4):
        df.loc[df['Category'] == category_list[i], 'Category'] = color_list[i]
    df.loc[df['tmp'] > 6, 'tmp'] = 50
    df.loc[(df['tmp'] <= 6) & (df['tmp'] >=3), 'tmp'] = 35
    df.loc[df['tmp'] < 3, 'tmp'] = 20
    
    df = df.sort_values('tmp', ascending=False)
    # バブルを配置するパラメータ
    center_x, center_y = 200, 300  # 円の中心
    num_bubbles = [len(df[df['tmp'] == 50]), len(df[df['tmp'] == 35]), len(df[df['tmp'] == 20])]  # バブルの数
    radius = [60, 40, 20]  # 円の半径

    # バブルの初期位置を円周上に均等に配置
    x_positions, y_positions = place_bubbles_on_circle(num_bubbles[0], center_x, center_y, radius[0])
    x_positions2, y_positions2 = place_bubbles_on_circle(num_bubbles[1], center_x, center_y, radius[1]*10)
    x_positions3, y_positions3 = place_bubbles_on_circle(num_bubbles[2], center_x, center_y, radius[2]*25)

    x_positions.extend(x_positions2)
    x_positions.extend(x_positions3)

    y_positions.extend(y_positions2)
    y_positions.extend(y_positions3)

    df['x'] = x_positions
    df['y'] = y_positions
    # バブルの半径（例: 固定または可変）
    # df = df.sample(n=50)
    radii =  df['tmp'].values.tolist() # [40, 50, 60, 55, 25, 34, 60, 30]
    count = df['Learning Point'].values.tolist() 
    name = df['Word'].values.tolist()
    mean = df['Meaning'].values.tolist()
    example = df['Example Sentence'].values.tolist()
    color = df['Category'].values.tolist()
    x = df['x'].values.tolist()
    y = df['y'].values.tolist()
    num_bubbles = len(radii)

    return radii, name, mean, example, color, x, y, num_bubbles, count


def mendo_paper(df, done):
    color_list = ['#0000d0', '#E69F00', '#009E73', '#D52300']
    category_list = ['認知科学', '強化学習', 'データ分析', 'その他']
    df['tmp'] = df['Learning Point']
    df = df[df['Done'] == done]

    for i in range(4):
        df.loc[df['Category'] == category_list[i], 'Category'] = color_list[i]
    df.loc[df['tmp'] > 6, 'tmp'] = 50
    df.loc[(df['tmp'] <= 6) & (df['tmp'] >=3), 'tmp'] = 35
    df.loc[df['tmp'] < 3, 'tmp'] = 20
    
    df = df.sort_values('tmp', ascending=False)
    # バブルを配置するパラメータ
    center_x, center_y = 200, 300  # 円の中心
    num_bubbles = [len(df[df['tmp'] == 50]), len(df[df['tmp'] == 35]), len(df[df['tmp'] == 20])]  # バブルの数
    radius = [60, 40, 20]  # 円の半径

    # バブルの初期位置を円周上に均等に配置
    x_positions, y_positions = place_bubbles_on_circle(num_bubbles[0], center_x, center_y, radius[0])
    x_positions2, y_positions2 = place_bubbles_on_circle(num_bubbles[1], center_x, center_y, radius[1]*10)
    x_positions3, y_positions3 = place_bubbles_on_circle(num_bubbles[2], center_x, center_y, radius[2]*25)

    x_positions.extend(x_positions2)
    x_positions.extend(x_positions3)

    y_positions.extend(y_positions2)
    y_positions.extend(y_positions3)

    df['x'] = x_positions
    df['y'] = y_positions
    # バブルの半径（例: 固定または可変）
    # df = df.sample(n=50)
    radii =  df['tmp'].values.tolist() # [40, 50, 60, 55, 25, 34, 60, 30]
    count = df['Learning Point'].values.tolist() 
    name = df['Word'].values.tolist()
    mean = df['Meaning'].values.tolist()
    color = df['Category'].values.tolist()
    x = df['x'].values.tolist()
    y = df['y'].values.tolist()
    num_bubbles = len(radii)

    return radii, name, mean, color, x, y, num_bubbles, count