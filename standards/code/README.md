# 代码规范

本目录包含 Amazing 框架的代码规范标准，适用于所有初始化的项目。

## 规范文件

- `python.md` - Python 代码规范（PEP 8 + 项目约定）
- `typescript.md` - TypeScript/JavaScript 代码规范
- `go.md` - Go 代码规范
- `naming.md` - 命名规范（通用）
- `comments.md` - 注释与文档规范
- `error-handling.md` - 错误处理规范

## 使用方式

项目初始化时，根据选择的技术栈自动应用对应规范：

```bash
python3 scripts/init.py my-project --tech-stack=python
# 自动应用 python.md + naming.md + comments.md + error-handling.md
```

## 规范检查

所有规范都配置了自动化检查工具：

- Python: `black` + `ruff`
- TypeScript: `eslint` + `prettier`
- Go: `gofmt` + `golangci-lint`

CI/CD 流水线会自动执行规范检查。
