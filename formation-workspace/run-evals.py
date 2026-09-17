#!/usr/bin/env python3
"""
run-evals.py — KnowPitch 阵型学习法评估运行脚本

对标 ELI5 的评估系统：A/B 测试 + LLM Judge

用法:
    python run-evals.py --config evals.json --output results/
    python run-evals.py --config evals.json --judge --output results/

功能:
    1. 加载 evals.json 测试用例
    2. 构建 A/B 配置（With Skill / Without Skill）
    3. 运行每个测试（需要接入 LLM API）
    4. LLM Judge 评分（每个 assertion 判 PASS/FAIL）
    5. 汇总通过率，保存结果
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class EvalRunner:
    """评估运行器"""

    def __init__(self, config_path: str, output_dir: str):
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.skill_name = self.config.get("skill_name", "knowpitch")
        self.evals = self.config.get("evals", [])

    def build_prompt(self, eval_item: Dict, with_skill: bool = True) -> str:
        """构建测试 prompt"""
        base_prompt = eval_item["prompt"]

        if with_skill:
            # With Skill: 附加技能上下文
            skill_context = f"""
你是一个使用 {self.skill_name} 技能的 AI 助手。
请使用足球阵型的方式回答以下问题，遵循以下规则：
1. 输出包含主教练（一句话核心思想）
2. 输出包含门将（最底层基础）、后卫（基础概念）、中场（机制/方法）、前锋（应用/结论）
3. 每个球员用 ELI5 风格：是什么 + 像什么（日常类比）
4. 输出包含教练战术板（学习路径 + 关键连线 + 三种输球方式）
5. 假设零背景，用大白话解释

问题：{base_prompt}
"""
            return skill_context
        else:
            # Without Skill: 直接提问
            return f"请回答以下问题：{base_prompt}"

    def run_llm(self, prompt: str) -> str:
        """
        运行 LLM 生成响应

        注意：这里需要接入实际的 LLM API。
        示例使用 OpenAI 兼容 API，实际使用时请替换为你的 API。
        """
        # TODO: 接入实际 LLM API
        # 示例：
        # import openai
        # client = openai.OpenAI(api_key="your-api-key")
        # response = client.chat.completions.create(
        #     model="gpt-4",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response.choices[0].message.content

        # 占位：返回模拟响应
        return f"[模拟响应] 这是对 prompt 的响应：{prompt[:50]}..."

    def judge_response(self, response: str, assertions: List[str]) -> List[Dict]:
        """
        LLM Judge: 对每个 assertion 判 PASS/FAIL

        注意：这里需要接入实际的 LLM API 进行评判。
        """
        results = []
        for assertion in assertions:
            # TODO: 接入实际 LLM Judge
            # judge_prompt = f"""
            # 请判断以下响应是否满足断言：
            # 响应：{response[:2000]}
            # 断言：{assertion}
            # 只回答 PASS 或 FAIL，并简要说明理由。
            # """
            # result = self.run_llm(judge_prompt)

            # 占位：默认判为待评估
            results.append({
                "assertion": assertion,
                "result": "PENDING",
                "reason": "需要接入 LLM Judge"
            })
        return results

    def run_eval(self, eval_item: Dict, with_skill: bool) -> Dict:
        """运行单个测试用例"""
        eval_id = eval_item["id"]
        config_name = "with-skill" if with_skill else "without-skill"

        print(f"\n{'='*60}")
        print(f"运行: {eval_id} ({config_name})")
        print(f"名称: {eval_item['name']}")
        print(f"{'='*60}")

        # 构建 prompt
        prompt = self.build_prompt(eval_item, with_skill)

        # 运行 LLM
        start_time = time.time()
        response = self.run_llm(prompt)
        elapsed = time.time() - start_time

        # Judge 评分
        judge_results = self.judge_response(response, eval_item.get("assertions", []))

        # 计算通过率
        passed = sum(1 for r in judge_results if r["result"] == "PASS")
        total = len(judge_results)
        pass_rate = passed / total * 100 if total > 0 else 0

        result = {
            "eval_id": eval_id,
            "name": eval_item["name"],
            "config": config_name,
            "prompt": prompt,
            "response": response,
            "elapsed_seconds": round(elapsed, 2),
            "judge_results": judge_results,
            "pass_rate": round(pass_rate, 1),
            "passed": passed,
            "total": total
        }

        # 保存响应
        eval_dir = self.output_dir / eval_id / config_name
        eval_dir.mkdir(parents=True, exist_ok=True)

        with open(eval_dir / "response.md", "w", encoding="utf-8") as f:
            f.write(f"# {eval_item['name']}\n\n")
            f.write(f"## Prompt\n\n```\n{prompt}\n```\n\n")
            f.write(f"## Response\n\n{response}\n\n")
            f.write(f"## Timing\n\n- Elapsed: {elapsed:.2f}s\n")

        with open(eval_dir / "timing.json", "w", encoding="utf-8") as f:
            json.dump({"elapsed_seconds": elapsed}, f, indent=2)

        print(f"  通过率: {passed}/{total} ({pass_rate:.1f}%)")
        print(f"  耗时: {elapsed:.2f}s")

        return result

    def run_all(self, judge: bool = False) -> Dict:
        """运行所有测试用例"""
        results = {
            "skill_name": self.skill_name,
            "run_time": datetime.now().isoformat(),
            "configs": ["with-skill", "without-skill"],
            "evals": []
        }

        for eval_item in self.evals:
            # With Skill
            with_skill_result = self.run_eval(eval_item, with_skill=True)
            results["evals"].append(with_skill_result)

            # Without Skill
            without_skill_result = self.run_eval(eval_item, with_skill=False)
            results["evals"].append(without_skill_result)

        # 汇总
        summary = self.summarize(results)
        results["summary"] = summary

        # 保存汇总结果
        with open(self.output_dir / "results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # 打印汇总
        self.print_summary(summary)

        return results

    def summarize(self, results: Dict) -> Dict:
        """汇总评估结果"""
        summary = {
            "with_skill": {"total": 0, "passed": 0, "pass_rate": 0.0},
            "without_skill": {"total": 0, "passed": 0, "pass_rate": 0.0},
            "delta": 0.0
        }

        for eval_result in results["evals"]:
            config = eval_result["config"]
            key = "with_skill" if config == "with-skill" else "without_skill"
            summary[key]["total"] += eval_result["total"]
            summary[key]["passed"] += eval_result["passed"]

        # 计算通过率
        for key in ["with_skill", "without_skill"]:
            if summary[key]["total"] > 0:
                summary[key]["pass_rate"] = round(
                    summary[key]["passed"] / summary[key]["total"] * 100, 1
                )

        # 计算 Delta
        summary["delta"] = round(
            summary["with_skill"]["pass_rate"] - summary["without_skill"]["pass_rate"], 1
        )

        return summary

    def print_summary(self, summary: Dict):
        """打印汇总结果"""
        print("\n" + "="*60)
        print("📊 评估汇总")
        print("="*60)
        print(f"{'Metric':<20} {'With Skill':<15} {'Without Skill':<15} {'Delta':<10}")
        print("-"*60)
        print(f"{'Pass Rate':<20} {summary['with_skill']['pass_rate']:<15.1f}% "
              f"{summary['without_skill']['pass_rate']:<15.1f}% "
              f"{summary['delta']:<+10.1f}%")
        print(f"{'Passed/Total':<20} "
              f"{summary['with_skill']['passed']}/{summary['with_skill']['total']:<10} "
              f"{summary['without_skill']['passed']}/{summary['without_skill']['total']:<10}")
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description="KnowPitch 评估运行脚本")
    parser.add_argument("--config", default="evals.json", help="评估配置文件路径")
    parser.add_argument("--output", default="results", help="输出目录")
    parser.add_argument("--judge", action="store_true", help="启用 LLM Judge 评分")
    parser.add_argument("--single", help="只运行单个测试用例 ID")

    args = parser.parse_args()

    runner = EvalRunner(args.config, args.output)

    if args.single:
        # 只运行单个测试
        eval_item = next((e for e in runner.evals if e["id"] == args.single), None)
        if not eval_item:
            print(f"❌ 未找到测试用例: {args.single}")
            sys.exit(1)
        runner.run_eval(eval_item, with_skill=True)
    else:
        # 运行所有测试
        runner.run_all(judge=args.judge)


if __name__ == "__main__":
    main()
