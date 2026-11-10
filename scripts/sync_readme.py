#!/usr/bin/env python3
"""把 _conf_schema.json 同步成 README 里的配置表。

用法：
    python scripts/sync_readme.py          # 就地更新 README
    python scripts/sync_readme.py --check  # 只检查，不一致就返回 1（给 CI 用）
    python scripts/sync_readme.py --init   # 第一次运行，给旧表格补上标记
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SCHEMA = ROOT / "_conf_schema.json"

START = "<!-- CONFIG_TABLE:START -->"
END = "<!-- CONFIG_TABLE:END -->"
HEADER = ["| 键 | 说明 | 默认 |", "|---|---|---|"]


def build_block() -> str:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8-sig"))
    rows = []
    for key, item in schema.items():
        if not isinstance(item, dict):
            continue
        desc = str(item.get("description") or "").replace("|", "／")
        default = item.get("default")
        rows.append(f"| `{key}` | {desc} | `{default}` |")
    return "\n".join([START, *HEADER, *rows, END])


def locate_table(lines: list[str]) -> tuple[int, int] | None:
    """找不到标记时，用旧的表头定位表格范围。"""
    for index, line in enumerate(lines):
        if line.strip() == "| 键 | 说明 | 默认 |":
            end = index
            while end < len(lines) and lines[end].startswith("|"):
                end += 1
            return index, end
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--init", action="store_true")
    args = parser.parse_args()

    if not README.exists():
        print("找不到 README.md", file=sys.stderr)
        return 2
    if not SCHEMA.exists():
        print("找不到 _conf_schema.json", file=sys.stderr)
        return 2

    text = README.read_text(encoding="utf-8")
    block = build_block()

    if START in text and END in text:
        head, rest = text.split(START, 1)
        _, tail = rest.split(END, 1)
        new_text = head + block + tail
    elif args.init:
        lines = text.splitlines()
        span = locate_table(lines)
        if not span:
            print("没找到配置表，先手动加一对标记", file=sys.stderr)
            return 2
        start, end = span
        lines[start:end] = block.splitlines()
        new_text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    else:
        print("README 里没有标记块，先跑 --init", file=sys.stderr)
        return 2

    if new_text == text:
        print("配置表已是最新")
        return 0
    if args.check:
        print("配置表和 _conf_schema.json 不一致，请运行 scripts/sync_readme.py", file=sys.stderr)
        return 1

    README.write_text(new_text, encoding="utf-8")
    print("已更新 README 配置表")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
