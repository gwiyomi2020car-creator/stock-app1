import streamlit as st
import pandas as pd
import twstock

# 頁面基本設定
st.set_page_config(
    page_title="台股智慧選股",
    page_icon="📈",
    layout="centered"
)

# --- 注入極簡質感與夜間模式 CSS ---
st.markdown("""
    <style>
    /* 隱藏預設雜訊 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    .header-card {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #1E293B;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    .header-title {
        font-size: 18px;
        font-weight: 700;
        color: #F9FAFB;
        margin-bottom: 4px;
    }
    .header-subtitle {
        font-size: 12px;
        color: #9CA3AF;
    }

    .stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, #3B82F6 100%, #1D4ED8 0%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(59, 130, 246, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- 頂部視覺 Banner ---
st.markdown("""
    <div class="header-card">
        <div class="header-title">📊 智慧台股選股與分析儀表板</div>
        <div class="header-subtitle">行動版即時行情 ‧ 技術指標篩選 ‧ 走勢分析</div>
    </div>
""", unsafe_allow_html=True)

# --- 自動載入台股所有上市櫃股票字典 ---
@st.cache_data
def get_all_stocks():
    stock_dict = {}
    for code, obj in twstock.codes.items():
        if len(code) == 4 and obj.type in ['股票', 'ETF']:
            stock_dict[code] = obj.name
    return stock_dict

all_stocks = get_all_stocks()

# --- 側邊欄設定 ---
st.sidebar.markdown("### ⚙️ 篩選條件設定")
default_selection = ["2330", "2317", "2454", "2308", "2382", "2881", "2882", "2603"]

selected_pool = st.sidebar.multiselect(
    "選擇監控股票清單",
    options=list(all_stocks.keys()),
    default=default_selection,
    format_func=lambda x: f"{x} {all_stocks[x]}"
)

st.sidebar.markdown("---")
min_vol = st.sidebar.slider("最低成交量門檻 (張)", 100, 50000, 2000, step=500)
ma_filter = st.sidebar.checkbox("僅顯示多頭排列 (5MA > 20MA)", value=True)

# --- 主畫面：執行選股 ---
st.markdown("### ⚡ 即時選股掃描")
if st.button("開始執行智慧篩選"):
    if not selected_pool:
        st.warning("請至少選擇一支股票！")
    else:
        with st.spinner("正在進行多維度數據運算..."):
            results = []
            for code in selected_pool:
                try:
                    stock = twstock.Stock(code)
                    if len(stock.price) >= 20:
                        closes = stock.price[-60:]
                        capacities = stock.capacity[-60:]
                        
                        if len(closes) >= 20:
                            close = closes[-1]
                            prev_close = closes[-2]
                            change_pct = ((close - prev_close) / prev_close) * 100
                            
                            df_closes = pd.Series(closes)
                            ma5 = df_closes.rolling(window=5).mean().iloc[-1]
                            ma20 = df_closes.rolling(window=20).mean().iloc[-1]
                            vol = int(capacities[-1] / 1000)
                            
                            status = "✅ 多頭" if ma5 > ma20 else "⚠️ 盤整"
                            
                            results.append({
                                "代號": code,
                                "名稱": all_stocks.get(code, ""),
                                "收盤價": round(close, 2),
                                "漲跌幅(%)": round(change_pct, 2),
                                "5日線": round(ma5, 2),
                                "20日線": round(ma20, 2),
                                "成交量": vol,
                                "狀態": status
                            })
                except Exception:
                    pass
            
            if results:
                df_res = pd.DataFrame(results)
                if ma_filter:
                    df_res = df_res[df_res['5日線'] > df_res['20日線']]
                df_res = df_res[df_res['成交量'] >= min_vol]
                
                st.success(f"篩選完成！找到 {len(df_res)} 支符合標的。")
                st.dataframe(df_res, use_container_width=True)
            else:
                st.warning("目前沒有符合條件的股票。")

# --- 個股歷史走勢區 ---
st.markdown("---")
st.markdown("### 📉 個股技術走勢")

target_stock = st.selectbox(
    "選擇或搜尋個股", 
    options=list(all_stocks.keys()), 
    format_func=lambda x: f"{x} {all_stocks[x]}"
)

if st.button("載入技術走勢圖"):
    with st.spinner("圖表繪製中..."):
        try:
            stock = twstock.Stock(target_stock)
            closes = stock.price[-60:]
            if len(closes) > 0:
                df_chart = pd.DataFrame({"收盤價": closes})
                st.line_chart(df_chart["收盤價"])
            else:
                st.error("無法取得歷史資料。")
        except Exception:
            st.error("載入失敗，請稍後再試。")

# --- 🎵 看盤背景音樂區 ---
st.markdown("---")
st.markdown("### 🎵 看盤放鬆音樂")

# 提供一首免版權的輕音樂/Lo-fi 串流音訊供播放
audio_url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf756.mp3?filename=lofi-study-112191.mp3"
st.audio(audio_url, format="audio/mp3", autoplay=False)
