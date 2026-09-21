# Changelog

所有显著的更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 计划中
- [ ] 添加更多阵型（5-3-2）
- [ ] 运行评估并发布结果
- [ ] 支持多语言（日文）
- [ ] HF Demo 自定义主题输入
- [ ] 闪卡/复习卡生成
- [ ] v2.0「The Season」：训练营、学习档案、间隔重复（单独立项）

## [1.5.0] - 2026-09-20

主题：**自测题（kps / quiz）**。在不改动阵型渲染与 v1.4 健壮性的前提下，新增显式触发的出题模式，把"学完一支球队"变成"考一支球队"。

### 新增
- 🧠 **新触发词 `kps`（自测模式）**：`kps 主题` 先排阵容再出 10 道自测题；`kps 自测` 基于当前阵容出题，不重排
- 📐 **固定 10 题、三层分层**：L1 基础层 3 题（门将+后卫，每题 5 分）/ L2 机制层 4 题（中场，每题 10 分）/ L3 应用层 3 题（前锋，每题 15 分），满分 100；题型混合（单选/判断/简答）
- 🎯 **答案 + ELI5 解析 + 回链位置**：先出题藏答案，用户答完逐题讲评，每题回链阵型位置（📍 位置代码 + 球员名）
- 🩺 **评分与阵型体检**：总分按三层列小分，指出哪条线弱 = 哪个位置没踢明白，给下一步学习建议 + 主教练口吻一句话点评
- 📄 `references/quiz.md`：出题契约（触发定位、10 题分布、每题结构、评分体检、6 条红线）
- 📄 SKILL.md 新增 Step 9（quiz 分支）、Step 1 深度模式与输入契约加入 `kps`、frontmatter description 补充自测触发词

### 约束
- 无状态、不写盘：纯对话出题，不生成文件、不存进度
- 不改阵型图：kps 模式只出题讲评，不重新渲染 SVG
- 每题可回链到当前阵型的某个位置；不出纯背诵题；解析与正常阵型学习同一把 ELI5 尺子

## [1.4.0] - 2026-09-19

主题：**绝不静默（fail loud）+ 机械断言锁死 + 文档渐进式披露**。针对第三方评测暴露的"内容静默丢失/被改写"缺陷做健壮性加固，不含视觉布局变更。

### 新增
- 🛡️ **fail-loud 渲染契约**：同名位置超额、位置不在阵型、flow 含非法代码等"内容可能丢失"的情况，脚本一律在 stderr 明确告警（含位置、槽位、多出人数与球员名），不再静默处理
- ✅ **`--strict` 模式与退出码**：`0` 成功；`2` 输入错误（文件缺失 / JSON 损坏 / 阵型不支持，均为中文报错、无裸 Traceback）；`3` strict 模式下存在任何告警（SVG 仍会写出便于排查）
- ✅ **机械断言测试**：`tests/` 17 个标准库 unittest 用例（零依赖），覆盖 T1/T2/T5/T6/T8/N2/N4 缺陷与三个官方示例零警告回归
- ✅ **GitHub Actions CI**：`.github/workflows/test.yml`，ubuntu + windows × Python 3.8/3.11/3.12 矩阵
- ✅ `references/json-schema.md`：JSON 字段、位置代码、8 条渲染行为契约、退出码与 --strict 自检
- ✅ `references/examples.md`：三个端到端完整示例迁出 SKILL.md 独立承载

### 修复
- 🔧 **同名位置超额不再蒸发球员（T1）**：如 4-3-3 只有 2 个 CB 槽却给了 3 个 CB，多出的球员转入替补席并告警，一个都不丢
- 🔧 **CAM/AMD 别名争槽同样处理（N2）**：别名归一后超额球员转替补席并告警
- 🔧 **flow 非法代码不再静默跳过（T6）**：阵型外代码逐条告警（报告原始写法），有效节点不足 2 个时不画箭头并再次告警
- 🔧 **球员名/替补名彻底不再丢字（T2）**：重写换行逻辑，英文按单词、中文按字符完整折行；`fit_font_size()` 按名字长度动态缩字号，长名字（BRAF V600E、Bethesda Classification、Medullary Thyroid Carcinoma）完整显示，无硬截断、无省略号
- 🔧 **替补席长名重叠/溢出画布（T8）**：替补名按可用宽度折行缩字号，画布高度随替补行数自适应
- 🔧 **Windows 命令兼容（N1）**：文档统一命令回退链 `python3` → `python` → `py -3`，frontmatter allowed-tools 同步补充

### 改进
- 📄 SKILL.md 从 918 行精简到 497 行：JSON Schema 与完整示例迁入 references（渐进式披露），Step 7 重写为"读 stderr → 修 JSON 重跑 → --strict 自检"强制流程
- 📄 删除异常表中"阵型图生成失败降级 ASCII 艺术"条款：禁止静默降级，修复前停止交付
- 📄 Step 6 补充 flow 同名多槽默认连第一个槽的语义说明（N3）
- 📄 SKILL.en.md 顶部新增翻译滞后声明：英文跟踪至 v1.3，v1.4+ 以中文 SKILL.md 为权威版

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

[Unreleased]: https://github.com/IYABAO/knowpitch/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/IYABAO/knowpitch/releases/tag/v1.5.0
[1.4.0]: https://github.com/IYABAO/knowpitch/releases/tag/v1.4.0
[1.3.0]: https://github.com/IYABAO/knowpitch/releases/tag/v1.3.0
[1.2.1]: https://github.com/IYABAO/knowpitch/releases/tag/v1.2.1
[1.2.0]: https://github.com/IYABAO/knowpitch/releases/tag/v1.2.0
[1.1.0]: https://github.com/IYABAO/knowpitch/releases/tag/v1.1.0
[1.0.0]: https://github.com/IYABAO/knowpitch/releases/tag/v1.0.0
