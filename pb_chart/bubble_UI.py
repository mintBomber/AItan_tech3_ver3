def write_UI_burst(num_bubbles, radii, x, y, name, mean, example, color):
    button_html = """
    <style>
    .bubble-container {
        position: relative;
        width: 600px;
        height: 600px;
        margin: 0 auto;
    }

    .bubble-container button {
        position: absolute;
        border-radius: 50%;
        border: none;
        color:white;
        font-weight: bold;
        cursor: pointer;
    }

    /* 小さい円のスタイル */
    .small-circle {
        position: absolute;
        border-radius: 50%;
        transition: transform 0.5s, opacity 0.5s;  
        opacity: 1;
    }

    .animate-out {
        transform: translate(var(--x), var(--y));  
        opacity: 0;  
    }

    </style>

    <div class="bubble-container">
    """

    for i in range(num_bubbles):
        button_html += f'''
            <div id="bubble-{i}" style="position:absolute; width: {radii[i] * 2}px; height: {radii[i] * 2}px; text-align:center;">
                <button style="width: {radii[i] * 2}px; height: {radii[i] * 2}px; font-size: {10+radii[i]/5}px; top:{y[i]-radii[i]+100}px; left:{x[i]-radii[i]}px; background-color: {color[i]};" 
                        onclick="startChainDeletion({i})">{name[i]}</button>
            </div>
        '''

    button_html += """
    </div>

    <script>
    let bubbleContainer = document.querySelector('.bubble-container');  // ここでbubbleContainerを定義
    let bubbleIndex = 0;
    let numBubbles = """ + str(num_bubbles) + """;

    function rgbToHex(rgb) {
        // rgbの形式から数値を抽出
        let rgbValues = rgb.match(/\\d+/g);
        
        // 各値を16進数に変換し、2桁の文字列にする
        let r = parseInt(rgbValues[0]).toString(16).padStart(2, '0');
        let g = parseInt(rgbValues[1]).toString(16).padStart(2, '0');
        let b = parseInt(rgbValues[2]).toString(16).padStart(2, '0');
        
        // #RRGGBB形式で文字列として返す
        return `#${r}${g}${b}`;
    }

    function deleteBubble(bubbleNumber) {
        var bubble = document.getElementById("bubble-" + bubbleNumber);
        if (bubble) {
            // rectを使用してバブルの位置とサイズを取得
            var rect = bubble.querySelector('button');
            var radiusx = window.getComputedStyle(rect).getPropertyValue('width'); // 半径を計
            var radius = parseFloat(radiusx)/2;
            var bubbleXx = window.getComputedStyle(rect).getPropertyValue('left');  // スクロールオフセットを加える
            var bubbleX = parseFloat(bubbleXx)+radius;
            var bubbleYx = window.getComputedStyle(rect).getPropertyValue('top');  // スクロールオフセットを加える
            var bubbleY = parseFloat(bubbleYx)+radius;
            var colorx = window.getComputedStyle(rect).getPropertyValue('background-color');
            var color = rgbToHex(colorx);
            
            bubble.remove();  // バブルを削除
            
            // バブルが消えた後に小さな円を作成してアニメーションさせる
            var numSmallCircles = Math.floor(Math.PI * Math.pow(radius, 2) / 10) * 0.50;
            var smallCircles = [];
            
            for (var i = 0; i < numSmallCircles; i++) {
                var angle = Math.random() * 2 * Math.PI;
                var r = Math.sqrt(Math.random()) * radius;
                var xMove = r * Math.cos(angle);
                var yMove = r * Math.sin(angle);

                var smallCircle = document.createElement('div');
                smallCircle.className = 'small-circle';
                smallCircle.style.width = '10px';
                smallCircle.style.height = '10px';
                
                smallCircle.style.backgroundColor = color;
                console.log(color);
                smallCircle.style.left = (bubbleX + xMove - 5) + 'px';
                smallCircle.style.top = (bubbleY + yMove - 5) + 'px';
                bubbleContainer.appendChild(smallCircle);
                smallCircles.push(smallCircle);
            }

            // アニメーション処理
            setTimeout(() => {
                smallCircles.forEach((circle) => {
                    var angle = Math.random() * 2 * Math.PI;
                    var distance = Math.random() * 200 + 50;
                    circle.style.setProperty('--x', (distance * Math.cos(angle)) + 'px');
                    circle.style.setProperty('--y', (distance * Math.sin(angle)) + 'px');
                    circle.classList.add('animate-out');
                });
            }, 10);
        }
    }

    // 1つ目のバブルがクリックされたら1秒間隔で順に削除する
    function startChainDeletion(startIndex) {
        bubbleIndex = 0;
        deleteNextBubble();
    }

    // 次のバブルを1秒間隔で削除する
    function deleteNextBubble() {
        if (bubbleIndex < numBubbles) {
            deleteBubble(bubbleIndex);
            bubbleIndex++;
            setTimeout(function() {
                deleteNextBubble();  // 次のバブルを1秒後に削除
            }, 500);
        }
    }
    </script>
    """

    return button_html







def write_UI_visualize(num_bubbles, radii, x, y, name, mean, example, colors, count):
    button_html = """
    <style>
    .bubble-container {
        position: relative;
        width: 600px;
        height: 600px;
        margin: 0 auto;
    }

    .bubble-container button {
        position: absolute;
        border-radius: 50%;
        color: white;
        border: none;
        font-weight: bold;
        cursor: pointer;
    }

    /* オーバーレイスタイル */
    .overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .overlay.active {
        display: flex;
    }

    .overlay-content {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        position: relative;
        width: 300px;
    }

    /* バツボタンのスタイル */
    .close-button {
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
        font-size: 18px;
        background: none;
        border: none;
    }
    </style>

    <div class="bubble-container">
    """

    for i in range(num_bubbles):
        # 各バブルに対応する色を設定
        button_html += '''
        <button style="width: {0}px; height: {0}px; font-size: {7}px; top: {1}px; left: {2}px; background-color: {6};"
                onclick="showOverlay('{3}', '{4}', '{5}', '{8}')">
                {3}
        </button>'''.format(radii[i] * 2, y[i]-radii[i]+100, x[i]-radii[i], name[i], mean[i], example[i], colors[i], 10+radii[i]/5, count[i])

    button_html += """
    </div>

    <!-- オーバーレイのHTML -->
    <div id="overlay" class="overlay">
        <div class="overlay-content">
            <button class="close-button" onclick="closeOverlay()">×</button>
            <h3 id="overlay-title">Overlay</h3>
            <p id="overlay-message"></p>
        </div>
    </div>
    """

    # JavaScriptを埋め込む
    button_html += """
    <script>
    function showOverlay(Word, mean, example, count) {
        var overlay = document.getElementById('overlay');
        var title = document.getElementById('overlay-title');
        var message = document.getElementById('overlay-message');
        title.innerText = Word;  // ボタン名をオーバーレイのタイトルに設定
        message.innerText = '単語の意味:'+ mean + '\\n 例文:' + example + '\\n 回数:' + count;
        overlay.classList.add('active');
    }

    function closeOverlay() {
        var overlay = document.getElementById('overlay');
        overlay.classList.remove('active');
    }
    </script>
    """

    return button_html


def write_paper_UI_visualize(num_bubbles, radii, x, y, name, mean, colors, count):
    button_html = """
    <style>
    .bubble-container {
        position: relative;
        width: 600px;
        height: 600px;
        margin: 0 auto;
    }

    .bubble-container button {
        position: absolute;
        border-radius: 50%;
        color: white;
        border: none;
        font-weight: bold;
        cursor: pointer;
    }

    /* オーバーレイスタイル */
    .overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .overlay.active {
        display: flex;
    }

    .overlay-content {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        position: relative;
        width: 300px;
    }

    /* バツボタンのスタイル */
    .close-button {
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
        font-size: 18px;
        background: none;
        border: none;
    }
    </style>

    <div class="bubble-container">
    """

    for i in range(num_bubbles):
        # 各バブルに対応する色を設定
        button_html += '''
        <button style="width: {0}px; height: {0}px; font-size: {6}px; top: {1}px; left: {2}px; background-color: {5};"
                onclick="showOverlay('{3}', '{4}', '{7}')">
                {3}
        </button>'''.format(radii[i] * 2, y[i]-radii[i]+100, x[i]-radii[i], name[i], mean[i], colors[i], 10+radii[i]/5, count[i])

    button_html += """
    </div>

    <!-- オーバーレイのHTML -->
    <div id="overlay" class="overlay">
        <div class="overlay-content">
            <button class="close-button" onclick="closeOverlay()">×</button>
            <h3 id="overlay-title">Overlay</h3>
            <p id="overlay-message"></p>
        </div>
    </div>
    """

    # JavaScriptを埋め込む
    button_html += """
    <script>
    function showOverlay(Word, mean, count) {
        var overlay = document.getElementById('overlay');
        var title = document.getElementById('overlay-title');
        var message = document.getElementById('overlay-message');
        title.innerText = Word;  // ボタン名をオーバーレイのタイトルに設定
        message.innerText = '単語の意味:'+ mean + '\\n 回数:' + count;
        overlay.classList.add('active');
    }

    function closeOverlay() {
        var overlay = document.getElementById('overlay');
        overlay.classList.remove('active');
    }
    </script>
    """

    return button_html