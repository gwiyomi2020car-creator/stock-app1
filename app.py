import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="蝦皮 5 折秒殺傳送門",
    page_icon="🔥",
    layout="centered"
)

# --- 注入極簡質感與夜間模式 CSS ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    .header-card {
        background: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    .header-title {
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .header-subtitle {
        font-size: 12px;
        color: #FEE2E2;
    }

    /* 商品卡片設計 */
    .deal-card {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 15px;
    }
    .deal-title {
        font-size: 15px;
        font-weight: 600;
        color: #F9FAFB;
        margin-bottom: 6px;
    }
    .deal-price {
        font-size: 14px;
        color: #EF4444;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .original-price {
        text-decoration: line-through;
        color: #9CA3AF;
        font-size: 12px;
        margin-left: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 頂部 Banner ---
st.markdown("""
    <div class="header-card">
        <div class="header-title">🔥 蝦皮 5 折以下秒殺傳送門</div>
        <div class="header-subtitle">精選全網超殺折扣商品 ‧ 附圖即時搶購</div>
    </div>
""", unsafe_allow_html=True)

# --- 含有商品圖片、資訊與連結的清單 ---
deals = [
    {
        "title": "【官方旗艦】無線藍牙降噪耳機 (限時3.3折)",
        "price": "NT$ 990",
        "origin": "NT$ 2,990",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60",
        "link": "https://shopee.tw"
    },
    {
        "title": "北歐風簡約實木床頭櫃 (破盤4.4折)",
        "price": "NT$ 799",
        "origin": "NT$ 1,800",
        "image": "https://images.unsplash.com/photo-1538688525198-9b88f6f53126?w=500&auto=format&fit=crop&q=60",
        "link": "https://shopee.tw"
    },
    {
        "title": "大容量石墨烯發熱被 (秒殺4.4折)",
        "price": "NT$ 1,100",
        "origin": "NT$ 2,500",
        "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=500&auto=format&fit=crop&q=60",
        "link": "https://shopee.tw"
    },
    {
        "title": "超強吸力無線手持吸塵器 (下殺3.8折)",
