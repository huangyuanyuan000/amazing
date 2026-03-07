# Git 规范

本目录包含 Amazing 框架的 Git 工作流规范。

## 规范文件

- `workflow.md` - Git 工作流完整规范
- `commit-message.md` - Commit Message 规范（待补充）
- `branch-strategy.md` - 分支策略详解（待补充）
- `code-review.md` - Code Review 流程（待补充）

## 快速参考

### 分支命名
```bash
feature/user-authentication    # 功能分支
bugfix/login-error             # Bug 修复
hotfix/security-patch          # 紧急修复
release/v1.2.0                 # 发布分支
```

### Commit Message
```
<type>(<scope>): <subject>

feat(auth): 添加 JWT 认证
fix(api): 修复用户查询 500 错误
docs(readme): 更新安装说明
```

### Type 类型
- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档更新
- `style` - 代码格式
- `refactor` - 重构
- `perf` - 性能优化
- `test` - 测试相关
- `chore` - 其他杂项
