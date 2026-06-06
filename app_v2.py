import streamlit as st
import random
import os

# 1. 初始化設定網頁佈局
st.set_page_config(page_title="Lavender English Puzzle", layout="wide")

# 2. 頂級深藍黑科技儀表板 UI 樣式表 (CSS)
st.markdown("""
<style>
    /* 移除 Streamlit 頂部預設 header 的干擾 */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* 全局科技感深藍黑背景 */
    .stApp {
        background: radial-gradient(circle at 50% 30%, #0B153A 0%, #05081C 70%, #02040A 100%) !important;
        color: #E2E8F0 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
    }
    
    /* 垂直居中核心包裹器 */
    .block-container {
        padding-top: 1.5rem !important; 
        padding-bottom: 0rem !important;
        min-height: 95vh; 
        display: flex;
        align-items: center; 
        justify-content: center;
    }
    
    /* 讓左右兩欄高度強行等高伸展 */
    [data-testid="stHorizontalBlock"] {
        width: 100%;
        align-items: center !important; 
    }

    /* 左側圖片維持精緻圓角與陰影 */
    .pure-image-card {
        width: 100%;
        display: flex;
        align-items: center; 
        justify-content: center;
        padding: 10px !important;
    }
    .pure-image-card img {
        object-fit: cover;
        height: 68vh !important; 
        width: auto !important;
        max-width: 100%;
        border-radius: 24px !important;
        border: 1px solid rgba(59, 130, 246, 0.25) !important;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.7) !important;
    }
    
    /* 狀態標籤：18px、細體 */
    .status-label {
        font-weight: 300 !important; 
        color: #94A3B8;
        font-size: 18px !important; 
        letter-spacing: 0.5px;
    }
    /* 關卡徽章：18px、細體 */
    .stage-badge {
        background: rgba(59, 130, 246, 0.1);
        color: #60A5FA;
        padding: 6px 16px;
        border-radius: 20px;
        font-weight: 300 !important; 
        font-size: 18px !important; 
        border: 1px solid rgba(59, 130, 246, 0.25);
    }
    
    /* 右側各區塊面板外框 */
    .status-badge-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(18, 26, 62, 0.85);
        padding: 22px 28px; 
        border-radius: 20px;
        border: 1px solid rgba(59, 130, 246, 0.2); 
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    /* Streamlit 原生進度條高度與顏色微調 */
    .stProgress {
        margin-bottom: 16px !important;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, #3B82F6, #8B5CF6) !important;
        height: 8px !important;
    }
    
    /* 任務提示框 */
    .duo-hint-box {
        background: rgba(15, 23, 56, 0.9);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 28px 24px; 
        border-radius: 24px;
        margin-bottom: 16px;
        text-align: center; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    /* 提示副標題：18px、細體 */
    .duo-hint-title {
        color: #38BDF8; 
        font-size: 18px !important; 
        font-weight: 300 !important; 
        display: block; 
        text-transform: uppercase; 
        margin-bottom: 10px;
        letter-spacing: 1.5px;
    }
    /* 中文提示主文字：18px、細體 */
    .duo-hint-text {
        font-size: 18px !important; 
        font-weight: 300 !important; 
        color: #FFFFFF;
        line-height: 1.5;
    }
    
    /* 區塊小標題：18px、細體 */
    .panel-section-title {
        font-weight: 300 !important; 
        color: #94A3B8; 
        font-size: 18px !important; 
        margin: 14px 0px 10px 4px !important;
        text-align: center; 
    }
    
    /* 玩家組合結果框：18px、細體 */
    .sentence-display-box {
        background: rgba(9, 15, 38, 0.95);
        border: 2px dashed rgba(96, 165, 250, 0.3);
        padding: 22px; 
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px !important; 
        color: #60A5FA;
        font-weight: 300 !important; 
        border-radius: 20px;
        margin-bottom: 18px;
        text-align: center;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.1);
    }

    /* 🎯 點選模塊：4 個方塊按鈕維持 20px + 顯著粗體 🎯 */
    div.stButton > button {
        background: rgba(18, 26, 62, 0.85) !important;
        color: #E2E8F0 !important;
        font-size: 20px !important; 
        font-weight: 700 !important; 
        border: 1px solid rgba(59, 130, 246, 0.35) !important; 
        border-radius: 18px !important;
        padding: 14px 20px !important; 
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    
    div.stButton > button:hover:not([disabled]) {
        background: rgba(25, 37, 84, 0.95) !important;
        border-color: rgba(96, 165, 250, 0.7) !important; 
        color: #FFFFFF !important;
        box-shadow: 0 0 18px rgba(59, 130, 246, 0.4) !important;
    }
    
    div.stButton > button[disabled] {
        background: rgba(10, 15, 30, 0.4) !important;
        color: #475569 !important;
        border: 1px solid rgba(59, 130, 246, 0.05) !important;
        opacity: 0.3;
    }

    /* 重來與一般設定頁按鈕容器：內含文字改為 18px、細體 */
    .reset-btn div.stButton > button, .setup-container div.stButton > button {
        background: rgba(30, 41, 59, 0.7) !important;
        color: #94A3B8 !important;
        font-size: 18px !important; 
        font-weight: 300 !important;
        padding: 12px 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .reset-btn div.stButton > button:hover {
        background: rgba(239, 68, 68, 0.2) !important;
        border-color: rgba(239, 68, 68, 0.6) !important;
        color: #FCA5A5 !important;
    }
    .setup-container div.stButton > button:hover {
        background: rgba(59, 130, 246, 0.2) !important;
        border-color: rgba(59, 130, 246, 0.6) !important;
        color: #93C5FD !important;
    }

    /* 前進與主啟動按鈕：18px、細體 */
    div.stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        font-size: 18px !important; 
        font-weight: 300 !important;
        padding: 14px 20px !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3) !important;
    }

    /* 調整下拉選單標籤與內容字體為 18px 細體 */
    div[data-testid="stSelectbox"] label p {
        font-size: 18px !important;
        font-weight: 300 !important;
        color: #94A3B8 !important;
    }
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 18px !important;
        font-weight: 300 !important;
        background-color: rgba(18, 26, 62, 0.85) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
    }
    
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. 載入核心資料庫 (保持 30 張圖資料)
@st.cache_data
def get_expanded_game_data():
    return [
        {
            "id": 1, "img_path": "1.png", "hint": "男孩吃早餐",
            "sentences": [
                {"correct_words": ["The happy boy", "is eating", "yummy", "breakfast"], "hint_zh": "快樂的男孩正在吃美味的早餐。"},
                {"correct_words": ["A sweet child", "likes", "warm and healthy", "food"], "hint_zh": "可愛的孩子喜歡溫慢又健康的食物。"},
                {"correct_words": ["The little kid", "sits", "at the kitchen", "table"], "hint_zh": "小孩子坐在廚房的桌子旁。"}
            ]
        },
        {
            "id": 2, "img_path": "2.png", "hint": "女孩上學",
            "sentences": [
                {"correct_words": ["The cute girl", "walks", "to the beautiful", "school"], "hint_zh": "可愛的女孩走路去美麗的學校。"},
                {"correct_words": ["A young student", "carries", "a pink", "schoolbag"], "hint_zh": "年輕的學生背著一個粉紅色的書包。"},
                {"correct_words": ["The smart child", "looks", "very excited", "today"], "hint_zh": "這個聰明的孩子今天看起來非常興奮。"}
            ]
        },
        {
            "id": 3, "img_path": "3.png", "hint": "睡覺的貓咪",
            "sentences": [
                {"correct_words": ["The lazy cat", "is sleeping", "on the warm", "blanket"], "hint_zh": "懶惰的貓咪在溫慢的毛毯上睡覺。"},
                {"correct_words": ["A soft pet", "closes", "its two small", "eyes"], "hint_zh": "柔軟的寵物閉上了牠的兩隻小眼睛。"},
                {"correct_words": ["The grey kitty", "feels", "so safe", "and comfortable"], "hint_zh": "這隻灰色的小貓感到非常安全和舒服。"}
            ]
        },
        {
            "id": 4, "img_path": "4.png", "hint": "嬰兒洗澡",
            "sentences": [
                {"correct_words": ["The little baby", "takes", "a warm and clean", "bath"], "hint_zh": "小嬰兒洗了一個溫慢又乾淨的澡。"},
                {"correct_words": ["A happy infant", "plays", "with water", "happily"], "hint_zh": "快樂的幼兒高興地玩著水。"},
                {"correct_words": ["The cute child", "has", "many white", "bubbles"], "hint_zh": "可愛的孩子身上有許多白色的泡泡。"}
            ]
        },
        {
            "id": 5, "img_path": "5.png", "hint": "男孩寫功課",
            "sentences": [
                {"correct_words": ["The diligent boy", "writes", "his English", "homework"], "hint_zh": "勤奮的男孩正在寫他的英文功課。"},
                {"correct_words": ["A smart kid", "studies", "at his quiet", "desk"], "hint_zh": "聰明的小孩在他安靜的書桌前學習。"},
                {"correct_words": ["The young student", "uses", "a sharp", "pencil"], "hint_zh": "年輕的學生使用一枝鋒利的鉛筆。"}
            ]
        },
        {
            "id": 6, "img_path": "6.png", "hint": "女孩看書",
            "sentences": [
                {"correct_words": ["The quiet girl", "reads", "an interesting", "storybook"], "hint_zh": "安靜的女孩正在讀一本有趣的故事書。"},
                {"correct_words": ["A clever child", "learns", "many new", "words"], "hint_zh": "聰明的孩子學到了許多新的單字。"},
                {"correct_words": ["The young reader", "loves", "this fantastic", "library"], "hint_zh": "年輕的讀者喜愛這個奇妙的圖書館。"}
            ]
        },
        {
            "id": 7, "img_path": "7.png", "hint": "踢足球",
            "sentences": [
                {"correct_words": ["The active children", "play", "a soccer", "game"], "hint_zh": "活躍的孩子們正在踢一場足球賽。"},
                {"correct_words": ["A strong team", "runs", "on the green", "field"], "hint_zh": "強壯的隊伍在綠色的球場上跑步。"},
                {"correct_words": ["The excited players", "kick", "the round", "ball"], "hint_zh": "興奮的球員們踢著圓圓的球。"}
            ]
        },
        {
            "id": 8, "img_path": "8.png", "hint": "玩具摩托車",
            "sentences": [
                {"correct_words": ["The brave boy", "rides", "a red toy", "motorcycle"], "hint_zh": "勇敢的男孩騎著一輛紅色的玩具摩托車。"},
                {"correct_words": ["A cool kid", "wears", "a safe", "helmet"], "hint_zh": "酷炫的小孩戴著一頂安全的安全帽。"},
                {"correct_words": ["The small driver", "goes", "around the park", "safely"], "hint_zh": "小小的駕駛員安全地在公園裡繞行。"}
            ]
        },
        {
            "id": 9, "img_path": "9.png", "hint": "彈吉他",
            "sentences": [
                {"correct_words": ["The talented man", "plays", "the wooden", "guitar"], "hint_zh": "有才華的男子正在彈奏木吉他。"},
                {"correct_words": ["A nice musician", "sings", "a beautiful", "song"], "hint_zh": "優秀的音樂家正在唱一首美麗的歌。"},
                {"correct_words": ["The music coach", "makes", "very sweet", "sounds"], "hint_zh": "音樂教練發出了非常甜美的聲音。"}
            ]
        },
        {
            "id": 10, "img_path": "10.png", "hint": "刷牙",
            "sentences": [
                {"correct_words": ["The healthy boy", "brushes", "his white", "teeth"], "hint_zh": "健康的男孩正在刷他潔白的牙齒。"},
                {"correct_words": ["A clean kid", "uses", "a blue", "toothbrush"], "hint_zh": "愛乾淨的小孩使用一支藍色的牙刷。"},
                {"correct_words": ["The smart child", "washes", "his face", "every morning"], "hint_zh": "聰明的孩子每天早上都會洗臉。"}
            ]
        },
        {
            "id": 11, "img_path": "11.png", "hint": "美麗夕陽",
            "sentences": [
                {"correct_words": ["The orange sun", "goes", "down the mountain", "slowly"], "hint_zh": "橙色的太陽緩緩地落入山後。"},
                {"correct_words": ["A beautiful sunset", "makes", "the bright", "sky"], "hint_zh": "美麗的夕陽形成了明亮的天空。"},
                {"correct_words": ["The warm light", "shines", "on the quiet", "land"], "hint_zh": "溫慢的光芒照耀在安靜的大地上。"}
            ]
        },
        {
            "id": 12, "img_path": "12.png", "hint": "下雨天",
            "sentences": [
                {"correct_words": ["The cold rain", "falls", "on the dark", "window"], "hint_zh": "冰冷的雨水落在黑暗的窗戶上。"},
                {"correct_words": ["A heavy storm", "hits", "the big", "city"], "hint_zh": "一場大風暴襲擊了這座大城市。"},
                {"correct_words": ["The weather tonight", "looks", "very wet", "and gray"], "hint_zh": "今天晚上的天氣看起來非常潮濕且陰暗。"}
            ]
        },
        {
            "id": 13, "img_path": "13.png", "hint": "條紋小貓",
            "sentences": [
                {"correct_words": ["The tiny kitten", "sits", "on the clean", "floor"], "hint_zh": "微小的小貓坐在乾淨的地板上。"},
                {"correct_words": ["A lovely pet", "has", "brown and striped", "fur"], "hint_zh": "可愛的寵物擁有棕色條紋的毛髮。"},
                {"correct_words": ["The sweet animal", "watches", "the moving", "toy"], "hint_zh": "甜美的動物注視著移動的玩具。"}
            ]
        },
        {
            "id": 14, "img_path": "14.png", "hint": "飛舞蝴蝶",
            "sentences": [
                {"correct_words": ["The small butterfly", "flies", "in the sunny", "garden"], "hint_zh": "小蝴蝶在陽光明媚的花園裡飛舞。"},
                {"correct_words": ["A colorful insect", "visits", "the sweet", "flowers"], "hint_zh": "五彩繽紛的昆蟲拜訪了甜美的花朵。"},
                {"correct_words": ["The beautiful bug", "has", "two thin", "wings"], "hint_zh": "美麗的昆蟲有一雙薄薄的翅膀。"}
            ]
        },
        {
            "id": 15, "img_path": "15.png", "hint": "紅玫瑰花",
            "sentences": [
                {"correct_words": ["The red flower", "grows", "near the green", "bush"], "hint_zh": "紅色的花朵生長在綠色的灌木叢旁。"},
                {"correct_words": ["A fresh plant", "opens", "its bright", "petals"], "hint_zh": "新鮮的植物展開了它鮮豔的花瓣。"},
                {"correct_words": ["The beautiful rose", "smells", "very sweet", "and nice"], "hint_zh": "美麗的玫瑰聞起來非常香甜芬芳。"}
            ]
        },
        {
            "id": 16, "img_path": "16.png", "hint": "藍天枯樹",
            "sentences": [
                {"correct_words": ["The old tree", "stands", "under the blue", "sky"], "hint_zh": "古老的大樹佇立在藍天之下。"},
                {"correct_words": ["A tall plant", "loses", "all its dry", "leaves"], "hint_zh": "高大的植物失去了它所有乾枯的葉子。"},
                {"correct_words": ["The strong trunk", "looks", "very thin", "and gray"], "hint_zh": "強壯的樹幹看起來非常瘦且灰白。"}
            ]
        },
        {
            "id": 17, "img_path": "17.png", "hint": "小金魚",
            "sentences": [
                {"correct_words": ["The orange goldfish", "swims", "in the clear", "water"], "hint_zh": "橙色的金魚在清澈的水裡游泳。"},
                {"correct_words": ["A tiny animal", "moves", "its soft", "tail"], "hint_zh": "微小的動物擺動牠柔軟的尾巴。"},
                {"correct_words": ["The little fish", "lives", "in a glass", "bowl"], "hint_zh": "小魚住在一個玻璃魚缸裡。"}
            ]
        },
        {
            "id": 18, "img_path": "18.png", "hint": "綠色昆蟲",
            "sentences": [
                {"correct_words": ["The green insect", "walks", "on the big", "leaf"], "hint_zh": "綠色的昆蟲在大葉子上爬行。"},
                {"correct_words": ["A small bug", "eats", "the fresh", "plant"], "hint_zh": "小昆蟲吃著新鮮的植物。"},
                {"correct_words": ["The quiet creature", "rests", "in the sunny", "forest"], "hint_zh": "安靜的生物在陽光明媚的森林裡休息。"}
            ]
        },
        {
            "id": 19, "img_path": "19.png", "hint": "金色小麥",
            "sentences": [
                {"correct_words": ["The yellow wheat", "grows", "on the big", "farm"], "hint_zh": "黃色的小麥生長在大農場裡。"},
                {"correct_words": ["A strong wind", "blows", "across the open", "field"], "hint_zh": "強風吹過開闊的田野。"},
                {"correct_words": ["The healthy plant", "looks", "like golden", "money"], "hint_zh": "健康的植物看起來就像金色的錢幣。"}
            ]
        },
        {
            "id": 20, "img_path": "20.png", "hint": "藍天白雲",
            "sentences": [
                {"correct_words": ["The white cloud", "floats", "in the blue", "sky"], "hint_zh": "白色的雲朵漂浮在藍天中。"},
                {"correct_words": ["A sunny day", "brings", "the weather", "cloud"], "hint_zh": "晴朗的一天帶來了滿天的天氣雲朵。"},
                {"correct_words": ["The beautiful nature", "makes", "people feel", "happy"], "hint_zh": "美麗的大自然讓人們感到快樂。"}
            ]
        },
        {
            "id": 21, "img_path": "21.png", "hint": "生日派對",
            "sentences": [
                {"correct_words": ["The happy family", "celebrates", "a birthday", "party"], "hint_zh": "快樂的一家人正在慶祝生日派對。"},
                {"correct_words": ["A delicious cake", "has", "many small", "candles"], "hint_zh": "美味的蛋糕上有許多小蠟燭。"},
                {"correct_words": ["The excited boy", "makes", "a secret", "wish"], "hint_zh": "興奮的男孩許下了一個秘密的願望。"}
            ]
        },
        {
            "id": 22, "img_path": "22.png", "hint": "傷心的男孩",
            "sentences": [
                {"correct_words": ["The sad boy", "sits", "on the cold", "ground"], "hint_zh": "悲傷的男孩坐在冰冷的地板上。"},
                {"correct_words": ["A crying kid", "loses", "his favorite", "toy"], "hint_zh": "哭泣的小孩弄丟了他最愛的玩具。"},
                {"correct_words": ["The unhappy child", "needs", "a warm", "hug"], "hint_zh": "不高興的孩子需要一個溫慢的擁抱。"}
            ]
        },
        {
            "id": 23, "img_path": "23.png", "hint": "聖誕禮物",
            "sentences": [
                {"correct_words": ["The joyful kids", "open", "their Christmas", "gifts"], "hint_zh": "快樂的孩子們正在拆他們的聖誕禮物。"},
                {"correct_words": ["A beautiful tree", "stands", "in the warm", "room"], "hint_zh": "一棵美麗的樹佇立在溫慢的房間裡。"},
                {"correct_words": ["The colorful box", "holds", "a nice", "surprise"], "hint_zh": "五彩繽紛的盒子裡裝著一個好驚喜。"}
            ]
        },
        {
            "id": 24, "img_path": "24.png", "hint": "乾淨廚房",
            "sentences": [
                {"correct_words": ["The tidy kitchen", "looks", "very bright", "and clean"], "hint_zh": "整潔的廚房看起來意謂著明亮且乾淨。"},
                {"correct_words": ["A kind mother", "cooks", "some hot", "soup"], "hint_zh": "親切的媽媽正在煮一些熱湯。"},
                {"correct_words": ["The happy family", "gathers", "near the warm", "stove"], "hint_zh": "快樂的一家人聚集在溫慢的爐灶旁。"}
            ]
        },
        {
            "id": 25, "img_path": "25.png", "hint": "舒適臥室",
            "sentences": [
                {"correct_words": ["The quiet bedroom", "has", "a comfortable", "bed"], "hint_zh": "安靜的臥室有一張舒適的床。"},
                {"correct_words": ["A big window", "lets", "the bright sunlight", "in"], "hint_zh": "大窗戶讓明亮的陽光灑了進來。"},
                {"correct_words": ["The tidy room", "helps", "children sleep", "well"], "hint_zh": "整潔的房間幫助孩子們睡個好覺。"}
            ]
        },
        {
            "id": 26, "img_path": "26.png", "hint": "高山與湖泊",
            "sentences": [
                {"correct_words": ["The high mountains", "stand", "near the blue", "lake"], "hint_zh": "高聳的山脈佇立在藍色的湖泊旁。"},
                {"correct_words": ["A grand nature", "looks", "like a beautiful", "picture"], "hint_zh": "壯麗的大自然看起來就像一幅美麗的畫。"},
                {"correct_words": ["The green forest", "covers", "the whole", "valley"], "hint_zh": "綠色的森林覆蓋了整個山谷。"}
            ]
        },
        {
            "id": 27, "img_path": "27.png", "hint": "草莓蛋糕",
            "sentences": [
                {"correct_words": ["The sweet cake", "has", "fresh red", "strawberries"], "hint_zh": "甜美的蛋糕上有新鮮的紅草莓。"},
                {"correct_words": ["A hungry person", "eats", "the delicious", "dessert"], "hint_zh": "幾餓的人吃著美味的甜點。"},
                {"correct_words": ["The white plate", "holds", "a big", "slice"], "hint_zh": "白色的盤子裝著一大塊。"}
            ]
        },
        {
            "id": 28, "img_path": "28.png", "hint": "看電影",
            "sentences": [
                {"correct_words": ["The loving family", "watches", "an exciting", "movie"], "hint_zh": "相親相愛的一家人正在看一部刺激的電影。"},
                {"correct_words": ["A big television", "shines", "in the dark", "living-room"], "hint_zh": "大電視在黑暗的客廳裡閃爍.共享。"},
                {"correct_words": ["The happy group", "shares", "some sweet", "popcorn"], "hint_zh": "快樂的一群人分享著甜甜的爆米花。"}
            ]
        },
        {
            "id": 29, "img_path": "29.png", "hint": "城市剪影",
            "sentences": [
                {"correct_words": ["The tall buildings", "stand", "in the famous", "city"], "hint_zh": "高樓大廈佇立在这座著名的城市裡。"},
                {"correct_words": ["A great statue", "welcomes", "many international", "visitors"], "hint_zh": "巨大的雕像歡迎許多國際訪客。"},
                {"correct_words": ["The dark silhouette", "looks", "very beautiful", "at night"], "hint_zh": "黑暗的剪影在夜裡看起來非常美麗。"}
            ]
        },
        {
            "id": 30, "img_path": "30.png", "hint": "可愛小狗",
            "sentences": [
                {"correct_words": ["The playful puppy", "bites", "a red toy", "bone"], "hint_zh": "愛玩的小狗咬著一個紅色的玩具骨頭。"},
                {"correct_words": ["A cute dog", "lies", "on the soft", "carpet"], "hint_zh": "可愛的狗躺在柔軟的地毯上。"},
                {"correct_words": ["The young animal", "has", "very fluffy", "ears"], "hint_zh": "年幼的動物有一雙非常蓬鬆的耳朵。"}
            ]
        }
    ]

TOTAL_IMAGES = 30
all_images_data = get_expanded_game_data()

# 初始化工作階段變數
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

# 🌟 頁面路由：未開始時顯示「設定與關卡選擇頁面」
if not st.session_state.game_started:
    st.markdown("""
    <div class='duo-hint-box' style='text-align: center; width: 100%; padding: 40px 30px;'>
        <h2 style='color:#38BDF8; margin:0; font-weight: 800; font-size: 32px;'>English Magic Puzzle</h2>
        <p style='color:#94A3B8; margin-top: 12px; font-size: 18px; font-weight: 300;'>歡迎來到英語魔幻拼圖！請選擇你的挑戰模式：</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 建立關卡選單清單
    select_options = [f"第 {i+1} 關：{all_images_data[i]['hint']}" for i in range(TOTAL_IMAGES)]
    
    # 呈現選單與模式選擇
    chosen_stage_str = st.selectbox("🎯 選擇出發關卡 (跳關專用)：", select_options)
    chosen_idx = select_options.index(chosen_stage_str)
    
    st.markdown("<div class='setup-container'>", unsafe_allow_html=True)
    
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        # 模式一：原本的隨機洗牌模式
        if st.button("🚀 隨機洗牌挑戰 (30關隨機打亂)", type="primary", use_container_width=True):
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
            
    with col_mode2:
        # 模式二：從選定關卡依序前進
        if st.button(f"順序挑戰 ➡️ (從第 {chosen_idx+1} 關依序往後)", use_container_width=True):
            st.session_state.game_started = True
            # 生成從選定關卡開始，一路到第30關的順序陣列
            st.session_state.img_order = list(range(chosen_idx, TOTAL_IMAGES))
            st.session_state.current_img_idx = 0
            st.session_state.current_sub_sentence = 0
            st.session_state.selected_words = []
            
            first_img = st.session_state.img_order[0]
            words = all_images_data[first_img]["sentences"][0]["correct_words"].copy()
            random.shuffle(words)
            st.session_state.shuffled_words = words
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)

else:
    img_stage = st.session_state.current_img_idx
    sub_stage = st.session_state.current_sub_sentence
    active_total_stages = len(st.session_state.img_order)
    
    if img_stage < active_total_stages:
        real_img_id = st.session_state.img_order[img_stage]
        img_data = all_images_data[real_img_id]
        sentence_data = img_data["sentences"][sub_stage]
        
        left_col, right_col = st.columns([4.2, 5.8], gap="large")
        
        # === 【左邊：縮小版精緻圖片面版】 ===
        with left_col:
            base_name = str(real_img_id + 1)
            possible_paths = [img_data["img_path"], f"{base_name}.png", f"{base_name}.PNG"]
            final_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    final_path = p
                    break
            
            if final_path:
                st.markdown("<div class='pure-image-card'>", unsafe_allow_html=True)
                st.image(final_path, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error(f"🚨 找不到圖片檔案：{base_name}.png")

        # === 【右邊：全規格重塑面板】 ===
        with right_col:
            # 1. 狀態欄
            stars = ["⚪", "⚪", "⚪"]
            for s in range(sub_stage): stars[s] = "⭐"
            stars[sub_stage] = "🔄"
            
            # 動態顯示當前絕對關卡編號
            st.markdown(f"""
            <div class='status-badge-container'>
                <span class='status-label'>⚡ Progress: {' '.join(stars)}</span>
                <span class='stage-badge'>關卡: {real_img_id + 1} ({img_stage + 1} / {active_total_stages})</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress((img_stage * 3 + sub_stage) / (active_total_stages * 3))
            
            # 2. 中文提示框
            st.markdown(f"""
            <div class='duo-hint-box'>
                <span class='duo-hint-title'>Description / 中文提示</span>
                <div class='duo-hint-text'>{sentence_data['hint_zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 3. 點選字塊區 (按鈕固定為 20px 粗體)
            st.markdown("<p class='panel-section-title'>Word Bank / 點選模塊：</p>", unsafe_allow_html=True)
            
            cols = st.columns(2)
            for i, word in enumerate(st.session_state.shuffled_words):
                with cols[i % 2]:
                    is_disabled = word in st.session_state.selected_words
                    if st.button(word, key=f"btn_{real_img_id}_{sub_stage}_{i}_{word}", disabled=is_disabled, use_container_width=True):
                        st.session_state.selected_words.append(word)
                        st.rerun()
            
            # 4. 句子結果區 (框內文字降為 18px 細體)
            st.markdown("<p class='panel-section-title'>Your Sentence / 組合的句子：</p>", unsafe_allow_html=True)
            player_sentence = " ".join(st.session_state.selected_words)
            st.markdown(f"<div class='sentence-display-box'>{player_sentence if player_sentence else 'Select words from above to build...'}</div>", unsafe_allow_html=True)
            
            # 5. 底部控制按鈕
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                st.markdown("<div class='reset-btn'>", unsafe_allow_html=True)
                if st.button("🗑️ Reset / 重來", use_container_width=True):
                    st.session_state.selected_words = []
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
                    
            is_correct = st.session_state.selected_words == sentence_data["correct_words"]
            if len(st.session_state.selected_words) == len(sentence_data["correct_words"]):
                if is_correct:
                    st.toast("✨ System Verified: Perfect Match!", icon="🟢")
                    with btn_col2:
                        next_btn_label = "➡️ Next Sentence" if sub_stage < 2 else "🎆 Next Stage ➡️"
                        if st.button(next_btn_label, type="primary", use_container_width=True):
                            st.session_state.selected_words = []
                            
                            if sub_stage < 2:
                                st.session_state.current_sub_sentence += 1
                                next_words = img_data["sentences"][sub_stage + 1]["correct_words"].copy()
                            else:
                                st.session_state.current_img_idx += 1
                                st.session_state.current_sub_sentence = 0
                                if st.session_state.current_img_idx < active_total_stages:
                                    next_img_id = st.session_state.img_order[st.session_state.current_img_idx]
                                    next_words = all_images_data[next_img_id]["sentences"][0]["correct_words"].copy()
                                    
                            if st.session_state.current_img_idx < active_total_stages:
                                random.shuffle(next_words)
                                st.session_state.shuffled_words = next_words
                            st.rerun()
                else:
                    st.error("💡 Syntax Order Error! 調整一下單字的順序看看。")
                    
    else:
        st.balloons()
        st.markdown("<div class='duo-hint-box' style='text-align:center; width:100%;'><h2>🏆 MISSION ACCOMPLISHED / 本輪挑戰完美通關！</h2></div>", unsafe_allow_html=True)
        if st.button("🔄 返回首頁 / 重新選關", type="primary", use_container_width=True):
            st.session_state.game_started = False
            st.rerun()
