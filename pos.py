import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# === 初期化 ===
if "items" not in st.session_state:
    st.session_state.items = {"マドレーヌ": 300, "焼きそば": 250}
if "sales" not in st.session_state:
    st.session_state.sales = {i: 0 for i in st.session_state.items}

# === Google Sheets接続 ===
log_conn = st.connection("logsheet", type=GSheetsConnection)
summary_conn = st.connection("summarysheet", type=GSheetsConnection)

# === ページ選択 ===
page = st.radio("📋 ページを選択してください", ["販売ページ", "管理ページ"])

# === 販売ページ ===
if page == "販売ページ":
    st.markdown("## 🛍️ 商品販売")
    item = st.selectbox("販売する商品を選択", list(st.session_state.items.keys()), key="sell_item")
    count = st.number_input("販売個数", min_value=1, value=1, step=1, key="sell_count")

    if st.button("販売する", key="sell_button"):
        price = st.session_state.items[item]
        total = price * count
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.sales[item] += count

        # ログ保存
        log_df = pd.DataFrame([[timestamp, item, count, price, total]],
                              columns=["販売時刻", "商品名", "販売個数", "単価", "合計金額"])
        log_conn.insert(log_df)

        # サマリー保存
        summary_df = pd.DataFrame([
            [i, st.session_state.sales[i], st.session_state.items[i], st.session_state.sales[i]*st.session_state.items[i]]
            for i in st.session_state.items if st.session_state.sales[i] > 0
        ], columns=["商品名", "販売個数", "単価", "合計金額"])
        summary_conn.update(summary_df)

        st.success(f"{item} を {count} 個販売しました！（合計 ¥{total}）")

# === 管理ページ ===
elif page == "管理ページ":
    st.markdown("## 🧑‍💼 管理者ページ")
    code = st.text_input("🔒 パスコードを入力してください", type="password", key="admin_code")

    if code != "kaz":
        st.warning("正しいパスコードを入力してください。")
    else:
        # 商品追加
        with st.expander("🆕 商品追加"):
            new_name = st.text_input("商品名", key="new_name_input")
            new_price = st.number_input("価格", min_value=1, key="new_price_input")
            if st.button("追加", key="add_button"):
                if new_name in st.session_state.items:
                    st.error("既に存在する商品です。")
                else:
                    st.session_state.items[new_name] = new_price
                    st.session_state.sales[new_name] = 0
                    st.success(f"{new_name} を ￥{new_price} で追加しました。")

        # 価格変更
        with st.expander("✏️ 価格変更"):
            target = st.selectbox("対象商品", list(st.session_state.items.keys()), key="price_change_item")
            new_price2 = st.number_input("新しい価格", min_value=1, key="price_change_value")
            if st.button("変更", key="price_apply_button"):
                st.session_state.items[target] = new_price2
                st.success(f"{target} の価格を ￥{new_price2} に変更しました。")

        # 商品削除
        with st.expander("🗑️ 商品削除"):
            target_del = st.selectbox("削除対象", list(st.session_state.items.keys()), key="delete_item")
            if st.button("削除", key="delete_button"):
                if st.session_state.sales[target_del] == 0:
                    st.session_state.items.pop(target_del)
                    st.session_state.sales.pop(target_del)
                    st.warning(f"{target_del} を削除しました。")
                else:
                    st.error("販売済みの商品は削除できません。")

        # 販売記録リセット
        with st.expander("🔄 販売記録リセット"):
            if st.button("リセット", key="reset_sales_button"):
                for i in st.session_state.sales:
                    st.session_state.sales[i] = 0
                empty_df = pd.DataFrame(columns=["商品名", "販売個数", "単価", "合計金額"])
                summary_conn.update(empty_df)
                st.warning("販売記録を初期化しました。")