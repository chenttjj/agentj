# Architecture（僅供導覽 Agent 內部理解）

**禁止**整段貼給學生。學生問「為什麼」時最多摘 2 句白話。

## 資料流

```
使用者輸入 → agent_panel.render_chat_panel
  → _set_avatar_emotion("thinking")
  → agent.chat(..., on_token=...)
       → 首 token: talking
  → 結束: idle
  → _render_avatar_ui() 讀 data/avatar/{emotion}.gif
  → TTS（文字答完後 stream_tts_play）
```

## 邊界

- **不改** `peas-agent-core`：emotion 掛在 Shell 層 `agent_panel.py` 的 chat 包裝外。
- **Avatar 位置**：`render_chat_panel` 內，Agent 已連接、`_render_tts_settings_ui()` 之前。
- **素材路徑**：`SHELL_ROOT / "data" / "avatar"`（`--update` 保留 `data/`；勿用 `studio_shell/assets/`）。
- **session_state**：`avatar_emotion` ∈ {idle, thinking, talking, happy}。

## --update 風險

`agent-studio-installer --update` 會覆蓋根目錄 `agent_panel.py`；`data/`、`scripts/` 通常保留。Skill 定稿為直接改 `agent_panel.py`，更新 Shell 後需重做 Step 4。

## 與 vtuber-agent-guide 對照

| 指南概念 | 本 MVP |
|----------|--------|
| Emotion Event | `st.session_state["avatar_emotion"]` |
| 四狀態 GIF | Step 3 + Prompt A |
| TTS | 模板內建，無獨立步 |
| SOUL/USER/AGENTS | 不逐步帶；見 roadmap-future |
