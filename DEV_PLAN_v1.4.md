# KnowPitch v1.4.0 开发规划（第三方评测裁决 + 施工计划）

> 输入：4 份第三方文档（评测报告 B−/78、4 评审纪要、v2「The Season」方案、v2.1 修订方案），2026-09 产出。
> 本文档是对第三方意见的**裁决**（不是照单全收）与落到本仓库真实结构的施工计划。
> 制定日期：2026-09-20。

## 0. 关键前提：评测存在版本错位

第三方评测对象是 skillhub 安装的**已发布旧副本 v1.2.0**（路径 `~/.workbuddy/skills/knowpitch__skillhub`，脚本为 1020×980 旧版）。
权威仓库在 09-19 已修过一批缺陷并推送到 GitHub/HF，但**修复版没有重新发布到 skillhub/clawhub/skills.sh**，市场用户拿到的仍是带 bug 的旧版。

因此第三方的 FAIL 项必须逐条与权威代码核对，结论如下。

## 1. 缺陷裁决总表（以权威仓库 `skills/knowpitch/scripts/formation_diagram.py` 实读为准）

| 编号 | 缺陷 | 第三方判定 | 权威仓库现状 | v1.4 处理 |
|---|---|---|---|---|
| T1 | 同名位置超额，球员静默蒸发（3 CB 塞 2 槽，第 3 人消失） | FAIL | **仍存在**：`pos_queue.pop(0)` 用满槽位后残余无收集；`leftovers` 只抓"位置代码不在阵型"的，抓不到超额 | 修：残余球员进替补席 + stderr 警告，不丢一人 |
| T2 | 球员名硬截断丢字（`lines[:2]`） | FAIL | **09-19 已修**：`wrap_name` 完整折行 + `fit_font_size` 动态缩字号 | 补机械断言锁死，防回归 |
| T5 | 非法阵型抛裸 Traceback | FAIL | **仍存在**：`draw_team` 抛 ValueError，但 `main()` 无 try/except | 修：捕获后中文友好报错到 stderr，exit 2 |
| T6 | flow 含阵型外位置代码被静默跳过、球路被改写 | FAIL | **仍存在**：`if k in idx and idx[k]` 静默 continue | 修：未知代码逐条 stderr 警告；有效点 <2 再警告 |
| T8 | 替补溢出固定画布被裁 | FAIL | **已修**：`_bench_rows()` + 画布高度动态计算 | 补机械断言锁死 |
| N1 | `allowed-tools` 写死 `python3`，Windows 无此别名 | 风险 | **成立**：frontmatter 与 Step 7 都写死 python3 | 修：命令回退链 python3→python→py -3；frontmatter 补 python |
| N2 | CAM→AMD 别名归一后超额蒸发 | FAIL | **仍存在**：与 T1 同根因 | 随 T1 一并修复并加用例 |
| N3 | flow 同名多槽只连首槽 `idx[k][0]` | 隐患 | 存在 | 文档化语义（v1.4）；`CB#1/CB#2` 消歧列入 v1.5 |
| N4 | B 队 flow 被忽略（传了主队 flow） | FAIL | **已修**：传 `b_team.get("flow")`，且 B 队 flip 对攻 | 补机械断言锁死 |
| N5 | 主题名未做文件名清洗（C++/A/B/?） | 隐患 | 档案功能尚不存在 | 随 v2.0 档案功能做 |
| N6 | `--resume` 存全文还是重生成 | 设计问题 | 档案功能尚不存在 | v2.0 决策，见 §5 |

### 第三方"架构级"意见裁决

| 意见 | 裁决 | 理由 |
|---|---|---|
| C1 静默 bug 必修 P0 | **采纳** | 与 T1/T5/T6 一致，是 v1.4 主体 |
| C2 训练营不能默认全量输出 | **采纳** | kp11 默认行为不变；训练营显式 `kps`/`--season` 触发，排 v2.0 |
| C3 学习档案默认落盘是负债 | **采纳** | 默认不写盘，`--save` 显式开启，排 v2.0 |
| C4 自评闭环缺独立性 | **部分采纳** | v1.5 自测题答案固定、解析回链位置；"三人小组互评"这类重交互排 v2.0 |
| C5 SKILL.md 必须拆 references 防膨胀 | **采纳** | 当前 918 行（完整示例占约 370 行），拆后目标 ≤500 行 |
| C7 间隔重复（1/3/7 天） | **缓做** | 依赖档案系统，v2.0 |
| C9 L1/L2/L3 是三类验证动作不是层级 | **采纳** | v1.5 自测题按"再认/应用/迁移"三类动作设计 |
| C10 "结论相反"推送前须验证真冲突 | **缓做** | 属训练营/B 队联动，v2.0 |
| C11 判断题不能只给错误陈述（负性记忆） | **采纳** | v1.5 出题规则：错误陈述必须配正确陈述 |
| SkillSpector 安全扫描 | **顺手采纳** | CI 加一步扫描；脚本零依赖无网络，风险面小 |
| DSPy+GEPA / hermes 自动提示演化 | **不采纳** | 个人项目 ROI 低，过度工程 |
| 双盲 A/B benchmark 平台化 | **缓做** | 仓库已有 `formation-workspace/run-evals.py` 框架但 LLM API 全是 TODO、从未跑通；等有 API 预算再接，不是 v1.4 门禁 |
| 阵型图视觉/布局/字体调整 | **不纳入** | 已明确喊停"不纠结图片了"；v1.4 只修健壮性，不碰视觉 |

### 现状盘点中另发现的问题

1. **版本号不一致**：CHANGELOG 已到 1.3.0 + Unreleased（截断修复），SKILL.md frontmatter 仍写 `version: "1.2.0"`。
2. **市场版本滞后**：skillhub/clawhub/skills.sh 上是旧版，09-19 修复未重新发布；skills.sh 的 openclaw verify 曾因缺 `skill-card.md` 失败。
3. **HF clone 滞后**：`knowpitch-demo/formation_diagram.py` MD5 与权威版不一致（旧版）；`skills/scripts`、`hf-space`、仓库外 `knowpitch-hf-deploy` 三处一致（A9542EB3…）。
4. **无 CI**：仓库没有 `.github/workflows/`，脚本缺陷没有任何自动化门禁。
5. **英文版不同步**：`SKILL.en.md` 停在 v1.2.1，之后的 1.3.0/Unreleased 未跟。

## 2. v1.4.0 范围（稳健性版本，本次开发主体）

主题：**绝不静默（fail loud）+ 机械断言锁死 + 市场版本刷新**。
不带任何 flag 的 kp11 默认产出与 v1.3 保持一致（回归红线），本次只修健壮性与工程化，不加学习功能。

### A. 渲染脚本健壮性（`formation_diagram.py`，4 处同步）

- **A1（T1/N2）**：球员落位循环结束后，扫描 `pos_queue` 各位置残余（同位置超额），收集为 overflow 列表；stderr 输出明确警告（位置、槽位数、超额球员名单），超额球员**合流替补席渲染**，与"位置不在阵型"的 leftovers 语义统一，保证不丢一人。
- **A2（T6）**：flow 遍历中收集归一化后仍不在阵型的代码，循环后 stderr 逐条警告（"球路位置 X 不存在于阵型 Y，已跳过"）；有效连接点 <2 时追加"球路未画出"警告。
- **A3（T5）**：`main()` 包 try/except：JSON 解析失败、输入文件不存在、不支持的阵型 → stderr 中文友好错误（含可选阵型列表），`exit 2`，不出裸 Traceback。
- **A4（新增 --strict）**：正常情况下警告不阻断出图（exit 0）；`--strict` 时任何警告 → `exit 3`，供 CI 与 Agent 判定"带警告不得交付"。`draw_team` 改为返回 warnings 列表，main 统一汇总。
- **A5（N3）**：docstring 与 SKILL.md Step 6 写明"flow 中同名多槽位置默认连接第一个槽"。
- 同步点（改完必须 MD5 全一致）：
  1. `skills/knowpitch/scripts/formation_diagram.py`（权威）
  2. `hf-space/formation_diagram.py`
  3. `knowpitch-demo/formation_diagram.py`（先处理滞后 clone）
  4. 仓库外 `knowpitch-hf-deploy/formation_diagram.py`（HF 部署源）

### B. SKILL.md 提示层（fail-loud 传导给 Agent）

- **B1**：Step 7 改为强制流程——渲染后必须读 stderr；出现超额/未知球路/非法阵型警告时，**必须修正 JSON 重渲染，不得带警告交付**；写明 `--strict` 用法。
- **B2（N1）**：前置条件与 Step 7 写命令回退链：先 `python3`，命令不存在则 `python`，再不行 `py -3`；frontmatter `allowed-tools` 补充 `python` 形态。
- **B3**：异常处理表重写：非法阵型/超额/非法 flow 一律"按 stderr 修输入重渲染"，删除"降级 ASCII 艺术"这类静默兜底。
- **B4**：frontmatter version 同步 `1.4.0`。
- **B5（C5 拆分，控体积）**：
  - 「完整示例」（约 526–895 行，~370 行）整段移到 `references/examples.md`，SKILL.md 只保留一个最短示例 + "需要完整范例时读 references/examples.md"；
  - 「阵型图 JSON Schema」移到 `references/json-schema.md`；
  - 拆分后 SKILL.md 目标 ≤500 行，references 互相不嵌套。
- frontmatter 的 `***` 分隔符保持不变（有意为之，勿改成标准 `---`）。

### C. 测试与 CI（本次最高 ROI 的新增资产）

- **C1**：新增 `tests/test_formation_diagram.py`（标准库 unittest，**零第三方依赖**），用 subprocess 打 CLI 层（同时断言 exit code / stderr / SVG），用例：
  - T1：4-3-3 给 3 个 CB → 第 3 人完整出现在 SVG（替补席区）+ stderr 有超额警告；
  - N2：4-2-3-1 给 2 个 CAM/AMD → 同上；
  - T2：`Medullary Thyroid Carcinoma`、`BRAF V600E`、`宋明理学与陆王心学` → 剥离 SVG 标签后名字完整存在、无省略号；
  - T5：formation=`9-9-9` → exit 2 + stderr 友好错误、无 Traceback；
  - T6：flow 含 `ZZ` → stderr 警告；flow 全非法 → "球路未画出"警告；
  - T8：20 个替补 → SVG height 不小于内容底边估算值，全员名字在；
  - N4：B 队 flow → 使用 B 队自己的 flow 且渲染在翻转半场；
  - `--strict`：有警告时 exit 3、无警告时 exit 0；
  - 回归：`hf-space/examples/` 三个 JSON（通货膨胀/机器学习/React Hooks）全部 exit 0、SVG 非空、关键球员名在。
- **C2**：测试夹具放 `tests/fixtures/`。
- **C3**：新增 `.github/workflows/test.yml`：Python 3.8 / 3.11 / 3.12 ×（ubuntu + windows）矩阵跑 unittest；可选加一步 SkillSpector（`uvx` 安全扫描，失败不阻断主流程先观察）。
- **C4**：`formation-workspace/run-evals.py` 保留原位，README 注明"LLM A/B 评测，需自带 API Key，非 CI 门禁"；CI 门禁只认机械断言。

### D. 发布收尾

- D1. 四处脚本同步 + MD5 比对一致；
- D2. CHANGELOG 补 v1.4.0（修复项 + 测试体系 + CI + 拆分）；
- D3. 补 `skill-card.md`（修 skills.sh/openclaw verify 的 card.missing）；
- D4. 本地全测通过后打 tag `v1.4.0`、GitHub Release；
- D5. 重新 publish 到 skillhub.cn / clawhub.ai / skills.sh，**覆盖市场上的带 bug 旧版**；
- D6. HF Space 推送最新脚本并在线验证三个示例；
- D7. SKILL.en.md 按 §5 决策处理。

**验收红线**：① CI 全绿；② 不带 flag 的 kp11 对三个 examples 的 SVG 与 v1.3 视觉/结构一致（只允许健壮性相关差异）；③ 所有 T1/T5/T6 类输入都不再静默，stderr 有人话、exit code 语义明确；④ SKILL.md ≤500 行。

## 3. v1.5.0（学习闭环 · 自测题，v1.4 完成后开工）

- 触发：`kps` 或 `kp11 <主题> --quiz`，**显式触发、无状态、不写盘**；
- 新增 `references/quiz.md`（提示词资产，无新脚本）：
  - 固定 10 题：3 判断 + 4 单选 + 3 情景；
  - L1/L2/L3 定义为三类**验证动作**：再认（判断/单选）→ 应用（情景单选）→ 迁移（开放情景），不是难度层级；
  - C11：判断题错误陈述必须配正确陈述，禁止只给错误命题；
  - 每题给答案 + 一句 ELI5 解析 + 回链阵型位置（"这球该传给哪个位置"）；
  - 答完按位置给"薄弱位置回放"建议（哪些位置该重看），但不做持久化追踪。

## 4. v2.0.0（The Season 训练营 + 学习档案，看 v1.5 反馈再立项）

- 训练营四模块（训练课表 / 自测 / 三人小组演练 / 下一场比赛）、`--season` 显式开启；
- 学习档案：默认**不写盘**，`--save` 才落盘；跨平台路径用 `Path.home()` 下的 `~/.knowpitch/<安全文件名>.json`，主题名做非法字符清洗（N5，覆盖 C++/A/B/? 等）；
- 间隔重复：用 `days[].doneAt` 算 1/3/7 天复习提醒（C7）；
- C10："结论相反"的对阵内容在推送前必须验证两支队确实结论冲突，不能为了做对攻硬凑；
- N3 增强：flow 支持 `CB#1/CB#2` 显式消歧。

## 5. 需要你拍板的两个问题（附我的推荐）

1. **英文版 SKILL.en.md 怎么办？**
   - 推荐：**保留文件 + 顶部加滞后声明**（"English version tracks v1.3; Chinese is canonical for v1.4+"），v1.4 不全文翻译，等 v2.0 功能稳定后统一同步。
   - 理由：双份维护近千行文档成本高、过去已经不同步；核心用户盘是中文，滞后声明比错误的"看似最新"更诚实。
   - 备选：现在就全文同步（多花约一倍文档工时）；或直接删除英文版。
2. **v2.0 的 `--resume` 档案存什么？**（不阻塞 v1.4，提前定方向）
   - 推荐：**存结构不存全文**——档案只存阵型 JSON、答题记录、时间戳；正文每次重新生成（保证讲法最新、档案体积小）。
   - 备选：存全量正文，真续跑但档案大、可能复现旧错误。

## 6. 建议执行顺序

v1.4 内部按 A（脚本）→ C（测试，边修边锁）→ B（SKILL.md）→ D（发布）推进；
A/C 在本地全部跑绿之前不打 tag、不发市场。预计 v1.4 是一个可以当天收口的小版本，v1.5 紧随其后，v2.0 单独立项。
