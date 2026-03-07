# 代码风格规范

## Python
- 格式化: `black` (行宽 120)
- Lint: `ruff` (替代 flake8/isort/pyupgrade)
- 类型检查: `mypy --strict` (核心模块)
- 导入排序: isort (由 ruff 集成)

### ruff 配置 (pyproject.toml)
```toml
[tool.ruff]
line-length = 120
target-version = "py311"
select = ["E", "F", "W", "I", "N", "UP", "S", "B", "A", "COM", "C4", "DTZ", "T10", "ISC", "ICN", "PIE", "PT", "RSE", "RET", "SLF", "SIM", "TID", "TCH", "ARG", "PTH", "ERA"]

[tool.black]
line-length = 120
target-version = ["py311"]
```

### 命名规范
| 类型 | 风格 | 示例 |
|------|------|------|
| 模块/包 | snake_case | `user_service.py` |
| 类 | PascalCase | `UserService` |
| 函数/方法 | snake_case | `get_user_by_id()` |
| 常量 | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| 变量 | snake_case | `user_name` |

## Go
- 格式化: `gofmt`
- Lint: `golangci-lint`
- 命名: Go 官方规范（驼峰，导出首字母大写）

### golangci-lint 配置
```yaml
# .golangci.yml
run:
  timeout: 5m
linters:
  enable:
    - gofmt
    - govet
    - errcheck
    - staticcheck
    - gosimple
    - ineffassign
    - typecheck
    - unused
    - misspell
    - gosec
```

## TypeScript/React
- 格式化: `prettier`
- Lint: `eslint` (+ @typescript-eslint)
- 组件命名: PascalCase
- hooks: use 前缀

### ESLint 配置要点
```json
{
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended", "plugin:react-hooks/recommended", "prettier"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "react-hooks/exhaustive-deps": "warn"
  }
}
```
