#!/usr/bin/env python3
"""
KnowPitch (球知) - Hugging Face Space Demo
用足球阵型把知识讲透
"""

import json
import os
import tempfile
from pathlib import Path

import gradio as gr

try:
    import cairosvg
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False

# ZeroGPU 兼容：添加空 GPU 函数满足检测（实际应用纯 CPU，不需要 GPU）
try:
    from spaces import GPU
    @GPU
    def _dummy_gpu():
        """满足 ZeroGPU 检测的空函数"""
        pass
except ImportError:
    pass

# 阵型描述
FORMATION_DESC = {
    "4-3-3": "均衡阵型：4基础/3机制/3应用，最常见",
    "4-2-3-1": "单箭头：一个核心结论，背后三个创造者",
    "4-3-2-1": "圣诞树：主结论+两个衍生结论",
    "4-4-2": "双板块：理论vs实践对半分",
    "4-5-1": "中场厚：机制方法多，结论单一",
    "4-1-4-1": "单后腰：一个关键机制托底",
    "3-5-2": "三中卫：机制密集+双结论",
    "3-4-3": "三后卫：基础少，应用案例多",
}

# 位置说明
POSITION_DESC = {
    "HC": "主教练 - 一句话核心思想",
    "GK": "门将 - 最底层基础/第一性原理",
    "CB": "中后卫 - 核心基础概念",
    "LB/RB": "边后卫 - 背景/前置知识",
    "CDM": "后腰 - 机制/原理",
    "CM": "中前卫 - 方法/流程/步骤",
    "AMD/CAM": "前腰 - 核心思想/理论",
    "LW/RW": "边锋 - 应用/案例",
    "CF": "中锋 - 核心结论/主要产出",
    "SS": "影锋 - 衍生结论/推论",
    "SUB": "替补 - 进阶/边角知识点",
}

# 各位置的默认占位名称（基于主题生成）
POSITION_TEMPLATES = {
    "GK": "{topic}基础定义",
    "CB": "{topic}核心概念",
    "LB": "{topic}背景知识",
    "RB": "{topic}前置条件",
    "CDM": "{topic}底层机制",
    "CM": "{topic}实现方法",
    "CAM": "{topic}核心理论",
    "AMD": "{topic}核心思想",
    "LAM": "{topic}左侧理论",
    "RAM": "{topic}右侧理论",
    "LM": "{topic}左路方法",
    "RM": "{topic}右路方法",
    "LW": "{topic}应用案例",
    "RW": "{topic}实践场景",
    "CF": "{topic}核心结论",
    "SS": "{topic}衍生推论",
}


def load_examples():
    """加载所有预设示例"""
    examples_dir = Path(__file__).parent / "examples"
    examples = {}
    if examples_dir.exists():
        for f in examples_dir.glob("*.json"):
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                examples[data["topic"]] = data
    return examples


EXAMPLES = load_examples()


def generate_diagram(team_data):
    """生成阵型图，返回高分辨率 PNG 文件路径（SVG 转 2x PNG）"""
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from formation_diagram import main as diagram_main

    # 写临时 JSON
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(team_data, f, ensure_ascii=False)
        json_path = f.name

    svg_path = json_path.replace(".json", ".svg")
    png_path = json_path.replace(".json", ".png")

    # 调用生成脚本
    old_argv = sys.argv
    sys.argv = ["formation_diagram.py", json_path, svg_path]
    try:
        diagram_main()
    finally:
        sys.argv = old_argv

    # 转换成 2x 高分辨率 PNG（文字更清晰）
    if HAS_CAIROSVG:
        try:
            cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2.0)
            return png_path
        except Exception as e:
            print(f"⚠️ SVG转PNG失败，返回SVG: {e}")
            return svg_path
    else:
        return svg_path


def generate_custom_team(topic, formation="4-3-3"):
    """根据主题和阵型，自动生成占位阵型 JSON（框架模板）"""
    from formation_diagram import FORMATIONS

    topic = topic.strip()
    if not topic:
        topic = "未命名主题"

    slots = FORMATIONS.get(formation, FORMATIONS["4-3-3"])

    # 生成主教练
    coach = {
        "name": f"{topic}的核心思想",
        "desc": f"用一句话统领{topic}的全局"
    }

    # 生成球员（按阵型位置）
    players = []
    seen_pos = set()
    for code, px, py in slots:
        # 同名位置（如两个CB）只生成第一个，第二个留空
        if code in seen_pos:
            continue
        seen_pos.add(code)

        template = POSITION_TEMPLATES.get(code, f"{topic}知识点")
        name = template.format(topic=topic)
        players.append({
            "pos": code,
            "name": name,
            "desc": f"[{code}] {POSITION_DESC.get(code, '知识点')} - 待填充"
        })

    # 生成学习路径（球路）
    flow_map = {
        "4-3-3": ["GK", "CB", "CDM", "CM", "AMD", "CF"],
        "4-2-3-1": ["GK", "CB", "CDM", "AMD", "CF"],
        "4-3-2-1": ["GK", "CB", "CDM", "SS", "CF"],
        "4-4-2": ["GK", "CB", "CM", "CF"],
        "4-5-1": ["GK", "CB", "CDM", "CM", "CF"],
        "4-1-4-1": ["GK", "CB", "CDM", "CM", "CF"],
        "3-5-2": ["GK", "CB", "CDM", "CM", "CF"],
        "3-4-3": ["GK", "CB", "CM", "AMD", "CF"],
    }
    flow = flow_map.get(formation, ["GK", "CB", "CDM", "CF"])

    # 替补席（进阶提示）
    bench = [
        {"name": f"{topic}进阶内容", "desc": "进阶/边角知识点"},
        {"name": f"{topic}争议点", "desc": "待深入讨论"},
    ]

    return {
        "topic": topic,
        "formation": formation,
        "coach": coach,
        "players": players,
        "bench": bench,
        "flow": flow,
    }


def format_player_cards(team_data, is_template=False):
    """格式化球员卡文本"""
    lines = []

    if is_template:
        lines.append("⚠️ **这是自动生成的阵型框架，球员名为占位提示**")
        lines.append("")
        lines.append(f"使用 `kp11 {team_data['topic']}` 可生成完整 ELI5 球员卡内容")
        lines.append("")

    lines.append(f"## 主教练：{team_data['coach']['name']}")
    lines.append(f"> {team_data['coach']['desc']}")
    lines.append("")

    # 按位置分组
    groups = {"门将": [], "后卫": [], "中场": [], "前锋": []}
    pos_group = {
        "GK": "门将",
        "CB": "后卫", "LB": "后卫", "RB": "后卫",
        "CDM": "中场", "CM": "中场", "CAM": "中场", "AMD": "中场",
        "LAM": "中场", "RAM": "中场", "LM": "中场", "RM": "中场",
        "LW": "前锋", "RW": "前锋", "CF": "前锋", "SS": "前锋",
    }
    for p in team_data["players"]:
        g = pos_group.get(p["pos"], "中场")
        groups[g].append(p)

    for group_name, players in groups.items():
        if players:
            lines.append(f"### {group_name}")
            for p in players:
                lines.append(f"- **[{p['pos']}] {p['name']}**：{p['desc']}")
            lines.append("")

    if team_data.get("bench"):
        lines.append("### 替补席（进阶）")
        for p in team_data["bench"]:
            lines.append(f"- **{p['name']}**：{p['desc']}")
        lines.append("")

    return "\n".join(lines)


def format_tactic_board(team_data):
    """格式化战术板"""
    lines = []
    lines.append("## 教练战术板")
    lines.append("")
    lines.append(f"**阵型选择**：{team_data['formation']} - {FORMATION_DESC.get(team_data['formation'], '')}")
    lines.append("")

    if team_data.get("flow"):
        lines.append("**学习路径（球路）**：")
        lines.append(" → ".join(team_data["flow"]))
        lines.append("")

    lines.append("**位置说明**：")
    for pos, desc in list(POSITION_DESC.items())[:6]:
        lines.append(f"- {pos}：{desc}")

    return "\n".join(lines)


def on_select_example(topic):
    """选择示例主题"""
    if not topic or topic not in EXAMPLES:
        return None, "", "", ""

    team_data = EXAMPLES[topic]
    svg_path = generate_diagram(team_data)
    player_cards = format_player_cards(team_data, is_template=False)
    tactic_board = format_tactic_board(team_data)

    return svg_path, player_cards, tactic_board, f"✅ 已加载完整示例：{topic}"


def on_generate_custom(topic, formation):
    """生成自定义主题阵型框架"""
    if not topic or not topic.strip():
        return None, "", "", "⚠️ 请输入主题名称"

    topic = topic.strip()
    team_data = generate_custom_team(topic, formation)
    svg_path = generate_diagram(team_data)
    player_cards = format_player_cards(team_data, is_template=True)
    tactic_board = format_tactic_board(team_data)

    status = f"""✅ 已生成「{topic}」的 {formation} 阵型框架

💡 **下一步**：在 AI Agent 中输入 `kp11 {topic}` 生成完整 ELI5 内容"""

    return svg_path, player_cards, tactic_board, status


# 构建 Gradio 界面
with gr.Blocks(title="KnowPitch 球知 - 用足球阵型学知识", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # ⚽ KnowPitch 球知
    ### 用足球阵型把任何知识讲透

    > Put your knowledge on the pitch. 主教练=核心思想，门将=底层基础，后卫=基础概念，中场=机制方法，前锋=应用结论。

    **触发词**：kp11 / kpt / kpitch / knowpitch
    """)

    with gr.Row():
        with gr.Column(scale=1):
            # === 自定义主题输入 ===
            gr.Markdown("### 🎯 自定义主题（生成框架）")
            topic_input = gr.Textbox(
                label="输入你想学的主题",
                placeholder="例如：量子力学、React Hooks、通货膨胀...",
                lines=2,
            )
            formation_dropdown = gr.Dropdown(
                choices=list(FORMATION_DESC.keys()),
                label="选择阵型（或自动匹配）",
                value="4-3-3",
            )
            custom_btn = gr.Button("⚡ 生成阵型框架", variant="primary")

            gr.Markdown("---")

            # === 预设示例 ===
            gr.Markdown("### 📚 完整示例（含 ELI5 内容）")
            example_dropdown = gr.Dropdown(
                choices=list(EXAMPLES.keys()),
                label="主题示例",
                value=list(EXAMPLES.keys())[0] if EXAMPLES else None,
            )
            load_btn = gr.Button("📊 加载完整示例")

            gr.Markdown("---")
            gr.Markdown("### 📖 位置说明")
            gr.Markdown("""
            - **HC 主教练**：一句话核心思想
            - **GK 门将**：最底层基础
            - **CB 后卫**：核心基础概念
            - **CDM 后腰**：机制/原理
            - **CM 中前卫**：方法/流程
            - **AMD 前腰**：核心思想/理论
            - **LW/RW 边锋**：应用/案例
            - **CF 中锋**：核心结论
            """)

        with gr.Column(scale=2):
            status = gr.Markdown("选择主题后点击生成")
            svg_output = gr.Image(label="阵型图 Formation Diagram", type="filepath")

            with gr.Tabs():
                with gr.Tab("👥 球员卡 Player Cards"):
                    player_cards = gr.Markdown()
                with gr.Tab("📋 战术板 Tactic Board"):
                    tactic_board = gr.Markdown()

    gr.Markdown("---")
    gr.Markdown("""
    ### 🔗 相关链接
    - GitHub：https://github.com/IYABAO/knowpitch
    - SkillHub：搜索 "knowpitch" 或 "球知"
    - 触发方式：在 AI Agent 中输入 `kp11 + 主题`
    """)

    # 自定义主题按钮
    custom_btn.click(
        fn=on_generate_custom,
        inputs=[topic_input, formation_dropdown],
        outputs=[svg_output, player_cards, tactic_board, status],
    )

    # 预设示例按钮
    load_btn.click(
        fn=on_select_example,
        inputs=[example_dropdown],
        outputs=[svg_output, player_cards, tactic_board, status],
    )

    # 页面加载时自动生成第一个示例
    demo.load(
        fn=on_select_example,
        inputs=[example_dropdown],
        outputs=[svg_output, player_cards, tactic_board, status],
    )

if __name__ == "__main__":
    demo.launch()
