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

---

## 教學：從零開始設定 CI/CD 並部署到 Render

### 概念先懂

```
你的電腦 (dev branch)
    │
    │ git push
    ▼
GitHub (main branch)  ──→  GitHub Actions 自動跑測試 (ci.yml)
    │                                                      │
    │ Render 偵測到 main 有新 push                         │ 測試失敗 → 不讓 merge
    ▼
Render 自動重新部署
    │
    ▼
你的 Streamlit app 上線（https://your-app.onrender.com）
    ▲
    │ 每 20 分鐘 ping 一次（keep-alive.yml）
GitHub Actions 定時喚醒
```

整個流程你只需要 `git push`，其餘都是自動的。

---

### Part 1：設定 GitHub Actions CI

#### Step 1 — 確認 workflows 存在

Repo 裡已有以下兩個檔案，不需要額外設定：

```
.github/workflows/ci.yml          ← 自動測試
.github/workflows/keep-alive.yml  ← 定時喚醒 Render
```

#### Step 2 — 設定 keep-alive 所需的 Secret

> 注意：要先完成 Render 部署拿到網址才能做這步。

1. 進入 GitHub Repo → **Settings**（右上角齒輪）
2. 左側選單 → **Secrets and variables → Actions**
3. 點 **New repository secret**
4. 填入：
   - Name：`RENDER_APP_URL`
   - Secret：`https://你的app名稱.onrender.com`
5. 點 **Add secret**

完成後，每 20 分鐘 GitHub Actions 會自動 ping 你的 app，讓 Render 的 free tier 不會進入深度休眠。

---

### Part 2：部署到 Render

#### Step 1 — 建立 Render 帳號

前往 [render.com](https://render.com) 註冊，可直接用 GitHub 帳號登入。

#### Step 2 — 建立 Web Service

1. Dashboard → 右上角 **New +** → **Web Service**
2. 選 **Build and deploy from a Git repository** → Connect GitHub
3. 找到你的 repo（`solve24-game`）→ 點 **Connect**

#### Step 3 — 設定部署參數

Render 會自動讀取 `render.yaml`，大部分欄位會自動帶入。確認以下設定正確：

| 欄位 | 應填值 |
|---|---|
| Name | `solve24-game`（或自訂） |
| Region | `Oregon (US West)` 或任一 |
| Branch | **`main`**（重要：不要選 dev） |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `streamlit run interfaces/streamlit/app.py --server.port $PORT --server.address 0.0.0.0` |
| Plan | **Free** |

#### Step 4 — 點 Create Web Service

Render 開始第一次部署，過程約 2–3 分鐘。
部署完成後會得到一個網址：`https://solve24-game.onrender.com`（名稱依你設定而異）。

回到 [Part 1 Step 2](#step-2--設定-keep-alive-所需的-secret) 把這個網址填入 GitHub Secret。

---

### Part 3：日常開發流程

```bash
# 1. 在 dev branch 開發
git checkout dev

# 2. 改完後 commit
git add -A
git commit -m "feat: 你做了什麼"
git push origin dev
# → GitHub Actions 跑 ci.yml 測試（push dev 也會觸發）

# 3. 確認測試通過後，merge 到 main
git checkout main
git merge dev
git push origin main
# → Render 偵測到 main 有變動，自動重新部署（約 2 分鐘）

# 4. 部署完成，到 Render Dashboard 確認狀態是 "Live"
```

---

### 注意事項

**Render Free Tier 限制：**
- 每月 750 小時免費額度（單個 service 基本夠用）
- 超過 **15 分鐘無流量**會進入休眠，下次有人開啟需要等 30–60 秒冷啟動
- keep-alive workflow 每 20 分鐘 ping 一次，可大幅減少被休眠的機率，但不能完全避免（GitHub Actions 的 cron 本身有幾分鐘的執行誤差）
- **Filesystem 是暫時的**：每次重新部署，`data/game_count.txt` 都會重置，遊玩次數計數器歸零

**Branch 策略：**
- Render 只監聽 `main`，推 `dev` 不會觸發部署
- 不要直接在 `main` 上開發，永遠透過 `dev` → merge 的方式更新

**CI 失敗時：**
- GitHub Actions 測試失敗不會阻止你 push，但代表程式有問題，不應該 merge 到 main
- 到 GitHub Repo → **Actions** 頁面可以看到每次 CI 的執行結果和錯誤訊息

---

## 官方參考資料

### Streamlit
| 文件 | 連結 |
|---|---|
| 快速開始 | [docs.streamlit.io/get-started](https://docs.streamlit.io/get-started) |
| 多頁面 app 設計 | [docs.streamlit.io/develop/concepts/multipage-apps](https://docs.streamlit.io/develop/concepts/multipage-apps/overview) |
| `config.toml` 所有設定項 | [docs.streamlit.io/develop/api-reference/configuration/config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml) |
| `st.session_state` | [docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state) |

### Render
| 文件 | 連結 |
|---|---|
| Web Services 部署總覽 | [render.com/docs/web-services](https://render.com/docs/web-services) |
| `render.yaml` Infrastructure as Code | [render.com/docs/infrastructure-as-code](https://render.com/docs/infrastructure-as-code) |
| Free tier 限制說明 | [render.com/docs/free](https://render.com/docs/free) |
| 環境變數設定 | [render.com/docs/configure-environment-variables](https://render.com/docs/configure-environment-variables) |

### GitHub Actions
| 文件 | 連結 |
|---|---|
| Workflow 語法參考 | [docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions](https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions) |
| Secrets 設定方式 | [docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions) |
| Cron 排程語法 | [docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule](https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/events-that-trigger-workflows#schedule) |
| `actions/checkout` | [github.com/actions/checkout](https://github.com/actions/checkout) |
| `actions/setup-python` | [github.com/actions/setup-python](https://github.com/actions/setup-python) |

### FastMCP
| 文件 | 連結 |
|---|---|
| 官方文件 | [gofastmcp.com](https://gofastmcp.com) |
| GitHub | [github.com/jlowin/fastmcp](https://github.com/jlowin/fastmcp) |
| Model Context Protocol 規格 | [modelcontextprotocol.io](https://modelcontextprotocol.io) |
