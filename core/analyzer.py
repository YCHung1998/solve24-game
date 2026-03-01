# core/analyzer.py
from itertools import combinations_with_replacement
from core.models import RANKS, TARGET
from core.solver import Solver24

def analyze_game_difficulty(target: float = TARGET):
    """分析在此目標數字下，所有牌組的可解率"""
    solvable_count = 0
    unsolvable_count = 0

    for cards_tuple in combinations_with_replacement(RANKS, 4):
        cards = list(cards_tuple)
        solver = Solver24(cards, target)
        if solver.solve():
            solvable_count += 1
        else:
            unsolvable_count += 1

    total = solvable_count + unsolvable_count
    return {
        "target": target,
        "solvable": solvable_count,
        "unsolvable": unsolvable_count,
        "ratio": solvable_count / total if total > 0 else 0
    }
