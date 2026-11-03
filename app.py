import streamlit as st
import pandas as pd
import twstock

# 頁面基本設定
st.set_page_config(
    page_title="台股智慧選股與分析工具", page_icon="📈", layout="wide"
)

st.title("📈 實戰台股智慧選股與分析面板")
st.markdown("已串接台股官方資料庫（twstock），結合技術指標與量能條件自動篩選！")

# --- 側邊欄：選股與分析條件設定 ---
st.sidebar.header("⚙️ 篩選條件設定")

stock_dict = {
    "2330": "台積電",
    "2317": "鴻海",
    "2454": "聯發科",
    "2308": "台達電",
    "2382": "廣達",
    "2881": "富邦金",
    "2882": "國泰金",
    "2891": "中信金",
    "2603": "長榮",
    "3034": "聯詠",
    "2412": "中華電",
    "2002": "中鋼",
}

selected_pool = st.sidebar.multiselect(
    "選擇監控的股票池",
    options=list(stock_dict.keys()),
    default=list(stock_dict.keys())[:8],
    format_func=lambda x: f"{x} {stock_dict[x]}",
)

min_vol = st.sidebar.slider("最低成交量門檻 (張)", 1000, 50000, 3000, step=1000)
ma_filter = st.sidebar.checkbox(
    "僅顯示 5日線 > 20日線 (多頭排列)", value=True
)

# --- 主畫面：執行選股 ---
if st.button("🚀 開始抓取真實數據並選股", type="primary"):
  if not selected_pool:
    st.warning("請至少選擇一支股票！")
  else:
    with st.spinner("正在從台股資料庫抓取最新數據並計算指標..."):
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

              status = "✅ 多頭排列" if ma5 > ma20 else "⚠️ 盤整或空頭"

              results.append({
                  "代號": code,
                  "名稱": stock_dict.get(code, ""),
                  "收盤價": round(close, 2),
                  "漲跌幅(%)": round(change_pct, 2),
                  "5日線": round(ma5, 2),
                  "20日線": round(ma20, 2),
                  "當日成交量(張)": vol,
                  "狀態": status,
              })
        except Exception as e:
          pass

      if results:
        df_res = pd.DataFrame(results)
        if ma_filter:
          df_res = df_res[df_res["5日線"] > df_res["20日線"]]
        df_res = df_res[df_res["當日成交量(張)"] >= min_vol]

        st.success(f"篩選完成！共找到 {len(df_res)} 支符合條件的股票。")
        st.dataframe(df_res, use_container_width=True)
      else:
        st.error("目前無法取得數據，請稍後再試。")

# --- 個股歷史走勢區 ---
st.markdown("---")
st.subheader("🔍 個股近三個月走勢圖")
target_stock = st.selectbox(
    "選擇要檢視走勢的股票",
    options=list(stock_dict.keys()),
    format_func=lambda x: f"{x} {stock_dict[x]}",
)

if st.button("載入技術走勢圖"):
  with st.spinner(f"正在載入 {target_stock} 走勢..."):
    try:
      stock = twstock.Stock(target_stock)
      closes = stock.price[-60:]
      if len(closes) > 0:
        df_chart = pd.DataFrame({"Close": closes})
        st.line_chart(df_chart["Close"])
        st.success(
            f"已成功載入 {target_stock} ({stock_dict[target_stock]})"
            " 近期收盤價曲線。"
        )
      else:
        st.error(f"無法取得 {target_stock} 的歷史資料。")
    except Exception as e:
      st.error("載入走勢圖發生錯誤，請稍後再試。")
