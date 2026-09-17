# KnowPitch 评估工作流

> 对标 ELI5 的评估系统设计

## 评估目标

验证 KnowPitch 技能是否能有效提升知识学习的质量和结构化程度。

## 评估方法

### A/B 测试

- **A 组（With Skill）**：使用 KnowPitch 技能回答
- **B 组（Without Skill）**：不使用技能，直接回答

### LLM Judge

使用 LLM 作为评判者，对每个 assertion 判 PASS/FAIL。

## 评估流程

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 加载 evals.json                                          │
│    - 6 个测试用例                                           │
│    - 每个用例 5-10 个 assertions                            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. 构建 A/B 配置                                            │
│    - With Skill: 附加技能上下文                             │
│    - Without Skill: 直接提问                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. 运行每个测试                                             │
│    - 调用 LLM 生成响应                                      │
│    - 保存 response.md + timing.json                         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. LLM Judge 评分                                           │
│    - 对每个 assertion 判 PASS/FAIL                          │
│    - 保存评分理由                                           │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. 汇总通过率                                               │
│    - With Skill vs Without Skill                            │
│    - 计算 Delta                                             │
│    - 保存 results.json                                      │
└─────────────────────────────────────────────────────────────┘
```

## 测试用例设计

| ID | 名称 | 场景 | Assertions 数 |
|----|------|------|--------------|
| eval-001 | 机器学习基础 | 默认模式（kp11） | 10 |
| eval-002 | 通货膨胀 | 快速模式（kpt） | 7 |
| eval-003 | 深度学习 | 完整模式（kpitch，B队） | 8 |
| eval-004 | React Hooks | 技术主题 | 6 |
| eval-005 | 数据库索引 | 自然语言触发 | 6 |
| eval-006 | 量子计算 | ELI5 质量检查 | 6 |

## Assertion 分类

### 结构类（40%）
- 输出包含主教练/门将/后卫/中场/前锋
- 输出包含教练战术板
- 输出包含阵型图

### 内容类（30%）
- 每个球员有大白话解释
- 有日常类比
- 知识点数量符合模式要求

### 质量类（30%）
- 没有未解释的专业术语
- 位置分配符合职能逻辑
- 没有牺牲准确性

## 运行评估

```bash
# 运行所有评估（需要接入 LLM API）
python run-evals.py --config evals.json --output results/

# 启用 LLM Judge
python run-evals.py --config evals.json --judge --output results/

# 只运行单个测试
python run-evals.py --config evals.json --single eval-001
```

## 输出结构

```
results/
├── eval-001/
│   ├── with-skill/
│   │   ├── response.md
│   │   └── timing.json
│   └── without-skill/
│       ├── response.md
│       └── timing.json
├── eval-002/
│   └── ...
└── results.json
```

## 接入 LLM API

编辑 `run-evals.py` 中的 `run_llm()` 方法：

```python
def run_llm(self, prompt: str) -> str:
    import openai
    client = openai.OpenAI(api_key="your-api-key")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## 评估标准

| 通过率 | 等级 | 说明 |
|--------|------|------|
| ≥ 90% | 优秀 | 技能效果显著 |
| 75-89% | 良好 | 技能有效，有改进空间 |
| 60-74% | 一般 | 技能有一定效果 |
| < 60% | 需改进 | 技能效果不明显 |

## Delta 标准

| Delta | 说明 |
|-------|------|
| ≥ +30% | 技能效果非常显著 |
| +15-29% | 技能效果显著 |
| +5-14% | 技能有一定效果 |
| < +5% | 技能效果不明显 |
