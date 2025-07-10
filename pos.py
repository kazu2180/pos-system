import streamlit as st
import requests

# Webhook URL（Google Apps Scriptで公開した2つのURLを貼る）
LOG_URL = "https://script.google.com/macros/s/xxxxxxxxxxxxxxxxxxxxxxxxxxxx/exec"
SUMMARY_URL = "https://script.google.com/macros/s/yyyyyyyyyyyyyyyyyyyyyyyyyyyy/exec"

# UI
st.title("🍰 文化祭POSシステム")

item = st.selectbox("商品を選択", ["マドレーヌ", "クッキー", "パウンドケーキ"])
quantity = st.number_input("数量を入力", min_value=1, step=1)
submit = st.button("販売する")

if submit:
    payload = {
        "item": item,
        "quantity": quantity
    }

    # Webhook①：販売ログに記録
    r1 = requests.post(LOG_URL, json=payload)

    # Webhook②：販売サマリーに集計記録
    r2 = requests.post(SUMMARY_URL, json=payload)

    # 結果表示
    if r1.text.startswith("Success") and r2.text.startswith("Success"):
        st.success(f"{item} を {quantity} 個販売しました 📡")
    else:
        st.error("販売の記録または集計に失敗しました")

r1 = requests.post(LOG_URL, json=payload)
r2 = requests.post(SUMMARY_URL, json=payload)

st.write("Log response:", r1.text)
st.write("Summary response:", r2.text)


LOG_URL = "https://script.google.com/macros/s/AKfycbzPi1ufKS6svN6rxirlbJQpsfjzdgbVSvDeWrUfO3VOFPZpnsWQ_rTTbVEzqYOBZtXxPw/exec"  # ←販売ログWebhook

SUMMARY_URL = "https://script.google.com/macros/s/AKfycbzwedHNBDz4D2_l-xoeK-iKlLoDuUD4ZSjhmFSY4PY9AJCRY629wenZMzIGNHV_1XLz/exec"  # ←販売サマリーWebhook