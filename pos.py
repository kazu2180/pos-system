import streamlit as st
import pandas as pd
import pygsheets
from datetime import datetime

# 認証（secrets.tomlの "google" セクションから）
gc = pygsheets.authorize(service_account_info=st.secrets["google"])

# Google Sheets を開く
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1TxIn9VrOpazYxwEZqx6D134qGAuBNuwF9d_giD04fdU/edit"
sheet = gc.open_by_url(spreadsheet_url)
worksheet = sheet.worksheet_by_title("販売ログ")

# Streamlit UI
st.title("🍰 文化祭POSシステム（pygsheets版）")

item = st.selectbox("商品を選択", ["マドレーヌ", "クッキー", "パウンドケーキ"])
quantity = st.number_input("数量を入力", min_value=1, step=1)
submit = st.button("販売する")

# 販売処理
if submit:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = [item, quantity, timestamp]
    worksheet.append_table(new_row)
    st.success(f"{item} を {quantity} 個販売しました 📡")

# 販売ログの表示
st.subheader("📊 販売履歴")
data = worksheet.get_all_records()
df = pd.DataFrame(data)
st.dataframe(df)

# CSVダウンロード機能
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="販売履歴をCSVでダウンロード",
    data=csv,
    file_name=f"sales_{datetime.now().strftime('%Y-%m-%d')}.csv",
    mime="text/csv"
)