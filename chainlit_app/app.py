import shutil
import sys
from pathlib import Path
from uuid import uuid4

import chainlit as cl

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from agent_core import Agent


APP_DIR = Path(__file__).resolve().parent
SESSION_PATH = APP_DIR / "session.jsonl"
UPLOADS_DIR = APP_DIR / ".files" / "uploads"


def save_uploaded_image(message: cl.Message) -> str | None:
    elements = getattr(message, "elements", None) or []
    for element in elements:
        mime = getattr(element, "mime", "") or ""
        source_path = getattr(element, "path", None)
        if not mime.startswith("image/") or not source_path:
            continue

        source = Path(source_path)
        if not source.is_file():
            continue

        UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
        suffix = source.suffix or ".png"
        target = UPLOADS_DIR / f"{uuid4().hex}{suffix}"
        shutil.copy2(source, target)
        return target.relative_to(project_root).as_posix()
    return None


@cl.on_chat_start
async def start():
    try:
        agent = Agent.from_env(session_path=str(SESSION_PATH))
        cl.user_session.set("agent", agent)
        await cl.Message(
            content=(
                "法鬥超人 Agent 已就緒。\n"
                "你可以直接輸入文字，也可以上傳一張圖片一起提問。"
            )
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"Agent 初始化失敗，請檢查 `.env` 與 API Key：{e}"
        ).send()


@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    if not agent:
        await cl.Message(content="找不到 Agent 實例，請重新整理頁面後再試一次。").send()
        return

    image_path = save_uploaded_image(message)
    msg = cl.Message(content="")

    def on_token_callback(token: str):
        cl.run_sync(msg.stream_token(token))

    try:
        final_text = await cl.make_async(agent.chat)(
            user_text=message.content,
            image_path=image_path,
            on_token=on_token_callback,
        )

        if not msg.content and final_text:
            msg.content = final_text

        if msg.streaming:
            await msg.update()
        else:
            await msg.send()
    except Exception as e:
        await cl.Message(content=f"執行過程中發生錯誤：{e}").send()
