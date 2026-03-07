# CI/CD Pipeline Skill - 流水线模板

## 功能描述
提供 CI/CD 流水线模板、自动化测试集成和部署审批流程。

## 触发方式
- CI/CD 流水线配置
- 自动化部署设置
- 流水线优化

## 核心内容

### 1. 流水线阶段
| 阶段 | 触发 | 动作 | 失败处理 |
|------|------|------|----------|
| Lint | PR/Push | 代码风格检查 | 阻止合并 |
| Test | PR/Push | 单测+集成测试 | 阻止合并 |
| Build | Test 通过 | 构建镜像 | 通知开发者 |
| Deploy-Dev | develop 合并 | 自动部署 | 通知运维 |
| Deploy-Prod | main 合并 | 审批后部署 | 自动回滚 |

### 2. GitHub Actions 模板
```yaml
name: CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make lint
  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make test
  build:
    needs: test
    if: github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - run: make docker-build docker-push
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    environment: production
    runs-on: ubuntu-latest
    steps:
      - run: make k8s-deploy
```

### 3. 流水线优化
- 缓存依赖（pip/npm cache）
- 并行执行独立任务
- 条件执行（路径过滤）
- 增量构建

## 进化能力
- 流水线模板持续优化
- 执行时间持续缩短
- 新工具自动集成
