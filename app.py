import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# 頁面基本設定
st.set_page_config(
    page_title="全網蝦皮秒殺雷達 (高穩定版)",
    page_icon="🦐",
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
        <div class="app-title">🦐 蝦皮秒殺雷達（高穩定深度掃描版）</div>
        <div class="app-sub">免除 Telegram 頁面失效問題 ‧ 深度跨頁掃描 PTT 省錢版取得海量商品</div>
    </div>
""", unsafe_allow_html=True)

# 智慧萃取蝦皮與購物連結
def extract_shopee_links(text_or_html):
    if not text_or_html:
        return []
    found_links = re.findall(r'(https?://[^\s<>"]+)', text_or_html)
    links = []
    for link in found_links:
        if any(domain in link for domain in ["shopee.tw", "shp.ee", "tw.shp.ee"]):
            clean_link = link.rstrip('.,;:!?)')
            if clean_link not in links:
                links.append(clean_link)
    return links[:3]

# --- PTT 深度多頁爬蟲（確保高穩定、抓取大量商品） ---
@st.cache_data(ttl=300)
def fetch_deep_ptt_deals():
    headers = {"User-Agent": "Mozilla/5.0", "Cookie": "over18=1"}
    results = []
    base_url = "https://www.ptt.cc/bbs/Lifeismoney/index{}.html"
    
    try:
        res = requests.get("https://www.ptt.cc/bbs/Lifeismoney/index.html", headers=headers, timeout=6)
        if res.status_code != 200:
            return []
        
        soup = BeautifulSoup(res.text, "html.parser")
        paging_buttons = soup.find_all("a", class_="btn wide")
        prev_page_url = paging_buttons[1]["href"] if len(paging_buttons) > 1 else ""
        match = re.search(r'index(\d+)\.html', prev_page_url)
        
        if match:
            latest_index = int(match.group(1)) + 1
            # 為了確保能拿到足夠多的商品，我們直接抓最近 5 個分頁！
            pages_to_fetch = range(latest_index, latest_index - 5, -1)
        else:
            pages_to_fetch = [None]
            
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
                    
                    art_res = requests.get(article_url, headers=headers, timeout=4)
                    if art_res.status_code == 200:
                        art_soup = BeautifulSoup(art_res.text, "html.parser")
                        main_content = art_soup.find(id="main-content")
                        if main_content:
                            links = extract_shopee_links(str(main_content))
                            if links:
                                results.append({
                                    "platform": "PTT 省錢版 (深度掃描)",
                                    "title": title,
                                    "shopee_links": links
                                })
    except Exception:
        pass
    return results

# --- 畫面主邏輯 ---
if st.button("🔄 立即重新整理蝦皮雷達", use_container_width=True):
    st.cache_data.clear()

st.markdown("---")

with st.spinner("正在進行 PTT 省錢版多頁深度掃描，萃取蝦皮直達與縮址連結中..."):
    all_deals = fetch_deep_ptt_deals()

if not all_deals:
    st.warning("⚠️ 目前暫時沒有抓到含有蝦皮連結的文章，請點擊上方按鈕重新整理！")
else:
    st.markdown(f"### 🎯 掃描完成！成功鎖定共計 **{len(all_deals)}** 筆蝦皮優惠好物")
    
    for item in all_deals:
        with st.container():
            st.markdown(f"""
                <div class="deal-box">
                    <div><span class="platform-badge">{item['platform']}</span></div>
                    <div class="deal-title" style="margin-top: 8px;">{item['title']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            for idx, link in enumerate(item['shopee_links']):
                st.link_button(f"🔥 點我直接前往蝦皮搶購 (連結 {idx+1})", link, use_container_width=True)
                
            st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)
