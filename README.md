# 24點大師 (Solve24 Game)

這是一個 24 點遊戲的旗艦版實作，支援 **Streamlit UI** 介面以及 **FastMCP** AI 工具。

## 專案架構
```text
solve24-game/
├── core/                # 【核心邏輯層】負責 24 點算法、分析與檢查
├── interfaces/          # 【介面接入層】
│   ├── streamlit/       # Streamlit 網頁界面 (多頁面設計)
│   └── mcp/             # FastMCP 界面 (AI Tool)
├── services/            # 【共用服務層】處理計數器與資料持久化
├── data/                # 【資料存放區】
└── requirements.txt     # 依賴套件
```

## 安裝方式
```bash
pip install -r requirements.txt
```

## 如何執行

### 1. 啟動 Streamlit UI
在根目錄執行：
```bash
streamlit run interfaces/streamlit/app.py
```
這會開啟一個包含自動發牌、手動輸入、計時賽與難度分析的多頁面網頁。

### 2. 啟動 FastMCP 本地測試
在根目錄執行：
```bash
mcp dev interfaces/mcp/server.py
```
這會啟動 MCP Inspector，讓你可以直接在瀏覽器測試 AI 如何呼叫這些 Tool。

## 如何部署到 FastMCP Cloud

部署到 FastMCP Cloud 通常有以下幾種方式：

### 方式 A：使用 MCP CLI (推薦)
如果你已經安裝並登入了 MCP：
```bash
mcp deploy interfaces/mcp/server.py
```
*註：請確保你的環境變數中已設定好對應的 Cloud API Key。*

### 方式 B：GitHub 整合
1. 將此專案 Push 到 GitHub。
2. 在 FastMCP Cloud 控制台連結此 Repo。
3. 指定執行入口點為 `interfaces/mcp/server.py`。

### 方式 C：Docker 部署
如果 Cloud 支援 Docker，可以使用以下設定載入：
```bash
# Dockerfile 範例片段
CMD ["python", "interfaces/mcp/server.py"]
```

---
Developed by Dr. CV