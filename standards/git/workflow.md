# Git 工作流规范

基于 Conventional Commits 和 Git Flow，适配 Amazing 框架的协作模式。

## 1. 分支策略

### 主要分支
- `main` - 生产环境分支，只接受 merge，不直接提交
- `develop` - 开发主分支，集成所有功能

### 辅助分支
- `feature/*` - 功能开发分支
- `bugfix/*` - Bug 修复分支
- `hotfix/*` - 紧急修复分支
- `release/*` - 发布准备分支

### 分支命名规范
```bash
feature/user-authentication    # 功能分支
bugfix/login-error             # Bug 修复
hotfix/security-patch          # 紧急修复
release/v1.2.0                 # 发布分支
```

## 2. Commit Message 规范

### 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型
| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): 添加 JWT 认证` |
| `fix` | Bug 修复 | `fix(api): 修复用户查询 500 错误` |
| `docs` | 文档更新 | `docs(readme): 更新安装说明` |
| `style` | 代码格式（不影响逻辑） | `style: 格式化代码` |
| `refactor` | 重构 | `refactor(user): 提取用户服务层` |
| `perf` | 性能优化 | `perf(db): 优化用户查询索引` |
| `test` | 测试相关 | `test(auth): 添加登录测试用例` |
| `build` | 构建系统 | `build: 升级 webpack 到 5.0` |
| `ci` | CI/CD 配置 | `ci: 添加 GitHub Actions 工作流` |
| `chore` | 其他杂项 | `chore: 更新依赖` |
| `revert` | 回滚 | `revert: 回滚 feat(auth)` |

### Scope 范围
根据项目模块定义，例如：
- `auth` - 认证模块
- `user` - 用户模块
- `api` - API 层
- `db` - 数据库
- `ui` - 前端 UI
- `deploy` - 部署相关

### 示例
```bash
# 好的 commit
feat(auth): 添加 OAuth2.0 第三方登录支持

实现了 Google 和 GitHub 的 OAuth2.0 登录流程：
- 添加 OAuth2.0 客户端配置
- 实现授权码流程
- 添加用户绑定逻辑

Closes #123

# 不好的 commit
update code
fix bug
修改文件
```

## 3. 工作流程

### 功能开发流程
```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/user-profile

# 2. 开发并提交
git add .
git commit -m "feat(user): 添加用户资料编辑功能"

# 3. 推送到远程
git push origin feature/user-profile

# 4. 创建 Pull Request
# 在 GitHub/GitLab 上创建 PR，目标分支为 develop

# 5. Code Review 通过后合并
# 使用 Squash and Merge 保持历史清晰

# 6. 删除功能分支
git branch -d feature/user-profile
git push origin --delete feature/user-profile
```

### Bug 修复流程
```bash
# 1. 从 develop 创建 bugfix 分支
git checkout develop
git checkout -b bugfix/login-error

# 2. 修复并提交
git commit -m "fix(auth): 修复登录时 token 过期判断错误"

# 3. 推送并创建 PR
git push origin bugfix/login-error
```

### 紧急修复流程（Hotfix）
```bash
# 1. 从 main 创建 hotfix 分支
git checkout main
git checkout -b hotfix/security-patch

# 2. 修复并提交
git commit -m "fix(security): 修复 SQL 注入漏洞"

# 3. 合并到 main 和 develop
git checkout main
git merge --no-ff hotfix/security-patch
git tag -a v1.2.1 -m "安全补丁"
git push origin main --tags

git checkout develop
git merge --no-ff hotfix/security-patch
git push origin develop

# 4. 删除 hotfix 分支
git branch -d hotfix/security-patch
```

### 发布流程
```bash
# 1. 从 develop 创建 release 分支
git checkout develop
git checkout -b release/v1.2.0

# 2. 更新版本号、CHANGELOG
# 修改 package.json、pyproject.toml 等
git commit -m "chore(release): 准备 v1.2.0 发布"

# 3. 合并到 main
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin main --tags

# 4. 合并回 develop
git checkout develop
git merge --no-ff release/v1.2.0
git push origin develop

# 5. 删除 release 分支
git branch -d release/v1.2.0
```

## 4. Pull Request 规范

### PR 标题
遵循 Commit Message 规范：
```
feat(auth): 添加 OAuth2.0 登录支持
fix(api): 修复用户列表分页错误
```

### PR 描述模板
```markdown
## 变更类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 重构
- [ ] 文档更新
- [ ] 其他

## 变更说明
简要描述本次变更的内容和原因

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试通过

## 相关 Issue
Closes #123

## 截图（如适用）
```

### Code Review 检查清单
- [ ] 代码符合规范（Lint 通过）
- [ ] 有充分的测试覆盖
- [ ] 文档已更新
- [ ] 无安全漏洞
- [ ] 性能无明显下降
- [ ] 向后兼容（如适用）

## 5. Tag 规范

### 版本号规范（Semantic Versioning）
```
v<major>.<minor>.<patch>

v1.0.0 - 初始版本
v1.1.0 - 新增功能
v1.1.1 - Bug 修复
v2.0.0 - 破坏性变更
```

### Tag 命名
```bash
# 正式版本
git tag -a v1.2.0 -m "Release v1.2.0"

# 预发布版本
git tag -a v1.2.0-rc.1 -m "Release Candidate 1"
git tag -a v1.2.0-beta.1 -m "Beta 1"
git tag -a v1.2.0-alpha.1 -m "Alpha 1"
```

## 6. .gitignore 规范

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
.env

# Node.js
node_modules/
dist/
.next/
.nuxt/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# 项目特定
.agents/handoffs/state/*.json
.agents/evolution/history/*.json
logs/
*.log
```

## 7. 禁止事项

- ❌ 直接提交到 main 分支
- ❌ 提交包含密钥/密码的代码
- ❌ 提交大文件（> 10MB）
- ❌ 提交 `node_modules/`、`venv/` 等依赖目录
- ❌ Force push 到共享分支
- ❌ 不写 commit message 或写无意义的 message

## 8. Git Hooks

### Pre-commit Hook
```bash
#!/bin/sh
# .git/hooks/pre-commit

# 运行 Lint
npm run lint || exit 1

# 运行测试
npm test || exit 1

# 检查敏感信息
git diff --cached --name-only | xargs grep -E "(password|secret|api_key)" && exit 1
```

### Commit-msg Hook
```bash
#!/bin/sh
# .git/hooks/commit-msg

# 验证 commit message 格式
commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .{1,100}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "错误: Commit message 不符合规范"
  echo "格式: <type>(<scope>): <subject>"
  exit 1
fi
```

## 9. 冲突解决

```bash
# 1. 更新本地 develop
git checkout develop
git pull origin develop

# 2. 切换到功能分支并 rebase
git checkout feature/my-feature
git rebase develop

# 3. 解决冲突
# 编辑冲突文件
git add .
git rebase --continue

# 4. 强制推送（仅限个人分支）
git push origin feature/my-feature --force-with-lease
```

## 10. 最佳实践

- ✅ 小步提交，频繁推送
- ✅ 每个 commit 只做一件事
- ✅ 提交前运行测试
- ✅ 及时同步 develop 分支
- ✅ 使用有意义的分支名和 commit message
- ✅ Code Review 前自己先检查一遍
- ✅ 保持 PR 小而聚焦（< 500 行变更）
