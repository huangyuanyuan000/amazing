# Skill: Code Review
# Version: 1.0.0
# Agent: review
# Tags: review, quality, security

## 描述
代码审核清单和自动检查规则。

## 审核清单

### 1. 代码规范
- [ ] 符合项目代码风格（black/ruff/eslint）
- [ ] 命名规范（变量、函数、类、文件）
- [ ] 无 hardcoded 密钥/密码
- [ ] 无 TODO/FIXME 遗留（或有对应 Issue）

### 2. 安全审查
- [ ] SQL 注入防护（参数化查询）
- [ ] XSS 防护（输出转义）
- [ ] CSRF 防护
- [ ] 认证授权检查
- [ ] 敏感数据不在日志中输出
- [ ] 文件上传安全（类型/大小检查）

### 3. 性能审查
- [ ] N+1 查询问题
- [ ] 大数据量分页处理
- [ ] 缓存策略合理性
- [ ] 资源泄漏（连接/文件句柄）

### 4. 架构一致性
- [ ] 遵循分层架构（Router → Service → Repository）
- [ ] 接口定义符合 OpenAPI 规范
- [ ] 错误处理统一格式
- [ ] 日志记录规范

### 5. 测试覆盖
- [ ] 单测覆盖核心逻辑
- [ ] 边界条件测试
- [ ] 异常路径测试
- [ ] API 集成测试

## 自动检查命令
```bash
# Python
ruff check . && black --check . && bandit -r app/ && pytest --cov=app --cov-report=term-missing

# Go
golangci-lint run && go test -race -coverprofile=coverage.out ./...

# Frontend
eslint --ext .ts,.tsx src/ && prettier --check src/ && npm run test -- --coverage
```

## 审核结果模板
```markdown
## Code Review Report
- **审核人**: Review Agent v{version}
- **审核时间**: {timestamp}
- **结果**: PASS / NEEDS_CHANGES / REJECT

### 发现问题
| # | 严重度 | 类型 | 文件 | 行号 | 描述 |
|---|--------|------|------|------|------|
| 1 | HIGH   | 安全 | xxx  | xx   | xxx  |

### 建议
- ...
```
