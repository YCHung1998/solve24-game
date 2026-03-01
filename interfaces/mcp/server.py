# interfaces/mcp/server.py
from fastmcp import FastMCP
from interfaces.mcp import tools

mcp = FastMCP("Solve24Game")

# 註冊 Tools
@mcp.tool()
def solve_24(cards: list[str]) -> dict:
    """找出 4 張牌的所有 24 點解答"""
    return tools.solve_24_tool(cards)

@mcp.tool()
def get_random_hand() -> dict:
    """取得一組隨機有解的手牌"""
    return tools.get_random_hand_tool()

@mcp.tool()
def verify_answer(cards: list[str], expression: str) -> dict:
    """驗證玩家的解答算式"""
    return tools.verify_answer_tool(cards, expression)

@mcp.tool()
def analyze_difficulty(target: float = 24.0) -> dict:
    """分析特定目標分數的難度"""
    return tools.analyze_difficulty_tool(target)

if __name__ == "__main__":
    mcp.run()
