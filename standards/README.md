# Amazing 框架规范标准

本目录包含 Amazing 框架的所有开发规范标准，适用于所有初始化的项目。

## 目录结构

```
standards/
├── code/           # 代码规范
│   ├── python.md
│   ├── typescript.md
│   ├── go.md
│   └── README.md
├── git/            # Git 工作流规范
│   ├── workflow.md
│   └── README.md
├── api/            # API 设计规范
│   ├── restful.md
│   └── README.md
├── testing/        # 测试规范
│   ├── testing-standards.md
│   └── README.md
└── README.md       # 本文件
```

## 规范分类

### 1. 代码规范 (`code/`)
定义各语言的代码风格、命名规范、最佳实践。

- Python: PEP 8 + 项目约定
- TypeScript: Airbnb Style Guide + 项目约定
- Go: Effective Go + 项目约定

### 2. Git 规范 (`git/`)
定义 Git 工作流、分支策略、Commit Message 规范。

- 基于 Git Flow
- Conventional Commits
- Pull Request 流程

### 3. API 规范 (`api/`)
定义 API 设计标准、响应格式、错误处理。

- RESTful API 设计
- OpenAPI 3.0 文档
- 认证授权规范

### 4. 测试规范 (`testing/`)
定义测试策略、覆盖率要求、测试工具链。

- 测试金字塔
- 单元/集成/E2E 测试
- 性能测试

## 使用方式

### 项目初始化时自动应用
```bash
python3 scripts/init.py my-project --tech-stack=python
# 自动应用对应的代码规范、Git 规范、API 规范、测试规范
```

### 手动查阅
```bash
# 查看 Python 代码规范
cat standards/code/python.md

# 查看 Git 工作流规范
cat standards/git/workflow.md

# 查看 API 设计规范
cat standards/api/restful.md

# 查看测试规范
cat standards/testing/testing-standards.md
```

### CI/CD 自动检查
所有规范都配置了自动化检查工具，在 CI/CD 流水线中自动执行：

- 代码规范: `black`, `ruff`, `eslint`, `prettier`
- Git 规范: commit-msg hook
- API 规范: OpenAPI 文档验证
- 测试规范: 覆盖率检查

## 规范更新

规范文件由 Amazing 框架维护，定期更新以反映最佳实践。

项目可以在 `.amazing/standards-override/` 目录中覆盖特定规范：

```
my-project/
├── .amazing/
│   └── standards-override/
│       └── code/
│           └── python.md  # 覆盖默认 Python 规范
```

## 规范检查

```bash
# 检查代码规范
make lint

# 检查测试覆盖率
make test-coverage

# 检查 API 文档
make api-docs-validate

# 全面检查
make check-all
```

## 贡献规范

如需修改或补充规范，请：

1. Fork 项目
2. 创建分支 `feature/update-standards`
3. 修改规范文件
4. 提交 PR 并说明修改原因
5. 等待 Review 和合并

## 相关文档

- [CLAUDE.md](../CLAUDE.md) - 框架总体文档
- [CONTRIBUTING.md](../CONTRIBUTING.md) - 贡献指南
- [examples/](../examples/) - 示例项目
