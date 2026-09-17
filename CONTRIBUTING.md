# 贡献指南

感谢你对 KnowPitch 的兴趣！我们欢迎各种形式的贡献。

## 🚀 如何贡献

### 1. 报告 Bug
- 使用 GitHub Issues 报告 bug
- 请包含：复现步骤、预期行为、实际行为、环境信息

### 2. 提交功能请求
- 使用 GitHub Issues 提交功能请求
- 请说明：使用场景、期望行为、示例

### 3. 提交代码
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📋 贡献方向

### 阵型扩展
- 添加新阵型（如 4-1-4-1、5-3-2、4-2-2-2）
- 优化现有阵型的位置坐标
- 添加阵型选择逻辑

### 示例集
- 添加更多主题的完整示例（技术/科学/历史/艺术等）
- 优化现有示例的 ELI5 解释质量
- 添加多语言示例

### 评估系统
- 增加测试用例覆盖
- 优化 LLM Judge 提示词
- 添加自动化评估 CI

### 可视化
- 优化阵型图 SVG 样式
- 添加主题/配色方案
- 支持导出 PNG/PDF

### 文档
- 完善使用教程
- 添加最佳实践指南
- 翻译文档（英文/日文等）

## ✅ 代码规范

### Python
- 遵循 PEP 8
- 使用类型注解
- 添加 docstring

### Markdown
- 使用中文（项目主要语言）
- 标题层级清晰
- 代码块标注语言

## 🧪 测试

提交前请确保：
1. 技能文件通过 `quick_validate.py` 验证
2. 阵型图脚本可以正常运行
3. 示例输出符合输出模板

## 📝 提交信息规范

```
<type>(<scope>): <subject>

类型：
- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- style: 格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

示例：
- feat(formation): 添加 4-1-4-1 阵型
- fix(diagram): 修复中文换行问题
- docs(readme): 更新安装说明
```

## 🤝 行为准则

- 尊重他人，友善交流
- 接受建设性批评
- 关注对社区有益的事情
- 对其他成员表示同理心

## 📄 许可证

通过贡献，你同意你的贡献将根据 MIT 许可证获得许可。

## ❓ 问题

有任何问题，请开启 GitHub Issue 或联系维护者。
