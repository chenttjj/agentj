# GIF 素材生圖指南（維護用）

與 `step-scripts.md` Step 3.1–3.4 的 `copy_paste_block` **保持逐字同步**。修改時先改本檔，再同步 step-scripts。

## 共通規則

- 工具：ChatGPT 或 Gemini **網頁／App**（學生 Step 3.0 已選）。
- `[角色描述]`：Step 3.1 定一句，3.2–3.4 **原句複製**。
- 存檔：`studio_shell/data/avatar/_src/{emotion}.png`
- 預設角色描述（學生說不出時）：短髮、戴髮夾的動漫少女，穿淺色校服，大眼睛

## idle

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：idle — 微笑、平靜、眼睛睜開
不要文字、不要 watermark、不要複數人物
```

## thinking

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：thinking — 微皺眉或看上方、像在思考
不要文字、不要 watermark、不要複數人物
```

## talking

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：talking — 嘴微張、像在說話
不要文字、不要 watermark、不要複數人物
```

## happy

```text
請生成一張 PNGtuber 用的半身頭像圖（正方形，適合做直播小頭像）。
風格：簡潔日系插畫，透明或純色背景。
角色外觀：[角色描述]
這張表情：happy — 開心大笑或燦爛微笑
不要文字、不要 watermark、不要複數人物
```

## 卡關（無老師 zip）

- 長不像同一人 → 重做 3.1，固定 `[角色描述]`。
- happy 做不出 → 複製 idle.png 為 happy.png 先通關。
