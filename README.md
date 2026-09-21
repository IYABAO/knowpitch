# KnowPitch — 阵型学习法

> **Put your knowledge on the pitch.**（把你的知识放上球场）

用足球阵型的方式，把任何知识领域拆解成"一支球队"来深入学习与讲透。
内化了 ELI5 内核：假设零背景、不是零智商，用大白话+日常类比讲懂任何知识。

> 对标项目：[DreambigOu/ELI5](https://github.com/DreambigOu/ELI5)（1.3k ⭐）

---

## 🎮 在线体验

**[👉 Hugging Face Space Demo](https://huggingface.co/spaces/IYABAO/knowpitch-demo)** — 无需安装，直接体验阵型图生成

---

## 📦 已发布平台

| 平台 | 链接 | 说明 |
|------|------|------|
| GitHub | [IYABAO/knowpitch](https://github.com/IYABAO/knowpitch) | 主仓库 |
| skillhub.cn | 球知 | 中文名"球知" |
| clawhub.ai | 已发布 | |
| skills.sh | 已发布 | |

---

## ✨ 特性

- 🎯 **阵型化学习**：8 种阵型（4-3-3/4-2-3-1/3-5-2等）匹配不同知识结构
- 🧑‍🏫 **ELI5 内核**：零背景可懂，大白话+日常类比
- 🎨 **可视化输出**：自动生成 SVG 阵型图（含教练/球员/替补/学习路径）
- 📋 **结构化球员卡**：每个知识点 = 是什么/像什么/传给谁/为什么在这
- 👥 **受众适配**：`--age` / `--job` / `--grade` 参数，自动调整语言难度和类比方向
- 🧪 **完整评估系统**：evals.json + LLM Judge + A/B 测试
- 🔧 **快捷命令**：kp11 / kpt / kpitch / knowpitch
- 🌍 **多语言支持**：中文为主，英文触发词已预留

---

## ⚽ 支持的阵型

| 阵型 | 适合的知识结构 |
|------|----------------|
| 4-3-3 | 均衡：基础/机制/应用三层均衡 |
| 4-2-3-1 | 单一主结论，背后三个创造者 |
| 4-3-2-1 | 主结论明确，且有两个重要衍生结论 |
| 4-4-2 | 前后两大平行板块（理论 vs 实践） |
| 4-5-1 | 机制/方法特别多，主结论只有一个 |
| 4-1-4-1 | 单后腰护航一条线，四个并列过程 |
| 3-5-2 | 机制/过程密集，且结论有两个 |
| 3-4-3 | 基础概念不多，但应用/案例非常多 |

---

## 🚀 快捷命令

```bash
# 默认阵型学习（4-3-3，标准深度）
kp11 讲一下机器学习

# 快速模式（精简阵容，≤5 个知识点）
kpt 讲一下通货膨胀

# 完整模式（启用 B 队，全面深入）
kpitch 讲一下深度学习

# 完整项目名触发
knowpitch 讲一下 React Hooks

# 自然语言触发
用足球阵型讲一下数据库索引
把这个概念排成球队给我讲

# 受众适配（给不同人讲）
kp11 数据库索引 --age 5          # 给 5 岁小孩讲
kp11 代码库结构 --job manager    # 给经理讲（商务化）
kp11 Git 合并冲突 --grade 5th    # 给 5 年级学生讲
```

---

## 👥 受众适配参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--age` | 受众年龄，调整语言难度 | `--age 5` / `--age 10` / `--age 15` / `--age 25+` |
| `--job` | 受众职业，调整类比方向 | `--job manager` / `--job developer` / `--job student` |
| `--grade` | 受众年级，调整专业深度 | `--grade 5th` / `--grade college` / `--grade grad` |

**适配规则：**
- `--age 5`：极简单词，玩具/动画类比，每句 ≤10 字
- `--age 10`：简单词汇，学校/游戏类比，每句 ≤15 字
- `--job manager`：商业框架，ROI/风险/决策导向，避免代码
- `--job developer`：技术类比，代码/架构/性能导向

---

## 📦 安装

### 方式 1：复制到 skills 目录

```bash
git clone https://github.com/IYABAO/knowpitch.git
cp -r knowpitch/skills/knowpitch ~/.your-agent/skills/knowpitch
```

### 方式 2：通过 Skill 市场安装

```bash
skillhub install knowpitch
```

### 前置要求

- Python 3.8+（用于生成阵型图 SVG）
- 支持 Skill 系统的 AI Agent（如 Claude、Doubao 等）

---

## 📝 输出示例

### 机器学习（kp11，4-2-3-1 + B 队）

**主教练**：机器学习 = 让电脑从数据中自己找规律，而不是人写死规则

**阵型图**：
[SVG 阵型图 - 自动生成]

**首发阵容（4-2-3-1）**：

| 位置 | 知识点 | 一句话解释 |
|------|--------|-----------|
| GK | 什么是"从数据找规律" | 电脑看很多例子，自己总结出规律 |
| CB | 特征/标签/训练集 | 练习题+答案+题库 |
| CDM | 梯度下降 | 蒙眼下山，每步往最陡的方向走 |
| CDM | 损失函数 | 考试扣分，错一题扣一分 |
| AMD | 监督学习 | 做练习题对答案，做多了就会考试了 |
| AMD | 无监督学习 | 给一堆水果，自己按颜色分组 |
| AMD | 强化学习 | 训练小狗，做对给零食 |
| LW | 分类与回归 | 选择题 vs 填空题 |
| RW | 聚类与降维 | 整理衣柜 vs 厚书浓缩 |
| CF | 预测 | 学会了知识点后去考试 |

**教练战术板**：
- 球路：GK → CB → CDM → AMD → CF
- 关键连线：梯度下降 ↔ 损失函数
- 三种输球方式：过拟合/欠拟合/数据泄露

**B 队（3-4-3）**：CV/NLP/推荐系统 + 正则化/集成学习/深度学习

---

### 数据库索引（kp11 --age 5，给 5 岁小孩讲）

**主教练**：索引 = 书的目录，找东西不用一页页翻

**首发阵容（精简 5 人）**：
- GK【什么是索引】就像书前面的目录
- CB【没有索引会怎样】要一页一页翻，很慢很慢
- CDM【为什么索引快】目录告诉你在哪一页，直接翻过去
- LW【生活中的索引】字典的拼音检字表、超市的分类牌
- CF【结果】找东西又快又准

---

## 🆚 KnowPitch vs ELI5

| 维度 | KnowPitch | ELI5 |
|------|-----------|------|
| **核心隐喻** | 足球阵型（空间化） | 5 岁小孩（语言简化） |
| **输出结构** | 阵型图 + 球员卡 + 战术板 | 纯文本解释 |
| **可视化** | ✅ SVG 阵型图 | ❌ 无 |
| **知识关系** | ✅ 位置职能 + 学习路径 + 关键连线 | ❌ 无显式关系 |
| **受众适配** | ✅ --age/--job/--grade | ✅ 内置 age 参数 |
| **B 队扩展** | ✅ >20 知识点自动拆分 | ❌ 无 |
| **评估系统** | ✅ A/B + LLM Judge | ✅ A/B + LLM Judge |
| **快捷触发** | kp11/kpt/kpitch | eli5 |
| **GitHub Stars** | 0（新项目） | 1.3k |

**KnowPitch 的差异化优势：**
1. **空间化记忆**：知识点有"位置"，大脑更容易记住
2. **知识关系可视化**：阵型图一眼看出"谁依赖谁"
3. **结构化学习系统**：主教练→门将→后卫→中场→前锋，学习路径清晰
4. **可扩展**：B 队机制支持大型知识体系

---

## 🧪 评估

### 评估系统

对标 ELI5 的评估系统，包含：
- `formation-workspace/evals.json`：测试用例（6 个场景，43 个 assertions）
- `formation-workspace/run-evals.py`：评估运行脚本（A/B 测试 + LLM Judge）
- `formation-workspace/eval-workflow.md`：评估工作流文档
- `formation-workspace/eval-results.md`：评估结果文档

### 评估流程

```
加载 evals.json → 构建配置（A/B）→ 运行每个测试
    ↓
保存响应（response.md + timing.json）
    ↓
LLM Judge 评分（每个 assertion 判 PASS/FAIL）
    ↓
解析评分 → 通过率汇总 → 保存产物
```

### 质量评分

| 评分维度 | 分数 | 说明 |
|----------|------|------|
| skill-assistant-pro 10 维度 | **85.6/100 (B+)** | 优化后评分 |
| SkillLens 五维评测 | **80.9/100 (B+)** | 市场竞争力 75、效果稳定性 72 |
| A/B 测试（3 主题） | **87.2% pass** | vs ELI5 80.0%，+7.2% |

> 详细评估结果见 [formation-workspace/eval-results.md](formation-workspace/eval-results.md)

---

## 📁 项目结构

```
knowpitch/
├── skills/knowpitch/          # 技能本体
│   ├── SKILL.md                # 主技能文件（v1.2.0）
│   ├── references/
│   │   ├── formations.md       # 阵型规则
│   │   └── positions.md        # 位置映射
│   └── scripts/
│       └── formation_diagram.py # 阵型图生成（已测试）
├── formation-workspace/         # 评估工作区
│   ├── evals.json               # 测试用例（6 个，43 assertions）
│   ├── run-evals.py             # 评估运行脚本
│   ├── eval-workflow.md         # 评估工作流文档
│   └── eval-results.md          # 评估结果文档
├── examples/                     # 示例集
├── COMPARISON.md                 # kp11 vs ELI5 对比报告
├── COMPARISON_v2.md              # 多平台对比评测报告
├── EVALUATION.md                 # SkillLens 评测报告
├── OPTIMIZATION_PLAN.md          # 优化方案
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

---

## 🛠️ 开发

### 生成阵型图

```bash
cd skills/knowpitch
python3 scripts/formation_diagram.py team.json output.svg
```

### 运行评估

```bash
cd formation-workspace
python3 run-evals.py --config evals.json --output results/
```

> 注意：运行评估需要配置 LLM API key（见 run-evals.py 中的 TODO）

### 验证 Skill

```bash
python3 ~/.skills/skill-creator-for-work/scripts/quick_validate.py skills/knowpitch
```

---

## 🤝 贡献

PRs welcome！改进方向：
- 添加更多阵型（如 4-1-4-1、5-3-2）
- 添加更多示例
- 改进评估覆盖
- 支持多语言（英文/日文等）
- 阵型图样式主题
- 接入更多 LLM API 用于评估

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📋 Roadmap

- [x] v1.0.0：基础阵型学习法 + SVG 生成
- [x] v1.1.0：质量优化（NEVER 清单、输入输出契约、完整示例）
- [x] v1.2.0：受众适配参数（--age/--job/--grade）
- [x] v1.2.1：英文版 SKILL.en.md
- [x] v1.3.0：HF Space Demo + 多平台发布（skillhub / clawhub / skills.sh）
- [x] v1.4.0：fail-loud 渲染契约（绝不静默丢球员）+ 17 单测 + CI
- [x] v1.5.0：kps 自测题（10 题三层 L1/L2/L3 + 评分配阵型体检）
- [ ] v1.6.0：收尾（英文版同步 v1.5、市场重发布）+ HF Demo 自定义主题输入
- [ ] v1.7.0：闪卡/复习卡（学→考→练闭环）+ 5-3-2 阵型
- [ ] v1.8.0+：接入 LLM 评估发真实数据、多语言（日文）
- [ ] v2.0「The Season」：训练营、学习档案、间隔重复（单独立项）

---

## 🙏 致谢

- 灵感来源：[DreambigOu/ELI5](https://github.com/DreambigOu/ELI5)
- 评估系统设计：参考 ELI5 的 eli5-workspace
- 质量评测：skill-assistant-pro、SkillLens

---

## 📄 License

MIT
