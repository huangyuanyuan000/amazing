# 后端开发约束规则

## 代码规范

### Python 规范
- **必须遵循 PEP 8 规范**
- **必须使用 black 格式化代码**
- **必须使用 ruff 进行代码检查**
- **必须有类型注解（Type Hints）**
  ```python
  def get_user(user_id: int) -> Optional[User]:
      """获取用户信息"""
      pass
  ```
- **必须有 docstring**
  ```python
  def create_order(user_id: int, items: List[OrderItem]) -> Order:
      """
      创建订单

      Args:
          user_id: 用户 ID
          items: 订单项列表

      Returns:
          Order: 创建的订单对象

      Raises:
          ValueError: 当订单项为空时
          InsufficientStockError: 当库存不足时
      """
      pass
  ```

### Go 规范
- **必须使用 gofmt 格式化代码**
- **必须使用 golangci-lint 检查代码**
- **必须有错误处理**
  ```go
  func GetUser(userID int) (*User, error) {
      if userID <= 0 {
          return nil, errors.New("invalid user id")
      }
      // ...
  }
  ```
- **必须有注释**
  ```go
  // GetUser 根据用户 ID 获取用户信息
  // 参数:
  //   userID: 用户 ID
  // 返回:
  //   *User: 用户对象
  //   error: 错误信息
  func GetUser(userID int) (*User, error) {
      // ...
  }
  ```

### 通用规范
- **单个函数不超过 50 行**
- **单个文件不超过 500 行**
- **循环复杂度不超过 10**
- **必须有单元测试**
- **禁止硬编码配置**
- **禁止使用全局变量**

## API 规范

### RESTful 规范
- **必须遵循 RESTful 设计原则**
  - GET: 查询资源
  - POST: 创建资源
  - PUT: 完整更新资源
  - PATCH: 部分更新资源
  - DELETE: 删除资源

- **必须使用正确的 HTTP 状态码**
  - 200: 成功
  - 201: 创建成功
  - 204: 删除成功（无内容）
  - 400: 请求参数错误
  - 401: 未认证
  - 403: 无权限
  - 404: 资源不存在
  - 500: 服务器错误

- **必须有统一的响应格式**
  ```json
  {
    "code": 0,
    "message": "success",
    "data": {
      "id": 1,
      "name": "张三"
    },
    "timestamp": 1678291200
  }
  ```

- **必须有统一的错误格式**
  ```json
  {
    "code": 40001,
    "message": "用户不存在",
    "errors": [
      {
        "field": "user_id",
        "message": "用户 ID 123 不存在"
      }
    ],
    "timestamp": 1678291200
  }
  ```

### OpenAPI 文档
- **每个 API 必须有 OpenAPI 文档**
- **必须包含完整的请求参数说明**
- **必须包含完整的响应示例**
- **必须包含错误码说明**
- **必须包含认证方式说明**

示例：
```yaml
/api/v1/users/{user_id}:
  get:
    summary: 获取用户信息
    description: 根据用户 ID 获取用户详细信息
    tags:
      - 用户管理
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: integer
        description: 用户 ID
    responses:
      '200':
        description: 成功
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserResponse'
      '404':
        description: 用户不存在
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
    security:
      - bearerAuth: []
```

### API 版本管理
- **必须在 URL 中包含版本号**: `/api/v1/users`
- **��兼容的变更必须升级版本号**
- **旧版本必须保留至少 6 个月**
- **必须在响应头中返回 API 版本**: `X-API-Version: v1`

## 数据库规范

### Schema 设计
- **必须有主键**
- **必须有创建时间和更新时间字段**
  ```sql
  CREATE TABLE users (
      id BIGSERIAL PRIMARY KEY,
      username VARCHAR(50) NOT NULL UNIQUE,
      email VARCHAR(100) NOT NULL UNIQUE,
      created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
      updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
  );
  ```

- **必须有软删除字段（如需要）**
  ```sql
  deleted_at TIMESTAMP NULL
  ```

- **外键必须有索引**
- **字符串字段必须指定长度**
- **必须有字段注释**

### 迁移脚本
- **必须使用迁移工具**（Alembic, Flyway, golang-migrate）
- **必须有 up 和 down 脚本**
- **必须按时间戳命名**: `20260308120000_create_users_table.sql`
- **必须在迁移前备份数据**
- **禁止直接修改已执行的迁移脚本**

示例：
```python
# migrations/versions/20260308120000_create_users_table.py
"""create users table

Revision ID: 20260308120000
Revises:
Create Date: 2026-03-08 12:00:00
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    op.create_index('idx_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('idx_users_email', 'users')
    op.drop_table('users')
```

### 索引设计
- **必须为查询条件字段创建索引**
- **必须为外键创建索引**
- **必须为排序字段创建索引**
- **复合索引必须遵循最左前缀原则**
- **索引数量不超过 5 个/表**

### 查询优化
- **禁止使用 SELECT ***
- **必须使用分页查询**
- **必须使用连接池**
- **慢查询必须优化（> 100ms）**
- **必须使用 EXPLAIN 分析查询计划**

## 安全约束

### 认证授权
- **所有 API 必须有认证（除公开接口）**
- **必须使用 JWT Token 或 OAuth2**
- **Token 必须有过期时间（< 24 小时）**
- **必须支持 Token 刷新**
- **必须实现权限控制（RBAC/ABAC）**

示例：
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    user = await get_user_by_id(payload["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

@app.get("/api/v1/users/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user
```

### 输入验证
- **必须验证所有输入参数**
- **必须使用 Pydantic/Validator 进行验证**
- **必须防止 SQL 注入**
- **必须防止 XSS 攻击**
- **必须限制请求大小（< 10MB）**

示例：
```python
from pydantic import BaseModel, Field, validator

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    email: str = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=100)

    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', v):
            raise ValueError('Invalid email format')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        return v
```

### 敏感数据
- **密码必须加密存储（bcrypt/argon2）**
- **敏感数据必须加密传输（HTTPS）**
- **日志中禁止记录敏感信息**
- **必须脱敏显示敏感数据**

示例：
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """加密密码"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def mask_email(email: str) -> str:
    """脱敏邮箱"""
    username, domain = email.split('@')
    return f"{username[:2]}***@{domain}"
```

## 性能约束

### 响应时间
- **API 响应时间 < 200ms（P95）**
- **数据库查询时间 < 100ms**
- **缓存命中率 > 80%**
- **并发请求 > 1000 QPS**

### 资源使用
- **单个请求内存 < 100MB**
- **CPU 使用率 < 70%**
- **数据库连接数 < 100**
- **必须使用连接池**

### 缓存策略
- **热点数据必须缓存**
- **缓存必须有过期时间**
- **必须有缓存更新策略**
- **必须有缓存穿透防护**

示例：
```python
from functools import lru_cache
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_user_cached(user_id: int) -> Optional[User]:
    """获取用户（带缓存）"""
    cache_key = f"user:{user_id}"

    # 尝试从缓存获取
    cached = redis_client.get(cache_key)
    if cached:
        return User.parse_raw(cached)

    # 从数据库获取
    user = await get_user_from_db(user_id)
    if user:
        # 写入缓存，过期时间 1 小时
        redis_client.setex(cache_key, 3600, user.json())

    return user
```

## 测试约束

### 单元测试
- **覆盖率必须 > 80%**
- **每个函数必须有测试**
- **必须测试边界条件**
- **必须测试异常情况**

### 集成测试
- **必须测试 API 端到端**
- **必须测试数据库事务**
- **必须测试缓存逻辑**
- **必须测试认证授权**

### 性能测试
- **必须进行压力测试**
- **必须测试并发场景**
- **必须测试慢查询**
- **必须有性能基准**

## 部署约束

### 容器化
- **必须使用 Docker**
- **必须使用多阶段构建**
- **镜像大小 < 500MB**
- **必须有健康检查**

示例：
```dockerfile
# 多阶段构建
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 配置管理
- **禁止硬编码配置**
- **必须使用环境变量**
- **必须有配置验证**
- **敏感配置必须加密**

### 日志规范
- **必须使用结构化日志**
- **必须包含请求 ID**
- **必须记录关键操作**
- **禁止记录敏感信息**

示例：
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)

    def info(self, message: str, **kwargs):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": "INFO",
            "message": message,
            **kwargs
        }
        self.logger.info(json.dumps(log_data))

logger = StructuredLogger(__name__)
logger.info("User created", user_id=123, username="zhangsan")
```

## 违规处理

### 警告级别
- 代码格式不规范
- 缺少注释
- 测试覆盖率不足

### 拒绝级别
- 无认证授权
- SQL 注入风险
- 硬编码敏感信息
- 性能严重不达标
- 无迁移脚本的数据库变更
