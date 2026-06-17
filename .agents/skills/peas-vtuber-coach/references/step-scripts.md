# Step Scripts（導覽 Agent 主檔）

**用法**：每則回覆學生前，讀取 **當前 `step_id` 整段**，只輸出「學生可見模板」。禁止合并下一步、禁止只寫「詳見某檔」而不貼全文。

**學生可見格式**（四段）：

```
步驟 M／6 · {title}
{purpose}
你要做的事：{student_action}
{copy_paste_block 若有則空一行後整段貼上}
完成後跟我說：「{completion_phrases 任一句}」
```

**用詞表**（Step 1 與全程必守）：

| 稱呼 | 指誰 |
|------|------|
| 導覽助手 | 現在跟你對話、帶步驟的我 |
| 改程式助手／coding agent | 幫你改專案檔的 AI（Cursor、Copilot、Claude Code 等皆可） |
| 聊天 Agent | 右欄「我的 Agent」裡會回你話的那個 |
| 生圖網站 | ChatGPT 或 Google Gemini 網頁／App |

---

## Step 1 · step_id: 1

**title**：認識路線

**purpose**：這條路線會讓右欄聊天 Agent 有臉（GIF 頭像）也有聲音（模板已內建語音）。我們分 6 大步：開 App → 做四張臉 → 轉 GIF → 接程式 → 試玩 → 驗收。每一步只做一件事。

**student_action**：若了解，回覆「開始」。

**copy_paste_block**：（無）

**completion_phrases**：開始｜好了開始｜可以開始

**if_stuck**：

- **A 問「要改 core 嗎？」** → 不用，只改 Agent Studio 專案裡的 `studio_shell/`，不動 `peas-agent-core`。
- **B 問「一定要用 Cursor 嗎？」** → 不用；生圖用 ChatGPT 或 Gemini 網頁，改程式用你平常的 coding agent 即可。

**agent_must_not**：不得貼 Prompt A/B；不得一次列出 Step 2–6 待辦

**學生可見模板**：

```
步驟 1／6 · 認識路線

這條路線會讓右欄聊天 Agent 有臉（GIF 頭像）也有聲音（App 裡已內建語音設定）。我們分 6 大步完成，每一步只做一件事。

你要做的事：若了解，回覆「開始」。

完成後跟我說：「開始」
```

---

## Step 2 · step_id: 2

**title**：開 App

**purpose**：先確認 Agent Studio 能跑、右欄能聊天。聊天 Agent 要能回答，需要 LLM 的 api_key。

**student_action**：

1. 在專案根目錄終端執行：`uv run streamlit run studio_shell/app.py`
2. 瀏覽器開啟後，看右欄「我的 Agent」
3. 若顯示未啟用，按 **「啟用 Agent」**（需已設定 `~/.peas-agent/config.json` 的 api_key）
4. 在右欄輸入一句話試聊，確認有文字回覆

**copy_paste_block**：

```bash
uv run streamlit run studio_shell/app.py
```

**completion_phrases**：App 好了｜可以聊天了｜有回覆了

**if_stuck**：

- **A 啟用 Agent 失敗** → 開 `~/.peas-agent/config.json` 確認 `api_key`；存檔後再按「啟用 Agent」。
- **B 找不到 uv** → 確認在 Agent Studio 專案根目錄。
- **C 想開語音** → 本步不要求；右欄「語音播放」可之後再開。

**agent_must_not**：不得要求做圖或改 `agent_panel.py`

**學生可見模板**：

```
步驟 2／6 · 開 App

先確認 App 能跑、右欄聊天 Agent 能回你話。

你要做的事：
1. 在專案根目錄終端執行下面指令
2. 瀏覽器開 App，看右欄「我的 Agent」
3. 若未啟用，按「啟用 Agent」（需 ~/.peas-agent/config.json 有 api_key）
4. 輸入一句話試聊，確認有文字回覆

uv run streamlit run studio_shell/app.py

完成後跟我說：「App 好了」
```

---

## Step 3.0 · step_id: 3.0

**title**：選生圖工具

**purpose**：接下來在**生圖網站**做四張頭像（不在 IDE 裡生圖）。先選 ChatGPT 或 Gemini，後面流程相同。

**student_action**：回覆「ChatGPT」或「Gemini」。

**completion_phrases**：ChatGPT｜Gemini｜用 ChatGPT｜用 Gemini

**if_stuck**：

- **A 沒帳號** → 用課堂允許的帳號或請老師協助。
- **B 想用 IDE 生圖** → 本課固定用 ChatGPT 或 Gemini 網頁。

**agent_internal_note**：記住學生選的工具，3.1–3.4 文案替換網站名稱。

**學生可見模板**：

```
步驟 3／6 · 選生圖工具

接下來在生圖網站做四張 PNG 頭像。先選一個你方便用的。

你要做的事：回覆「ChatGPT」或「Gemini」。

完成後跟我說：「ChatGPT」或「Gemini」
```

---

## Step 3.1 · step_id: 3.1

**title**：做 idle 臉

**purpose**：四張臉要同一角色。這步做 **idle（平靜微笑）** 並用一句話定長相。

**student_action**：描述角色 → 貼 idle prompt → 存 `studio_shell/data/avatar/_src/idle.png`

**預設角色描述**：短髮、戴髮夾的動漫少女，穿淺色校服，大眼睛

**copy_paste_block**：

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：idle — 微笑、平靜、眼睛睜開
不要文字、不要 watermark、不要複數人物
```

**completion_phrases**：idle 好了｜idle 存好了｜第一張好了

**if_stuck**：

- **A 不像同一人** → 後續 `[角色描述]` 必須與本步同一句。
- **B 不會建資料夾** → 建立 `studio_shell/data/avatar/_src/`。

**學生可見模板**：

```
步驟 3／6 · 做 idle 臉

四張臉要是同一角色。這一步做 idle（平靜微笑）。

你要做的事：
1. 用一句話描述角色（可改：短髮、戴髮夾的動漫少女，穿淺色校服，大眼睛）
2. 開生圖網站，貼下面 prompt，把 [角色描述] 換成你的句子
3. 下載 PNG，存到 studio_shell/data/avatar/_src/idle.png

請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：idle — 微笑、平靜、眼睛睜開
不要文字、不要 watermark、不要複數人物

完成後跟我說：「idle 好了」
```

---

## Step 3.2 · step_id: 3.2

**title**：做 thinking 臉

**copy_paste_block**：

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：thinking — 微皺眉或看上方、像在思考
不要文字、不要 watermark、不要複數人物
```

**student_action**：貼 prompt（`[角色描述]` 與 3.1 同句）→ 存 `_src/thinking.png`

**completion_phrases**：thinking 好了｜第二張好了

**if_stuck**：**A 長相跑掉** → `[角色描述]` 原封不動沿用 3.1 那句。

**學生可見模板**：

```
步驟 3／6 · 做 thinking 臉

同一角色，thinking（思考中）。

你要做的事：貼下面 prompt（[角色描述] 與 idle 同一句），存成 studio_shell/data/avatar/_src/thinking.png

請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：thinking — 微皺眉或看上方、像在思考
不要文字、不要 watermark、不要複數人物

完成後跟我說：「thinking 好了」
```

---

## Step 3.3 · step_id: 3.3

**title**：做 talking 臉

**copy_paste_block**：

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：talking — 嘴微張、像在說話
不要文字、不要 watermark、不要複數人物
```

**student_action**：存 `_src/talking.png`

**completion_phrases**：talking 好了｜第三張好了

**學生可見模板**：

```
步驟 3／6 · 做 talking 臉

同一角色，talking（說話中）。

你要做的事：貼下面 prompt，存成 studio_shell/data/avatar/_src/talking.png

請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：talking — 嘴微張、像在說話
不要文字、不要 watermark、不要複數人物

完成後跟我說：「talking 好了」
```

---

## Step 3.4 · step_id: 3.4

**title**：做 happy 臉

**copy_paste_block**：

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：happy — 開心大笑或燦爛微笑
不要文字、不要 watermark、不要複數人物
```

**student_action**：存 `_src/happy.png`（可先複製 idle 另存通關）

**completion_phrases**：happy 好了｜四張圖放好了

**if_stuck**：**A 做不出 happy** → 複製 idle.png 為 happy.png 先通關。

**學生可見模板**：

```
步驟 3／6 · 做 happy 臉

同一角色，happy（開心）。可先和 idle 很像，但檔案要有。

你要做的事：存成 studio_shell/data/avatar/_src/happy.png

請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：happy — 開心大笑或燦爛微笑
不要文字、不要 watermark、不要複數人物

完成後跟我說：「四張圖放好了」
```

---

## Step 3.5 · step_id: 3.5

**title**：轉 GIF

**purpose**：App 讀 `.gif`。改程式助手轉檔；**轉好後 App 還不會顯示臉**，下一步才接程式。

**student_action**：貼 **Prompt B 全文** 給 coding agent

**copy_paste_block**：

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

**completion_phrases**：gif 好了｜四個 gif 都有了｜轉好了

**if_stuck**：

- **A coding agent 失敗** → https://ezgif.com/png-to-gif 手動轉，放到 `studio_shell/data/avatar/`。
- **B 問為何沒臉** → 正常，下一步 Step 4 才接 UI。

**agent_must_not**：不得同時貼 Prompt A

**學生可見模板**：

```
步驟 3／6 · 轉 GIF

請改程式助手把 PNG 轉成 data/avatar/ 底下四個 gif。轉好後 App 還不會顯示臉。

你要做的事：複製下面整段貼給 coding agent。

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

完成後跟我說：「gif 好了」
```

---

## Step 4 · step_id: 4

**title**：接程式

**purpose**：右欄「語音播放」**上方**顯示 GIF；聊天時 idle → thinking → talking → idle。

**student_action**：貼 Prompt A → Rerun → 確認有頭像

**copy_paste_block**：

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
   - on_token 收到第一個非空 token 時：_set_avatar_emotion("talking")
   - agent.chat 結束後（成功或 except 皆要）：_set_avatar_emotion("idle")
   - 若 st.session_state 尚無 avatar_emotion，初始化為 "idle"

4. 素材已放在 studio_shell/data/avatar/idle.gif、thinking.gif、talking.gif、happy.gif，請直接讀取，不要硬編碼其他路徑。

5. 不要修改 peas-agent-core、app.py、page_shell.py。只改 agent_panel.py。

6. 改完提醒使用者：在 Streamlit 按 Rerun，或重跑 uv run streamlit run studio_shell/app.py。

補充：日後若執行 agent-studio-installer --update，根目錄的 agent_panel.py 可能被覆蓋，屆時需重做本步或請老師更新 template。
```

**completion_phrases**：rerun 後右欄看得到臉｜看到頭像了｜有臉了

**if_stuck**：

- **A 沒臉** → Rerun；檢查 gif 路徑與 `_render_avatar_ui` 在 `_render_tts_settings_ui` 之前。
- **B --update** → 可能覆蓋 `agent_panel.py`，需重做本步。

**學生可見模板**：

```
步驟 4／6 · 接程式

在右欄「語音播放」上方顯示 GIF，聊天時切換表情。

你要做的事：
1. 複製下面整段貼給 coding agent
2. Streamlit Rerun
3. 確認右欄語音設定上方有頭像

請在 Agent Studio 專案的 studio_shell/agent_panel.py 加入 VTuber Avatar（PNGtuber 四狀態），要求如下：

1. 在 SHELL_ROOT 定義之後新增：
   - AVATAR_DIR = SHELL_ROOT / "data" / "avatar"
   - 合法 emotion：idle, thinking, talking, happy
   - def _set_avatar_emotion(emotion: str) -> None：寫入 st.session_state["avatar_emotion"]（非法值忽略）
   - def _render_avatar_ui() -> None：讀 AVATAR_DIR / f"{emotion}.gif"，用 st.image 顯示（寬度約 160）；缺檔時 st.info 提示缺少哪個檔名

2. 在 render_chat_panel 中，Agent Core 已連接、且呼叫 _render_tts_settings_ui 之前，插入 _render_avatar_ui()。

3. 在使用者送出問題、呼叫 agent.chat 的流程中：
   - agent.chat 之前：_set_avatar_emotion("thinking")
   - on_token 收到第一個非空 token 時：_set_avatar_emotion("talking")
   - agent.chat 結束後（成功或 except 皆要）：_set_avatar_emotion("idle")
   - 若 st.session_state 尚無 avatar_emotion，初始化為 "idle"

4. 素材已放在 studio_shell/data/avatar/idle.gif、thinking.gif、talking.gif、happy.gif，請直接讀取，不要硬編碼其他路徑。

5. 不要修改 peas-agent-core、app.py、page_shell.py。只改 agent_panel.py。

6. 改完提醒使用者：在 Streamlit 按 Rerun，或重跑 uv run streamlit run studio_shell/app.py。

補充：日後若執行 agent-studio-installer --update，根目錄的 agent_panel.py 可能被覆蓋，屆時需重做本步或請老師更新 template。

完成後跟我說：「rerun 後右欄看得到臉」
```

---

## Step 5 · step_id: 5

**title**：試 VTuber

**purpose**：確認臉、聲音、狀態。語音在**文字答完後**才播，臉可能先回 idle，正常。

**student_action**：開「語音播放」+ tts.json → 問需思考較久的問題 → 觀察 thinking/talking

**completion_phrases**：有 thinking 和 talking｜有看到換表情｜試過了

**if_stuck**：

- **A 換太快** → 再問更長問題；曾閃過即算。
- **B 沒聲音** → 檢查 `~/.peas-agent/tts.json` 的 api_key。

**學生可見模板**：

```
步驟 5／6 · 試 VTuber

確認臉、聲音、狀態。語音答完才播，臉可能先回 idle，正常。

你要做的事：
1. 右欄「語音播放」啟用；沒聲音就設 ~/.peas-agent/tts.json 的 api_key
2. 問一個要想幾秒的問題
3. 看頭像有沒有 thinking 或 talking

完成後跟我說：「有 thinking 和 talking」
```

---

## Step 6 · step_id: 6

**title**：驗收

**purpose**：逐項確認 MVP；**一次只問一條**。

**驗收問句（依序）**：

1. App 能跑嗎？
2. 右欄 TTS 上方看見 Avatar 嗎？
3. 四個 gif 都在 `studio_shell/data/avatar/` 嗎？
4. 未聊天時是 idle 嗎？
5. 送出問題後有 thinking 或 talking 嗎？
6. 開語音時答完聽得到聲音嗎？
7. 沒有改 `peas-agent-core` 嗎？

**completion_phrases**：全部 OK｜都好了｜驗收完成

**if_stuck**：某一項「還沒」→ 只回對應 Step（缺 gif→3.5；沒臉→4；沒聲→5）

**agent_must_not**：不得一次列出 7 條讓學生填表

**學生可見模板（首次）**：

```
步驟 6／6 · 驗收

逐項確認，一次一項。

你要做的事：App 能跑嗎？回「OK」或「還沒」。

（後續則依驗收問句 2–7 逐條進行；全部 OK 後請學生說「全部 OK」）
```

---

## 步驟順序速查

| step_id | 下一 step_id | 完成句範例 |
|---------|--------------|------------|
| 1 | 2 | 開始 |
| 2 | 3.0 | App 好了 |
| 3.0 | 3.1 | ChatGPT / Gemini |
| 3.1 | 3.2 | idle 好了 |
| 3.2 | 3.3 | thinking 好了 |
| 3.3 | 3.4 | talking 好了 |
| 3.4 | 3.5 | 四張圖放好了 |
| 3.5 | 4 | gif 好了 |
| 4 | 5 | rerun 後右欄看得到臉 |
| 5 | 6 | 有 thinking 和 talking |
| 6 | 結束 | 全部 OK |
