import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 頁面基本設定
st.set_page_config(
    page_title="全網聚合蝦皮秒殺雷達",
    page_icon="⚡",
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
    .deal-title {
        font-size: 16px;
        font-weight: 600;
        color: #38BDF8;
        margin-bottom: 8px;
    }
    .platform-badge-ptt {
        background-color: #3B82F6;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 6px;
    }
    .platform-badge-dcard {
        background-color: #006AA7;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 700;
        margin-right: 6px;
    }
    .platform-badge-tg {
        background-color: #0284C7;
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
        <div class="app-title">⚡ 全網聚合蝦皮秒殺雷達</div>
        <div class="app-sub">同步 PTT ＋ Dcard ＋ Telegram ‧ 自動精準萃取蝦皮商品直達與縮址連結</div>
    </div>
""", unsafe_allow_html=True)

# 共用過濾蝦皮連結的函式
def extract_shopee_links(text_or_html):
    if not text_or_html:
        return []
    # 支援標準網址與常見縮址
    found_links = re.findall(r'(https?://[^\s<>"]+)', text_or_html)
    shopee_links = []
    for link in found_links:
        if any(domain in link for domain in ["shopee.tw", "shp.ee", "tw.shp.ee"]):
            # 清理結尾可能帶有的標點符號
            clean_link = link.rstrip('.,;:!?)')
            if clean_link not in shopee_links:
                shopee_links.append(clean_link)
    return shopee_links[:2] # 限制每篇最多取 2 個

# --- 1. 爬取 PTT 省錢版 ---
@st.cache_data(ttl=300)
def fetch_ptt_deals():
    url = "https://www.ptt.cc/bbs/Lifeismoney/index.html"
    headers = {"User-Agent": "Mozilla/5.0", "Cookie": "over18=1"}
    results = []
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            for art in soup.find_all("div", class_="r-ent")[:15]:
                a_tag = art.find("div", class_="title").find("a") if art.find("div", class_="title") else None
                if a_tag:
                    title = a_tag.get_text().strip()
                    article_url = "https://www.ptt.cc" + a_tag["href"]
                    # 進入內文抓取
                    art_res = requests.get(article_url, headers=headers, timeout=5)
                    if art_res.status_code == 200:
                        art_soup = BeautifulSoup(art_res.text, "html.parser")
                        main_content = art_soup.find(id="main-content")
                        if main_content:
                            links = extract_shopee_links(str(main_content))
                            if links:
                                results.append({
                                    "platform": "PTT 省錢版",
                                    "badge_class": "platform-badge-ptt",
                                    "title": title,
                                    "source_link": article_url,
                                    "shopee_links": links
                                })
    except Exception:
        pass
    return results

# --- 2. 爬取 Dcard 購物板 (透過官方 API) ---
@st.cache_data(ttl=300)
def fetch_dcard_deals():
    url = "https://www.dcard.tw/service/api/v2/forums/buy/posts?limit=20"
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            posts = res.json()
            for post in posts:
                title = post.get("title", "")
                post_id = post.get("id")
                excerpt = post.get("excerpt", "")
                
                # 先從摘要檢查是否有蝦皮連結
                links = extract_shopee_links(excerpt)
                
                # 如果摘要沒有，去抓詳細內文
                if not links and post_id:
                    detail_url = f"https://www.dcard.tw/service/api/v2/posts/{post_id}"
                    det_res = requests.get(detail_url, headers=headers, timeout=5)
                    if det_res.status_code == 200:
                        content = det_res.json().get("content", "")
                        links = extract_shopee_links(content)
                
                if links:
                    source_url = f"https://www.dcard.cc/f/buy/p/{post_id}"
                    results.append({
                        "platform": "Dcard 購物板",
                        "badge_class": "platform-badge-dcard",
                        "title": title,
                        "source_link": source_url,
                        "shopee_links": links
                    })
    except Exception:
        pass
    return results

# --- 3. 爬取 Telegram 頻道 ---
@st.cache_data(ttl=300)
def fetch_telegram_deals(channel_username):
    url = f"https://t.me/s/{channel_username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    results = []
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            for msg in soup.find_all("div", class_="tgme_widget_message")[:15]:
                text_div = msg.find("div", class_="tgme_widget_message_text")
                text = text_div.get_text(separator="\n").strip() if text_div else ""
                links = extract_shopee_links(text)
                if links:
                    # 取第一行或前30字作為標題
                    title = text.split("\n")[0][:40] + "..." if text else "Telegram 優惠訊息"
                    results.append({
                        "platform": f"TG 頻道 ({channel_username})",
                        "badge_class": "platform-badge-tg",
                        "title": title,
                        "source_link": url,
                        "shopee_links": links
                    })
    except Exception:
        pass
    return results

# --- 畫面操作與重新整理 ---
if st.button("🔄 立即重新整理全網雷達", use_container_width=True):
    st.cache_data.clear()

st.markdown("---")

with st.spinner("正在同步 PTT、Dcard 與 Telegram，正在全面過濾蝦皮直達商品..."):
    ptt_results = fetch_ptt_deals()
    dcard_results = fetch_dcard_deals()
    tg_results = fetch_telegram_deals("ShopeeDealsTW") # 可自行更換或增加 TG 頻道
    
    # 合併所有平台的結果
    all_deals = ptt_results + dcard_results + tg_results

if not all_deals:
    st.warning("⚠️ 目前各平台暫時沒有抓到含有蝦皮直達連結的新文章，請點擊上方按鈕重新整理！")
else:
    st.markdown(f"### 🎯 全網同步完成！共鎖定 {len(all_deals)} 筆蝦皮優惠好物")
    
    for item in all_deals:
        with st.container():
            st.markdown(f"""
                <div class="deal-box">
                    <div><span class="{item['badge_class']}">{item['platform']}</span></div>
                    <div class="deal-title" style="margin-top: 8px;">{item['title']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 渲染該文章內抓到的所有蝦皮商品搶購按鈕
            for idx, link in enumerate(item['shopee_links']):
                st.link_button(f"🔥 點我直接前往蝦皮搶購 (連結 {idx+1})", link, use_container_width=True)
                
            st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)
