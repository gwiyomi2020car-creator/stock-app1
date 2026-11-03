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
        <div class="app-sub">自動同步 Telegram 頻道 & PTT 省錢版 ‧ 即時取得搶購連結</div>
    </div>
""", unsafe_allow_html=True)

# --- 1. 爬取 Telegram 頻道功能 ---
@st.cache_data(ttl=300)
def fetch_telegram_deals(channel_username):
    url = f"https://t.me/s/{channel_username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
        
        soup = BeautifulSoup(response.text, "html.parser")
        messages = soup.find_all("div", class_="tgme_widget_message")
        
        results = []
        for msg in messages:
            text_div = msg.find("div", class_="tgme_widget_message_text")
            text = text_div.get_text(separator="\n").strip() if text_div else ""
            if not text:
                continue

            photo_div = msg.find("a", class_="tgme_widget_message_photo_wrap")
            image_url = None
            if photo_div and "style" in photo_div.attrs:
                style = photo_div["style"]
                match = re.search(r"background-image:url\('(.*?)'\)", style)
                if match:
                    image_url = match.group(1)
            
            links = []
            if text_div:
                for a in text_div.find_all("a", href=True):
                    href = a["href"]
                    if "t.me" not in href and href.startswith("http"):
                        links.append(href)
            
            results.append({
                "text": text,
                "image": image_url,
                "links": links
            })
        return results[::-1]
    except Exception:
        return []

# --- 2. 爬取 PTT 省錢版 (Lifeismoney) 功能 ---
@st.cache_data(ttl=300)
def fetch_ptt_lifeismoney():
    url = "https://www.ptt.cc/bbs/Lifeismoney/index.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Cookie": "over18=1"  # 繞過 PTT 18歲同意成年詢問頁面
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
                link = "https://www.ptt.cc" + a_tag["href"]
                
                # 簡單過濾，抓取具有雷達價值或全部文章
                results.append({
                    "title": title,
                    "link": link
                })
        return results[::-1]
    except Exception:
        return []

# --- 來源選單切換 ---
source_mode = st.selectbox("選擇資訊來源平台：", ["🔥 PTT 省錢版 (Lifeismoney)", "✈️ Telegram 優惠頻道"])

st.markdown("---")

if source_mode == "🔥 PTT 省錢版 (Lifeismoney)":
    st.markdown("### 🏷️ PTT 省錢版最新熱門優惠")
    with st.spinner("正在同步 PTT 最新省錢文章..."):
        ptt_deals = fetch_ptt_lifeismoney()
    
    if not ptt_deals:
        st.warning("⚠️ 目前無法取得 PTT 資料，請稍後再試。")
    else:
        for item in ptt_deals:
            with st.container():
                st.markdown(f"""
                    <div class="deal-box">
                        <div class="ptt-title">{item['title']}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.link_button("🔗 點我前往 PTT 看詳細討論與連結", item['link'], use_container_width=True)
                st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

else:
    channel_input = st.text_input("輸入 Telegram 公開頻道 ID:", "ShopeeDealsTW")
    if st.button("🔄 立即重新整理", use_container_width=True):
        st.cache_data.clear()
        
    if channel_input:
        with st.spinner(f"正在自動同步 [{channel_input}] 最新情報..."):
            deals = fetch_telegram_deals(channel_input.strip())
        
        if not deals:
            st.warning("⚠️ 找不到訊息，請確認該頻道為「公開頻道」且 ID 正確。")
        else:
            st.markdown(f"### 📢 Telegram 最新抓取優惠 ({len(deals)} 則)")
            for item in deals:
                with st.container():
                    st.markdown(f"""
                        <div class="deal-box">
                            <div class="deal-text">{item['text']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if item['image']:
                        st.image(item['image'], use_container_width=True)
                    
                    if item['links']:
                        for link_idx, link_url in enumerate(item['links']):
                            st.link_button(f"🔗 點我直接搶購 (連結 {link_idx+1})", link_url, use_container_width=True)
                    else:
                        st.caption("ℹ️ 此訊息未附帶直接外部連結")
                        
                    st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
