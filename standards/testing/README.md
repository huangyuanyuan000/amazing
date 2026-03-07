# 测试规范

## 测试金字塔
```
         /  E2E  \          (少量，关键路径)
        / 集成测试 \         (中等，API 级别)
       /  单元测试  \        (大量，函数级别)
      /_____________\
```

## 单元测试 (Unit Test)
- 覆盖率目标: > 80%
- 框架: pytest (Python) / go test (Go) / vitest (TS)
- 命名: `test_<function_name>_<scenario>_<expected>`

### Python 示例
```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import AsyncMock
from app.services.user_service import UserService

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def user_service(mock_db):
    return UserService(mock_db)

async def test_create_user_success(user_service):
    user_in = UserCreate(username="test", email="test@example.com", password="Test1234!")
    result = await user_service.create(user_in)
    assert result.username == "test"

async def test_create_user_duplicate_raises(user_service):
    user_service.repo.get_by_username = AsyncMock(return_value=existing_user)
    with pytest.raises(DuplicateError):
        await user_service.create(user_in)
```

## 集成测试 (Integration Test)
```python
# tests/integration/test_user_api.py
import pytest
from httpx import AsyncClient

@pytest.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

async def test_create_and_get_user(client, auth_headers):
    # 创建
    resp = await client.post("/api/v1/users", json={"username": "test", "email": "t@t.com", "password": "Test1234!"}, headers=auth_headers)
    assert resp.status_code == 201
    user_id = resp.json()["data"]["id"]

    # 查询
    resp = await client.get(f"/api/v1/users/{user_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"]["username"] == "test"
```

## 测试命令
```bash
# 全部测试
make test

# 单元测试
pytest tests/unit/ -v --cov=app

# 集成测试
pytest tests/integration/ -v

# 生成覆盖率报告
pytest --cov=app --cov-report=html
```

## CI 中的测试
- PR 合并前必须通过全部测试
- 覆盖率下降超过 2% 则阻止合并
- 新功能必须包含对应测试
