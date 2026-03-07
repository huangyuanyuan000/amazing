# Contributing to Amazing

感谢你对 Amazing 项目的贡献！

## 贡献方式

### 1. 报告 Bug

使用 GitHub Issues 报告 Bug:
- 描述问题
- 复现步骤
- 期望行为
- 实际行为
- 环境信息

### 2. 提交功能请求

使用 GitHub Issues 提交功能请求:
- 功能描述
- 使用场景
- 预期收益

### 3. 提交代码

1. Fork 项目
2. 创建分支 (`git checkout -b feature/amazing-feature`)
3. 提交代码 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 开发规范

### 代码风格

- Python: black + ruff
- Go: gofmt + golangci-lint
- TypeScript: eslint + prettier

### 提交规范

遵循 Conventional Commits:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `ci`: CI/CD 相关
- `chore`: 其他修改

### 测试要求

- 单测覆盖率 > 80%
- 所有测试必须通过
- 添加必要的集成测试

## Code Review

所有 PR 必须经过 Code Review:
- 代码质量
- 测试覆盖
- 文档完善
- 性能影响

## 许可证

MIT License
