import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 頁面基本設定
st.set_page_config(
    page_title="全網破盤 5 折秒殺雷達",
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
    
    .app-header {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.4);
    }
    .app-title {
        font-size: 20px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .app-sub {
        font-size: 13px;
        color: #E0F2FE;
    }

    .deal-box {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .deal-text {
        font-size: 14px;
        color: #E2E8F0;
        line-height: 1.6;
        white-space: pre-wrap;
        margin-bottom: 10px;
    }
    .ptt-title {
        font-size: 16px;
        font-weight: 600;
        color: #38BDF8;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 頂部 Banner ---
st.markdown("""
    <div class="app-header">
        <div class="app-title">⚡ 全網破盤 5 折秒殺雷達</div>
        <div class="app-sub">自動同步 PTT 省錢版 ‧ 自動萃取文章內商品直達連結</div>
    </div>
""", unsafe_allow_html=True)

# --- 爬取 PTT 省錢版文章清單與內文連結 ---
@st.cache_data(ttl=300)
def fetch_ptt_deals():
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
        for art in articles[:10]:  # 預設抓取最新 10 篇避免載入過久
            title_div = art.find("div", class_="title")
            a_tag = title_div.find("a") if title_div else None
            
            if a_tag:
                title = a_tag.get_text().strip()
                article_url = "https://www.ptt.cc" + a_tag["href"]
                
                # 點進文章內頁抓取實際商品連結
                product_links = fetch_ptt_article_links(article_url, headers)
                
                results.append({
                    "title": title,
                    "ptt_link": article_url,
                    "product_links": product_links
                })
        return results[::-1]
    except Exception:
        return []

# --- 輔助函式：進入 PTT 內頁萃取商品連結 ---
def fetch_ptt_article_links(article_url, headers):
    try:
        res = requests.get(article_url, headers=headers, timeout=5)
        if res.status_code != 200:
            return []
        
        soup = BeautifulSoup(res.text, "html.parser")
        main_content = soup.find(id="main-content")
        if not main_content:
            return []
        
        links = []
        # 找出內文中的所有超連結
        for a in main_content.find_all("a", href=True):
            href = a["href"]
            # 過濾並保留常見的購物或外部直達連結
            if any(domain in href for domain in ["shopee.tw", "taobao.com", "tmall.com", "momo.com.tw", " PChome"]):
                if href not in links:
                    links.append(href)
            elif href.startswith("http") and "ptt.cc" not in href:
                # 其他外部短網址或導購連結
                if href not in links:
                    links.append(href)
                    
        return links[:3]  # 限制最多抓取前 3 個商品連結
    except Exception:
        return []

# --- 畫面渲染 ---
st.markdown("### 🏷️ PTT 省錢版即時商品雷達")

if st.button("🔄 立即重新整理", use_container_width=True):
    st.cache_data.clear()

with st.spinner("正在同步 PTT 省錢版並自動萃取商品直達連結..."):
    deals = fetch_ptt_deals()

if not deals:
    st.warning("⚠️ 目前無法取得資料，請稍後再試。")
else:
    for item in deals:
        with st.container():
            st.markdown(f"""
                <div class="deal-box">
                    <div class="ptt-title">{item['title']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 如果成功在內文中抓到商品直達連結，直接顯示按鈕
            if item['product_links']:
                for idx, prod_link in enumerate(item['product_links']):
                    st.link_button(f"🔥 點我直接前往商品搶購 (連結 {idx+1})", prod_link, use_container_width=True)
            else:
                # 若內文沒直接抓到外部連結，則提供 PTT 原始討論頁面按鈕
                st.link_button("🔗 前往 PTT 檢視原文與討論", item['ptt_link'], use_container_width=True)
                
            st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
