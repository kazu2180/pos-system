import streamlit as st
import requests

# 🚀 Webhook URL（それぞれの Google Apps Script の「ウェブアプリ」として公開したURLを貼る）
LOG_URL = "https://script.google.com/macros/s/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/exec"
SUMMARY_URL = "https://script.google.com/macros/s/YYYYYYYYYYYYYYYYYYYYYYYYYY/exec"

# 🎯 Streamlit UI
st.title("🍰 文化祭POSシステム")

item = st.selectbox("商品を選択", ["マドレーヌ", "クッキー", "パウンドケーキ"])
quantity = st.number_input("数量", min_value=1, step=1)
submit = st.button("販売する")

# ✅ ボタンが押されたときの処理
if submit:
    payload = {
        "item": item,
        "quantity": quantity
    }

    try:
        # 🌐 WebhookへPOST
        r1 = requests.post(LOG_URL, json=payload)
        r2 = requests.post(SUMMARY_URL, json=payload)

        # 🧾 結果確認
        st.write("📜 販売ログからの応答:", r1.text)
        st.write("📊 サマリーからの応答:", r2.text)

        if r1.text.startswith("Success") and r2.text.startswith("Success"):
            st.success(f"{item} を {quantity} 個販売しました！記録完了 📡")
        else:
            st.error("販売の記録または集計に失敗しました 🚨")

    except Exception as e:
        st.error(f"通信エラーが発生しました: {e}")


LOG_URL = "https://script.google.com/macros/s/AKfycbzPi1ufKS6svN6rxirlbJQpsfjzdgbVSvDeWrUfO3VOFPZpnsWQ_rTTbVEzqYOBZtXxPw/exec"  # ←販売ログWebhook

SUMMARY_URL = "https://script.google.com/macros/s/AKfycbzwedHNBDz4D2_l-xoeK-iKlLoDuUD4ZSjhmFSY4PY9AJCRY629wenZMzIGNHV_1XLz/exec"  # ←販売サマリーWebhook