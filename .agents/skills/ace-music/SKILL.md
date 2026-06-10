---
name: ace-music
description: Generate AI music using ACE-Step 1.5 via ACE Music's free API. Use when the user asks to create, generate, or compose music, songs, beats, instrumentals, or audio tracks. Supports lyrics, style prompts, covers, and repainting. Free API, no cost.
---

# ACE Music - AI Music Generation

Generate music via ACE Music's free hosted API (ACE-Step 1.5 model).

## Setup

**API Key** is stored in env `ACE_MUSIC_API_KEY`. If not set:
1. Open https://acemusic.ai/playground/api-key in the browser for the user
2. Ask them to sign up (free) and paste the API key
3. Store it: add `ACE_MUSIC_API_KEY=<key>` to your `.env` or `TOOLS.md`, or set via PowerShell: `$env:ACE_MUSIC_API_KEY="<key>"`

## Quick Generation

Use `scripts/generate.py` for one-shot generation. It reads `ACE_MUSIC_API_KEY` from the environment and prints the saved file path(s) to stdout.

```bash
# Simple prompt (AI decides everything)
python scripts/generate.py "upbeat pop song about summer" --duration 30 --output summer.mp3

# With lyrics (Tagged mode — recommended)
python scripts/generate.py "gentle acoustic ballad, female vocal" \
  --lyrics "[Verse 1]\nSunlight through the window\n\n[Chorus]\nWe are the dreamers" \
  --duration 60 --output ballad.mp3

# Instrumental only
python scripts/generate.py "lo-fi hip hop beats, chill, rainy day" --instrumental --duration 120 --output lofi.mp3

# Natural language — AI writes everything
python scripts/generate.py --sample-mode --output jazz.mp3

# Specific settings (BPM, key, seed)
python scripts/generate.py "rock anthem" --bpm 140 --key "E minor" --language en --seed 42 --output rock.mp3

# Multiple variations
python scripts/generate.py "electronic dance track" --batch 3 --output edm.mp3
```

The script prints the saved file path(s) to **stdout** (one per line). Send those files to the user.

## Advanced Usage (covers / repainting)

For covers and repainting, pass `--task cover` or `--task repaint`:

```bash
# Cover (requires base64 audio — see api-docs.md for multimodal input)
python scripts/generate.py "Cover this song in jazz style" --task cover --cover-strength 0.8 --output cover.mp3

# Repaint a section (seconds 10–30)
python scripts/generate.py "Add electric guitar solo" --task repaint --repaint-start 10 --repaint-end 30 --output repaint.mp3
```

For full API spec (audio input, streaming) — see `references/api-docs.md`.

## Parameters Guide

| Want | CLI argument |
|------|-------------|
| Specific style | `"jazz, saxophone solo, smoky bar"` as the prompt |
| Custom lyrics | `--lyrics "[Verse]...[Chorus]..."` |
| AI writes everything | `--sample-mode` |
| No vocals | `--instrumental` |
| Longer songs | `--duration 120` (seconds) |
| Specific tempo | `--bpm 120` |
| Specific key | `--key "C major"` |
| Multiple outputs | `--batch 3` |
| Reproducible | `--seed 42` |
| Non-English vocals | `--language ja` (zh, en, ja, ko, etc.) |
| Cover a song | `--task cover --cover-strength 0.8` |
| Repaint a section | `--task repaint --repaint-start 10 --repaint-end 30` |

## Notes

- API is **free forever** (confirmed by ACE Music team)
- Base URL: `https://api.acemusic.ai`
- Audio returned as base64 MP3; `generate.py` decodes and saves it automatically
- Duration: if omitted, AI decides based on content
- For best results, use Tagged mode (prompt + lyrics separated via XML tags)
