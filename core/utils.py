import random
from typing import List, Tuple, Set, Dict

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
