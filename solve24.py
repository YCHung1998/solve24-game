from typing import List, Tuple, Set
import math
import random

from itertools import combinations_with_replacement
from typing import List, Tuple, Dict


EPS = 1e-6
TARGET = 24.0

RANK_TO_VALUE = {
    'A': 1, '2': 2, '3': 3, '4': 4, '5': 5,
    '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13
}

def enumerate_all_24_hands_with_solution(
    solver_func,
) -> Dict[str, List[Tuple[str, ...]]]:
    """
    solver_func: function(cards: List[str]) -> List[str]
                 回傳所有解（算式），無解則回傳空 list
    """

    ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']

    solvable = []
    unsolvable = []

    for cards in combinations_with_replacement(ranks, 4):
        solutions = solver_func(list(cards))

        if solutions:
            solvable.append(cards)
        else:
            unsolvable.append(cards)

    return {
        "solvable": solvable,
        "unsolvable": unsolvable,
        "total": len(solvable) + len(unsolvable),
        "solvable_count": len(solvable),
        "unsolvable_count": len(unsolvable),
    }


def card_to_value(card: str) -> float:
    """Convert card symbol to numeric value"""
    card = card.upper()
    if card == 'A':
        return 1.0
    if card == 'J':
        return 11.0
    if card == 'Q':
        return 12.0
    if card == 'K':
        return 13.0
    return float(card)


class Solver24:
    def __init__(self, cards: List[str]):
        self.initial = [
            (card_to_value(c), c) for c in cards
        ]
        self.solutions: Set[str] = set()

    def solve(self) -> Set[str]:
        self._dfs(self.initial)
        return self.solutions

    def _dfs(self, items: List[Tuple[float, str]]):
        if len(items) == 1:
            value, expr = items[0]
            if abs(value - TARGET) < EPS:
                self.solutions.add(expr)
            return

        n = len(items)
        for i in range(n):
            for j in range(i + 1, n):
                a_val, a_expr = items[i]
                b_val, b_expr = items[j]

                rest = [
                    items[k] for k in range(n) if k != i and k != j
                ]

                candidates = self._combine(a_val, a_expr, b_val, b_expr)

                for new_val, new_expr in candidates:
                    rest.append((new_val, new_expr))
                    self._dfs(rest)
                    rest.pop()

    def _combine(
        self,
        a_val: float,
        a_expr: str,
        b_val: float,
        b_expr: str
    ) -> List[Tuple[float, str]]:

        results = []

        # Addition (commutative)
        results.append((
            a_val + b_val,
            f"({a_expr}+{b_expr})"
        ))

        # Multiplication (commutative)
        results.append((
            a_val * b_val,
            f"({a_expr}*{b_expr})"
        ))

        # Subtraction (non-commutative)
        results.append((
            a_val - b_val,
            f"({a_expr}-{b_expr})"
        ))
        results.append((
            b_val - a_val,
            f"({b_expr}-{a_expr})"
        ))

        # Division (non-commutative)
        if abs(b_val) > EPS:
            results.append((
                a_val / b_val,
                f"({a_expr}/{b_expr})"
            ))
        if abs(a_val) > EPS:
            results.append((
                b_val / a_val,
                f"({b_expr}/{a_expr})"
            ))

        return results


def random_poker_hand() -> list[str]:
    ranks = ['A', '2', '3', '4', '5', '6', '7',
             '8', '9', '10', 'J', 'Q', 'K']

    deck = []
    for _ in range(4):  # 4 suits
        deck.extend(ranks)

    return random.sample(deck, 4)




if __name__ == "__main__":
    # cards = ["8", "8", "3", "3"]
    cards = random_poker_hand()

    # cards = [13, 1, 11, 6]
    cards = list(map(str, cards))
    print(cards)

    solver = Solver24(cards)
    solutions = solver.solve()

    print(f"Total solutions: {len(solutions)}")
    for s in solutions:
        print(s)


    result = enumerate_all_24_hands_with_solution(Solver24)

    print("Total:", result["total"])
    print("Solvable:", result["solvable_count"])
    print("Unsolvable:", result["unsolvable_count"])
