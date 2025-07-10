import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# === 商品マスター初期設定 ===
items = {"マドレーヌ": 300, "焼きそば": 250}
sales = {i: 0 for i in items}

# ✅ Google Sheets接続
log_conn = st.connection("logsheet", type=GSheetsConnection)
summary_conn = st.connection("summarysheet", type=GSheetsConnection)

# === ページ構成 ===
tab1, tab2 = st.tabs(["🛍️ 販売ページ", "🧑‍💼 管理ページ"])

# === 販売ページ ===
with tab1:
    st.markdown("<h1 style='text-align:center;'>🎪 商品販売</h1>", unsafe_allow_html=True)
    item = st.selectbox("販売する商品を選んでください", list(items.keys()))
    count = st.number_input("販売個数", min_value=1, value=1, step=1)

    if st.button("販売する"):
        price = items[item]
        total = price * count
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sales[item] += count

        # ✅ ログ保存（追記）
        log_df = pd.DataFrame([[timestamp, item, count, price, total]],
                              columns=["販売時刻", "商品名", "販売個数", "単価", "合計金額"])
        log_conn.insert(log_df)

        # ✅ サマリー保存（上書き）
        summary_df = pd.DataFrame([
            [i, sales[i], items[i], sales[i]*items[i]] 
            for i in items if sales[i] > 0
        ], columns=["商品名", "販売個数", "単価", "合計金額"])
        summary_conn.update(summary_df)

        st.success(f"{item} を {count} 個販売しました！（合計 ¥{total}）")

# === 管理ページ ===
with tab2:
    st.markdown("<h1 style='text-align:center;'>🧑‍💼 管理者ページ</h1>", unsafe_allow_html=True)
    admin_code = st.text_input("パスコードを入力してください", type="password")

    if admin_code != "kaz":
        st.warning("正しいパスコードを入力してください。")
    else:
        # 商品追加
        with st.expander("🆕 商品追加"):
            new_item = st.text_input("商品名", key="add_name")
            new_price = st.number_input("価格", min_value=1, key="add_price")
            if st.button("追加", key="add_button"):
                if new_item in items:
                    st.error("既に存在する商品です。")
                else:
                    items[new_item] = new_price
                    sales[new_item] = 0
                    st.success(f"{new_item} を ￥{new_price} で追加しました。")

        # 価格変更
        with st.expander("✏️ 価格変更"):
            change_item = st.selectbox("対象商品", list(items.keys()), key="change_item")
            new_price2 = st.number_input("新しい価格", min_value=1, key="change_price")
            if st.button("変更", key="apply_price"):
                items[change_item] = new_price2
                st.success(f"{change_item} の価格を ￥{new_price2} に変更しました。")

        # 商品削除
        with st.expander("🗑️ 商品削除"):
            delete_item = st.selectbox("削除対象", list(items.keys()), key="delete_item")
            if st.button("削除", key="apply_delete"):
                if sales[delete_item] == 0:
                    items.pop(delete_item)
                    sales.pop(delete_item)
                    st.warning(f"{delete_item} を削除しました。")
                else:
                    st.error("販売済みの商品は削除できません。")

        # 販売記録リセット
        with st.expander("🔄 販売記録リセット"):
            if st.button("リセット", key="reset_sales"):
                for i in sales:
                    sales[i] = 0
                empty_df = pd.DataFrame(columns=["商品名", "販売個数", "単価", "合計金額"])
                summary_conn.update(empty_df)
                st.warning("販売記録を初期化しました。")