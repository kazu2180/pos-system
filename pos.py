import streamlit as st
import requests

# ✅ Webhook URL（Google Apps Scriptから取得した「ウェブアプリ」URLをここに貼る）
LOG_URL = "https://script.google.com/macros/s/AKfycbxo3rEbi_Z0s6HmXd_m2dJggEYRTdAWEpwFCgpCfre59qWrbcVmhzGgKaLMDdZIqlDv/exec"
SUMMARY_URL = "https://script.google.com/macros/s/AKfycbwnEq8ZRjYRp754GIzOLJ05h_gxsdgRqVo83qds7j_yjaujaZVI_KknIm54AT68_q9N/exec"

# 🎯 UI：販売画面
st.title("🍰 文化祭POSシステム")

item = st.selectbox("商品を選択", ["マドレーヌ", "クッキー", "パウンドケーキ"])
quantity = st.number_input("数量", min_value=1, step=1)
submit = st.button("販売する")

# ✅ 処理：販売記録＆集計送信
if submit:
    payload = {
        "item": item,
        "quantity": quantity
    }

    try:
        # 🚀 WebhookにPOST送信（ログ＆サマリー）
        r1 = requests.post(LOG_URL, json=payload)
        r2 = requests.post(SUMMARY_URL, json=payload)

        # 📜 応答を画面に表示（診断にも使える！）
        st.write("📜 販売ログからの応答:", r1.text)
        st.write("📊 サマリーからの応答:", r2.text)

        # 🎉 成功判定
        if r1.text.startswith("Success") and r2.text.startswith("Success"):
            st.success(f"✅ {item} を {quantity} 個販売しました！記録完了 📡")
        else:
            st.error("🚨 販売ログまたは集計に失敗しました。Webhookを再確認してください")

    except Exception as e:
        st.error(f"通信エラーが発生しました 🚧: {e}")