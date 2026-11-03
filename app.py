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
