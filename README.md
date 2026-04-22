# AgentJ

這是一個基於 LangChain 和 OpenAI 的 AI 助手專案。

## 快速開始

### 1. 安裝依賴
建議使用 `uv` 或 `pip` 安裝：
```bash
# 使用 uv (推薦)
uv sync

# 或使用 pip
pip install -r requirements.txt  # 如果有產生的話
```

### 2. 設定環境變數
將 `.env.example` 複製並重新命名為 `.env`，然後填入您的 OpenAI API Key：
```bash
cp .env.example .env
```
在 `.env` 中修改：
```env
OPENAI_API_KEY=your_actual_key_here
```

### 3. 執行程式
```bash
python main.py
```

## 專案結構
- `main.py`: 主程式入口，初始化 AI 助手。
- `.env`: 存放敏感資訊（已加入 .gitignore）。
- `.env.example`: 環境變數範本。
- `.gitignore`: 忽略不必要的檔案。
