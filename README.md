# 24點大師 (Solve24 Game)

給 4 張撲克牌，用 `+ − × ÷` 和括號湊出 24。
這個 repo 是完整的遊戲平台，同時支援 **Streamlit 網頁介面**（給人玩）和 **FastMCP AI Tool**（給 AI 呼叫）。

> Developed by Dr. CV

---

## 專案架構

```text
solve24-game/
├── core/                    # 純算法層（無 UI 依賴）
│   ├── models.py            # 常數：牌面、EPS、TARGET
│   ├── solver.py            # DFS solver + 答案驗證
│   └── analyzer.py         # 全牌型可解率分析
│
├── interfaces/
│   ├── streamlit/           # Streamlit 多頁面 Web UI
│   │   ├── app.py           # 首頁 + 全域計數器
│   │   └── pages/
│   │       ├── 01_📖_Rules.py
│   │       ├── 02_🎮_Practice.py
│   │       ├── 03_⏱️_Time_Trial.py
│   │       └── 04_📊_Analysis.py
│   └── mcp/                 # FastMCP AI Tool 介面
│       ├── server.py        # MCP server entry point
│       └── tools.py         # Tool 實作
│
├── services/
│   └── persistence.py       # 遊玩次數計數器（file-based）
│
├── data/                    # 執行期資料（不進 git）
│
├── .github/workflows/
│   ├── ci.yml               # Push/PR 自動跑 smoke tests
│   └── keep-alive.yml       # 定時 ping Render，防止 idle 休眠
│
├── .streamlit/config.toml   # Streamlit server 設定
├── render.yaml              # Render 部署設定
└── requirements.txt
```

---

## 本地開發

### 環境需求

- Python 3.12+
- pip

### Step 1：Clone & 安裝

```bash
git clone <your-repo-url>
cd solve24-game
pip install -r requirements.txt
```

### Step 2：啟動 Streamlit UI

```bash
streamlit run interfaces/streamlit/app.py
```

瀏覽器會自動開啟 `http://localhost:8501`，包含四個模式：

| 頁面 | 說明 |
|---|---|
| 📖 遊戲規則 | 規則說明與卡片數值對照 |
| 🎮 自由練習 | 隨機發牌或自訂題目，可呼叫 AI 解答 |
| ⏱️ 極速計時賽 | 計時模式，連續解題記錄成績 |
| 📊 難度分析器 | 掃描 1820 種牌型，計算特定目標數的可解率 |

### Step 3：啟動 MCP Server（本地測試）

```bash
mcp dev interfaces/mcp/server.py
```

這會開啟 MCP Inspector，讓你在瀏覽器直接測試 AI Tool：

| Tool | 說明 |
|---|---|
| `solve_24` | 輸入 4 張牌，回傳所有解法 |
| `get_random_hand` | 取得一組保證有解的隨機手牌 |
| `verify_answer` | 驗證玩家的算式是否正確 |
| `analyze_difficulty` | 分析特定目標數的可解率 |

---

## 部署到 Render

Render free tier 在長時間無流量後會自動休眠，冷啟動約 30–60 秒。
這是可接受的，配合下方的 keep-alive workflow 可減少發生頻率。

### Step 1：推到 GitHub

```bash
git push origin main
```

### Step 2：建立 Render Service

1. 前往 [render.com](https://render.com) → **New → Web Service**
2. 連結你的 GitHub repo
3. Render 會自動偵測 `render.yaml`，設定會自動帶入：
   - Build Command：`pip install -r requirements.txt`
   - Start Command：`streamlit run interfaces/streamlit/app.py --server.port $PORT --server.address 0.0.0.0`
4. 點 **Create Web Service**

### Step 3：取得 Render 網址

部署完成後，Render 會給你一個網址，格式如：
```
https://solve24-game.onrender.com
```

### Step 4：設定 GitHub Secret（keep-alive 用）

1. 進入 GitHub Repo → **Settings → Secrets and variables → Actions**
2. 點 **New repository secret**
3. Name：`RENDER_APP_URL`，Value：你的 Render 網址
4. 完成後，keep-alive workflow 每 20 分鐘會自動 ping 一次，防止 app 進入深度休眠

---

## CI/CD 說明

| Workflow | 觸發條件 | 做什麼 |
|---|---|---|
| `ci.yml` | push to `main`/`dev`，對 `main` 發 PR | Solver 正確性測試、Analyzer 測試、MCP import 檢查 |
| `keep-alive.yml` | 每 20 分鐘（cron），或手動觸發 | curl ping Render app，狀態非 2xx/4xx 則標記警告 |

---

## 已知限制

- **計數器不持久**：`data/game_count.txt` 在 Render free tier 每次重新部署後會重置（ephemeral filesystem）。計數器只在單次部署週期內有效。
- **Solver 為 DFS 全解搜尋**，難度分析頁面掃描 1820 種牌型，首次執行約需 5–10 秒。
