# 選修：Agent 主動切 happy

**時機**：Step 6 全部 OK 後，學生有興趣再提。

## 概念

MVP 只在 chat 流程切 idle / thinking / talking。選修可讓聊天 Agent 在適當時機（例如稱讚學生）把 `avatar_emotion` 設為 `happy`，數秒後回到 `idle`。

## 給 coding agent 的提示方向（非逐步劇本）

- 在 `agent_panel.py` 或 agent workspace 工具回傳後，呼叫 `_set_avatar_emotion("happy")`。
- 需定義「何時 happy」（例如 assistant 回覆含特定鼓勵句、或 tool 成功）。
- `happy.gif` 已存在於 `data/avatar/`（Step 3 產出）。

本選修**不**納入 Step 6 驗收。
