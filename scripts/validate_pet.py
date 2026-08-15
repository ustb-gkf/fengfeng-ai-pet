#!/usr/bin/env python3
"""Validate the packaged Fengfeng Codex v2 pet."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PET_DIR = ROOT / "pet" / "fengfeng"
PET_JSON = PET_DIR / "pet.json"
SPRITESHEET = PET_DIR / "spritesheet.webp"

EXPECTED_SIZE = (1536, 2288)
CELL_SIZE = (192, 208)
# Row 0 includes six idle frames plus the neutral look frame at column 6.
FRAME_COUNTS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not PET_JSON.is_file() or not SPRITESHEET.is_file():
        fail("pet.json or spritesheet.webp is missing")

    metadata = json.loads(PET_JSON.read_text(encoding="utf-8"))
    if metadata.get("id") != "fengfeng":
        fail("pet id must be 'fengfeng'")
    if metadata.get("spriteVersionNumber") != 2:
        fail("spriteVersionNumber must be 2")
    if metadata.get("spritesheetPath") != "spritesheet.webp":
        fail("spritesheetPath must point to spritesheet.webp")

    image = Image.open(SPRITESHEET).convert("RGBA")
    if image.size != EXPECTED_SIZE:
        fail(f"unexpected atlas size: {image.size}, expected {EXPECTED_SIZE}")

    alpha = image.getchannel("A")
    width, height = CELL_SIZE
    used_cells = 0
    blank_cells = 0

    for row, frame_count in enumerate(FRAME_COUNTS):
        for column in range(8):
            box = (
                column * width,
                row * height,
                (column + 1) * width,
                (row + 1) * height,
            )
            extrema = alpha.crop(box).getextrema()
            has_content = extrema[1] > 0
            if column < frame_count:
                if not has_content:
                    fail(f"used cell row={row}, column={column} is empty")
                used_cells += 1
            else:
                if has_content:
                    fail(f"unused cell row={row}, column={column} is not empty")
                blank_cells += 1

    result = {
        "ok": True,
        "spriteVersionNumber": 2,
        "size": list(image.size),
        "mode": image.mode,
        "used_cells": used_cells,
        "blank_cells": blank_cells,
        "animation_rows": 9,
        "look_directions": 16,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
