import streamlit as st
import random
import os

# 1. 設定網頁標題與風格（強制寬版版面以利左右分割）
st.set_page_config(page_title="Kids English Magic Puzzle", layout="wide")

# 套用 Figma 風格的自訂 CSS 樣式
st.markdown("""
<style>
    /* 全局背景與字體優化 */
    .stApp {
        background-color: #0F0E17;
        color: #FFFFFE;
    }
    
    /* 左側紫色視覺區裝飾 */
    .left-hero-container {
        background: linear-gradient(135deg, #6246EA 0%, #3B21B9 100%);
        padding: 30px;
        border-radius: 24px;
        box-shadow: 0px 10px 30px rgba(98, 70, 234, 0.3);
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* 右側任務提示框 */
    .task-hint-box {
        background-color: #1F1E26;
        border-left: 6px solid #6246EA;
        padding: 15px 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* 答案顯示框 */
    .sentence-display-box {
        background: rgba(98, 70, 234, 0.1);
        border: 2px dashed #6246EA;
        padding: 20px;
        border-radius: 16px;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        color: #FFFFFE;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# 2. 初始化 30 張本地圖片的資料庫
@st.cache_data
def get_expanded_game_data():
    return [
        {
            "id": 1, "img_path": "1.png", "hint": "Boy eating breakfast",
            "sentences": [
                {"correct_words": ["The happy boy", "is eating", "yummy", "breakfast"], "hint_zh": "快樂的男孩正在吃美味的早餐。"},
                {"correct_words": ["A sweet child", "likes", "warm and healthy", "food"], "hint_zh": "可愛的孩子喜歡溫暖又健康的食物。"},
                {"correct_words": ["The little kid", "sits", "at the kitchen", "table"], "hint_zh": "小孩子坐在廚房的桌子旁。"}
            ]
        },
        {
            "id": 2, "img_path": "2.png", "hint": "Girl going to school",
            "sentences": [
                {"correct_words": ["The cute girl", "walks", "to the beautiful", "school"], "hint_zh": "可愛的女孩走路去美麗的學校。"},
                {"correct_words": ["A young student", "carries", "a pink", "schoolbag"], "hint_zh": "年輕的學生背著一個粉紅色的書包。"},
                {"correct_words": ["The smart child", "looks", "very excited", "today"], "hint_zh": "這個聰明的孩子今天看起來非常興奮。"}
            ]
        },
        {
            "id": 3, "img_path": "3.png", "hint": "Sleeping cat",
            "sentences": [
                {"correct_words": ["The lazy cat", "is sleeping", "on the warm", "blanket"], "hint_zh": "懶惰的貓咪在溫暖的毛毯上睡覺。"},
                {"correct_words": ["A soft pet", "closes", "its two small", "eyes"], "hint_zh": "柔軟的寵物閉上了牠的兩隻小眼睛。"},
                {"correct_words": ["The grey kitty", "feels", "so safe", "and comfortable"], "hint_zh": "這隻灰色的小貓感到非常安全和舒服。"}
            ]
        },
        {
            "id": 4, "img_path": "4.png", "hint": "Baby taking a bath",
            "sentences": [
                {"correct_words": ["The little baby", "takes", "a warm and clean", "bath"], "hint_zh": "小嬰兒洗了一個溫暖又乾淨的澡。"},
                {"correct_words": ["A happy infant", "plays", "with water", "happily"], "hint_zh": "快樂的幼兒高興地玩著水。"},
                {"correct_words": ["The cute child", "has", "many white", "bubbles"], "hint_zh": "可愛的孩子身上有許多白色的泡泡。"}
            ]
        },
        {
            "id": 5, "img_path": "5.png", "hint": "Boy doing homework",
            "sentences": [
                {"correct_words": ["The diligent boy", "writes", "his English", "homework"], "hint_zh": "勤奮的男孩正在寫他的英文功課。"},
                {"correct_words": ["A smart kid", "studies", "at his quiet", "desk"], "hint_zh": "聰明的小孩在他安靜的書桌前學習。"},
                {"correct_words": ["The young student", "uses", "a sharp", "pencil"], "hint_zh": "年輕的學生使用一枝鋒利的鉛筆。"}
            ]
        },
        {
            "id": 6, "img_path": "6.png", "hint": "Girl reading a book",
            "sentences": [
                {"correct_words": ["The quiet girl", "reads", "an interesting", "storybook"], "hint_zh": "安靜的女孩正在讀一本有趣的故事書。"},
                {"correct_words": ["A clever child", "learns", "many new", "words"], "hint_zh": "聰明的孩子學到了許多新的單字。"},
                {"correct_words": ["The young reader", "loves", "this fantastic", "library"], "hint_zh": "年輕的讀者喜愛這個奇妙的圖書館。"}
            ]
        },
        {
            "id": 7, "img_path": "7.png", "hint": "Kids playing soccer",
            "sentences": [
                {"correct_words": ["The active children", "play", "a soccer", "game"], "hint_zh": "活躍的孩子們正在踢一場足球賽。"},
                {"correct_words": ["A strong team", "runs", "on the green", "field"], "hint_zh": "強壯的隊伍在綠色的球場上跑步。"},
                {"correct_words": ["The excited players", "kick", "the round", "ball"], "hint_zh": "興奮的球員們踢著圓圓的球。"}
            ]
        },
        {
            "id": 8, "img_path": "8.png", "hint": "Riding a toy motorcycle",
            "sentences": [
                {"correct_words": ["The brave boy", "rides", "a red toy", "motorcycle"], "hint_zh": "勇敢的男孩騎著一輛紅色的玩具摩托車。"},
                {"correct_words": ["A cool kid", "wears", "a safe", "helmet"], "hint_zh": "酷炫的小孩戴著一頂安全的安全帽。"},
                {"correct_words": ["The small driver", "goes", "around the park", "safely"], "hint_zh": "小小的駕駛員安全地在公園裡繞行。"}
            ]
        },
        {
            "id": 9, "img_path": "9.png", "hint": "Playing the guitar",
            "sentences": [
                {"correct_words": ["The talented man", "plays", "the wooden", "guitar"], "hint_zh": "有才華的男子正在彈奏木吉他。"},
                {"correct_words": ["A nice musician", "sings", "a beautiful", "song"], "hint_zh": "優秀的音樂家正在唱一首美麗的歌。"},
                {"correct_words": ["The music coach", "makes", "very sweet", "sounds"], "hint_zh": "音樂教練發出了非常甜美的聲音。"}
            ]
        },
        {
            "id": 10, "img_path": "10.png", "hint": "Boy brushing teeth",
            "sentences": [
                {"correct_words": ["The healthy boy", "brushes", "his white", "teeth"], "hint_zh": "健康的男孩正在刷他潔白的牙齒。"},
                {"correct_words": ["A clean kid", "uses", "a blue", "toothbrush"], "hint_zh": "愛乾淨的小孩使用一支藍色的牙刷。"},
                {"correct_words": ["The smart child", "washes", "his face", "every morning"], "hint_zh": "聰明的孩子每天早上都會洗臉。"}
            ]
        },
        {
            "id": 11, "img_path": "11.png", "hint": "Beautiful sunset",
            "sentences": [
                {"correct_words": ["The orange sun", "goes", "down the mountain", "slowly"], "hint_zh": "橙色的太陽緩緩地落入山後。"},
                {"correct_words": ["A beautiful sunset", "makes", "the bright", "sky"], "hint_zh": "美麗的夕陽形成了明亮的天空。"},
                {"correct_words": ["The warm light", "shines", "on the quiet", "land"], "hint_zh": "溫暖的光芒照耀在安靜的大地上。"}
            ]
        },
        {
            "id": 12, "img_path": "12.png", "hint": "Rainy night",
            "sentences": [
                {"correct_words": ["The cold rain", "falls", "on the dark", "window"], "hint_zh": "冰冷的雨水落在黑暗的窗戶上。"},
                {"correct_words": ["A heavy storm", "hits", "the big", "city"], "hint_zh": "一場大風暴襲擊了這座大城市。"},
                {"correct_words": ["The weather tonight", "looks", "very wet", "and gray"], "hint_zh": "今天晚補的天氣看起來非常潮濕且陰暗。"}
            ]
        },
        {
            "id": 13, "img_path": "13.png", "hint": "Cute kitten sitting",
            "sentences": [
                {"correct_words": ["The tiny kitten", "sits", "on the clean", "floor"], "hint_zh": "微小的小貓坐在乾淨的地板上。"},
                {"correct_words": ["A lovely pet", "has", "brown and striped", "fur"], "hint_zh": "可愛的寵物擁有棕色條紋的毛髮。"},
                {"correct_words": ["The sweet animal", "watches", "the moving", "toy"], "hint_zh": "甜美的動物注視著移動的玩具。"}
            ]
        },
        {
            "id": 14, "img_path": "14.png", "hint": "Butterfly flying",
            "sentences": [
                {"correct_words": ["The small butterfly", "flies", "in the sunny", "garden"], "hint_zh": "小蝴蝶在陽光明媚的花園裡飛舞。"},
                {"correct_words": ["A colorful insect", "visits", "the sweet", "flowers"], "hint_zh": "五彩繽紛的昆蟲拜訪了甜美的花朵。"},
                {"correct_words": ["The beautiful bug", "has", "two thin", "wings"], "hint_zh": "美麗的昆蟲有一雙薄薄的翅膀。"}
            ]
        },
        {
            "id": 15, "img_path": "15.png", "hint": "Blooming red flower",
            "sentences": [
                {"correct_words": ["The red flower", "grows", "near the green", "bush"], "hint_zh": "紅色的花朵生長在綠色的灌木叢旁。"},
                {"correct_words": ["A fresh plant", "opens", "its bright", "petals"], "hint_zh": "新鮮的植物展開了它鮮豔的花瓣。"},
                {"correct_words": ["The beautiful rose", "smells", "very sweet", "and nice"], "hint_zh": "美麗的玫瑰聞起來非常香甜芬芳。"}
            ]
        },
        {
            "id": 16, "img_path": "16.png", "hint": "Dead tree and blue sky",
            "sentences": [
                {"correct_words": ["The old tree", "stands", "under the blue", "sky"], "hint_zh": "古老的大樹佇立在藍天之下。"},
                {"correct_words": ["A tall plant", "loses", "all its dry", "leaves"], "hint_zh": "高大的植物失去了它所有乾枯的葉子。"},
                {"correct_words": ["The strong trunk", "looks", "very thin", "and gray"], "hint_zh": "強壯的樹幹看起來非常瘦且灰白。"}
            ]
        },
        {
            "id": 17, "img_path": "17.png", "hint": "Swimming goldfish",
            "sentences": [
                {"correct_words": ["The orange goldfish", "swims", "in the clear", "water"], "hint_zh": "橙色的金魚在清澈的水裡游泳。"},
                {"correct_words": ["A tiny animal", "moves", "its soft", "tail"], "hint_zh": "微小的動物擺動牠柔軟的尾巴。"},
                {"correct_words": ["The little fish", "lives", "in a glass", "bowl"], "hint_zh": "小魚住在一個玻璃魚缸裡。"}
            ]
        },
        {
            "id": 18, "img_path": "18.png", "hint": "Insect on leaf",
            "sentences": [
                {"correct_words": ["The green insect", "walks", "on the big", "leaf"], "hint_zh": "綠色的昆蟲在大葉子上爬行。"},
                {"correct_words": ["A small bug", "eats", "the fresh", "plant"], "hint_zh": "小昆蟲吃著新鮮的植物。"},
                {"correct_words": ["The quiet creature", "rests", "in the sunny", "forest"], "hint_zh": "安靜的生物在陽光明媚的森林裡休息。"}
            ]
        },
        {
            "id": 19, "img_path": "19.png", "hint": "Wheat field",
            "sentences": [
                {"correct_words": ["The yellow wheat", "grows", "on the big", "farm"], "hint_zh": "黃色的小麥生長在大農場裡。"},
                {"correct_words": ["A strong wind", "blows", "across the open", "field"], "hint_zh": "強風吹過開闊的田野。"},
                {"correct_words": ["The healthy plant", "looks", "like golden", "money"], "hint_zh": "健康的植物看起來就像金色的錢幣。"}
            ]
        },
        {
            "id": 20, "img_path": "20.png", "hint": "Blue sky and white cloud",
            "sentences": [
                {"correct_words": ["The white cloud", "floats", "in the blue", "sky"], "hint_zh": "白色的雲朵漂浮在藍天中。"},
                {"correct_words": ["A sunny day", "brings", "very warm", "weather"], "hint_zh": "晴朗的一天帶來了非常溫暖的天氣。"},
                {"correct_words": ["The beautiful nature", "makes", "people feel", "happy"], "hint_zh": "美麗的大自然讓人們感到快樂。"}
            ]
        },
        {
            "id": 21, "img_path": "21.png", "hint": "Birthday party",
            "sentences": [
                {"correct_words": ["The happy family", "celebrates", "a birthday", "party"], "hint_zh": "快樂的一家人正在慶祝生日派對。"},
                {"correct_words": ["A delicious cake", "has", "many small", "candles"], "hint_zh": "美味的蛋糕上有許多小蠟燭。"},
                {"correct_words": ["The excited boy", "makes", "a secret", "wish"], "hint_zh": "興奮的男孩許下了一個秘密的願望。"}
            ]
        },
        {
            "id": 22, "img_path": "22.png", "hint": "Sad boy",
            "sentences": [
                {"correct_words": ["The sad boy", "sits", "on the cold", "ground"], "hint_zh": "悲傷的男孩坐在冰冷的地板上。"},
                {"correct_words": ["A crying kid", "loses", "his favorite", "toy"], "hint_zh": "哭泣的小孩弄丟了他最愛的玩具。"},
                {"correct_words": ["The unhappy child", "needs", "a warm", "hug"], "hint_zh": "不高興的孩子需要一個溫暖的擁抱。"}
            ]
        },
        {
            "id": 23, "img_path": "23.png", "hint": "Christmas gifts",
            "sentences": [
                {"correct_words": ["The joyful kids", "open", "their Christmas", "gifts"], "hint_zh": "快樂的孩子們正在拆他們的聖誕禮物。"},
                {"correct_words": ["A beautiful tree", "stands", "in the warm", "room"], "hint_zh": "一棵美麗的樹佇立在溫暖的房間裡。"},
                {"correct_words": ["The colorful box", "holds", "a nice", "surprise"], "hint_zh": "五彩繽紛的盒子裡裝著一個好驚喜。"}
            ]
        },
        {
            "id": 24, "img_path": "24.png", "hint": "Cozy kitchen",
            "sentences": [
                {"correct_words": ["The tidy kitchen", "looks", "very bright", "and clean"], "hint_zh": "整潔的廚房看起來非常明亮且乾淨。"},
                {"correct_words": ["A kind mother", "cooks", "some hot", "soup"], "hint_zh": "親切的媽媽正在煮一些熱湯。"},
                {"correct_words": ["The happy family", "gathers", "near the warm", "stove"], "hint_zh": "快樂的一家人聚集在溫暖的爐灶旁。"}
            ]
        },
        {
            "id": 25, "img_path": "25.png", "hint": "Clean bedroom",
            "sentences": [
                {"correct_words": ["The quiet bedroom", "has", "a comfortable", "bed"], "hint_zh": "安靜的臥室有一張舒適的床。"},
                {"correct_words": ["A big window", "lets", "the bright sunlight", "in"], "hint_zh": "大窗戶讓明亮的陽光灑了進來。"},
                {"correct_words": ["The tidy room", "helps", "children sleep", "well"], "hint_zh": "整潔的房間幫助孩子們睡個好覺。"}
            ]
        },
        {
            "id": 26, "img_path": "26.png", "hint": "Beautiful mountains",
            "sentences": [
                {"correct_words": ["The high mountains", "stand", "near the blue", "lake"], "hint_zh": "高聳的山脈佇立在藍色的湖泊旁。"},
                {"correct_words": ["A grand nature", "looks", "like a beautiful", "picture"], "hint_zh": "壯麗的大自然看起來就像一幅美麗的畫。"},
                {"correct_words": ["The green forest", "covers", "the whole", "valley"], "hint_zh": "綠色的森林覆蓋了整個山谷。"}
            ]
        },
        {
            "id": 27, "img_path": "27.png", "hint": "Strawberry cake",
            "sentences": [
                {"correct_words": ["The sweet cake", "has", "fresh red", "strawberries"], "hint_zh": "甜美的蛋糕上有新鮮的紅草莓。"},
                {"correct_words": ["A hungry person", "eats", "the delicious", "dessert"], "hint_zh": "飢餓的人吃著美味的甜點。"},
                {"correct_words": ["The white plate", "holds", "a big", "slice"], "hint_zh": "白色的盤子裝著一大塊（蛋糕）。"}
            ]
        },
        {
            "id": 28, "img_path": "28.png", "hint": "Watching a movie",
            "sentences": [
                {"correct_words": ["The loving family", "watches", "an exciting", "movie"], "hint_zh": "相親相愛的一家人正在看一部刺激的電影。"},
                {"correct_words": ["A big television", "shines", "in the dark", "living-room"], "hint_zh": "大電視在黑暗的客廳裡閃爍。"},
                {"correct_words": ["The happy group", "shares", "some sweet", "popcorn"], "hint_zh": "快樂的一群人分享著甜甜的爆米花。"}
            ]
        },
        {
            "id": 29, "img_path": "29.png", "hint": "City silhouette",
            "sentences": [
                {"correct_words": ["The tall buildings", "stand", "in the famous", "city"], "hint_zh": "高樓大廈佇立在這座著名的城市裡。"},
                {"correct_words": ["A great statue", "welcomes", "many international", "visitors"], "hint_zh": "巨大的雕像歡迎許多國際訪客。"},
                {"correct_words": ["The dark silhouette", "looks", "very beautiful", "at night"], "hint_zh": "黑暗的剪影在夜裡看起來非常美麗。"}
            ]
        },
        {
            "id": 30, "img_path": "30.png", "hint": "Puppy playing with toy",
            "sentences": [
                {"correct_words": ["The playful puppy", "bites", "a red toy", "bone"], "hint_zh": "愛玩的小狗咬著一個紅色的玩具骨頭。"},
                {"correct_words": ["A cute dog", "lies", "on the soft", "carpet"], "hint_zh": "可愛的狗躺在柔軟的地毯上。"},
                {"correct_words": ["The young animal", "has", "very fluffy", "ears"], "hint_zh": "年幼的動物有一雙非常蓬鬆的耳朵。"}
            ]
        }
    ]

TOTAL_IMAGES = 30

# 初始化狀態
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "current_img_idx" not in st.session_state:
    st.session_state.current_img_idx = 0
if "current_sub_sentence" not in st.session_state:
    st.session_state.current_sub_sentence = 0
if "selected_words" not in st.session_state:
    st.session_state.selected_words = []
if "shuffled_words" not in st.session_state:
    st.session_state.shuffled_words = []
if "img_order" not in st.session_state:
    st.session_state.img_order = list(range(TOTAL_IMAGES))

all_images_data = get_expanded_game_data()

# --- 遊戲大標題 ---
st.title("🧙‍♂️ Letmeask 英語魔法拼圖 (Figma 旗艦版)")
st.markdown("---")

# 開始 / 結束畫面
if not st.session_state.game_started:
    st.markdown("""
    <div class='left-hero-container'>
        <h2 style='color:#FFFFFE; margin:0;'>✨ Toda pergunta tem uma resposta. ✨</h2>
        <p style='color:#E4ECFC; opacity:0.9;'>看圖學語法，點選正確的魔法模組，挑戰 90 道語感關卡！</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 開始拼圖大挑戰 (Start)", type="primary", use_container_width=True):
        st.session_state.game_started = True
        random.shuffle(st.session_state.img_order)
        st.session_state.current_img_idx = 0
        st.session_state.current_sub_sentence = 0
        st.session_state.selected_words = []
        
        first_img = st.session_state.img_order[0]
        words = all_images_data[first_img]["sentences"][0]["correct_words"].copy()
        random.shuffle(words)
        st.session_state.shuffled_words = words
        st.rerun()
else:
    img_stage = st.session_state.current_img_idx
    sub_stage = st.session_state.current_sub_sentence
    
    if img_stage < TOTAL_IMAGES:
        real_img_id = st.session_state.img_order[img_stage]
        img_data = all_images_data[real_img_id]
        sentence_data = img_data["sentences"][sub_stage]
        
        # 🟢 核心工程優化：將頁面一分為二 (左邊照片，右邊題目選項)
        left_col, right_col = st.columns([5, 5], gap="large")
        
        # === 左邊：照片展示區 ===
        with left_col:
            st.markdown(f"### 🖼️ 圖片關卡：第 {img_stage + 1} / {TOTAL_IMAGES} 張")
            
            # Windows 防呆檢測機制 (8.png 或 8.png.png 自動通配)
            possible_paths = [img_data["img_path"], img_data["img_path"] + ".png"]
            final_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    final_path = p
                    break
            
            if final_path:
                # 仿照 Figma 加點圓角美化
                st.image(final_path, use_container_width=True)
            else:
                st.error(f"🚨 找不到圖片檔案: {img_data['img_path']}")
                
            # 左側小卡片進度提示
            stars = ["⚪", "⚪", "⚪"]
            for s in range(sub_stage): stars[s] = "⭐"
            stars[sub_stage] = "🔄"
            
            st.markdown(f"""
            <div style='background-color:#1F1E26; padding:15px; border-radius:12px; text-align:center;'>
                <span style='font-size:16px;'>本圖進度: {' '.join(stars)}</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress((img_stage * 3 + sub_stage) / (TOTAL_IMAGES * 3))

        # === 右邊：題目選項與互動區 ===
        with right_col:
            st.markdown("### 🧩 任務與單字模組")
            
            # 任務提示框
            st.markdown(f"""
            <div class='task-hint-box'>
                <span style='color:#94A1B2; font-size:14px; display:block;'>請拼出對應此圖片的句子:</span>
                <strong style='font-size:18px; color:#FFFFFE;'>{sentence_data['hint_zh']}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # 選項方塊區
            st.markdown("##### 💡 點選以下模組方塊：")
            cols = st.columns(2)  # 改為2列，按鈕更大、更好點選
            for i, word in enumerate(st.session_state.shuffled_words):
                with cols[i % 2]:
                    is_disabled = word in st.session_state.selected_words
                    # 套用主題色按鈕
                    if st.button(word, key=f"w_{img_stage}_{sub_stage}_{i}_{word}", disabled=is_disabled, use_container_width=True):
                        st.session_state.selected_words.append(word)
                        st.rerun()
            
            st.markdown("---")
            
            # 你的句子 (Your Sentence) 顯示區
            st.markdown("##### 📝 你的組合句子 (Your Sentence)：")
            player_sentence = " ".join(st.session_state.selected_words)
            
            # 用自訂 CSS 框表現 Figma 般的文字輸入感
            st.markdown(f"<div class='sentence-display-box'>{player_sentence if player_sentence else '(等待選擇方塊...)'}</div>", unsafe_allow_html=True)
            
            # 底部控制鈕
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🗑️ 清除重來 (Reset)", use_container_width=True):
                    st.session_state.selected_words = []
                    st.rerun()
                    
            # 自動判定與回饋
            is_correct = st.session_state.selected_words == sentence_data["correct_words"]
            if len(st.session_state.selected_words) == len(sentence_data["correct_words"]):
                if is_correct:
                    st.success("🎉 完美！語法順序完全正確！", icon="✅")
                    with btn_col2:
                        next_btn_label = "➡️ 下一句 (Next)" if sub_stage < 2 else "🎆 完成本圖，解鎖下一張！"
                        if st.button(next_btn_label, type="primary", use_container_width=True):
                            st.session_state.selected_words = []
                            
                            if sub_stage < 2:
                                st.session_state.current_sub_sentence += 1
                                next_words = img_data["sentences"][sub_stage + 1]["correct_words"].copy()
                            else:
                                st.session_state.current_img_idx += 1
                                st.session_state.current_sub_sentence = 0
                                if st.session_state.current_img_idx < TOTAL_IMAGES:
                                    next_img_id = st.session_state.img_order[st.session_state.current_img_idx]
                                    next_words = all_images_data[next_img_id]["sentences"][0]["correct_words"].copy()
                                    
                            if st.session_state.current_img_idx < TOTAL_IMAGES:
                                random.shuffle(next_words)
                                st.session_state.shuffled_words = next_words
                            st.rerun()
                else:
                    st.error("❌ 組合順序不太對喔，再試試看！", icon="🚨")
                    
    else:
        # 全部通關
        st.balloons()
        st.markdown("<div class='left-hero-container'><h2>🏆 恭喜大腦與小朋友完成全圖通關！</h2><p>成功掌握了 30 張情境圖、90 道語法方塊魔法！</p></div>", unsafe_allow_html=True)
        if st.button("🔄 重新大挑戰 (Play Again)", type="primary", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()