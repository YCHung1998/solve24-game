# core/solver.py
import random
import re
from typing import List, Tuple, Set
from core.models import RANKS, EPS, TARGET

def card_to_value(card: str) -> float:
    """將撲克牌符號轉換為數值"""
    card = card.upper().strip()
    if card == "A": return 1.0
    if card == "J": return 11.0
    if card == "Q": return 12.0
    if card == "K": return 13.0
    try:
        return float(card)
    except ValueError:
        return 0.0

def random_hand() -> List[str]:
    """隨機產生四張牌"""
    deck = RANKS * 4
    return random.sample(deck, 4)

class Solver24:
    def __init__(self, cards: List[str], target: float = TARGET):
        self.target = target
        self.initial = [(card_to_value(c), c) for c in cards]
        self.solutions: Set[str] = set()

    def solve(self) -> List[str]:
        """計算並回傳所有不重複的解法列表"""
        self.solutions.clear()
        if any(v == 0 for v, _ in self.initial):
            return []
        self._dfs(self.initial)
        return sorted(list(self.solutions), key=len)

    def _dfs(self, items: List[Tuple[float, str]]):
        if len(items) == 1:
            value, expr = items[0]
            if abs(value - self.target) < EPS:
                self.solutions.add(expr)
            return

        n = len(items)
        for i in range(n):
            for j in range(i + 1, n):
                a_val, a_expr = items[i]
                b_val, b_expr = items[j]
                rest = [items[k] for k in range(n) if k != i and k != j]
                candidates = self._combine(a_val, a_expr, b_val, b_expr)
                for new_val, new_expr in candidates:
                    rest.append((new_val, new_expr))
                    self._dfs(rest)
                    rest.pop()

    def _combine(self, a_val: float, a_expr: str, b_val: float, b_expr: str) -> List[Tuple[float, str]]:
        results = []
        results.append((a_val + b_val, f"({a_expr}+{b_expr})"))
        results.append((a_val * b_val, f"({a_expr}*{b_expr})"))
        results.append((a_val - b_val, f"({a_expr}-{b_expr})"))
        results.append((b_val - a_val, f"({b_expr}-{a_expr})"))
        if abs(b_val) > EPS:
            results.append((a_val / b_val, f"({a_expr}/{b_expr})"))
        if abs(a_val) > EPS:
            results.append((b_val / a_val, f"({b_expr}/{a_expr})"))
        return results

def check_user_answer(cards: List[str], user_expr: str, target: float = TARGET) -> Tuple[bool, str]:
    """驗證使用者的算式是否合法且正確"""
    try:
        allowed = set("0123456789+-*/(). ")
        if not set(user_expr).issubset(allowed):
            return False, "❌ 算式包含非法字元，請只使用數字和運算符號。"

        # Basic safety check for eval
        result = eval(user_expr, {"__builtins__": {}}, {})

        if abs(result - target) > 0.001:
            return False, f"❌ 算式結果是 {result}，不是 {int(target)} 喔！"

        user_nums = re.findall(r"\d+", user_expr)
        card_vals = []
        for c in cards:
            v = card_to_value(c)
            card_vals.append(str(int(v)) if v.is_integer() else str(v))

        if sorted(user_nums) != sorted(card_vals):
            return False, f"❌ 你使用的數字跟手牌不符！請確認 A=1, J=11, Q=12, K=13"

        return True, "🎉 正確答案！太強了！"
    except Exception:
        return False, "❌ 算式格式錯誤 (括號有對齊嗎？)"
