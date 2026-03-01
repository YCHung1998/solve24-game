# interfaces/streamlit/pages/04_📊_Analysis.py
import streamlit as st
import os
import sys

# 將專案根目錄加入路徑
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if root_path not in sys.path:
    sys.path.append(root_path)

from core.analyzer import analyze_game_difficulty

st.set_page_config(page_title="難度分析", page_icon="📊")

st.title("📊 題目難度分析器")
target = st.number_input("設定目標數字", value=24.0, step=1.0)

if st.button("開始分析"):
    with st.spinner("正在掃描 1820 種牌型..."):
        stats = analyze_game_difficulty(target)

    c1, c2 = st.columns(2)
    c1.metric("可解組合", stats["solvable"])
    c2.metric("無解組合", stats["unsolvable"])

    ratio = stats["ratio"]
    st.progress(ratio, text=f"成功率: {ratio:.1%}")

    if ratio < 0.2:
        st.error("地獄級難度 🔥")
    elif ratio > 0.8:
        st.success("新手村難度 🍰")
    else:
        st.info("標準難度 ⚖️")
