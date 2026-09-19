# Changelog

所有显著的更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 修复
- 🔧 **球员名/替补名彻底不再丢字**：重写换行逻辑，英文按单词、中文按字符完整折行；新增 `fit_font_size()` 按名字长度动态缩小字号，长名字（如 BRAF V600E、Bethesda VI、Medullary Thyroid Carcinoma）完整显示，不再硬截断或加省略号
- 🔧 **替补席长名重叠**：替补名按可用宽度折行缩字号，横向间距与换行行距自适应；画布高度随替补席行数自动扩展，内容不再被裁切

### 计划中
- [ ] 添加更多阵型（4-1-4-1、5-3-2）
- [ ] 运行评估并发布结果
- [ ] 支持多语言（日文）
- [ ] HF Demo 自定义主题输入
- [ ] 闪卡/复习卡生成

## [1.3.0] - 2026-09-18

### 新增
- ✅ **Hugging Face Space Demo**：在线体验阵型图生成（https://huggingface.co/spaces/IYABAO/knowpitch-demo）
- ✅ **多平台发布**：GitHub、skillhub.cn（球知）、clawhub.ai、skills.sh
- ✅ **项目图标**：1024x1024 足球+灯泡主题图标

### 修复（阵型图渲染）
- 🔧 **标题与主教练重合**：标题移到最上方，主教练移到标题下方，完全分开
- 🔧 **替补席标题与内容重合**：间距从 8px 增加到 22px
- 🔧 **足球场地线条缺失**：修复 pitch_lines() 未被调用的 bug，现在有完整草地条纹、中线、中圈、禁区、球门
- 🔧 **球员名硬截断**：首发从 4 字符→6 字符，替补从 5 字符→8 字符，支持 2 行，超出用省略号

### 改进
- 🔧 画布高度从 980→1140，给替补席留更多空间
- 🔧 球员圈半径从 24→22，更紧凑
- 🔧 替补席显示人数：替补席（N人）
- 🔧 学习路径箭头更细（4px），不遮挡球员

### 验证
- ✅ HF Space Demo 正常运行（ZeroGPU 兼容）
- ✅ 3 个预设示例（通货膨胀/机器学习/React Hooks）
- ✅ 阵型图渲染问题全部修复

## [1.2.1] - 2026-09-17

### 新增
- ✅ **英文支持**：SKILL.en.md（完整英文版，25.4 KB，529 行，3 个完整示例）
- ✅ **发布介绍文章**：PUBLISH_ARTICLE.md（完整发布文案，含示例、对比、Roadmap）
- ✅ **GitHub 发布说明**：RELEASE_NOTES.md（v1.2.0 发布说明）

### 验证
- ✅ SKILL.en.md 开头正确（---）
- ✅ 3 个完整英文示例（Machine Learning/Inflation/Database Indexing --age5）
- ✅ 中英文版本功能对齐

## [1.2.0] - 2026-09-17

### 新增（受众适配参数）
- ✅ **--age 参数**：受众年龄（5/10/15/18/25+），自动调整语言难度
- ✅ **--job 参数**：受众职业（manager/developer/student），自动调整类比方向
- ✅ **--grade 参数**：受众年级（5th/college/grad），自动调整专业深度
- ✅ **受众适配规则表**：7 条规则，明确每个参数的语言/类比调整方式
- ✅ **第三个完整示例**：数据库索引（kp11 --age 5，给 5 岁小孩讲，5 人精简阵容）
- ✅ **质量自查清单扩展**：从 9 项增加到 10 项，增加受众参数应用检查

### 改进
- 🔧 README.md 完善：增加受众适配参数说明、KnowPitch vs ELI5 对比表、质量评分、Roadmap
- 🔧 输入示例从 4 个增加到 7 个（增加 3 个受众适配示例）
- 🔧 Step 1/Step 2/Step 5 增加受众参数处理逻辑

### 验证
- ✅ quick_validate.py 验证通过
- ✅ 3 个完整示例（机器学习/通货膨胀/数据库索引--age5）
- ✅ 10 项质量自查清单

## [1.1.0] - 2026-09-17

### 新增（基于 skill-assistant-pro 质检优化）
- ✅ **NEVER 反模式清单**（8 条，每条带 WHY 和错误示例）— D5 +45 分
- ✅ **输入输出契约**（参数表 + JSON Schema + 边界值说明）— D4 +25 分
- ✅ **异常处理章节**（5 种异常情况的处理方式表格）— D3 +8 分
- ✅ **适用边界和前置条件**（适合/不适合场景 + Python 依赖）— D2 +10 分
- ✅ **核心思维模式**（排阵型前三问：门将/前锋/中场）— D2 +5 分
- ✅ **阵型选择决策树**（ASCII 决策树 + 阵型权衡分析）— D0 +10 分
- ✅ **完整示例**（机器学习 11 人完整阵容 + 通货膨胀精简阵容，无 "..."）— D4 +10 分
- ✅ **质量自查清单扩展**（从 7 项增加到 9 项，增加 NEVER 检查和输球方式检查）

### 改进
- 🔧 frontmatter 增加 Negative Boundaries（Do NOT use for）— D1 +10 分
- 🔧 frontmatter 增加 allowed-tools 和 metadata（version/category/compatibility/tags）
- 🔧 description 精简触发词，从 15+ 减少到核心 8 个，提升路由准确率
- 🔧 SKILL.md 从 8.3KB 增加到 11.4KB，但仍在 500 行以内（320 行）

### 质检结果
- **优化前：71.3/100（C+）**
- **优化后：85.6/100（B+）**，提升 +14.3 分
- 最大提升：D5 反模式清单（40→85，+45）
- 质检工具：skill-assistant-pro v2.1.0（10 维度 D0-D9）

## [1.0.0] - 2026-09-17

### 新增
- ✅ 初始版本发布
- ✅ 8 种阵型支持（4-3-3/4-2-3-1/4-3-2-1/4-4-2/4-5-1/4-1-4-1/3-5-2/3-4-3）
- ✅ ELI5 内核集成（零背景可懂 + 日常类比）
- ✅ SVG 阵型图自动生成（含教练/球员/替补/学习路径）
- ✅ 快捷命令：kp11 / kpt / kpitch / knowpitch
- ✅ 完整评估系统（evals.json + run-evals.py + LLM Judge）
- ✅ 6 个测试用例（43 个 assertions）
- ✅ 位置映射表（12 个位置 + 职能定义）
- ✅ 阵型选择规则（按知识结构形态匹配）
- ✅ B 队支持（>20 个知识点时启用）
- ✅ 球员卡模板（是什么/像什么/传给谁/为什么在这）
- ✅ 教练战术板（学习路径/关键连线/三种输球方式）

### 技术
- 阵型图脚本：Python + SVG（无外部依赖）
- 评估脚本：Python + JSON（可接入任意 LLM API）
- 技能格式：标准 SKILL.md（YAML frontmatter + Markdown）

### 文档
- README.md（项目介绍/安装/使用/评估）
- CONTRIBUTING.md（贡献指南）
- eval-workflow.md（评估工作流文档）
- eval-results.md（评估结果模板）

[Unreleased]: https://github.com/IYABAO/knowpitch/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/IYABAO/knowpitch/releases/tag/v1.0.0
