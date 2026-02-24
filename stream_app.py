import streamlit as st
from core.game1 import solver as c_solver
import time
import os
import re

# --- 全域設定 ---
st.set_page_config(page_title="24點挑戰賽 Pro", page_icon="♠️", layout="wide")

# --- 工具函數：全域計數器 (File Based) ---
COUNTER_FILE = "game_count.txt"


def load_and_increment_counter():
    """讀取並增加遊玩次數"""
    if "has_counted" not in st.session_state:
        # 初始化
        count = 0
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    content = f.read().strip()
                    if content.isdigit():
                        count = int(content)
            except:
                pass  # 讀取失敗就算了

        # 增加次數
        count += 1
        st.session_state["has_counted"] = True

        # 寫回檔案
        try:
            with open(COUNTER_FILE, "w") as f:
                f.write(str(count))
        except:
            pass  # 寫入失敗（例如權限問題）也忽略

        return count
    else:
        # 如果這次 session 已經算過了，就只讀取不增加
        if os.path.exists(COUNTER_FILE):
            try:
                with open(COUNTER_FILE, "r") as f:
                    return int(f.read().strip())
            except:
                return 0
        return 0


# --- 工具函數：驗證使用者算式 ---
def check_user_answer(cards: list, user_expr: str, target: float) -> tuple[bool, str]:
    """
    驗證使用者的算式是否合法且正確。
    1. 是否等於 target
    2. 是否使用了正確的四張牌
    """
    try:
        # 1. 安全性過濾：只允許數字、括號、運算符
        allowed = set("0123456789+-*/(). ")
        if not set(user_expr).issubset(allowed):
            return False, "❌ 算式包含非法字元，請只使用數字和運算符號。"

        # 2. 計算結果
        # eval 在這裡相對安全，因為我們過濾過字元
        result = eval(user_expr)

        if abs(result - target) > 0.001:
            return False, f"❌ 算式結果是 {result}，不是 {int(target)} 喔！"

        # 3. 驗證是否用了那四張牌 (稍微複雜一點的邏輯)
        # 把使用者輸入的數字萃取出來
        user_nums = re.findall(r"\d+", user_expr)
        # 把卡片轉成數字字串 (J->11, etc.)
        card_vals = []
        for c in cards:
            v = c_solver.card_to_value(c)
            card_vals.append(str(int(v)) if v.is_integer() else str(v))

        # 排序後比較
        if sorted(user_nums) != sorted(card_vals):
            # 這裡有個小漏洞：如果使用者輸入 1+1 (原本是 11)，這裡暫不處理太複雜的拆解
            # 簡單版：只檢查數字出現次數
            return False, f"❌ 你使用的數字跟手牌不符！請確認 J=11, Q=12, K=13"

        return True, "🎉 正確答案！太強了！"

    except Exception as e:
        return False, "❌ 算式格式錯誤 (括號有對齊嗎？)"


# ==========================================
# 頁面 1: 📖 遊戲規則
# ==========================================
def page_rules():
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
    *   正確解法：`8 / ( 3 - 8 / 3 )` = 24  (這題很難喔！)
    """
    )
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Poker_Hand_Royal_Flush_in_Clubs.jpg/640px-Poker_Hand_Royal_Flush_in_Clubs.jpg",
        # "https://www.mksucai.com/png/qkpbwlkm.html",
        caption="準備好接受挑戰了嗎？",
        width=400,
    )


# ==========================================
# 頁面 2: 🎮 自由練習 (原本的主程式)
# ==========================================
def page_practice():
    st.title("🎮 自由練習模式")
    st.caption("輕鬆玩，可以自訂題目，也可以讓 AI 幫你算。")
    col_settings, col_display = st.columns([1, 3])

    with col_settings:
        target_num = st.number_input("目標數字", value=24.0, step=1.0, format="%.0f")

        def deal_cards_practice():
            st.session_state["p_cards"] = c_solver.random_hand()
            # 同步 input key
            for i in range(4):
                st.session_state[f"p_input_{i}"] = st.session_state["p_cards"][i]
            if "p_solutions" in st.session_state:
                del st.session_state["p_solutions"]

        st.button("🎲 隨機發牌", on_click=deal_cards_practice, key="btn_practice_deal")

    # 初始化 state
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
                solver = c_solver.Solver24(input_cards, target=target_num)
                solutions = solver.solve()
                if solutions:
                    st.success(f"找到 {len(solutions)} 種解法！")
                    for s in solutions[:5]:
                        st.code(f"{s} = {int(target_num)}")
                else:
                    st.warning("無解！")


# ==========================================
# 頁面 3: ⏱️ 極速計時賽 (新功能)
# ==========================================
def page_time_trial():
    st.title("⏱️ 極速計時賽")
    st.caption("系統自動出題，請在下方輸入算式 (例如：(3+8)*2+2)。看你解多快！")
    st.caption("數入答案時請將字母請換成數字填寫: A=1, J=11, Q=12, K=13")

    # 初始化計時賽變數
    if "tt_active" not in st.session_state:
        st.session_state["tt_active"] = False
        st.session_state["tt_cards"] = []
        st.session_state["tt_start_time"] = 0
        st.session_state["tt_solved_count"] = 0

    # 開始遊戲按鈕
    if not st.session_state["tt_active"]:
        if st.button("🔥 開始挑戰 (計時開始)", type="primary"):
            st.session_state["tt_active"] = True
            st.session_state["tt_start_time"] = time.time()
            st.session_state["tt_solved_count"] = 0
            # 發第一手牌 (必須保證有解)
            while True:
                hand = c_solver.random_hand()
                if c_solver.Solver24(hand, 24).solve():
                    st.session_state["tt_cards"] = hand
                    break
            st.rerun()
    else:
        # 遊戲進行中
        elapsed = time.time() - st.session_state["tt_start_time"]
        st.metric(
            "⏳ 已用時間",
            f"{elapsed:.1f} 秒",
            f"已解決: {st.session_state['tt_solved_count']} 題",
        )

        # 顯示卡片 (大一點)
        cols = st.columns(4)
        for i, card in enumerate(st.session_state["tt_cards"]):
            cols[i].markdown(
                f"<h1 style='text-align: center; color: #FF4B4B; border: 2px solid #ddd; border-radius: 10px;'>{card}</h1>",
                unsafe_allow_html=True,
            )

        # 使用者輸入答案區
        user_answer = st.text_input("輸入你的算式 (按 Enter 送出):", key="tt_input")

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("✅ 送出答案", type="primary"):
                is_correct, msg = check_user_answer(
                    st.session_state["tt_cards"], user_answer, 24.0
                )
                if is_correct:
                    st.success(msg)
                    st.session_state["tt_solved_count"] += 1
                    time.sleep(1)  # 讓使用者看到成功訊息
                    # 發下一手牌
                    while True:
                        hand = c_solver.random_hand()
                        if c_solver.Solver24(hand, 24).solve():
                            st.session_state["tt_cards"] = hand
                            break
                    st.rerun()  # 重新整理頁面清空輸入框 (需要配合 key 重置技巧，這裡簡化處理)
                else:
                    st.error(msg)

        with c2:
            if st.button("🏳️ 放棄 / 結束"):
                st.session_state["tt_active"] = False
                st.balloons()
                st.info(
                    f"遊戲結束！你解決了 {st.session_state['tt_solved_count']} 題，總耗時 {elapsed:.1f} 秒。"
                )

        st.markdown("---")
        with st.expander("🙈 實在解不出來？偷看答案"):
            if st.button("顯示解答"):
                solver = c_solver.Solver24(st.session_state["tt_cards"], 24)
                st.write(solver.solve())


# ==========================================
# 頁面 4: 📊 難度分析
# ==========================================
def page_analysis():
    st.title("📊 題目難度分析器")
    target = st.number_input("設定目標數字", value=24.0, step=1.0)

    if st.button("開始分析"):
        with st.spinner("正在掃描 1820 種牌型..."):
            stats = c_solver.analyze_game_difficulty(target)

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


# ==========================================
# 主程式入口 (Main Logic)
# ==========================================
def main():
    # 1. 載入全域遊玩次數
    total_plays = load_and_increment_counter()

    # 2. 側邊欄導航 (Navigation)
    with st.sidebar:
        st.title("♠️ 24點大師")

        # 使用 radio button 當作選單
        page = st.radio(
            "請選擇模式：",
            ["📖 遊戲規則", "🎮 自由練習", "⏱️ 極速計時賽", "📊 難度分析"],
            index=1,  # 預設在自由練習
        )

        st.divider()
        st.caption(f"Developed by Dr. CV")

    # 3. 根據選擇渲染對應頁面
    if page == "📖 遊戲規則":
        page_rules()
    elif page == "🎮 自由練習":
        page_practice()
    elif page == "⏱️ 極速計時賽":
        page_time_trial()
    elif page == "📊 難度分析":
        page_analysis()

    # 4. 右下角懸浮計數器 (Floating Counter)
    # 使用 CSS 固定位置
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
