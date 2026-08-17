#!/usr/bin/env python3
"""Initialize a NovelGame save from a settings file.

Reads a settings file (Markdown), generates the initial save, and prints the
opening guidance. The initial-state parser accepts English, Chinese, and
Japanese section keywords so settings can be authored in any supported language.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

# Section keywords accepted in English / Chinese / Japanese
_SECTION_PATTERNS = {
    "stats": r"(?:##\s*)?(?:Initial State|初始状态|初期状態)",
    "affinity": r"(?:affinity|好感度|親密度)",
    "inventory": r"(?:inventory|背包|所持品|持ち物)",
    "flags": r"(?:flag|特殊|special|フラグ|特別)",
}


def parse_initial_state(settings_text: str) -> tuple[dict, list, dict]:
    """Parse stats / inventory / flags from the "Initial State" section.

    Supported formats (one per line, colon in English or Chinese):
    - Affinity: Erin=10, Old Hawke=20
    - Inventory: old pocket watch, case files
    - Special flags: met_erin=true
    """
    stats: dict[str, int] = {}
    inventory: list[str] = []
    flags: dict[str, str] = {}
    m = re.search(r"##\s*(?:Initial State|初始状态|初期状態)\s*\n(.*?)(?=\n##\s|\Z)", settings_text, re.S)
    if not m:
        return stats, inventory, flags
    for line in m.group(1).splitlines():
        line = line.strip().lstrip("-").strip()
        if not line:
            continue
        if re.search(r"[：:]", line):
            key, val = re.split(r"[：:]", line, maxsplit=1)
        else:
            key, val = line, ""
        key, val = key.strip(), val.strip()
        if re.search(_SECTION_PATTERNS["affinity"], key, re.I):
            for item in val.replace("，", ",").split(","):
                item = item.strip()
                if "=" not in item:
                    continue
                k, _, v = item.partition("=")
                try:
                    stats[k.strip()] = int(v.strip())
                except ValueError:
                    pass
        elif re.search(_SECTION_PATTERNS["inventory"], key, re.I):
            for item in val.replace("，", ",").replace("、", ",").split(","):
                item = item.strip()
                if item and item.lower() not in ("无", "なし", "none"):
                    inventory.append(item)
        elif re.search(_SECTION_PATTERNS["flags"], key, re.I):
            if val.lower() in ("", "无", "なし", "none"):
                continue
            for item in val.replace("，", ",").split(","):
                item = item.strip()
                if not item:
                    continue
                if "=" in item:
                    k, _, v = item.partition("=")
                    flags[k.strip()] = v.strip()
                else:
                    flags[item] = "true"
    return stats, inventory, flags


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a NovelGame story")
    parser.add_argument("--settings", required=True, help="path to the settings file")
    parser.add_argument("--title", default="")
    parser.add_argument("--story", default="")
    parser.add_argument("--dir", default="")
    args = parser.parse_args()

    sp = Path(args.settings)
    if not sp.exists():
        sys.exit(f"Settings file not found: {sp}")
    settings_text = sp.read_text(encoding="utf-8")

    data_dir = Path(args.dir) if args.dir else Path(os.environ.get("NOVEL_DATA_DIR", "saves"))
    data_dir.mkdir(parents=True, exist_ok=True)

    story_id = args.story or uuid.uuid4().hex[:8]
    stats, inventory, flags = parse_initial_state(settings_text)
    state = {
        "story_id": story_id,
        "title": args.title or sp.stem,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "current_node": "start",
        "flags": flags,
        "stats": stats,
        "inventory": inventory,
        "history": [],
        "branch_log": [],
        "memory": {
            "short": [],
            "mid": [],
            "long": [],
        },
        "snapshots": [],
        "settings": settings_text,
    }
    out = data_dir / f"{story_id}.json"
    out.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Story created: {story_id} ({state['title']})")
    print(f"Save: {out}")
    print("Opening: write the opening passage and 2-4 choices based on the settings.")


if __name__ == "__main__":
    main()
