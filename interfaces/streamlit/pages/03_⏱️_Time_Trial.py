# interfaces/streamlit/pages/03_⏱️_Time_Trial.py
import streamlit as st
import time
import os
import sys

# 將專案根目錄加入路徑
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if root_path not in sys.path:
    sys.path.append(root_path)

from core.solver import Solver24, random_hand, check_user_answer

st.set_page_config(page_title="極速計時賽", page_icon="⏱️")

st.title("⏱️ 極速計時賽")
st.caption("系統自動出題，請在下方輸入算式 (例如：(3+8)*2+2)。看你解多快！")
st.caption("數入答案時請將字母請換成數字填寫: A=1, J=11, Q=12, K=13")

if "tt_active" not in st.session_state:
    st.session_state["tt_active"] = False
    st.session_state["tt_cards"] = []
    st.session_state["tt_start_time"] = 0
    st.session_state["tt_solved_count"] = 0

if not st.session_state["tt_active"]:
    if st.button("🔥 開始挑戰 (計時開始)", type="primary"):
        st.session_state["tt_active"] = True
        st.session_state["tt_start_time"] = time.time()
        st.session_state["tt_solved_count"] = 0
        while True:
            hand = random_hand()
            if Solver24(hand, 24).solve():
                st.session_state["tt_cards"] = hand
                break
        st.rerun()
else:
    elapsed = time.time() - st.session_state["tt_start_time"]
    st.metric(
        "⏳ 已用時間",
        f"{elapsed:.1f} 秒",
        f"已解決: {st.session_state['tt_solved_count']} 題",
    )

    cols = st.columns(4)
    for i, card in enumerate(st.session_state["tt_cards"]):
        cols[i].markdown(
            f"<h1 style='text-align: center; color: #FF4B4B; border: 2px solid #ddd; border-radius: 10px;'>{card}</h1>",
            unsafe_allow_html=True,
        )

    user_answer = st.text_input("輸入你的算式 (按 Enter 送出):", key="tt_input")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("✅ 送出答案", type="primary"):
            is_correct, msg = check_user_answer(st.session_state["tt_cards"], user_answer, 24.0)
            if is_correct:
                st.success(msg)
                st.session_state["tt_solved_count"] += 1
                time.sleep(1)
                while True:
                    hand = random_hand()
                    if Solver24(hand, 24).solve():
                        st.session_state["tt_cards"] = hand
                        break
                st.rerun()
            else:
                st.error(msg)

    with c2:
        if st.button("🏳️ 放棄 / 結束"):
            st.session_state["tt_active"] = False
            st.balloons()
            st.info(f"遊戲結束！你解決了 {st.session_state['tt_solved_count']} 題，總耗時 {elapsed:.1f} 秒。")

    st.markdown("---")
    with st.expander("🙈 實在解不出來？偷看答案"):
        if st.button("顯示解答"):
            solver = Solver24(st.session_state["tt_cards"], 24)
            st.write(solver.solve())
