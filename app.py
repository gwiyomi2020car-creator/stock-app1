import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 頁面基本設定
st.set_page_config(
    page_title="Telegram 智慧優惠聚合雷達",
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
    </style>
""", unsafe_allow_html=True)

# --- 頂部 Banner ---
st.markdown("""
    <div class="app-header">
        <div class="app-title">⚡ 優惠情報智慧聚合雷達</div>
        <div class="app-sub">自動同步精選特賣頻道 ‧ 獲取真實商品直達連結</div>
    </div>
""", unsafe_allow_html=True)

# --- 爬蟲核心功能 ---
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
        
    except Exception as e:
        return []

# --- 預設優質頻道清單（免手動輸入，直接下拉切換） ---
predefined_channels = {
    "🔥 預設精選優惠頻道 (ShopeeDealsTW)": "ShopeeDealsTW",
    "🛒 更多特賣情報頻道 (範例頻道B)": "your_another_channel", # 可自行替換為其他已知公開頻道
    "✏️ 自訂輸入頻道 ID": "custom"
}

selected_option = st.selectbox("選擇要自動同步的頻道來源：", list(predefined_channels.keys()))

if selected_option == "✏️ 自訂輸入頻道 ID":
    channel_input = st.text_input("輸入 Telegram 公開頻道 ID:", "ShopeeDealsTW")
else:
    channel_input = predefined_channels[selected_option]

if st.button("🔄 立即重新整理", use_container_width=True):
    st.cache_data.clear()

st.markdown("---")

# --- 渲染資料 ---
if channel_input and channel_input != "your_another_channel":
    with st.spinner(f"正在自動同步 [{channel_input}] 最新情報..."):
        deals = fetch_telegram_deals(channel_input.strip())
    
    if not deals:
        st.warning("⚠️ 暫無資料或該頻道 ID 不存在/非公開頻道。")
    else:
        st.markdown(f"### 📢 最新抓取優惠 ({len(deals)} 則)")
        
        for idx, item in enumerate(deals):
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
else:
    st.info("💡 請選擇或輸入一個有效的 Telegram 公開頻道以開始自動抓取。")
