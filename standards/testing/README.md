# 测试规范

本目录包含 Amazing 框架的测试规范标准。

## 规范文件

- `testing-standards.md` - 完整测试规范（单元/集成/E2E）
- `unit-testing.md` - 单元测试详细指南
- `integration-testing.md` - 集成测试详细指南
- `e2e-testing.md` - E2E 测试详细指南
- `performance-testing.md` - 性能测试指南

## 测试覆盖率要求

| 层级 | 覆盖率 | 说明 |
|------|--------|------|
| 单元测试 | > 80% | 核心业务逻辑 100% |
| 集成测试 | > 60% | 所有 API 端点 |
| E2E 测试 | 关键路径 | 核心业务流程 |

## 快速开始

```bash
# Python 项目
pytest --cov=app --cov-report=html

# TypeScript 项目
npm test -- --coverage

# E2E 测试
npx playwright test
```
