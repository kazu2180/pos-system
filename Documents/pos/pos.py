import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 認証スコープ設定
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# 認証情報読み込み（販売ログ用）
log_creds = Credentials.from_service_account_info(
    st.secrets["connections"]["logsheet"], scopes=scopes
)
log_client = gspread.authorize(log_creds)
log_sheet = log_client.open_by_url(st.secrets["connections"]["logsheet"]["spreadsheet"])
log_ws = log_sheet.worksheet(st.secrets["connections"]["logsheet"]["worksheet"])

# 認証情報読み込み（販売サマリー用）
summary_creds = Credentials.from_service_account_info(
    st.secrets["connections"]["summarysheet"], scopes=scopes
)
summary_client = gspread.authorize(summary_creds)
summary_sheet = summary_client.open_by_url(st.secrets["connections"]["summarysheet"]["spreadsheet"])
summary_ws = summary_sheet.worksheet(st.secrets["connections"]["summarysheet"]["worksheet"])

# 商品リスト（必要に応じて変更）
items = ["マドレーヌ", "クッキー", "パウンドケーキ"]

st.title("🍰 文化祭POSシステム")

# UI: 商品と数量
item = st.selectbox("商品を選択", items)
quantity = st.number_input("数量", min_value=1, step=1)
submit = st.button("販売する")

# 販売処理
if submit:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [item, quantity, now]
    log_ws.append_row(new_row)
    st.success(f"{item} を {quantity} 個販売しました！ 🧾")

# サマリー表示とダウンロード
st.subheader("📊 販売サマリー")
data = summary_ws.get_all_records()
df = pd.DataFrame(data)

st.dataframe(df)

# CSVダウンロード機能
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="販売サマリーをダウンロードする",
    data=csv,
    file_name=f"sales_summary_{datetime.now().strftime('%Y-%m-%d')}.csv",
    mime="text/csv"
)