import streamlit as st
import pandas as pd
import twstock

# 頁面基本設定
st.set_page_config(
    page_title="台股全市場智慧選股與分析工具", page_icon="📈", layout="wide"
)

st.title("📈 台股全市場智慧選股與分析面板")
st.markdown("已載入台股所有上市櫃股票代號，支援全市場自動篩選與技術走勢！")

# --- 自動載入台股所有上市櫃股票字典 ---
@st.cache_data
def get_all_stocks():
  stock_dict = {}
  # twstock.codes 包含了台股所有的股票代號與名稱
  for code, obj in twstock.codes.items():
    # 過濾掉權證、ETF以外的一般股票或確認是股票/ETF（可依需求調整，這裡收錄所有代號長度為4碼的股票）
    if len(code) == 4 and obj.type in ["股票", "ETF"]:
      stock_dict[code] = obj.name
  return stock_dict


all_stocks = get_all_stocks()

# --- 側邊欄：選股與分析條件設定 ---
st.sidebar.header("⚙️ 全市場篩選條件設定")

# 預設選取幾檔熱門股避免預設載入太多
default_selection = ["2330", "2317", "2454", "2308", "2382", "2881", "2882", "2603"]

selected_pool = st.sidebar.multiselect(
    "選擇或搜尋監控的股票（可複選多檔）",
    options=list(all_stocks.keys()),
    default=default_selection,
    format_func=lambda x: f"{x} {all_stocks[x]}",
)

min_vol = st.sidebar.slider("最低成交量門檻 (張)", 100, 50000, 2000, step500:=500)
ma_filter = st.sidebar.checkbox(
    "僅顯示 5日線 > 20日線 (多頭排列)", value=True
)

# --- 主畫面：執行選股 ---
if st.button("🚀 開始針對已選股票進行智慧篩選", type="primary"):
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

              status = "✅ 多頭排列" if ma5 > ma20 else "⚠️ 盤整或空頭"

              results.append({
                  "代號": code,
                  "名稱": all_stocks.get(code, ""),
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
st.subheader("🔍 全市場個股歷史走勢圖")

# 讓使用者可以從全部股票中搜尋並挑選一檔來看走勢
target_stock = st.selectbox(
    "搜尋或選擇要檢視走勢的股票",
    options=list(all_stocks.keys()),
    format_func=lambda x: f"{x} {all_stocks[x]}",
)

if st.button("載入該股票技術走勢圖"):
  with st.spinner(f"正在載入 {target_stock} 走勢..."):
    try:
      stock = twstock.Stock(target_stock)
      closes = stock.price[-60:]
      if len(closes) > 0:
        df_chart = pd.DataFrame({"Close": closes})
        st.line_chart(df_chart["Close"])
        st.success(
            f"已成功載入 {target_stock} ({all_stocks[target_stock]})"
            " 近期收盤價曲線。"
        )
      else:
        st.error(f"無法取得 {target_stock} 的歷史資料。")
    except Exception as e:
      st.error("載入走勢圖發生錯誤，請稍後再試。")
