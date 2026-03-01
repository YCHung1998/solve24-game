# interfaces/streamlit/app.py
import streamlit as st
import os
import sys

# 將專案根目錄加入路徑以便 import core 和 services
root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from services.persistence import load_and_increment_counter

st.set_page_config(page_title="24點挑戰賽 Pro", page_icon="♠️", layout="wide")

def main():
    total_plays = load_and_increment_counter(st.session_state)

    st.title("♠️ 24點大師 - 旗艦版")
    st.markdown("""
    ### 歡迎來到 24 點挑戰賽！
    請從側邊欄選擇您想要的模式：
    - **📖 遊戲規則**: 了解如何遊玩。
    - **🎮 自由練習**: 自定義題目或隨機練習，AI 隨時待命。
    - **⏱️ 極速計時賽**: 挑戰您的極限速度！
    - **📊 難度分析器**: 分析不同目標數字下的可解機率。
    """)

    st.sidebar.success("請選擇上方模式開始遊玩")
    st.sidebar.divider()
    st.sidebar.caption("Developed by Dr. CV")

    # 懸浮計數器
    st.markdown(
        f"""
        <style>
        .floating-counter {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #f0f2f6;
            padding: 10px 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            border: 1px solid #dcdcdc;
            font-family: monospace;
            z-index: 9999;
            color: #31333F;
        }}
        </style>
        <div class="floating-counter">
            🌏 Global Plays: <b>{total_plays}</b>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
