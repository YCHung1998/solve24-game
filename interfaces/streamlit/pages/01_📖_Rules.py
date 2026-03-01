# interfaces/streamlit/pages/01_📖_Rules.py
import streamlit as st

st.set_page_config(page_title="遊戲規則", page_icon="📖")

st.title("📖 遊戲規則與說明")
st.markdown(
    """
    ### 歡迎來到 24 點挑戰賽！
    這是一個訓練數學敏感度的經典遊戲。
    #### 🃏 基礎規則
    1. 系統會給你 **4 張撲克牌**。
    2. 你必須使用 `+` (加), `-` (減), `*` (乘), `/` (除) 以及 `()` (括號)。
    3. 每張牌的數字 **必須使用一次且只能使用一次**。
    4. 計算結果必須等於 **目標數字** (通常是 24)。
    #### 🔢 卡片數值轉換
    *   **A** = 1
    *   **2 ~ 10** = 牌面數字
    *   **J** = 11
    *   **Q** = 12
    *   **K** = 13
    #### 💡 範例
    假設拿到：`3, 3, 8, 8`
    *   錯誤寫法：`8 + 8 + 3` (少用一張 3)
    *   正確解法：`(8/(3-(8/3)))` = 24  (這題很難喔！)
    """
)
st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Poker_Hand_Royal_Flush_in_Clubs.jpg/640px-Poker_Hand_Royal_Flush_in_Clubs.jpg",
    caption="準備好接受挑戰了嗎？",
    width=400,
)
