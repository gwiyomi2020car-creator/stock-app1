import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 頁面基本設定
st.set_page_config(
    page_title="全網 50+ 蝦皮秒殺雷達",
    page_icon="🔥",
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
        font-size: 15px;
        font-weight: 600;
        color: #38BDF8;
        margin-bottom: 8px;
    }
    .platform-badge {
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
        <div class="app-title">🔥 全網 50+ 蝦皮秒殺雷達（高容量聚合版）</div>
        <div class="app-sub">深度掃描多頁討論區與多個 Telegram 優惠頻道 ‧ 目標解鎖 50+ 商品</div>
    </div>
""", unsafe_allow_html=True)

# 智慧萃取蝦皮與購物連結
def extract_shopee_links(text_or_html):
    if not text_or_html:
        return []
    found_links = re.findall(r'(https?://[^\s<>"]+)', text_or_html)
    links = []
    for link in found_links:
        # 擴大涵蓋蝦皮長網址、縮址以及常見的導購短網址
        if any(domain in link for domain in ["shopee.tw", "shp.ee", "tw.shp.ee", "reurl.cc"]):
            clean_link = link.rstrip('.,;:!?)')
            if clean_link not in links:
                links.append(clean_link)
    return links[:3]

# --- 1. PTT 深度多頁爬蟲（抓取多頁以累積大量商品） ---
@st.cache_data(ttl=300)
def fetch_deep_ptt_deals():
    headers = {"User-Agent": "Mozilla/5.0", "Cookie": "over18=1"}
    results = []
    
    # 爬取 PTT 省錢版最近的 3 個分頁
    base_url = "https://www.ptt.cc/bbs/Lifeismoney/index{}.html"
    
    try:
        # 先取得最新頁數
        res = requests.get("https://www.ptt.cc/bbs/Lifeismoney/index.html", headers=headers, timeout=6)
        if res.status_code != 200:
            return []
        
        soup = BeautifulSoup(res.text, "html.parser")
        # 尋找上一頁的連結來推算最新頁碼
        paging_buttons = soup.find_all("a", class_="btn wide")
        prev_page_url = paging_buttons[1]["href"] if len(paging_buttons) > 1 else ""
        match = re.search(r'index(\d+)\.html', prev_page_url)
        
        if match:
            latest_index = int(match.group(1)) + 1
            pages_to_fetch = range(latest_index, latest_index - 3, -1) # 抓最近 3 頁
        else:
            pages_to_fetch = [None] # 備用
            
        for p in pages_to_fetch:
            target_url = base_url.format(p) if p else "https://www.ptt.cc/bbs/Lifeismoney/index.html"
            page_res = requests.get(target_url, headers=headers, timeout=6)
            if page_res.status_code != 200:
                continue
            
            page_soup = BeautifulSoup(page_res.text, "html.parser")
            for art in page_soup.find_all("div", class_="r-ent"):
                a_tag = art.find("div", class_="title").find("a") if art.find("div", class_="title") else None
                if a_tag:
                    title = a_tag.get_text().strip()
                    article_url = "https://www.ptt.cc" + a_tag["href"]
                    
                    # 快速抓取內文連結
                    art_res = requests.get(article_url, headers=headers, timeout=4)
                    if art_res.status_code == 200:
                        art_soup = BeautifulSoup(art_res.text, "html.parser")
                        main_content = art_soup.find(id="main-content")
                        if main_content:
                            links = extract_shopee_links(str(main_content))
                            if links:
                                results.append({
                                    "platform": "PTT 省錢版 (深度)",
                                    "title": title,
                                    "shopee_links": links
                                })
    except Exception:
        pass
    return results

# --- 2. 聚合多個 Telegram 優惠頻道 ---
@st.cache_data(ttl=300)
def fetch_multiple_telegram_deals():
    channels = ["ShopeeDealsTW", "goodbuytw", "shopee_discount"] # 多個熱門優惠頻道
    results = []
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for ch in channels:
        url = f"https://t.me/s/{ch}"
        try:
            res = requests.get(url, headers=headers, timeout=6)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for msg in soup.find_all("div", class_="tgme_widget_message"):
                    text_div = msg.find("div", class_="tgme_widget_message_text")
                    text = text_div.get_text(separator="\n").strip() if text_div else ""
                    links = extract_shopee_links(text)
                    if links:
                        title = text.split("\n")[0][:45] + "..." if text else f"TG 頻道 ({ch}) 優惠"
                        results.append({
                            "platform": f"TG 頻道 ({ch})",
                            "title": title,
                            "shopee_links": links
                        })
        except Exception:
            continue
    return results

# --- 畫面主邏輯 ---
if st.button("🔄 深度重新整理 (解鎖 50+ 商品)", use_container_width=True):
    st.cache_data.clear()

st.markdown("---")

with st.spinner("正在進行全網深度掃描（跨多頁 PTT ＋ 多個 Telegram 頻道），請稍候約 5~10 秒..."):
    ptt_deals = fetch_deep_ptt_deals()
    tg_deals = fetch_multiple_telegram_deals()
    
    all_deals = ptt_deals + tg_deals

if not all_deals:
    st.warning("⚠️ 目前暫時無法取得足夠資料，請點擊上方按鈕重新整理！")
else:
    st.markdown(f"### 🎯 深度掃描完成！成功解鎖共計 **{len(all_deals)}** 筆商品與優惠")
    
    for item in all_deals:
        with st.container():
            st.markdown(f"""
                <div class="deal-box">
                    <div><span class="platform-badge">{item['platform']}</span></div>
                    <div class="deal-title" style="margin-top: 8px;">{item['title']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            for idx, link in enumerate(item['shopee_links']):
                st.link_button(f"🔥 點我直接前往搶購 (連結 {idx+1})", link, use_container_width=True)
                
            st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)
