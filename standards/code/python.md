# Python 代码规范

基于 PEP 8，结合 Amazing 框架最佳实践。

## 1. 代码格式化

### 工具链
- **black**: 代码格式化（行长 88）
- **ruff**: Linter（替代 flake8 + isort + pylint）

### 配置文件
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
ignore = ["E501"]  # black 已处理行长
```

## 2. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块 | 小写下划线 | `user_service.py` |
| 类 | 大驼峰 | `UserService` |
| 函数/方法 | 小写下划线 | `get_user_by_id()` |
| 变量 | 小写下划线 | `user_count` |
| 常量 | 大写下划线 | `MAX_RETRY_COUNT` |
| 私有成员 | 单下划线前缀 | `_internal_method()` |

## 3. 类型注解

**强制要求**：所有公共 API 必须有类型注解

```python
# ✅ 正确
def get_user(user_id: int) -> User | None:
    """获取用户信息"""
    return db.query(User).filter(User.id == user_id).first()

# ❌ 错误
def get_user(user_id):
    return db.query(User).filter(User.id == user_id).first()
```

## 4. 文档字符串

使用 Google 风格 docstring：

```python
def create_user(username: str, email: str, role: str = "user") -> User:
    """创建新用户

    Args:
        username: 用户名，3-50 字符
        email: 邮箱地址
        role: 用户角色，默认 "user"

    Returns:
        创建的用户对象

    Raises:
        ValueError: 用户名或邮箱格式不正确
        DuplicateError: 用户名或邮箱已存在
    """
    pass
```

## 5. 导入顺序

```python
# 1. 标准库
import os
from datetime import datetime

# 2. 第三方库
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# 3. 本地模块
from app.models import User
from app.schemas import UserCreate
from app.core.config import settings
```

## 6. 错误处理

```python
# ✅ 具体异常
try:
    user = get_user(user_id)
except UserNotFoundError:
    raise HTTPException(status_code=404, detail="用户不存在")

# ❌ 泛化异常
try:
    user = get_user(user_id)
except Exception:
    raise HTTPException(status_code=500)
```

## 7. FastAPI 最佳实践

### 路由定义
```python
@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """创建用户"""
    return await user_service.create(db, user)
```

### 依赖注入
```python
# dependencies.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    return await auth_service.verify_token(db, token)
```

## 8. 数据库操作

### SQLAlchemy 模型
```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
```

### 查询规范
```python
# ✅ 使用 Repository 模式
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[User]:
        result = await self.db.execute(
            select(User).offset(skip).limit(limit)
        )
        return result.scalars().all()
```

## 9. 异步编程

```python
# ✅ 正确的异步调用
async def get_user_with_orders(user_id: int) -> UserWithOrders:
    user, orders = await asyncio.gather(
        user_repo.get_by_id(user_id),
        order_repo.get_by_user_id(user_id),
    )
    return UserWithOrders(user=user, orders=orders)

# ❌ 错误：串行执行
async def get_user_with_orders(user_id: int) -> UserWithOrders:
    user = await user_repo.get_by_id(user_id)
    orders = await order_repo.get_by_user_id(user_id)
    return UserWithOrders(user=user, orders=orders)
```

## 10. 测试规范

```python
# tests/test_user_service.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient, db: AsyncSession):
    """测试创建用户成功"""
    response = await client.post(
        "/api/v1/users",
        json={"username": "testuser", "email": "test@example.com"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
```

## 11. 禁止事项

- ❌ 使用 `import *`
- ❌ 可变默认参数 `def func(items=[])`
- ❌ 裸 `except:` 子句
- ❌ 全局可变状态
- ❌ 硬编码配置（使用环境变量）
- ❌ SQL 字符串拼接（使用参数化查询）

## 12. 性能优化

```python
# ✅ 使用生成器处理大数据
def process_large_file(file_path: str):
    with open(file_path) as f:
        for line in f:  # 逐行读取，不占用大量内存
            yield process_line(line)

# ✅ 批量数据库操作
async def bulk_create_users(users: list[UserCreate]):
    db_users = [User(**user.dict()) for user in users]
    db.add_all(db_users)
    await db.commit()
```

## 13. 安全规范

```python
# ✅ 密码哈希
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash(password)

# ✅ 输入验证
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    password: constr(min_length=8)
```

## 自动化检查

```bash
# 格式化
black .
ruff check --fix .

# 类型检查
mypy .

# 测试
pytest --cov=app --cov-report=html
```
