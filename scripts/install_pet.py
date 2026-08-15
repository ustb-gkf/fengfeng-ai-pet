#!/usr/bin/env python3
"""Install the packaged pet into a local Codex pets directory."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "pet" / "fengfeng"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the Fengfeng Codex pet")
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=None,
        help="Codex home directory; defaults to CODEX_HOME or ~/.codex",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace an existing fengfeng pet directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    default_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    codex_home = (args.codex_home or default_home).expanduser().resolve()
    destination = codex_home / "pets" / "fengfeng"

    if destination.exists():
        if not args.force:
            raise SystemExit(
                f"{destination} already exists; rerun with --force to replace it"
            )
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, destination)
    print(f"Installed Fengfeng to {destination}")
    print("Restart Codex and select 峰峰 in Settings → Pets.")


if __name__ == "__main__":
    main()

