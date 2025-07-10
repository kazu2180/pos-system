import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="文化祭POSシステム", layout="centered")

# --- 商品リスト ---
items = ["マドレーヌ", "チョコケーキ", "いちごクレープ", "抹茶どら焼き"]

# --- ファイル名 ---
log_file = "sales_log.csv"
summary_file = "sales_summary.csv"

# --- 販売ログ保存 ---
def save_sales_log(item, quantity):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame([[item, quantity, timestamp]], columns=["商品", "数量", "日時"])

    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(log_file, index=False, encoding="utf_8_sig")
    return df

# --- 販売サマリー更新 ---
def update_summary(item, quantity):
    if os.path.exists(summary_file):
        df_sum = pd.read_csv(summary_file)
    else:
        df_sum = pd.DataFrame(columns=["商品", "総数"])

    if item in df_sum["商品"].values:
        df_sum.loc[df_sum["商品"] == item, "総数"] += quantity
    else:
        df_sum = pd.concat([df_sum, pd.DataFrame([[item, quantity]], columns=["商品", "総数"])], ignore_index=True)

    df_sum.to_csv(summary_file, index=False, encoding="utf_8_sig")
    return df_sum

# --- UI ---
st.title("🍰 文化祭POSシステム")

item = st.selectbox("商品を選択", items)
quantity = st.number_input("数量", min_value=1, step=1)

if st.button("販売する"):
    df_log = save_sales_log(item, quantity)
    df_summary = update_summary(item, quantity)
    st.success(f"{item} を {quantity}個 販売しました！")
    st.dataframe(df_log.tail(5), use_container_width=True)
    st.dataframe(df_summary, use_container_width=True)

    # --- ダウンロードボタン ---
    with open(log_file, "rb") as f:
        st.download_button("📥 販売ログをダウンロード", f, file_name=log_file, mime="text/csv")
    with open(summary_file, "rb") as f:
        st.download_button("📥 サマリーをダウンロード", f, file_name=summary_file, mime="text/csv")