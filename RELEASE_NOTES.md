# KnowPitch v1.2.0 发布说明

## 🎉 发布概要

KnowPitch 是一个用足球阵型把知识领域拆解成"一支球队"来深入学习与讲透的 AI Agent Skill。

**Slogan：Put your knowledge on the pitch.**（把你的知识放上球场）

## ✨ 核心特性

- 🎯 **8 种阵型**匹配不同知识结构（4-3-3/4-2-3-1/3-5-2 等）
- 🧑‍🏫 **ELI5 内核**：零背景可懂，大白话+日常类比
- 🎨 **可视化输出**：自动生成 SVG 阵型图（含教练/球员/替补/学习路径）
- 📋 **结构化球员卡**：每个知识点 = 是什么/像什么/传给谁/为什么在这
- 👥 **受众适配**：`--age` / `--job` / `--grade` 参数，自动调整语言难度
- 🌍 **中英文支持**：SKILL.md（中文）+ SKILL.en.md（英文）
- 🧪 **完整评估系统**：evals.json + LLM Judge + A/B 测试
- 🔧 **快捷命令**：kp11 / kpt / kpitch / knowpitch

## 📦 安装

```bash
git clone https://github.com/IYABAO/knowpitch.git
cp -r knowpitch/skills/knowpitch ~/.your-agent/skills/knowpitch
```

## 🚀 快速开始

```bash
# 默认阵型学习（4-3-3，标准深度）
kp11 讲一下机器学习

# 快速模式（精简阵容，≤5 个知识点）
kpt 讲一下通货膨胀

# 完整模式（启用 B 队，全面深入）
kpitch 讲一下深度学习

# 受众适配（给 5 岁小孩讲）
kp11 数据库索引 --age 5
```

## 📊 质量评分

| 评分维度 | 分数 |
|----------|------|
| skill-assistant-pro 10 维度 | **85.6/100 (B+)** |
| SkillLens 五维评测 | **80.9/100 (B+)** |
| A/B 测试（3 主题） | **87.2% pass**（vs ELI5 80.0%） |

## 🆚 与 ELI5 的对比

| 维度 | KnowPitch | ELI5 |
|------|-----------|------|
| 核心隐喻 | 足球阵型（空间化） | 5 岁小孩（语言简化） |
| 可视化 | ✅ SVG 阵型图 | ❌ 无 |
| 知识关系 | ✅ 位置+路径+连线 | ❌ 无显式关系 |
| B 队扩展 | ✅ >20 知识点自动拆分 | ❌ 无 |
| GitHub Stars | 0（新项目） | 1.3k |

## 📁 项目结构

```
knowpitch/
├── skills/knowpitch/
│   ├── SKILL.md                # 中文版（v1.2.0）
│   ├── SKILL.en.md             # 英文版（v1.2.0）
│   ├── references/
│   │   ├── formations.md
│   │   └── positions.md
│   └── scripts/
│       └── formation_diagram.py
├── formation-workspace/
│   ├── evals.json
│   ├── run-evals.py
│   └── eval-results.md
├── README.md
├── PUBLISH_ARTICLE.md         # 发布介绍文章
├── CHANGELOG.md
├── CONTRIBUTING.md
└── LICENSE
```

## 🛣️ Roadmap

- [x] v1.0.0：基础阵型学习法 + SVG 生成
- [x] v1.1.0：质量优化（NEVER 清单、输入输出契约、完整示例）
- [x] v1.2.0：受众适配参数（--age/--job/--grade）
- [x] v1.2.1：英文支持
- [ ] v1.3.0：评估系统接入 LLM API，发布真实效果数据
- [ ] v1.4.0：发布到 Skill 市场
- [ ] v1.5.0：更多阵型 + 阵型图样式主题

## 🤝 贡献

PRs welcome！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 🙏 致谢

- 灵感来源：[DreambigOu/ELI5](https://github.com/DreambigOu/ELI5)
- 质量评测：skill-assistant-pro、SkillLens

## 📄 License

MIT
