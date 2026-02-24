import random
from typing import List, Tuple, Set, Dict
from itertools import combinations_with_replacement

# 常數定義
RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
EPS = 1e-6


def card_to_value(card: str) -> float:
    """將撲克牌符號轉換為數值"""
    card = card.upper().strip()
    if card == "A":
        return 1.0
    if card == "J":
        return 11.0
    if card == "Q":
        return 12.0
    if card == "K":
        return 13.0
    try:
        return float(card)
    except ValueError:
        return 0.0  # 處理無效輸入


def random_hand() -> List[str]:
    """隨機產生四張牌"""
    deck = RANKS * 4
    return random.sample(deck, 4)


class Solver24:
    def __init__(self, cards: List[str], target: float = 24.0):
        self.target = target
        self.initial = [(card_to_value(c), c) for c in cards]
        self.solutions: Set[str] = set()

    def solve(self) -> List[str]:
        """計算並回傳所有不重複的解法列表"""
        self.solutions.clear()
        # 驗證輸入是否有效 (避免有 0.0 的情況導致除法錯誤或其他問題)
        if any(v == 0 for v, _ in self.initial):
            return []

        self._dfs(self.initial)
        # 排序讓輸出比較美觀，短的算式在前面
        return sorted(list(self.solutions), key=len)

    def _dfs(self, items: List[Tuple[float, str]]):
        if len(items) == 1:
            value, expr = items[0]
            # 使用 self.target 取代全域變數
            if abs(value - self.target) < EPS:
                self.solutions.add(expr)
            return

        n = len(items)
        for i in range(n):
            for j in range(i + 1, n):
                a_val, a_expr = items[i]
                b_val, b_expr = items[j]

                # 剩下的牌
                rest = [items[k] for k in range(n) if k != i and k != j]

                # 取得所有運算組合
                candidates = self._combine(a_val, a_expr, b_val, b_expr)

                for new_val, new_expr in candidates:
                    rest.append((new_val, new_expr))
                    self._dfs(rest)
                    rest.pop()  # Backtracking

    def _combine(
        self, a_val: float, a_expr: str, b_val: float, b_expr: str
    ) -> List[Tuple[float, str]]:
        results = []

        # 加法 (a+b)
        results.append((a_val + b_val, f"({a_expr}+{b_expr})"))

        # 乘法 (a*b)
        results.append((a_val * b_val, f"({a_expr}*{b_expr})"))

        # 減法 (a-b, b-a)
        results.append((a_val - b_val, f"({a_expr}-{b_expr})"))
        results.append((b_val - a_val, f"({b_expr}-{a_expr})"))

        # 除法 (a/b, b/a) - 需檢查除數不為 0
        if abs(b_val) > EPS:
            results.append((a_val / b_val, f"({a_expr}/{b_expr})"))
        if abs(a_val) > EPS:
            results.append((b_val / a_val, f"({b_expr}/{a_expr})"))

        return results


# 用於統計分析的工具函數
def analyze_game_difficulty(target: float = 24.0):
    """分析在此目標數字下，所有牌組的可解率"""
    solvable_count = 0
    unsolvable_count = 0

    # 使用 ranks 組合 (不重複組合)
    for cards_tuple in combinations_with_replacement(RANKS, 4):
        cards = list(cards_tuple)
        solver = Solver24(cards, target)
        if solver.solve():
            solvable_count += 1
        else:
            unsolvable_count += 1

    return {
        "target": target,
        "solvable": solvable_count,
        "unsolvable": unsolvable_count,
        "ratio": (
            solvable_count / (solvable_count + unsolvable_count)
            if (solvable_count + unsolvable_count) > 0
            else 0
        ),
    }
