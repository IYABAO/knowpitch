#!/usr/bin/env python3
"""formation_diagram.py 的机械断言测试（零依赖，标准库 unittest）。

运行：
    python -m unittest discover -s tests -v

覆盖第三方评测暴露的静默失败缺陷：
    T1  同名位置超额球员不得静默蒸发（转入替补席 + stderr 警告）
    T2  超长球员名/替补名完整显示，绝不截断丢字
    T5  非法阵型 / 坏 JSON / 文件缺失 → exit 2 + 中文错误，无裸 Traceback
    T6  flow 含阵型外代码 → stderr 警告；有效点不足不画箭头
    T8  大量替补时画布高度自适应，内容不被裁切
    N2  CAM/AMD 别名归一后超额同样不丢球员
    N4  B 队使用自己的 flow 画球路
    --strict 有任何警告 → exit 3
    三个官方示例零警告回归
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "knowpitch" / "scripts" / "formation_diagram.py"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
EXAMPLES = ROOT / "hf-space" / "examples"


def _squash(text):
    """去掉所有空白，便于把折行渲染的名字拼回完整字符串。"""
    return re.sub(r"\s+", "", text)


def _visible_text(svg):
    """提取 SVG 中全部 <text> 可见文本并拼接。"""
    parts = re.findall(r"<text[^>]*>(.*?)</text>", svg, re.S)
    return _squash("".join(re.sub(r"<[^>]+>", "", p) for p in parts))


def run_diagram(data=None, strict=False, fixture=None, raw_text=None, input_path=None):
    """以 CLI 子进程方式运行渲染脚本，返回 (CompletedProcess, svg_text)。"""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        inp = tmp / "team.json"
        out = tmp / "out.svg"
        if fixture is not None:
            inp = FIXTURES / fixture
        elif raw_text is not None:
            inp.write_text(raw_text, encoding="utf-8")
        elif input_path is not None:
            inp = input_path
        else:
            inp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        cmd = [sys.executable, str(SCRIPT), str(inp), str(out)]
        if strict:
            cmd.append("--strict")
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        proc = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", env=env)
        svg = out.read_text(encoding="utf-8") if out.exists() else ""
        return proc, svg


def load_fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class TestHappyPath(unittest.TestCase):
    def test_valid_team_no_warnings(self):
        proc, svg = run_diagram(fixture="valid_433.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("⚠️", proc.stderr)
        self.assertTrue(svg.lstrip().startswith("<svg"))
        self.assertIn("</svg>", svg)
        vis = _visible_text(svg)
        for name in ["门将基础", "核心概念甲", "核心结论", "进阶知识点"]:
            self.assertIn(name, vis)

    def test_strict_clean_exit0(self):
        proc, _ = run_diagram(fixture="valid_433.json", strict=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_official_examples_regression(self):
        examples = sorted(EXAMPLES.glob("*.json"))
        self.assertGreaterEqual(len(examples), 3, "三个官方示例必须存在")
        for ex in examples:
            with self.subTest(example=ex.name):
                proc, svg = run_diagram(input_path=ex)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertNotIn("⚠️", proc.stderr,
                                 f"{ex.name} 不应产生警告：\n{proc.stderr}")
                self.assertIn("</svg>", svg)
                self.assertGreater(len(svg), 1000)


class TestT1Overflow(unittest.TestCase):
    def test_overflow_player_goes_to_bench_not_lost(self):
        proc, svg = run_diagram(fixture="overflow_cb.json")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("只有 2 个槽", proc.stderr)
        self.assertIn("多出 1 人", proc.stderr)
        self.assertIn("中后卫丙超额", proc.stderr)
        # 关键断言：超额球员仍然出现在图上（替补席），没有凭空消失
        self.assertIn("中后卫丙超额", _visible_text(svg))

    def test_overflow_strict_exit3(self):
        proc, svg = run_diagram(fixture="overflow_cb.json", strict=True)
        self.assertEqual(proc.returncode, 3, proc.stdout)
        self.assertIn("中后卫丙超额", _visible_text(svg))  # exit 3 时 SVG 仍写出

    def test_n2_cam_amd_alias_overflow(self):
        # 4-2-3-1 只有 1 个 AMD 槽；CAM 与 AMD 别名归一后两人争 1 槽
        data = {
            "topic": "别名超额测试",
            "formation": "4-2-3-1",
            "coach": {"name": "核心", "desc": ""},
            "players": [
                {"pos": "GK", "name": "门将"},
                {"pos": "CAM", "name": "前腰甲CAM"},
                {"pos": "AMD", "name": "前腰乙AMD"},
                {"pos": "CF", "name": "中锋"},
            ],
            "bench": [],
        }
        proc, svg = run_diagram(data)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("多出 1 人", proc.stderr)
        vis = _visible_text(svg)
        self.assertIn("前腰甲CAM", vis)
        self.assertIn("前腰乙AMD", vis)


class TestT2LongNames(unittest.TestCase):
    LONG_NAMES = [
        "Medullary Thyroid Carcinoma",
        "BRAF V600E Mutation Pathway",
        "Bethesda Classification Category",
        "宋明理学与陆王心学之辨",
        "Radiofrequency Ablation Therapy Option",
    ]

    def test_long_names_complete(self):
        proc, svg = run_diagram(fixture="long_names.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        vis = _visible_text(svg)
        for name in self.LONG_NAMES:
            self.assertIn(_squash(name), vis, f"长名被截断丢失：{name}")

    def test_no_ellipsis_or_question_loss(self):
        _, svg = run_diagram(fixture="long_names.json")
        self.assertNotIn("…", svg)  # 旧版硬截断用省略号，禁止回归


class TestT5InputErrors(unittest.TestCase):
    def test_invalid_formation_exit2(self):
        proc, svg = run_diagram(fixture="invalid_formation.json")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("不支持的阵型", proc.stderr)
        self.assertEqual(svg, "")

    def test_broken_json_exit2(self):
        proc, _ = run_diagram(fixture="broken.json")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("JSON", proc.stderr)

    def test_missing_file_exit2(self):
        proc, _ = run_diagram(input_path=Path("/nonexistent/team.json"))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("找不到", proc.stderr)

    def test_no_raw_traceback(self):
        for fixture in ("invalid_formation.json", "broken.json"):
            with self.subTest(fixture=fixture):
                proc, _ = run_diagram(fixture=fixture)
                self.assertNotIn("Traceback", proc.stderr)


class TestT6Flow(unittest.TestCase):
    def test_unknown_flow_code_warns(self):
        proc, svg = run_diagram(fixture="flow_unknown.json")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("不存在的位置", proc.stderr)
        self.assertIn("ZZ", proc.stderr)
        # GK 与 CF 仍合法，箭头照常画出
        self.assertIn("marker-end", svg)

    def test_flow_all_invalid_no_arrow(self):
        data = load_fixture("flow_unknown.json")
        data["flow"] = ["ZZ", "QQ"]
        proc, svg = run_diagram(data)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("不存在的位置", proc.stderr)
        self.assertIn("不足 2 个", proc.stderr)
        self.assertNotIn("marker-end", svg)

    def test_flow_warning_strict_exit3(self):
        proc, _ = run_diagram(fixture="flow_unknown.json", strict=True)
        self.assertEqual(proc.returncode, 3)


class TestT8BenchCanvas(unittest.TestCase):
    def test_heavy_bench_grows_canvas_and_keeps_everyone(self):
        data = load_fixture("valid_433.json")
        data["bench"] = [
            {"name": f"替补知识点{i:02d}", "desc": ""} for i in range(40)]
        proc, svg = run_diagram(data)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        match = re.search(r'<svg[^>]*height="(\d+)"', svg)
        self.assertIsNotNone(match)
        # 40 人 / 每行 19 个 = 3 行 → 画布高度 1300+3*80+60 = 1600
        self.assertGreaterEqual(int(match.group(1)), 1600)
        vis = _visible_text(svg)
        for i in range(40):
            self.assertIn(f"替补知识点{i:02d}", vis, f"替补 {i} 被裁切")


class TestN4BTeamFlow(unittest.TestCase):
    def test_bteam_uses_its_own_flow(self):
        proc, svg = run_diagram(fixture="b_team_flow.json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("⚠️", proc.stderr)
        self.assertIn("arrow_pitch_b", svg)       # B 队有合法 flow
        self.assertNotIn("arrow_pitch_main", svg)  # 主队无 flow


if __name__ == "__main__":
    unittest.main(verbosity=2)
