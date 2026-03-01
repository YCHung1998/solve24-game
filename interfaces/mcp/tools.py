# interfaces/mcp/tools.py
import os
import sys

# 將專案根目錄加入路徑
root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from core.solver import Solver24, random_hand, check_user_answer
from core.analyzer import analyze_game_difficulty

def solve_24_tool(cards: list[str]) -> dict:
    """提供 4 張撲克牌，計算出所有能得到 24 點的算式。"""
    solver = Solver24(cards)
    solutions = solver.solve()
    return {
        "cards": cards,
        "solutions": solutions,
        "count": len(solutions)
    }

def get_random_hand_tool() -> dict:
    """隨機產生一組保證有解的手牌。"""
    while True:
        hand = random_hand()
        if Solver24(hand).solve():
            return {"hand": hand}

def verify_answer_tool(cards: list[str], expression: str) -> dict:
    """驗證算式是否正確使用手牌並得到 24 點。"""
    success, message = check_user_answer(cards, expression)
    return {
        "is_correct": success,
        "message": message
    }

def analyze_difficulty_tool(target: float = 24.0) -> dict:
    """分析目標數字下的題目難度（可解率）。"""
    return analyze_game_difficulty(target)
