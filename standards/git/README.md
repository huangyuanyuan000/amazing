# Git 提交规范

## Conventional Commits

### 格式
```
<type>(<scope>): <subject>

[body]

[footer]
```

### Type
| Type | 描述 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add JWT authentication` |
| `fix` | Bug 修复 | `fix(data): fix pagination offset error` |
| `docs` | 文档更新 | `docs(api): update swagger annotations` |
| `style` | 代码风格 | `style(common): format with black` |
| `refactor` | 重构 | `refactor(compute): extract scheduler` |
| `test` | 测试 | `test(model): add deploy unit tests` |
| `ci` | CI/CD | `ci: add github actions pipeline` |
| `chore` | 构建/工具 | `chore: update dependencies` |
| `perf` | 性能优化 | `perf(inference): optimize batch size` |
| `revert` | 回滚 | `revert: revert "feat(auth): ..."` |

### Scope（模块范围）
`common` | `compute` | `data` | `training` | `model-service` | `frontend` | `deploy` | `docs`

### 分支规范
| 分支 | 用途 | 命名 |
|------|------|------|
| `main` | 稳定版本 | - |
| `develop` | 开发集成 | - |
| `feature/*` | 功能开发 | `feature/auth-jwt` |
| `fix/*` | Bug 修复 | `fix/pagination-error` |
| `hotfix/*` | 紧急修复 | `hotfix/security-patch` |
| `release/*` | 发布准备 | `release/v1.2.0` |

### Git Hooks (pre-commit)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
    - id: conventional-pre-commit
      stages: [commit-msg]
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
    - id: ruff
    - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
    - id: trailing-whitespace
    - id: end-of-file-fixer
    - id: check-yaml
    - id: check-json
    - id: check-added-large-files
      args: ['--maxkb=1000']
    - id: detect-private-key
```

### 回滚流程
```bash
# 1. 查看提交历史，定位问题
git log --oneline -20

# 2. 创建回滚分支
git checkout -b revert/issue-description

# 3. 回滚指定提交
git revert <commit-hash>
# 或回滚多个提交
git revert <oldest-hash>..<newest-hash>

# 4. 验证回滚结果
make test

# 5. 提交回滚
git push origin revert/issue-description

# 6. 创建 PR 合并回滚
```
