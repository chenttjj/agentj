from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT / "studio_shell" / "data" / "avatar" / "_src"
OUT_DIR = ROOT / "studio_shell" / "data" / "avatar"
AVATAR_NAMES = ("idle", "thinking", "talking", "happy")


def convert_png_to_single_frame_gif(source_path: Path, output_path: Path) -> None:
    with Image.open(source_path) as image:
        frame = image.convert("RGBA")
        transparency_mask = frame.getchannel("A")
        palette_frame = frame.convert("P", palette=Image.ADAPTIVE, colors=255)
        palette_frame.info["transparency"] = 255
        palette_frame.paste(255, mask=Image.eval(transparency_mask, lambda alpha: 255 if alpha == 0 else 0))
        palette_frame.save(
            output_path,
            format="GIF",
            save_all=True,
            append_images=[],
            loop=0,
            disposal=2,
            transparency=255,
        )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for avatar_name in AVATAR_NAMES:
        source_path = SRC_DIR / f"{avatar_name}.png"
        output_path = OUT_DIR / f"{avatar_name}.gif"

        if not source_path.exists():
            raise FileNotFoundError(f"Missing source PNG: {source_path}")

        convert_png_to_single_frame_gif(source_path, output_path)
        print(f"Created {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
