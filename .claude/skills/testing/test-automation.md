# Test Automation Skill - 自动化测试框架

## 功能描述
提供自动化测试框架配置、CI 集成方案和测试工具链。

## 触发方式
- 自动化测试搭建
- CI 测试集成
- 测试框架选型

## 核心内容

### 1. 测试框架选型
| 语言 | 单测 | 集成测试 | E2E |
|------|------|----------|-----|
| Python | Pytest | Pytest + httpx | Playwright |
| TypeScript | Jest/Vitest | Supertest | Playwright |
| Go | testing | httptest | Playwright |

### 2. Pytest 配置
```ini
[pytest]
testpaths = tests
addopts = -v --cov=src --cov-report=html --cov-fail-under=80
markers =
    unit: 单元测试
    integration: 集成测试
    e2e: 端到端测试
```

### 3. CI 集成
```yaml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: pytest -m unit
    - run: pytest -m integration
    - uses: codecov/codecov-action@v3
```

### 4. 测试数据管理
- Fixture: 测试数据工厂
- Factory Boy: 模型数据生成
- Faker: 随机测试数据
- 数据库: 每个测试独立事务，自动回滚

## 示例
```python
@pytest.fixture
async def test_user(db_session):
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    await db_session.commit()
    yield user
```

## 进化能力
- 测试框架配置持续优化
- 新工具自动评估
- 测试执行效率提升
