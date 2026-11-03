import streamlit as st
import requests
from bs4 import BeautifulSoup

# 頁面基本設定
st.set_page_config(
    page_title="蝦皮專屬 5 折秒殺雷達",
    page_icon="🦐",
    layout="centered"
)

# --- 注入現代化夜間 App 風格 CSS (蝦皮經典橘紅配色) ---
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
        background: linear-gradient(135deg, #EE4D2D 0%, #FF7337 100%);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(238, 77, 45, 0.4);
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
    .ptt-title {
        font-size: 16px;
        font-weight: 600;
        color: #38BDF8;
        margin-bottom: 8px;
    }
    .shopee-badge {
        background-color: #EE4D2D;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 頂部 Banner ---
st.markdown("""
    <div class="app-header">
        <div class="app-title">🦐 蝦皮專屬 5 折破盤秒殺雷達</div>
        <div class="app-sub">自動過濾全網討論 ‧ 精準鎖定蝦皮（Shopee）商品直達與縮址連結</div>
    </div>
""", unsafe_allow_html=True)

# --- 爬取 PTT 省錢版並支援蝦皮縮址與長網址 ---
@st.cache_data(ttl=300)
def fetch_shopee_deals():
    url = "https://www.ptt.cc/bbs/Lifeismoney/index.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Cookie": "over18=1"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="r-ent")
        
        results = []
        for art in articles:
            title_div = art.find("div", class_="title")
            a_tag = title_div.find("a") if title_div else None
            
            if a_tag:
                title = a_tag.get_text().strip()
                article_url = "https://www.ptt.cc" + a_tag["href"]
                
                # 進入內文抓取，擴大支援 shopee.tw、shp.ee、tw.shp.ee
                shopee_links = fetch_shopee_links_from_article(article_url, headers)
                
                if shopee_links:
                    results.append({
                        "title": title,
                        "ptt_link": article_url,
                        "shopee_links": shopee_links
                    })
        return results[::-1]
    except Exception:
        return []

# --- 輔助函式：過濾並萃取蝦皮專屬與縮址網址 ---
def fetch_shopee_links_from_article(article_url, headers):
    try:
        res = requests.get(article_url, headers=headers, timeout=5)
        if res.status_code != 200:
            return []
        
        soup = BeautifulSoup(res.text, "html.parser")
        main_content = soup.find(id="main-content")
        if not main_content:
            return []
        
        shopee_links = []
        for a in main_content.find_all("a", href=True):
            href = a["href"]
            # 同時涵蓋蝦皮標準網址與常見的官方縮址
            if any(domain in href for domain in ["shopee.tw", "shp.ee", "tw.shp.ee"]):
                if href not in shopee_links:
                    shopee_links.append(href)
                
        return shopee_links[:2]
    except Exception:
        return []

# --- 畫面渲染 ---
st.markdown("### 🔥 最新蝦皮特賣與折扣商品")

if st.button("🔄 立即重新整理蝦皮雷達", use_container_width=True):
    st.cache_data.clear()

with st.spinner("正在同步各大討論區並過濾蝦皮直達與縮址連結..."):
    deals = fetch_shopee_deals()

if not deals:
    st.warning("⚠️ 目前暫時沒有抓到含有蝦皮連結的新文章，請稍後再試或點擊重新整理！")
else:
    st.markdown(f"### 🎯 成功鎖定 {len(deals)} 筆帶有蝦皮連結的優惠")
    for item in deals:
        with st.container():
            st.markdown(f"""
                <div class="deal-box">
                    <div><span class="shopee-badge">SHOPEE</span></div>
                    <div class="ptt-title" style="margin-top: 6px;">{item['title']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            for idx, link in enumerate(item['shopee_links']):
                st.link_button(f"🔥 點我直接前往蝦皮搶購 (連結 {idx+1})", link, use_container_width=True)
                
            st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
