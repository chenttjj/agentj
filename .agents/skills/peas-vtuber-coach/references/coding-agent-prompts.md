# Coding Agent Prompts（維護用；與 step-scripts 同步）

Step 3.5、4 的 `copy_paste_block` 須與本檔 **逐字一致**。修改時先改本檔，再同步 `step-scripts.md`。

---

## Prompt B（Step 3.5 · PNG → GIF）

```text
請在 Agent Studio 專案將四張 PNG 轉成 GIF，存放於 studio_shell/data/avatar/：

輸入（學生已放好）：
- studio_shell/data/avatar/_src/idle.png
- studio_shell/data/avatar/_src/thinking.png
- studio_shell/data/avatar/_src/talking.png
- studio_shell/data/avatar/_src/happy.png

輸出（請產生這四個檔）：
- studio_shell/data/avatar/idle.gif
- studio_shell/data/avatar/thinking.gif
- studio_shell/data/avatar/talking.gif
- studio_shell/data/avatar/happy.gif

做法：
1. 用 Python + Pillow 寫可執行腳本（例如 studio_shell/scripts/png_to_avatar_gif.py），或在本機一次性執行等效程式。
2. 每張 PNG 轉成「單格 GIF」（loop=0，可保留透明）。
3. 執行腳本後，確認上述四個 .gif 都存在。
4. 不要修改 peas-agent-core、app.py、page_shell.py。

完成後告訴我四個 gif 的完整路徑。
```

**備援（學生手動）**：若 coding agent 失敗，可到 https://ezgif.com/png-to-gif 逐張轉檔，檔名仍須為 idle.gif … happy.gif，放到 `studio_shell/data/avatar/`。

---

## Prompt A（Step 4 · emotion + 右欄 Avatar）

```text
請在 Agent Studio 專案的 studio_shell/agent_panel.py 加入 VTuber Avatar（PNGtuber 四狀態），要求如下：

1. 在 SHELL_ROOT 定義之後新增：
   - AVATAR_DIR = SHELL_ROOT / "data" / "avatar"
   - 合法 emotion：idle, thinking, talking, happy
   - def _set_avatar_emotion(emotion: str) -> None：寫入 st.session_state["avatar_emotion"]（非法值忽略）
   - def _render_avatar_ui() -> None：讀 AVATAR_DIR / f"{emotion}.gif"，用 st.image 顯示（寬度約 160）；缺檔時 st.info 提示缺少哪個檔名

2. 在 render_chat_panel 中，Agent Core 已連接、且呼叫 _render_tts_settings_ui 之前，插入 _render_avatar_ui()。

3. 在使用者送出問題、呼叫 agent.chat 的流程中：
   - agent.chat 之前：_set_avatar_emotion("thinking")
   - on_token 收到第一個非空 token 時：_set_avatar_emotion("talking")（用 nonlocal 或 list 旗標避免重複設定）
   - agent.chat 結束後（成功或 except 皆要）：_set_avatar_emotion("idle")
   - 若 st.session_state 尚無 avatar_emotion，初始化為 "idle"

4. 素材已放在 studio_shell/data/avatar/idle.gif、thinking.gif、talking.gif、happy.gif，請直接讀取，不要硬編碼其他路徑。

5. 不要修改 peas-agent-core、app.py、page_shell.py。只改 agent_panel.py。

6. 改完提醒使用者：在 Streamlit 按 Rerun，或重跑 uv run streamlit run studio_shell/app.py。

補充：日後若執行 agent-studio-installer --update，根目錄的 agent_panel.py 可能被覆蓋，屆時需重做本步或請老師更新 template。
```
