import streamlit as st
import pandas as pd
import twstock

# 頁面基本設定
st.set_page_config(
    page_title="台股智慧選股與分析工具",
    page_icon="📈",
    layout="wide"
)

# --- 注入精美現代化 CSS 樣式 ---
st.markdown("""
    <style>
    /* 全局與背景調整 */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* 標題卡片設計 */
    .hero-box {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hero-title {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .hero-subtitle {
        font-size: 13px;
        opacity: 0.9;
    }

    /* 區塊標題 */
    h3 {
        color: #1E293B;
        font-size: 18px !important;
        font-weight: 600 !important;
        margin-top: 15px !important;
    }

    /* 按鈕美化 */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    
    /* 卡片容器 */
    .custom-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 頂部精美視覺 Banner ---
st.markdown("""
    <div class="hero-box">
        <div class="hero-title">📈 智慧台股選股與分析儀表板</div>
        <div class="hero-subtitle">行動版即時行情、技術指標篩選與走勢分析工具</div>
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
st.sidebar.markdown("### ⚙️ 篩選與監控設定")

default_selection = ["2330", "2317", "2454", "2308", "2382", "2881", "2882", "2603"]

selected_pool = st.sidebar.multiselect(
    "選擇或搜尋監控股票",
    options=list(all_stocks.keys()),
    default=default_selection,
    format_func=lambda x: f"{x} {all_stocks[x]}"
)

st.sidebar.markdown("---")
min_vol = st.sidebar.slider("最低成交量門檻 (張)", 100, 50000, 2000, step=500)
ma_filter = st.sidebar.checkbox("僅顯示多頭排列 (5日線 > 20日線)", value=True)

# --- 主畫面：執行選股 ---
st.markdown("### 🚀 即時選股篩選器")
with st.container():
    if st.button("✨ 開始執行智慧篩選", type="primary", use_container_width=True):
        if not selected_pool:
            st.warning("請至少選擇一支股票！")
        else:
            with st.spinner(f"正在分析選取的 {len(selected_pool)} 支股票數據..."):
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
                                
                                status = "✅ 多頭排列" if ma5 > ma20 else "⚠️ 盤整/空頭"
                                
                                results.append({
                                    "代號": code,
                                    "名稱": all_stocks.get(code, ""),
                                    "收盤價": round(close, 2),
                                    "漲跌幅(%)": round(change_pct, 2),
                                    "5日線": round(ma5, 2),
                                    "20日線": round(ma20, 2),
                                    "成交量(張)": vol,
                                    "狀態": status
                                })
                    except Exception as e:
                        pass
                
                if results:
                    df_res = pd.DataFrame(results)
                    if ma_filter:
                        df_res = df_res[df_res['5日線'] > df_res['20日線']]
                    df_res = df_res[df_res['成交量(張)'] >= min_vol]
                    
                    st.success(f"篩選完成！共找到 {len(df_res)} 支符合條件的優質標的。")
                    st.dataframe(df_res, use_container_width=True)
                else:
                    st.error("目前沒有符合條件的股票，請放寬篩選條件後重試。")

# --- 個股歷史走勢區 ---
st.markdown("---")
st.markdown("### 🔍 個股技術走勢檢視")

target_stock = st.selectbox(
    "搜尋或選擇股票檢視走勢圖", 
    options=list(all_stocks.keys()), 
    format_func=lambda x: f"{x} {all_stocks[x]}"
)

if st.button("📊 載入走勢圖", use_container_width=True):
    with st.spinner(f"正在載入 {target_stock} 走勢..."):
        try:
            stock = twstock.Stock(target_stock)
            closes = stock.price[-60:]
            if len(closes) > 0:
                df_chart = pd.DataFrame({"收盤價": closes})
                st.line_chart(df_chart["收盤價"])
                st.info(f"已成功呈現 {target_stock} ({all_stocks[target_stock]}) 近期收盤價走勢。")
            else:
                st.error(f"無法取得 {target_stock} 的歷史資料。")
        except Exception as e:
            st.error("載入走勢圖發生錯誤，請稍後再試。")
