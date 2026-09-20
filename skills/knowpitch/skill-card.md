# KnowPitch（球知）— Skill Card

- **Type**: OpenClaw Skill / Agent Skill
- **Name**: knowpitch
- **Version**: 1.4.0
- **License**: MIT
- **Homepage**: https://github.com/IYABAO/KnowPitch
- **Online Demo**: https://huggingface.co/spaces/IYABAO/knowpitch-demo
- **Triggers**: `kp11` / `kpt` / `kpitch` / `knowpitch` + 学习主题
- **Language**: 中文为权威版本；`SKILL.en.md` 为英文摘要（跟踪至 v1.3，v1.4+ 以中文为准）
- **Requirements**: Python 3.8+，仅使用标准库（json / sys / html / math / argparse / collections），无第三方依赖

## 一句话介绍

KnowPitch 用足球阵型把任何知识领域拆成"一支球队"来深入学习与讲透：主教练是核心思想，门将是底层基础，后卫是基本概念，中场是机制与方法，前锋是应用与结论；再配 ELI5 风格球员卡、战术板和一张自动生成的 SVG 阵型图。

> Put your knowledge on the pitch — learn anything as a football formation.

## 核心能力

- **8 种阵型**：4-3-3 / 4-2-3-1 / 4-3-2-1 / 4-4-2 / 4-5-1 / 4-1-4-1 / 3-5-2 / 3-4-3，按知识结构形态匹配
- **位置角色映射**：HC / GK / CB / LB / RB / CDM / CM / AMD(CAM) / LAM / RAM / LM / RM / LW / RW / CF / SS / 替补 / B 队
- **SVG 阵型图自动生成**：球员、主教练、空位、替补席、B 队（水平翻转对攻）、学习路径箭头（flow）
- **ELI5 讲解**：假设零背景而非零智商，大白话 + 日常类比，每个球员配"是什么 / 像什么 / 传给谁 / 为什么在这"
- **fail-loud 渲染契约（v1.4）**：同名位置超额、位置不在阵型、flow 非法代码一律 stderr 告警，多出的球员转入替补席，绝不静默丢内容
- **`--strict` 与退出码**：`0` 成功；`2` 输入错误（文件缺失 / 坏 JSON / 非法阵型，中文报错无裸 Traceback）；`3` strict 下存在告警
- **长名字完整显示**：按词/按字折行 + 动态缩字号，不硬截断、不丢字；替补席画布高度自适应
- **受众适配**：`--age` / `--job` / `--grade` 调整语言难度与类比方向
- **三种深度**：`kpt`（≤5 知识点精简阵）、`kp11`（6–11 标准阵）、`kpitch`（>20 启用 B 队）

## 何时使用

- 系统学习、知识梳理、备考复习、教学备课、把一个陌生领域讲给零背景的人
- 需要一张结构化、可视化、可分享的"知识阵型图"

## 何时不要使用

- 快速概念解释（直接用 ELI5）、思维导图、闪卡
- 情感 / 咨询类非知识主题
- 需要精确数据或时效事实的报告（技能本身不联网，事实由调用方核实）

## 包内容

```
skills/knowpitch/
├── SKILL.md                 # 权威技能说明（中文，v1.4）
├── SKILL.en.md              # 英文摘要（跟踪 v1.3，含滞后声明）
├── skill-card.md            # 本卡片
├── scripts/
│   └── formation_diagram.py # SVG 渲染脚本（纯标准库，支持 --strict）
└── references/
    ├── positions.md         # 位置-知识角色映射
    ├── formations.md        # 阵型选择与人数规则
    ├── json-schema.md       # JSON 结构与 v1.4 渲染行为契约
    └── examples.md          # 三个端到端完整示例
```

仓库另含 `tests/`（17 个零依赖 unittest 机械断言）与 GitHub Actions CI（ubuntu + windows × Python 3.8 / 3.11 / 3.12）。

## 快速开始

```bash
python scripts/formation_diagram.py team.json output.svg
python scripts/formation_diagram.py team.json output.svg --strict
```

Windows 上若 `python3` 不存在，按 `python3` → `python` → `py -3` 回退。

## 安全说明

- 渲染脚本只读取指定输入 JSON、只写入指定输出 SVG，**不发起任何网络请求**，不访问技能目录之外的文件，无任何凭据或持久化
- 无第三方依赖，供应链面仅 Python 标准库
- 技能不内置事实数据源；知识点的真实性由调用方检索核实，不确定的内容要求标注"待考证"
