#!/usr/bin/env python3
"""
ACE-Step Music Generation via API
Usage: python generate.py <prompt> [options]

Options:
  --lyrics "..."       Lyrics text
  --duration 30        Duration in seconds
  --language en        Vocal language code (en, zh, ja, ko, ...)
  --instrumental       No vocals
  --output file.mp3    Output file path (default: output_<timestamp>.mp3)
  --bpm 120            Beats per minute
  --key "C major"      Musical key
  --seed 42            Random seed for reproducibility
  --sample-mode        Let AI generate everything (prompt + lyrics)
  --batch 3            Number of variations to generate
  --format mp3         Output format (mp3)
  --task cover         Task type: text2music (default), cover, repaint
  --repaint-start 10   Repaint start in seconds
  --repaint-end 30     Repaint end in seconds
  --cover-strength 0.8 Cover strength (0.0–1.0)
"""

import argparse
import base64
import os
import sys
import time

import requests


BASE_URL = os.environ.get("ACE_MUSIC_BASE_URL", "https://api.acemusic.ai")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate music via ACE Music API", add_help=True)
    p.add_argument("prompt", nargs="?", default="", help="Music style / description")
    p.add_argument("--lyrics", default="")
    p.add_argument("--duration", type=float, default=None)
    p.add_argument("--language", default="en")
    p.add_argument("--instrumental", action="store_true")
    p.add_argument("--output", "-o", default=None)
    p.add_argument("--bpm", type=int, default=None)
    p.add_argument("--key", default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--sample-mode", action="store_true")
    p.add_argument("--batch", type=int, default=1)
    p.add_argument("--format", default="mp3")
    p.add_argument("--task", default="text2music", choices=["text2music", "cover", "repaint"])
    p.add_argument("--repaint-start", type=float, default=0.0)
    p.add_argument("--repaint-end", type=float, default=None)
    p.add_argument("--cover-strength", type=float, default=1.0)
    return p.parse_args()


def build_payload(args: argparse.Namespace) -> dict:
    # Build message content
    if args.lyrics and args.prompt:
        content = f"<prompt>{args.prompt}</prompt>\n<lyrics>{args.lyrics}</lyrics>"
    elif args.lyrics:
        content = args.lyrics
    else:
        content = args.prompt

    # audio_config
    audio_config: dict = {"vocal_language": args.language, "format": args.format}
    if args.duration is not None:
        audio_config["duration"] = args.duration
    if args.bpm is not None:
        audio_config["bpm"] = args.bpm
    if args.key:
        audio_config["key_scale"] = args.key
    if args.instrumental:
        audio_config["instrumental"] = True

    payload: dict = {
        "messages": [{"role": "user", "content": content}],
        "audio_config": audio_config,
        "stream": False,
        "task_type": args.task,
    }

    if args.sample_mode:
        payload["sample_mode"] = True
    if args.seed is not None:
        payload["seed"] = args.seed
    if args.batch > 1:
        payload["batch_size"] = args.batch
    if args.task == "repaint":
        payload["repainting_start"] = args.repaint_start
        if args.repaint_end is not None:
            payload["repainting_end"] = args.repaint_end
    if args.task == "cover":
        payload["audio_cover_strength"] = args.cover_strength

    return payload


def save_outputs(audios: list, output_path: str) -> list[str]:
    saved = []
    base, ext = (output_path.rsplit(".", 1) if "." in output_path else (output_path, "mp3"))
    for i, audio in enumerate(audios):
        url = audio["audio_url"]["url"]
        data = base64.b64decode(url.split(",", 1)[1])
        fname = output_path if len(audios) == 1 else f"{base}_{i + 1}.{ext}"
        with open(fname, "wb") as f:
            f.write(data)
        print(f"Saved: {fname}", file=sys.stderr)
        print(fname)  # stdout: file path for the caller (agent)
        saved.append(fname)
    return saved


def main() -> None:
    args = parse_args()

    api_key = os.environ.get("ACE_MUSIC_API_KEY", "")
    if not api_key:
        print("ERROR: ACE_MUSIC_API_KEY not set.", file=sys.stderr)
        print("Get your free API key at: https://acemusic.ai/playground/api-key", file=sys.stderr)
        sys.exit(1)

    if not args.prompt and not args.sample_mode and not args.lyrics:
        print("ERROR: Provide a prompt, --lyrics, or --sample-mode.", file=sys.stderr)
        sys.exit(1)

    output = args.output or f"output_{int(time.time())}.mp3"
    payload = build_payload(args)

    print(f"🎵 Generating music...", file=sys.stderr)
    print(f"   Prompt   : {args.prompt or '[lyrics/sample mode]'}", file=sys.stderr)
    if args.duration:
        print(f"   Duration : {args.duration}s", file=sys.stderr)
    print(f"   Language : {args.language}", file=sys.stderr)
    print(f"   Task     : {args.task}", file=sys.stderr)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(
            f"{BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=300,
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"ERROR: API request failed: {e}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()

    if "choices" not in result:
        print("ERROR: Unexpected API response:", file=sys.stderr)
        print(result, file=sys.stderr)
        sys.exit(1)

    audios = result["choices"][0]["message"].get("audio", [])
    if not audios:
        print("ERROR: No audio in response.", file=sys.stderr)
        print(result, file=sys.stderr)
        sys.exit(1)

    save_outputs(audios, output)

    metadata = result["choices"][0]["message"].get("content", "")
    if metadata:
        print(f"\n📋 Metadata:\n{metadata}", file=sys.stderr)


if __name__ == "__main__":
    main()
