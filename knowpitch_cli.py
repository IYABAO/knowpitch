#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowpitch 命令行入口：把知识阵容 JSON 渲染成 SVG。

安装后使用：
    pip install -e .
    knowpitch svg examples/machine_learning.json out.svg

渲染逻辑仍由 `skills/knowpitch/scripts/formation_diagram.py` 单源提供，
本文件只负责命令分发和路径定位，不复制渲染实现。
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _candidate_scripts():
    """按“源码树优先、安装数据次之”的顺序找单源渲染脚本。"""
    yield ROOT / "skills" / "knowpitch" / "scripts" / "formation_diagram.py"
    yield Path(sys.prefix) / "share" / "knowpitch" / "skills" / "formation_diagram.py"


def _find_script():
    for path in _candidate_scripts():
        if path.is_file():
            return path
    raise FileNotFoundError(
        "找不到 formation_diagram.py；请在 knowpitch 源码目录执行 pip install -e .，"
        "或重新安装包含脚本数据的包"
    )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="knowpitch",
        description="把知识阵容 JSON 渲染成足球场 SVG 阵型图",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    svg = sub.add_parser("svg", help="从 JSON 生成 SVG")
    svg.add_argument("input", help="输入阵容 JSON 路径")
    svg.add_argument("output", help="输出 SVG 路径")
    svg.add_argument(
        "--strict",
        action="store_true",
        help="存在任何警告时以退出码 3 结束（交付前自检用）",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command != "svg":
        return 2

    try:
        script = _find_script()
    except FileNotFoundError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 2

    cmd = [sys.executable, str(script), args.input, args.output]
    if args.strict:
        cmd.append("--strict")
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
