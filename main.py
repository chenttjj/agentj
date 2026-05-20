from __future__ import annotations

import base64
import copy
import json
import os
import platform
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage, message_chunk_to_message
from langchain_core.tools import BaseTool, tool
from langchain_openai import ChatOpenAI


PROJECT_ROOT = Path(__file__).resolve().parent
SESSION_JSONL_PATH = PROJECT_ROOT / os.getenv("SESSION_JSONL_PATH", "session.jsonl")
MEMORY_DIR = PROJECT_ROOT / "memory"
MEMORY_PATH = MEMORY_DIR / "MEMORY.md"
MEMORY_HISTORY_PATH = MEMORY_DIR / "HISTORY.md"
BUILTIN_SKILLS_DIR = PROJECT_ROOT / ".agents" / "skills"

TOKEN_BUDGET = int(os.getenv("TOKEN_BUDGET", "30000"))
MEMORY_MAX_CHARS = int(os.getenv("MEMORY_MAX_CHARS", "6000"))
TOOL_OUTPUT_MAX_CHARS = int(os.getenv("TOOL_OUTPUT_MAX_CHARS", "4000"))
CONSOLIDATION_MAX_RETRIES = int(os.getenv("CONSOLIDATION_MAX_RETRIES", "2"))


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


# WG-12: system prompt identity and runtime notes.
def _runtime_env_note() -> str:
    system = platform.system()
    if os.name == "nt":
        shell_note = "目前是 Windows，exec 工具請使用單行 PowerShell 指令；不要假設 Bash，也不要使用 heredoc。"
    else:
        shell_note = "目前不是 Windows，exec 工具仍請使用單行、可攜的 shell 指令。"
    return f"【執行環境】platform.system()={system}, os.name={os.name}。{shell_note}"


def get_identity() -> str:
    return "\n".join(
        [
            "你是本課堂的 AgentJ，請使用繁體中文回覆，務必務實、精準、可驗收。",
            "【本場次顯示名稱】法鬥超人",
            _runtime_env_note(),
            "【exec 注意】請依執行環境選擇 shell 寫法。需要執行多行 Python 時，先用 write_file 寫成檔案，再用 exec 執行 `uv run python 相對路徑`。",
            "【工具規則】凡涉及檔案讀寫、列目錄、文字替換、shell 執行、或可由工具精準完成的計算，都應優先呼叫工具，不要只靠猜測。",
        ]
    )


# WG-14: workspace-safe file and exec tools.
def resolve_workspace_path(path: str) -> Path:
    candidate = (PROJECT_ROOT / path).resolve()
    try:
        candidate.relative_to(PROJECT_ROOT)
    except ValueError as exc:
        raise ValueError(f"path escapes workspace: {path}") from exc
    return candidate


@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers. Use this tool for arithmetic instead of mental math."""
    return a + b


@tool("read_file")
def read_file_tool(path: str, offset: int = 1, limit: int = 200) -> str:
    """Read a UTF-8 text file in the workspace by line range."""
    target = resolve_workspace_path(path)
    if not target.is_file():
        return f"[error] not a file: {path}"
    lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
    start = max(offset, 1) - 1
    end = min(start + max(limit, 1), len(lines))
    return "\n".join(f"{idx + 1}: {line}" for idx, line in enumerate(lines[start:end], start=start))


@tool("write_file")
def write_file_tool(path: str, content: str) -> str:
    """Write UTF-8 text to a workspace file, creating parent folders if needed."""
    target = resolve_workspace_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return f"[ok] wrote {path} ({len(content)} chars)"


@tool("edit_file")
def edit_file_tool(path: str, old_text: str, new_text: str, replace_all: bool = False) -> str:
    """Replace text in a workspace UTF-8 file."""
    target = resolve_workspace_path(path)
    if not target.is_file():
        return f"[error] not a file: {path}"
    text = target.read_text(encoding="utf-8", errors="replace")
    if old_text not in text:
        return "[error] old_text not found"
    count = text.count(old_text) if replace_all else 1
    updated = text.replace(old_text, new_text, -1 if replace_all else 1)
    target.write_text(updated, encoding="utf-8")
    return f"[ok] replaced {count} occurrence(s) in {path}"


@tool("list_dir")
def list_dir_tool(path: str = ".", recursive: bool = False, max_entries: int = 200) -> str:
    """List workspace directory entries."""
    target = resolve_workspace_path(path)
    if not target.is_dir():
        return f"[error] not a directory: {path}"
    iterator = target.rglob("*") if recursive else target.iterdir()
    rows: list[str] = []
    for entry in iterator:
        if len(rows) >= max_entries:
            rows.append(f"... truncated at {max_entries} entries")
            break
        rel = entry.relative_to(PROJECT_ROOT)
        suffix = "/" if entry.is_dir() else ""
        rows.append(f"{rel.as_posix()}{suffix}")
    return "\n".join(rows) if rows else "[empty]"


@tool("exec")
def exec_workspace_tool(command: str, timeout: int = 30) -> str:
    """Run one single-line shell command in the workspace and return exit code, stdout, and stderr."""
    if "\n" in command or "\r" in command:
        return "[error] exec only accepts a single-line command"
    timeout = min(max(int(timeout), 1), 120)
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
    )
    out = completed.stdout.strip()
    err = completed.stderr.strip()
    body = f"exit_code={completed.returncode}\nstdout:\n{out}\nstderr:\n{err}"
    return truncate_text(body, TOOL_OUTPUT_MAX_CHARS)


TOOLS: list[BaseTool] = [
    add_numbers,
    read_file_tool,
    write_file_tool,
    edit_file_tool,
    list_dir_tool,
    exec_workspace_tool,
]
TOOLS_BY_NAME = {t.name: t for t in TOOLS}


# WG-20: lightweight parameter schema, casting, and validation before invoke.
TOOL_PARAMETERS: dict[str, dict[str, Any]] = {
    "add_numbers": {
        "type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        "required": ["a", "b"],
    },
    "read_file": {
        "type": "object",
        "properties": {"path": {"type": "string"}, "offset": {"type": "integer"}, "limit": {"type": "integer"}},
        "required": ["path"],
    },
    "write_file": {
        "type": "object",
        "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
        "required": ["path", "content"],
    },
    "edit_file": {
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "old_text": {"type": "string"},
            "new_text": {"type": "string"},
            "replace_all": {"type": "boolean"},
        },
        "required": ["path", "old_text", "new_text"],
    },
    "list_dir": {
        "type": "object",
        "properties": {"path": {"type": "string"}, "recursive": {"type": "boolean"}, "max_entries": {"type": "integer"}},
        "required": [],
    },
    "exec": {
        "type": "object",
        "properties": {"command": {"type": "string"}, "timeout": {"type": "integer"}},
        "required": ["command"],
    },
}


def cast_value(value: Any, schema_type: str) -> Any:
    if schema_type == "integer" and isinstance(value, str):
        return int(value)
    if schema_type == "number" and isinstance(value, str):
        return float(value)
    if schema_type == "boolean" and isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    if schema_type == "string" and not isinstance(value, str):
        return str(value)
    return value


def cast_params(params: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    casted = dict(params)
    for name, prop in schema.get("properties", {}).items():
        if name in casted and "type" in prop:
            casted[name] = cast_value(casted[name], prop["type"])
    return casted


def validate_params(params: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for required in schema.get("required", []):
        if required not in params:
            errors.append(f"missing required parameter: {required}")
    for name, value in params.items():
        expected = schema.get("properties", {}).get(name, {}).get("type")
        if not expected:
            continue
        ok = (
            (expected == "string" and isinstance(value, str))
            or (expected == "integer" and isinstance(value, int) and not isinstance(value, bool))
            or (expected == "number" and isinstance(value, (int, float)) and not isinstance(value, bool))
            or (expected == "boolean" and isinstance(value, bool))
        )
        if not ok:
            errors.append(f"{name} must be {expected}")
    return errors


def prepare_tool_call(tool_call: dict[str, Any]) -> tuple[BaseTool | None, dict[str, Any], str | None]:
    name = tool_call.get("name")
    tool_obj = TOOLS_BY_NAME.get(name)
    if tool_obj is None:
        return None, {}, f"unknown tool: {name}"
    params = tool_call.get("args") or {}
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            return tool_obj, {}, f"tool args are not valid JSON: {params}"
    schema = TOOL_PARAMETERS.get(name, {"type": "object", "properties": {}, "required": []})
    try:
        casted = cast_params(dict(params), schema)
    except (TypeError, ValueError) as exc:
        return tool_obj, {}, f"parameter cast failed: {exc}"
    errors = validate_params(casted, schema)
    if errors:
        return tool_obj, casted, "; ".join(errors)
    return tool_obj, casted, None


# WG-15/WG-16: JSONL persistence.
def content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        return "\n".join(p for p in parts if p).strip()
    return str(content)


def message_to_row(message: BaseMessage) -> dict[str, Any] | None:
    base: dict[str, Any] = {"timestamp": now_iso()}
    if isinstance(message, HumanMessage):
        row = {**base, "role": "user", "content": content_to_text(message.content)}
        image_path = message.additional_kwargs.get("image_path")
        media_type = message.additional_kwargs.get("media_type")
        if image_path:
            row["image_path"] = image_path
        if media_type:
            row["media_type"] = media_type
        return row
    if isinstance(message, AIMessage):
        row = {**base, "role": "assistant", "content": content_to_text(message.content)}
        tool_calls = getattr(message, "tool_calls", None) or message.additional_kwargs.get("tool_calls")
        if tool_calls:
            row["tool_calls"] = tool_calls
        return row
    if isinstance(message, ToolMessage):
        return {
            **base,
            "role": "tool",
            "content": content_to_text(message.content),
            "tool_call_id": message.tool_call_id,
            "name": getattr(message, "name", None),
        }
    return None


def load_user_row_to_history_human(row: dict[str, Any]) -> HumanMessage:
    text = str(row.get("content", ""))
    image_rel = row.get("image_path")
    if not image_rel:
        return HumanMessage(content=text)
    media_type = row.get("media_type")
    placeholder = f"[此回合曾附圖，路徑：{image_rel}]"
    if media_type:
        placeholder += f" [media_type={media_type}]"
    return HumanMessage(content=f"{text}\n\n{placeholder}".strip())


def load_session_jsonl(path: Path) -> tuple[dict[str, Any], list[BaseMessage]]:
    if not path.exists():
        return {"created_at": now_iso(), "last_consolidated": 0}, []
    metadata: dict[str, Any] = {"created_at": now_iso(), "last_consolidated": 0}
    history: list[BaseMessage] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError:
                print(f"[warn] skip bad JSONL line {line_no}")
                continue
            role = row.get("role")
            if role == "metadata":
                metadata.update(row)
            elif role == "user":
                history.append(load_user_row_to_history_human(row))
            elif role == "assistant":
                kwargs = {}
                if row.get("tool_calls"):
                    kwargs["tool_calls"] = row["tool_calls"]
                history.append(AIMessage(content=row.get("content", ""), additional_kwargs=kwargs, tool_calls=row.get("tool_calls", [])))
            elif role == "tool":
                tool_call_id = row.get("tool_call_id")
                if not tool_call_id:
                    print(f"[warn] skip tool line without tool_call_id at {line_no}")
                    continue
                history.append(ToolMessage(content=row.get("content", ""), tool_call_id=tool_call_id, name=row.get("name")))
    return metadata, history


def save_session_jsonl(path: Path, history: list[BaseMessage], metadata: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {"role": "metadata", **metadata, "updated_at": now_iso()}
    with path.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for message in history:
            row = message_to_row(message)
            if row is not None:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")


# WG-17/WG-18: budget estimation, safe transcript cleanup, and context shaping.
def truncate_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 80] + f"\n...[truncated {len(text) - max_chars + 80} chars]"


def estimate_message_tokens(message: BaseMessage) -> int:
    cost = len(content_to_text(message.content))
    if isinstance(message, AIMessage):
        cost += len(json.dumps(getattr(message, "tool_calls", []) or [], ensure_ascii=False))
    if isinstance(message, ToolMessage):
        cost += 80
    return cost


def message_cost(messages: list[BaseMessage]) -> int:
    return sum(estimate_message_tokens(message) for message in messages)


def pick_consolidation_boundary(
    history: list[BaseMessage],
    last_consolidated: int,
    tokens_to_remove: int,
) -> int | None:
    if tokens_to_remove <= 0:
        return None
    running = 0
    candidate: int | None = None
    for index in range(last_consolidated, len(history)):
        msg = history[index]
        running += estimate_message_tokens(msg)
        next_is_user = index + 1 < len(history) and isinstance(history[index + 1], HumanMessage)
        if next_is_user and running >= tokens_to_remove:
            candidate = index + 1
            break
    return candidate


def _tool_call_ids(message: AIMessage) -> set[str]:
    ids: set[str] = set()
    for call in getattr(message, "tool_calls", []) or []:
        call_id = call.get("id")
        if call_id:
            ids.add(call_id)
    for call in message.additional_kwargs.get("tool_calls", []) or []:
        if isinstance(call, dict):
            call_id = call.get("id")
            if call_id:
                ids.add(call_id)
    return ids


def _human_to_text_only_placeholder(message: HumanMessage) -> HumanMessage:
    if isinstance(message.content, str):
        return message
    text = content_to_text(message.content) or "[此回合包含圖片，歷史送模時僅保留文字占位]"
    return HumanMessage(content=f"{text}\n\n[歷史圖片未重新送入模型]")


def clean_history_for_model(history: list[BaseMessage]) -> list[BaseMessage]:
    cleaned: list[BaseMessage] = []
    pending_tool_ids: set[str] = set()
    for original in history:
        msg = copy.deepcopy(original)
        if isinstance(msg, HumanMessage):
            cleaned.append(_human_to_text_only_placeholder(msg))
            pending_tool_ids.clear()
        elif isinstance(msg, AIMessage):
            cleaned.append(msg)
            pending_tool_ids = _tool_call_ids(msg)
        elif isinstance(msg, ToolMessage):
            if msg.tool_call_id not in pending_tool_ids:
                continue
            content = content_to_text(msg.content)
            if len(content) > TOOL_OUTPUT_MAX_CHARS:
                msg = ToolMessage(
                    content=truncate_text(content, TOOL_OUTPUT_MAX_CHARS),
                    tool_call_id=msg.tool_call_id,
                    name=getattr(msg, "name", None),
                )
            cleaned.append(msg)
            pending_tool_ids.discard(msg.tool_call_id)
    return cleaned


def build_messages_for_model(
    system_message: SystemMessage,
    past: list[BaseMessage],
    human_message: HumanMessage,
    max_chars: int = TOKEN_BUDGET,
) -> list[BaseMessage]:
    cleaned_past = clean_history_for_model(past)
    out: list[BaseMessage] = [copy.deepcopy(system_message), *cleaned_past, copy.deepcopy(human_message)]
    while message_cost(out) > max_chars and cleaned_past:
        first_user = next((i for i, m in enumerate(cleaned_past) if isinstance(m, HumanMessage)), None)
        if first_user is None:
            cleaned_past.pop(0)
        else:
            next_user = next((i for i in range(first_user + 1, len(cleaned_past)) if isinstance(cleaned_past[i], HumanMessage)), None)
            del cleaned_past[first_user : next_user or len(cleaned_past)]
        out = [copy.deepcopy(system_message), *cleaned_past, copy.deepcopy(human_message)]
    return out


# WG-19: long-term memory.
def memory_block_for_system() -> str:
    if not MEMORY_PATH.exists():
        return ""
    text = MEMORY_PATH.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return ""
    if len(text) > MEMORY_MAX_CHARS:
        text = text[-MEMORY_MAX_CHARS:]
    return f"## Long-term Memory\n\n{text}"


def append_memory_history(entry: str) -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    compact = " ".join(entry.split())
    with MEMORY_HISTORY_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {compact}\n")


def summarize_messages(messages: list[BaseMessage]) -> str:
    rows: list[str] = []
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant" if isinstance(msg, AIMessage) else "tool"
        rows.append(f"{role}: {truncate_text(content_to_text(msg.content), 1200)}")
    return "\n".join(rows)


def parse_consolidation_response(text: str, fallback_memory: str) -> tuple[str, str]:
    try:
        parsed = json.loads(text)
        history_entry = str(parsed.get("history_entry", "")).strip()
        memory_update = str(parsed.get("memory_update", "")).strip()
        if history_entry and memory_update:
            return history_entry, memory_update
    except json.JSONDecodeError:
        pass
    compact = " ".join(text.split())
    return compact[:500] or "[CONSOLIDATION-EMPTY]", fallback_memory


def consolidate_memory_if_needed(
    llm: ChatOpenAI,
    system_text: str,
    history: list[BaseMessage],
    human_message: HumanMessage,
    metadata: dict[str, Any],
) -> tuple[list[BaseMessage], dict[str, Any]]:
    last = int(metadata.get("last_consolidated", 0) or 0)
    past = history[last:]
    cost = len(system_text) + message_cost(past + [human_message])
    if cost <= TOKEN_BUDGET:
        return past, metadata

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    current_memory = MEMORY_PATH.read_text(encoding="utf-8", errors="replace") if MEMORY_PATH.exists() else ""

    while len(system_text) + message_cost(past + [human_message]) > TOKEN_BUDGET // 2:
        tokens_to_remove = max(0, len(system_text) + message_cost(past + [human_message]) - TOKEN_BUDGET // 2)
        boundary = pick_consolidation_boundary(history, last, tokens_to_remove)
        if boundary is None or boundary <= last:
            break
        chunk = history[last:boundary]
        prompt = (
            "請把以下舊對話濃縮為長期記憶。只回 JSON 物件，鍵為 history_entry 與 memory_update。\n"
            "memory_update 必須是完整取代 MEMORY.md 的 Markdown，保留未來仍需要的決策、狀態與偏好，不要逐字抄 tool 輸出。\n\n"
            f"現有 MEMORY.md:\n{current_memory}\n\n待整併 chunk:\n{summarize_messages(chunk)}"
        )
        ok = False
        for _ in range(CONSOLIDATION_MAX_RETRIES):
            response = llm.invoke([SystemMessage(content=get_identity()), HumanMessage(content=prompt)])
            history_entry, memory_update = parse_consolidation_response(content_to_text(response.content), current_memory)
            if history_entry and memory_update:
                append_memory_history(history_entry)
                MEMORY_PATH.write_text(memory_update, encoding="utf-8")
                current_memory = memory_update
                metadata["last_consolidated"] = boundary
                last = boundary
                past = history[last:]
                ok = True
                break
        if not ok:
            append_memory_history("[CONSOLIDATION-FAILED] unable to parse model response")
            break
        system_text = build_system_prompt(SkillsLoader(PROJECT_ROOT, BUILTIN_SKILLS_DIR))
    return past, metadata


# WG-20: skills loading and system prompt injection.
@dataclass
class SkillEntry:
    name: str
    path: Path
    source: str
    description: str
    always: bool
    body: str


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text
    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    body = "\n".join(lines[end + 1 :]).strip()
    return meta, body


class SkillsLoader:
    def __init__(self, workspace: Path, builtin_skills_dir: Path) -> None:
        self.workspace_skills = workspace / "skills"
        self.builtin_skills = builtin_skills_dir

    def _entries_from_dir(self, root: Path, source: str, skip: set[str]) -> list[SkillEntry]:
        if not root.exists():
            return []
        entries: list[SkillEntry] = []
        for skill_dir in sorted(root.iterdir()):
            skill_file = skill_dir / "SKILL.md"
            if not skill_dir.is_dir() or not skill_file.exists() or skill_dir.name in skip:
                continue
            text = skill_file.read_text(encoding="utf-8", errors="replace")
            meta, body = split_frontmatter(text)
            entries.append(
                SkillEntry(
                    name=skill_dir.name,
                    path=skill_file,
                    source=source,
                    description=meta.get("description") or skill_dir.name,
                    always=meta.get("always", "false").lower() == "true",
                    body=body,
                )
            )
        return entries

    def list_skills(self) -> list[SkillEntry]:
        workspace_entries = self._entries_from_dir(self.workspace_skills, "workspace", set())
        workspace_names = {entry.name for entry in workspace_entries}
        builtin_entries = self._entries_from_dir(self.builtin_skills, "builtin", workspace_names)
        return workspace_entries + builtin_entries

    def load_skill(self, name: str) -> str | None:
        for root in (self.workspace_skills, self.builtin_skills):
            path = root / name / "SKILL.md"
            if path.exists():
                return path.read_text(encoding="utf-8", errors="replace")
        return None


def build_skills_summary(entries: list[SkillEntry]) -> str:
    summarized = [entry for entry in entries if not entry.always]
    if not summarized:
        return ""
    return "\n".join(f"- **{entry.name}**：{entry.description} `{entry.path}`" for entry in summarized)


def build_system_prompt(loader: SkillsLoader) -> str:
    parts: list[str] = [get_identity()]
    memory = memory_block_for_system()
    if memory:
        parts.append(memory)
    entries = loader.list_skills()
    active = [entry for entry in entries if entry.always]
    if active:
        active_body = "\n\n---\n\n".join(f"### Skill: {entry.name}\n\n{entry.body}" for entry in active)
        parts.append(f"# Active Skills\n\n{active_body}")
    summary = build_skills_summary(entries)
    if summary:
        intro = (
            "以下技能可在需要時使用。若任務符合某技能，先用 read_file 讀取該路徑的 SKILL.md，"
            "再依其中流程操作；若技能需要額外依賴，請先說明並使用工具檢查環境。\n\n"
        )
        parts.append("# Skills\n\n" + intro + summary)
    return "\n\n---\n\n".join(parts)


# WG-21: current-turn image support, JSONL path-only persistence.
def image_bytes_to_data_url(data: bytes, media_type: str) -> str:
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{media_type};base64,{encoded}"


def guess_media_type(path: Path, fallback: str = "image/png") -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".webp":
        return "image/webp"
    if ext == ".gif":
        return "image/gif"
    return fallback


def parse_user_input(raw: str) -> tuple[str, Path | None]:
    if not raw.startswith("/image "):
        return raw, None
    rest = raw[len("/image ") :].strip()
    if not rest:
        return "", None
    first, _, tail = rest.partition(" ")
    text = tail.strip() or input("請輸入這張圖片要問的問題：").strip()
    return text, Path(first)


def build_human_messages_for_turn(text: str, image_rel: Path | None) -> tuple[HumanMessage, HumanMessage]:
    if image_rel is None:
        plain = HumanMessage(content=text)
        return plain, plain
    full = resolve_workspace_path(image_rel.as_posix())
    media_type = guess_media_type(full)
    if not full.is_file():
        print(f"[warn] 找不到圖片，改以純文字送出：{image_rel}")
        plain = HumanMessage(content=text)
        return plain, plain
    data_url = image_bytes_to_data_url(full.read_bytes(), media_type)
    model_message = HumanMessage(
        content=[
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": data_url}},
        ]
    )
    persisted_message = HumanMessage(
        content=text,
        additional_kwargs={"image_path": image_rel.as_posix(), "media_type": media_type},
    )
    return model_message, persisted_message


# WG-13/WG-14/WG-10: ReAct with streamed assistant output.
def merge_ai_chunks(chunks: list[Any]) -> AIMessage:
    message = None
    for chunk in chunks:
        message = chunk if message is None else message + chunk
    if message is None:
        return AIMessage(content="")
    merged = message_chunk_to_message(message)
    if isinstance(merged, AIMessage):
        return merged
    return AIMessage(content=content_to_text(merged.content))


def run_react_turn(
    llm_with_tools: Any,
    system_message: SystemMessage,
    past: list[BaseMessage],
    model_human_message: HumanMessage,
) -> list[BaseMessage]:
    produced: list[BaseMessage] = []
    context_messages = build_messages_for_model(system_message, past, model_human_message)
    while True:
        chunks: list[Any] = []
        for chunk in llm_with_tools.stream(context_messages):
            chunks.append(chunk)
            text = getattr(chunk, "content", "")
            if isinstance(text, str) and text:
                print(text, end="", flush=True)
        ai_message = merge_ai_chunks(chunks)
        print()
        produced.append(ai_message)
        context_messages.append(ai_message)
        tool_calls = getattr(ai_message, "tool_calls", []) or []
        if not tool_calls:
            break
        for tool_call in tool_calls:
            tool_obj, params, error = prepare_tool_call(tool_call)
            call_id = tool_call.get("id", f"tool-{len(produced)}")
            if error or tool_obj is None:
                result = f"[tool-error] {error}"
            else:
                try:
                    result = tool_obj.invoke(params)
                except Exception as exc:
                    result = f"[tool-error] {type(exc).__name__}: {exc}"
            tool_message = ToolMessage(content=str(result), tool_call_id=call_id, name=tool_call.get("name"))
            produced.append(tool_message)
            context_messages.append(tool_message)
    return produced


def main() -> None:
    # WG-01 to WG-07: executable entry, variable message, .env, API key branch, and main().
    agent_name = "AgentJ"
    message = f"Hello, 我是 {agent_name}，我們開始進入可對話的 Agent。"
    print(message)

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("找不到 OPENAI_API_KEY，請先在 .env 設定金鑰後再啟動。")
        return
    print("已讀取 OPENAI_API_KEY，可以呼叫模型。輸入 quit/exit/q 離開；附圖可用 `/image 相對路徑 問題`。")

    model_name = os.getenv("OPENAI_MODEL_NAME") or os.getenv("MODEL") or "gpt-4o"
    print(model_name)
    temperature_raw = os.getenv("TEMPERATURE", "0")
    try:
        temperature = float(temperature_raw)
    except ValueError:
        temperature = 0.0
    llm_kwargs: dict[str, Any] = {"model": model_name, "temperature": temperature}
    if os.getenv("BASE_URL"):
        llm_kwargs["base_url"] = os.getenv("BASE_URL")
    llm = ChatOpenAI(**llm_kwargs)
    llm_with_tools = llm.bind_tools(TOOLS)
    loader = SkillsLoader(PROJECT_ROOT, BUILTIN_SKILLS_DIR)
    metadata, history = load_session_jsonl(SESSION_JSONL_PATH)
    metadata.setdefault("created_at", now_iso())
    metadata.setdefault("last_consolidated", 0)

    while True:
        raw = input("\n你：").strip()
        if not raw:
            continue
        if raw.lower() in {"quit", "exit", "q"}:
            save_session_jsonl(SESSION_JSONL_PATH, history, metadata)
            print("已儲存 session，下次啟動會接續 JSONL 脈絡。")
            return

        text, image_rel = parse_user_input(raw)
        if not text:
            continue
        model_human_message, persisted_human_message = build_human_messages_for_turn(text, image_rel)

        system_text = build_system_prompt(loader)
        past, metadata = consolidate_memory_if_needed(llm, system_text, history, model_human_message, metadata)
        system_text = build_system_prompt(loader)
        system_message = SystemMessage(content=system_text)

        cost = len(system_text) + message_cost(past + [model_human_message])
        if cost > TOKEN_BUDGET:
            tokens_to_remove = max(0, cost - TOKEN_BUDGET // 2)
            boundary = pick_consolidation_boundary(history, int(metadata.get("last_consolidated", 0)), tokens_to_remove)
            if boundary is not None:
                past = history[boundary:]

        print("助理：", end="", flush=True)
        produced = run_react_turn(llm_with_tools, system_message, past, model_human_message)
        history.append(persisted_human_message)
        history.extend(produced)
        save_session_jsonl(SESSION_JSONL_PATH, history, metadata)


if __name__ == "__main__":
    main()
