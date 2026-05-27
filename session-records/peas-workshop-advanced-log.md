# PEAS Workshop Advanced Log

## WG-22 2a

- 日期：2026-05-27
- 題意摘要：將 WG-21 單檔 Agent 結構拆成 `agent_core.py` 與 `main.py`，並補齊執行所需資產。
- 專案現況：根目錄 `main.py` 原本為空檔，因此本輪採 reference-based 重建，再依 WG-22 邊界落成雙檔。
- 拆檔契約：
  - `agent_core.py`：承接 `Agent` 類別、tool、JSONL、token budget、memory consolidation、skills、vision 與 `Agent.chat(...)`。
  - `main.py`：只保留 CLI 入口、啟動訊息、輸入迴圈、`/image` 指令解析與 `Agent.from_env()` / `Agent.chat(...)` 呼叫。
- 額外處理：將 `references/project_assets/` 下的 `prompts/`、`templates/` 複製到專案根目錄，避免 memory merge 與 template 缺檔。
- 驗收結果：
  - [x] 已建立 `agent_core.py` 與新的 `main.py`
  - [x] 已補齊 `prompts/`、`templates/`
  - [x] `python -m py_compile agent_core.py main.py` 通過
  - [x] CLI 可啟動並正常顯示 WG-22 啟動訊息
- 調整紀錄：CLI 啟動時因 Windows `cp950` 編碼無法輸出 `≤` 而報錯，已改為 ASCII `<=`。
- 下一步：可接續 WG-22 2b/2c，針對 `Agent.chat`、CLI 指令流與驗收理解題做進一步教練。
