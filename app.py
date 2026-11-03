import streamlit as st
import pandas as pd
import yfinance as yf

# 頁面基本設定
st.set_page_config(
    page_title="台股智慧選股與分析工具",
    page_icon="📈",
    layout="wide"
)

st.title("📈 實戰台股智慧選股與分析面板")
st.markdown("已串接真實台股數據，結合技術指標與量能條件自動篩選！")

# --- 側邊欄：選股與分析條件設定 ---
st.sidebar.header("⚙️ 篩選條件設定")

# 預設台股熱門標的池（代號格式：股票代號.TW）
stock_dict = {
    "2330.TW": "台積電",
    "2317.TW": "鴻海",
    "2454.TW": "聯發科",
    "2308.TW": "台達電",
    "2382.TW": "廣達",
    "2881.TW": "富邦金",
    "2882.TW": "國泰金",
    "2891.TW": "中信金",
    "2603.TW": "長榮",
    "3034.TW": "聯詠",
    "2412.TW": "中華電",
    "2002.TW": "中鋼"
}

selected_pool = st.sidebar.multiselect(
    "選擇監控的股票池",
    options=list(stock_dict.keys()),
    default=list(stock_dict.keys())[:8],
    format_func=lambda x: f"{x} {stock_dict[x]}"
)

# 篩選條件
min_vol = st.sidebar.slider("最低成交量門檻 (張)", 1000, 50000, 3000, step=1000)
ma_filter = st.sidebar.checkbox("僅顯示 5日線 > 20日線 (多頭排列)", value=True)

# --- 主畫面：執行選股 ---
if st.button("🚀 開始抓取真實數據並選股", type="primary"):
    if not selected_pool:
        st.warning("請至少選擇一支股票！")
    else:
        with st.spinner("正在從股市資料庫抓取最新數據並計算指標..."):
            results = []
            for ticker in selected_pool:
                try:
                    # 抓取最近 60 天資料
                    stock = yf.Ticker(ticker)
                    df = stock.history(period="60d")
                    
                    if len(df) >= 20:
                        close = df['Close'].iloc[-1]
                        prev_close = df['Close'].iloc[-2]
                        change_pct = ((close - prev_close) / prev_close) * 100
                        
                        # 計算均線
                        ma5 = df['Close'].rolling(window=5).mean().iloc[-1]
                        ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
                        
                        # 計算成交量 (張)
                        vol = df['Volume'].iloc[-1] / 1000
                        
                        status = "✅ 多頭排列" if ma5 > ma20 else "⚠️ 盤整或空頭"
                        
                        results.append({
                            "代號": ticker.replace(".TW", ""),
                            "名稱": stock_dict.get(ticker, ""),
                            "收盤價": round(close, 2),
                            "漲跌幅(%)": round(change_pct, 2),
                            "5日線": round(ma5, 2),
                            "20日線": round(ma20, 2),
                            "當日成交量(張)": int(vol),
                            "狀態": status
                        })
                except Exception as e:
                    pass
            
            if results:
                df_res = pd.DataFrame(results)
                
                # 套用過濾條件
                if ma_filter:
                    df_res = df_res[df_res['5日線'] > df_res['20日線']]
                df_res = df_res[df_res['當日成交量(張)'] >= min_vol]
                
                st.success(f"篩選完成！共找到 {len(df_res)} 支符合條件的股票。")
                st.dataframe(df_res, use_container_width=True)
            else:
                st.error("無法取得資料，請稍後再試。")

# --- 個股歷史走勢區 ---
st.markdown("---")
st.subheader("🔍 個股近三個月走勢圖")
target_stock = st.selectbox(
    "選擇要檢視走勢的股票", 
    options=list(stock_dict.keys()), 
    format_func=lambda x: f"{x} {stock_dict[x]}"
)

if st.button("載入技術走勢圖"):
    with st.spinner(f"正在載入 {target_stock} 走勢..."):
        history_data = yf.Ticker(target_stock).history(period="3m")
        st.line_chart(history_data['Close'])
        st.success(f"已成功載入 {target_stock} ({stock_dict[target_stock]}) 近三個月收盤價曲線。")
