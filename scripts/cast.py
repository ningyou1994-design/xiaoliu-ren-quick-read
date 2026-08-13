#!/usr/bin/env python3
"""Deterministically cast the three palaces for xiaoliu-ren-quick-read."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


METHOD_VERSION = "1.0.1"
UNICODE_VERSION = "17.0.0"
PALACES = ("大安", "留连", "速喜", "赤口", "小吉", "空亡")
BRANCHES = ("子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥")
WRAPPERS = "「」『』“”\"'"


class InputError(ValueError):
    """Raised when a user-facing input cannot be normalized safely."""


def is_variation_selector(character: str) -> bool:
    codepoint = ord(character)
    return 0xFE00 <= codepoint <= 0xFE0F or 0xE0100 <= codepoint <= 0xE01EF


def normalize_character(raw: str) -> str:
    cleaned = raw.strip().strip(WRAPPERS).strip()
    characters = [character for character in cleaned if not is_variation_selector(character)]
    if len(characters) != 1:
        raise InputError("请只提供一个汉字，不要输入词语、句子或多个字。")
    return characters[0]


def normalize_branch(raw: str) -> str:
    cleaned = raw.strip()
    if cleaned.endswith("时"):
        cleaned = cleaned[:-1]
    if cleaned not in BRANCHES:
        raise InputError("时辰必须是子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥之一。")
    return cleaned


def branch_from_time(raw: str) -> str:
    match = re.fullmatch(r"\s*(\d{1,2})(?::(\d{1,2}))?\s*", raw)
    if not match:
        raise InputError("时间请使用 24 小时制，例如 21:30。")
    hour = int(match.group(1))
    minute = int(match.group(2) or "0")
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise InputError("时间超出有效范围，请使用 00:00 至 23:59。")
    branch_index = ((hour + 1) // 2) % 12
    return BRANCHES[branch_index]


def load_stroke_index(path: Path) -> dict[int, int]:
    if not path.is_file():
        raise RuntimeError(f"找不到笔画索引：{path}")
    index: dict[int, int] = {}
    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip() or line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) != 2:
                raise RuntimeError(f"笔画索引第 {line_number} 行格式错误。")
            codepoint_hex, stroke_text = fields
            index[int(codepoint_hex, 16)] = int(stroke_text)
    return index


def palace_for_number(number: int) -> tuple[int, str]:
    palace_number = ((number - 1) % 6) + 1
    return palace_number, PALACES[palace_number - 1]


def cast(
    character: str,
    branch: str,
    stroke_index: dict[int, int],
    stroke_override: int | None = None,
) -> dict[str, object]:
    if stroke_override is not None:
        if not 1 <= stroke_override <= 200:
            raise InputError("手动笔画数必须是 1 至 200 的正整数。")
        strokes = stroke_override
        stroke_source: dict[str, str] = {"type": "user_override"}
    else:
        codepoint = ord(character)
        if codepoint not in stroke_index:
            raise InputError("默认笔画数据中没有这个字符；请确认所选字，或用 --strokes 提供笔画数。")
        strokes = stroke_index[codepoint]
        stroke_source = {
            "type": "unicode_unihan",
            "version": UNICODE_VERSION,
            "property": "kTotalStrokes",
        }

    branch_number = BRANCHES.index(branch) + 1
    word_number, word_palace = palace_for_number(strokes)
    time_number, time_palace = palace_for_number(branch_number)
    result_number, result_palace = palace_for_number(strokes + branch_number - 1)

    return {
        "method_version": METHOD_VERSION,
        "character": character,
        "codepoint": f"U+{ord(character):04X}",
        "stroke_count": strokes,
        "stroke_source": stroke_source,
        "branch": branch,
        "branch_number": branch_number,
        "word_palace": {"number": word_number, "name": word_palace},
        "time_palace": {"number": time_number, "name": time_palace},
        "result_palace": {"number": result_number, "name": result_palace},
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="按一个汉字与时辰计算小六壬速断的字宫、时宫和落宫。"
    )
    parser.add_argument("--char", required=True, dest="character", help="用户亲自选的一个汉字")
    time_group = parser.add_mutually_exclusive_group(required=True)
    time_group.add_argument("--branch", help="时辰，如亥或亥时")
    time_group.add_argument("--time", help="24小时制当地时间，如21:30")
    parser.add_argument("--strokes", type=int, help="可选：用户明确指定的笔画数")
    parser.add_argument("--json", action="store_true", help="以JSON输出，便于代理读取")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        character = normalize_character(args.character)
        branch = normalize_branch(args.branch) if args.branch else branch_from_time(args.time)
        data_path = Path(__file__).resolve().parent.parent / "assets" / "unihan-total-strokes.txt"
        stroke_index = load_stroke_index(data_path)
        result = cast(character, branch, stroke_index, args.strokes)
    except (InputError, RuntimeError) as error:
        parser.exit(2, f"错误：{error}\n")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        source = result["stroke_source"]
        source_label = "用户指定笔画" if source["type"] == "user_override" else "Unicode 17.0.0 kTotalStrokes"
        print(f"字：{result['character']}（{result['stroke_count']}画；{source_label}）")
        print(f"时：{result['branch']}时（序{result['branch_number']}）")
        print(f"字宫：{result['word_palace']['name']}")
        print(f"时宫：{result['time_palace']['name']}")
        print(f"落宫：{result['result_palace']['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
