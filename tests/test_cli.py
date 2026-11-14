#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""命令行入口的机械验收测试（标准库 unittest，无第三方依赖）。"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "knowpitch_cli.py"
EXAMPLES = ROOT / "examples"


class TestKnowpitchCli(unittest.TestCase):
    def test_svg_from_top_level_example(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.svg"
            proc = subprocess.run(
                [sys.executable, str(CLI), "svg", str(EXAMPLES / "machine_learning.json"), str(out)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertTrue(out.is_file())
            svg = out.read_text(encoding="utf-8")
            self.assertTrue(svg.lstrip().startswith("<svg"))
            self.assertGreater(len(svg), 1000)
            self.assertIn("机器学习", svg)

    def test_missing_arguments_returns_2(self):
        proc = subprocess.run(
            [sys.executable, str(CLI), "svg", "only-one-arg.json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 2)

    def test_unknown_command_returns_2(self):
        proc = subprocess.run(
            [sys.executable, str(CLI), "nope"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
