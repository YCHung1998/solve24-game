# interfaces/streamlit/pages/02_🎮_Practice.py
import streamlit as st
import os
import sys

# 將專案根目錄加入路徑
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if root_path not in sys.path:
    sys.path.append(root_path)

from core.solver import Solver24, random_hand

st.set_page_config(page_title="自由練習", page_icon="🎮")

st.title("🎮 自由練習模式")
st.caption("輕鬆玩，可以自訂題目，也可以讓 AI 幫你算。")

col_settings, col_display = st.columns([1, 3])

with col_settings:
    target_num = st.number_input("目標數字", value=24.0, step=1.0, format="%.0f")

    def deal_cards_practice():
        st.session_state["p_cards"] = random_hand()
        for i in range(4):
            st.session_state[f"p_input_{i}"] = st.session_state["p_cards"][i]
        if "p_solutions" in st.session_state:
            del st.session_state["p_solutions"]

    st.button("🎲 隨機發牌", on_click=deal_cards_practice, key="btn_practice_deal")

if "p_cards" not in st.session_state:
    st.session_state["p_cards"] = ["", "", "", ""]

with col_display:
    c1, c2, c3, c4 = st.columns(4)
    new_cards = []
    for i, col in enumerate([c1, c2, c3, c4]):
        with col:
            val = st.text_input(
                f"卡片 {i+1}",
                value=st.session_state["p_cards"][i],
                key=f"p_input_{i}",
                max_chars=2,
            )
            new_cards.append(val)

    st.write("")
    if st.button("🚀 計算 AI 解答", type="primary"):
        input_cards = [c.strip().upper() for c in new_cards if c.strip() != ""]
        if len(input_cards) != 4:
            st.error("請輸入完整 4 張牌")
        else:
            solver = Solver24(input_cards, target=target_num)
            solutions = solver.solve()
            if solutions:
                st.success(f"找到 {len(solutions)} 種解法！")
                for s in solutions[:5]:
                    st.code(f"{s} = {int(target_num)}")
            else:
                st.warning("無解！")
