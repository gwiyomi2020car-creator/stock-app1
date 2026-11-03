import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="蝦皮 5 折秒殺專區 - 居家生活館",
    page_icon="🏠",
    layout="centered"
)

# --- 注入現代化夜間 App 風格 CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    .app-header {
        background: linear-gradient(135deg, #10B981 0%, #047857 100%);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.3);
    }
    .app-title {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .app-sub {
        font-size: 13px;
        color: #D1FAE5;
    }

    .deal-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .discount-badge {
        background-color: #EF4444;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
    }
    .category-badge {
        background-color: #3B82F6;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
        margin-left: 4px;
    }
    .item-name {
        font-size: 15px;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 8px;
    }
    .price-text {
        font-size: 16px;
        font-weight: 700;
        color: #EF4444;
    }
    .original-price {
        font-size: 12px;
        color: #94A3B8;
        text-decoration: line-through;
        margin-left: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 頂部 App 標題 ---
st.markdown("""
    <div class="app-header">
        <div class="app-title">🏠 蝦皮 5 折秒殺專區 - 居家生活館</div>
        <div class="app-sub">精選全網破盤家用品，點擊直接前往商品頁！</div>
    </div>
""", unsafe_allow_html=True)

# --- 家用品資料庫 (帶分類標籤) ---
deals = [
    {
        "category": "🛏️ 寢具家飾",
        "name": "日本石墨烯發熱保暖冬被 (雙人)",
        "price": "NT$ 1,100",
        "origin": "NT$ 2,500",
        "discount": "4.4 折",
        "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"  # 請替換為真實商品連結
    },
    {
        "category": "🪑 家具收納",
        "name": "北歐風簡約實木收納床頭櫃",
        "price": "NT$ 799",
        "origin": "NT$ 1,800",
        "discount": "4.4 折",
        "image": "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"  # 請替換為真實商品連結
    },
    {
        "category": "🧹 清潔衛浴",
        "name": "車用/家用無線強力吸塵器旗艦版",
        "price": "NT$ 680",
        "origin": "NT$ 1,680",
        "discount": "3.8 折",
        "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"  # 請替換為真實商品連結
    },
    {
        "category": "🍽️ 廚房餐飲",
        "name": "日式麥飯石不沾鍋平底鍋 28cm",
        "price": "NT$ 499",
        "origin": "NT$ 1,200",
        "discount": "4.1 折",
        "image": "https://images.unsplash.com/photo-1584992236310-6edddc08acff?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"  # 請替換為真實商品連結
    }
]

# --- 分類切換按鈕 ---
categories = ["全部", "🛏️ 寢具家飾", "🪑 家具收納", "🧹 清潔衛浴", "🍽️ 廚房餐飲"]
selected_cat = st.selectbox("選擇家用品分類過濾：", categories)

st.markdown("---")

# 根據選擇進行過濾
filtered_deals = deals if selected_cat == "全部" else [d for d in deals if d["category"] == selected_cat]

st.markdown(f"### 🔥 符合條件的商品 ({len(filtered_deals)} 件)")

# 渲染每個商品卡片
for item in filtered_deals:
    with st.container():
        st.markdown(f"""
            <div class="deal-box">
                <span class="discount-badge">🔥 {item['discount']}</span>
                <span class="category-badge">{item['category']}</span>
                <div class="item-name">{item['name']}</div>
                <div>
                    <span class="price-text">{item['price']}</span>
                    <span class="original-price">{item['origin']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.image(item['image'], use_container_width=True)
        st.link_button("🔗 點我直接前往搶購", item['link'], use_container_width=True)
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="蝦皮 5 折極速秒殺 App",
    page_icon="⚡",
    layout="centered"
)

# --- 注入現代化夜間 App 風格 CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* 頂部獨立 App 標題橫幅 */
    .app-header {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(239, 68, 68, 0.4);
    }
    .app-title {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .app-sub {
        font-size: 13px;
        color: #FEE2E2;
    }

    /* 商品獨立卡片 */
    .deal-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .discount-badge {
        background-color: #EF4444;
        color: white;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
    }
    .item-name {
        font-size: 15px;
        font-weight: 600;
        color: #F1F5F9;
        margin-bottom: 8px;
    }
    .price-text {
        font-size: 16px;
        font-weight: 700;
        color: #EF4444;
    }
    .original-price {
        font-size: 12px;
        color: #94A3B8;
        text-decoration: line-through;
        margin-left: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 頂部 App 標題 ---
st.markdown("""
    <div class="app-header">
        <div class="app-title">⚡ 蝦皮 5 折以下極速秒殺專區</div>
        <div class="app-sub">精選全網折扣低於 50% 的破盤神物，點擊直接前往搶購！</div>
    </div>
""", unsafe_allow_html=True)

# --- 嚴選 5 折以下的商品清單（附圖片與直達連結） ---
deals = [
    {
        "name": "【官方旗艦】ANC 主動降噪無線藍牙耳機",
        "price": "NT$ 990",
        "origin": "NT$ 2,990",
        "discount": "3.3 折",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"
    },
    {
        "name": "北歐風簡約實木收納床頭櫃",
        "price": "NT$ 799",
        "origin": "NT$ 1,800",
        "discount": "4.4 折",
        "image": "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"
    },
    {
        "name": "日本石墨烯發熱保暖冬被 (雙人)",
        "price": "NT$ 1,100",
        "origin": "NT$ 2,500",
        "discount": "4.4 折",
        "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"
    },
    {
        "name": "車用/家用無線強力吸塵器旗艦版",
        "price": "NT$ 680",
        "origin": "NT$ 1,680",
        "discount": "3.8 折",
        "image": "https://images.unsplash.com/photo-1558317374-067fb5f30001?w=600&auto=format&fit=crop&q=80",
        "link": "https://shopee.tw"
    }
]

st.markdown("### 🔥 目前符合條件的 5 折以下商品")

# 渲染每個商品卡片
for item in deals:
    with st.container():
        # 標題與折扣標籤區
        st.markdown(f"""
            <div class="deal-box">
                <span class="discount-badge">🔥 殺到 {item['discount']}</span>
                <div class="item-name">{item['name']}</div>
                <div>
                    <span class="price-text">{item['price']}</span>
                    <span class="original-price">{item['origin']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 商品圖片
        st.image(item['image'], use_container_width=True)
        
        # 直達搶購按鈕
        st.link_button("🔗 點我直接前往搶購", item['link'], use_container_width=True)
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
