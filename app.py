import streamlit as st

# 頁面基本設定
st.set_page_config(
    page_title="淘寶 5 折秒殺專區",
    page_icon="🛍️",
    layout="centered"
)

# --- 注入現代化夜間 App 風格 CSS (淘寶橘紅主題) ---
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
        background: linear-gradient(135deg, #F97316 0%, #EA580C 100%);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(249, 115, 22, 0.4);
    }
    .app-title {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .app-sub {
        font-size: 13px;
        color: #FFEDD5;
    }

    .deal-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .discount-badge {
        background-color: #F97316;
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
        color: #F97316;
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
        <div class="app-title">🛍️ 淘寶 5 折以下秒殺專區</div>
        <div class="app-sub">精選淘寶超殺破盤神物，點擊直接前往官方精準分類頁！</div>
    </div>
""", unsafe_allow_html=True)

# --- 淘寶家用品資料庫（已換成正確且可用的淘寶官方分類與搜尋網址） ---
deals = [
    {
        "category": "🛏️ 寢具家飾",
        "name": "北歐風簡約全棉水洗棉四件套",
        "price": "RMB 89",
        "origin": "RMB 220",
        "discount": "4.0 折",
        "image": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=600&auto=format&fit=crop&q=80",
        "link": "https://s.taobao.com/search?q=%E6%B0%B4%E6%B4%97%E6%A3%89%E5%9B%9b%E4%BB%B6%E5%A5%97"  # 淘寶「水洗棉四件套」官方搜尋頁
    },
    {
        "category": "🪑 家具收納",
        "name": "多功能透明防塵鞋盒（10個裝）",
        "price": "RMB 45",
        "origin": "RMB 110",
        "discount": "4.1 折",
        "image": "https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=600&auto=format&fit=crop&q=80",
        "link": "https://s.taobao.com/search?q=%E9%98%B2%E5%A1%B5%E9%9E%8B%E7%9B%92"  # 淘寶「防塵鞋盒」官方搜尋頁
    },
    {
        "category": "🧹 清潔衛浴",
        "name": "免手洗平底免手洗魔術拖把",
        "price": "RMB 39",
        "origin": "RMB 99",
        "discount": "3.9 折",
        "image": "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?w=600&auto=format&fit=crop&q=80",
        "link": "https://s.taobao.com/search?q=%E5%85%8D%E6%89%8B%E6%B4%97%E6%8B%96%E6%8A%8A"  # 淘寶「免手洗拖把」官方搜尋頁
    },
    {
        "category": "🍽️ 廚房餐飲",
        "name": "不銹鋼多功能瀝水碗盤收納架",
        "price": "RMB 59",
        "origin": "RMB 150",
        "discount": "3.9 折",
        "image": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=600&auto=format&fit=crop&q=80",
        "link": "https://s.taobao.com/search?q=%E6%BB%A4%E6%B0%B4%E7%A2%97%E7%9B%98%E6%94%B6%E7%BA%B3%E6%9E%B6"  # 淘寶「瀝水碗盤收納架」官方搜尋頁
    }
]

# --- 分類篩選 ---
categories = ["全部", "🛏️ 寢具家飾", "🪑 家具收納", "🧹 清潔衛浴", "🍽️ 廚房餐飲"]
selected_cat = st.selectbox("選擇淘寶家用品分類：", categories)

st.markdown("---")

filtered_deals = deals if selected_cat == "全部" else [d for d in deals if d["category"] == selected_cat]

st.markdown(f"### 🔥 符合條件的淘寶好物 ({len(filtered_deals)} 件)")

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
        st.link_button("🔗 點我前往淘寶正確搜尋頁", item['link'], use_container_width=True)
        st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
