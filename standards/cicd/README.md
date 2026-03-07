# CI/CD 流水线规范

## 流水线阶段
```
代码提交 → Lint → 单测 → 构建 → 集成测试 → 安全扫描 → 部署(dev) → 部署(staging) → 审核 → 部署(prod)
```

## GitHub Actions 模板
```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install ruff black
    - run: ruff check backend/
    - run: black --check backend/

  test:
    needs: lint
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_amazing
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - run: pip install -r requirements.txt
    - run: pytest --cov=app --cov-fail-under=80
      env:
        DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_amazing
        REDIS_URL: redis://localhost:6379/0

  security:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - run: pip install bandit safety
    - run: bandit -r backend/app/
    - run: safety check -r requirements.txt

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: docker/build-push-action@v5
      with:
        push: ${{ github.ref == 'refs/heads/main' }}
        tags: amazing/api-gateway:${{ github.sha }}

  deploy-dev:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    steps:
    - run: kubectl set image deployment/api-gateway api-gateway=amazing/api-gateway:${{ github.sha }} -n amazing-dev

  deploy-prod:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
    - run: kubectl set image deployment/api-gateway api-gateway=amazing/api-gateway:${{ github.sha }} -n amazing
```

## 部署策略
| 环境 | 触发 | 审批 |
|------|------|------|
| dev | push to develop | 自动 |
| staging | PR to main | 自动 |
| production | merge to main | 人工审批 |
