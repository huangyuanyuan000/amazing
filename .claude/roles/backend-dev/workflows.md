# 后端开发专属工作流

## API 开发工作流

### 流程概览
```
接口设计 → 数据库设计 → 编码实现 → 单元测试 → 集成测试 → API 文档 → 代码审查 → 部署
```

### 详细步骤

#### 1. 接口设计
**输入**: 需求文档（docs/requirements/）
**输出**: API 设计文档（docs/api/design/）

**操作步骤**:
1. 阅读需求文档，理解业务逻辑
2. 设计 API 端点和资源模型
3. 定义请求参数和响应格式
4. 设计错误码和异常处理
5. 与前端开发对接 API 接口

**检查点**:
- [ ] API 符合 RESTful 规范
- [ ] 请求参数完整且合理
- [ ] 响应格式统一
- [ ] 错误处理完善
- [ ] 前端开发已确认接口

**示例**:
```yaml
# docs/api/design/user-api.yml
openapi: 3.0.0
info:
  title: 用户管理 API
  version: 1.0.0

paths:
  /api/v1/users:
    post:
      summary: 创建用户
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - username
                - email
                - password
              properties:
                username:
                  type: string
                  minLength: 3
                  maxLength: 50
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
      responses:
        '201':
          description: 创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          description: 参数错误
```

#### 2. 数据库设计
**输入**: API 设计文档
**输出**: 数据库 Schema（migrations/）

**操作步骤**:
1. 设计数据表结构
2. 定义字段类型和约束
3. 设计索引策略
4. 编写迁移脚本
5. 执行迁移并验证

**检查点**:
- [ ] 表结构符合范式要求
- [ ] 索引设计合理
- [ ] 迁移脚本可回滚
- [ ] 已在开发环境验证

**示例**:
```python
# migrations/versions/20260308_create_users.py
"""create users table"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), primary_key=True),
        sa.Column('username', sa.String(50), nullable=False, unique=True),
        sa.Column('email', sa.String(100), nullable=False, unique=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now())
    )
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])

def downgrade():
    op.drop_table('users')
```

#### 3. 编码实现
**输入**: API 设计文档、数据库 Schema
**输出**: 后端代码（src/backend/）

**操作步骤**:
1. 创建数据模型（Model）
2. 实现数据访问层（Repository）
3. 实现业务逻辑层（Service）
4. 实现 API 控制器（Controller）
5. 添加输入验证和错误处理

**检查点**:
- [ ] 代码符合规范
- [ ] 有类型注解
- [ ] 有完整注释
- [ ] 有错误处理
- [ ] 有日志记录

**示例**:
```python
# src/backend/models/user.py
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    """用户模型"""
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# src/backend/repositories/user_repository.py
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.user import User

class UserRepository:
    """用户数据访问层"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        """创建用户"""
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """根据 ID 获取用户"""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await self.session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

# src/backend/services/user_service.py
from typing import Optional
from ..repositories.user_repository import UserRepository
from ..models.user import User
from ..schemas.user import CreateUserRequest
from ..utils.security import hash_password
from ..exceptions import UserAlreadyExistsError

class UserService:
    """用户业务逻辑层"""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, request: CreateUserRequest) -> User:
        """创建用户"""
        # 检查用户名是否已存在
        existing_user = await self.user_repo.get_by_username(request.username)
        if existing_user:
            raise UserAlreadyExistsError(f"Username {request.username} already exists")

        # 创建用户
        user = User(
            username=request.username,
            email=request.email,
            password_hash=hash_password(request.password)
        )
        return await self.user_repo.create(user)

# src/backend/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from ...database import get_db
from ...repositories.user_repository import UserRepository
from ...services.user_service import UserService
from ...schemas.user import CreateUserRequest, UserResponse
from ...exceptions import UserAlreadyExistsError

router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    db: AsyncSession = Depends(get_db)
):
    """创建用户"""
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)

    try:
        user = await user_service.create_user(request)
        return UserResponse.from_orm(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

#### 4. 单元测试
**输入**: 后端代码
**输出**: 测试代码（tests/backend/）

**操作步骤**:
1. 为每个函数编写测试
2. 测试正常场景
3. 测试边界条件
4. 测试异常情况
5. 运行测试并检查覆盖率

**检查点**:
- [ ] 测试覆盖率 > 80%
- [ ] 所有测试通过
- [ ] 测试了边界条件
- [ ] 测试了异常情况

**示例**:
```python
# tests/backend/services/test_user_service.py
import pytest
from src.backend.services.user_service import UserService
from src.backend.schemas.user import CreateUserRequest
from src.backend.exceptions import UserAlreadyExistsError

@pytest.mark.asyncio
async def test_create_user_success(user_service, user_repo):
    """测试创建用户成功"""
    request = CreateUserRequest(
        username="testuser",
        email="test@example.com",
        password="Test1234"
    )

    user = await user_service.create_user(request)

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.password_hash != "Test1234"  # 密码已加密

@pytest.mark.asyncio
async def test_create_user_duplicate_username(user_service, existing_user):
    """测试创建重复用户名"""
    request = CreateUserRequest(
        username=existing_user.username,
        email="new@example.com",
        password="Test1234"
    )

    with pytest.raises(UserAlreadyExistsError):
        await user_service.create_user(request)
```

#### 5. 集成测试
**输入**: API 端点
**输出**: 集成测试（tests/integration/）

**操作步骤**:
1. 启动测试数据库
2. 测试 API 端到端流程
3. 测试认证授权
4. 测试数据一致性
5. 清理测试数据

**检查点**:
- [ ] API 端到端测试通过
- [ ] 认证授权正常
- [ ] 数据一致性正确
- [ ] 测试数据已清理

#### 6. API 文档
**输入**: API 代码
**输出**: OpenAPI 文档（docs/api/）

**操作步骤**:
1. 自动生成 OpenAPI 文档
2. 补充接口说明
3. 添加请求示例
4. 添加响应示例
5. 发布文档

**检查点**:
- [ ] 文档完整
- [ ] 示例正确
- [ ] 已发布到文档平台

#### 7. 代码审查
**输入**: Pull Request
**输出**: 审查意见

**操作步骤**:
1. 提交 Pull Request
2. 等待 CI 检查通过
3. 请求同行审查
4. 修改审查意见
5. 获得批准

**检查点**:
- [ ] CI 检查通过
- [ ] 代码规范符合要求
- [ ] 测试覆盖率达标
- [ ] 至少 1 人审查通过

#### 8. 部署
**输入**: 合并后的代码
**输出**: 部署到环境

**操作步骤**:
1. 合并到主分支
2. 触发 CI/CD 流程
3. 部署到开发环境
4. 执行数据库迁移
5. 验证部署结果

**检查点**:
- [ ] 部署成功
- [ ] 数据库迁移成功
- [ ] 健康检查通过
- [ ] API 可正常访问

---

## 数据库设计工作流

### 流程概览
```
Schema 设计 → 索引设计 → 迁移脚本 → 测试验证 → 执行迁移 → 性能监控
```

### 详细步骤

#### 1. Schema 设计
**操作步骤**:
1. 分析业务需求
2. 设计实体关系图（ERD）
3. 定义表结构
4. 定义字段类型和约束
5. 设计外键关系

**设计原则**:
- 符合第三范式（3NF）
- 合理使用反范式
- 字段类型选择合适
- 必须有主键
- 必须有时间戳字段

**示例**:
```sql
-- 用户表
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    order_no VARCHAR(32) NOT NULL UNIQUE,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 订单项表
CREATE TABLE order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES orders(id),
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. 索引设计
**操作步骤**:
1. 分析查询模式
2. 识别高频查询字段
3. 设计单列索引
4. 设计复合索引
5. 评估索引开销

**索引原则**:
- 为查询条件字段创建索引
- 为外键创建索引
- 为排序字段创建索引
- 复合索引遵循最左前缀
- 避免过多索引（< 5 个/表）

**示例**:
```sql
-- 单列索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- 复合索引
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_orders_created ON orders(created_at DESC);

-- 唯一索引
CREATE UNIQUE INDEX idx_orders_order_no ON orders(order_no);

-- 部分索引
CREATE INDEX idx_orders_active ON orders(user_id) WHERE status = 'active';
```

#### 3. 迁移脚本
**操作步骤**:
1. 创建迁移文件
2. 编写 upgrade 函数
3. 编写 downgrade 函数
4. 在开发环境测试
5. 提交代码审查

**检查点**:
- [ ] 迁移可正向执行
- [ ] 迁移可回滚
- [ ] 已在开发环境验证
- [ ] 有数据备份计划

#### 4. 测试验证
**操作步骤**:
1. 执行迁移
2. 验证表结构
3. 验证索引
4. 验证约束
5. 测试查询性能

**验证命令**:
```sql
-- 查看表结构
\d+ users

-- 查看索引
\di+ users

-- 查看约束
SELECT conname, contype FROM pg_constraint WHERE conrelid = 'users'::regclass;

-- 测试查询
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

#### 5. 执行迁移
**操作步骤**:
1. 备份生产数据库
2. 在维护窗口执行迁移
3. 验证迁移结果
4. 监控应用状态
5. 准备回滚方案

**执行命令**:
```bash
# 备份数据库
pg_dump -h localhost -U postgres -d mydb > backup_$(date +%Y%m%d_%H%M%S).sql

# 执行迁移
alembic upgrade head

# 验证迁移
alembic current

# 回滚（如需要）
alembic downgrade -1
```

#### 6. 性能监控
**操作步骤**:
1. 监控慢查询
2. 分析查询计划
3. 优化索引
4. 调整配置参数
5. 持续监控

**监控指标**:
- 查询响应时间
- 索引命中率
- 表扫描次数
- 锁等待时间

---

## 服务开发工作流

### 流程概览
```
服务设计 → 接口定义 → 实现 → 测试 → 部署 → 监控
```

### 详细步骤

#### 1. 服务设计
**操作步骤**:
1. 分析业务需求
2. 设计服务边界
3. 定义服务职责
4. 设计服务间通信
5. 设计数据模型

**设计原则**:
- 单一职责原则
- 高内聚低耦合
- 服务自治
- 接口稳定

#### 2. 接口定义
**操作步骤**:
1. 定义 API 接口（REST）
2. 定义 RPC 接口（gRPC）
3. 定义消息格式
4. 定义错误码
5. 编写接口文档

**示例（gRPC）**:
```protobuf
// user_service.proto
syntax = "proto3";

package user;

service UserService {
  rpc CreateUser(CreateUserRequest) returns (UserResponse);
  rpc GetUser(GetUserRequest) returns (UserResponse);
  rpc UpdateUser(UpdateUserRequest) returns (UserResponse);
  rpc DeleteUser(DeleteUserRequest) returns (Empty);
}

message CreateUserRequest {
  string username = 1;
  string email = 2;
  string password = 3;
}

message UserResponse {
  int64 id = 1;
  string username = 2;
  string email = 3;
  int64 created_at = 4;
}
```

#### 3. 实现
**操作步骤**:
1. 实现服务逻辑
2. 实现数据访问
3. 实现缓存策略
4. 实现错误处理
5. 添加日志和监控

#### 4. 测试
**操作步骤**:
1. 单元测试
2. 集成测试
3. 性能测试
4. 压力测试
5. 混沌测试

#### 5. 部署
**操作步骤**:
1. 构建 Docker 镜像
2. 部署到 K8s
3. 配置服务发现
4. 配置负载均衡
5. 配置健康检查

#### 6. 监控
**操作步骤**:
1. 配置日志收集
2. 配置指标监控
3. 配置链路追踪
4. 配置告警规则
5. 创建监控面板

---

## 性能优化工作流

### 流程概览
```
问题识别 → 性能分析 → 优化方案 → 实施验证 → 持续监控
```

### 详细步骤

#### 1. 问题识别
**数据来源**:
- 慢查询日志
- APM 监控
- 用户反馈
- 性能测试

**识别方法**:
```sql
-- 查看慢查询
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 10;
```

#### 2. 性能分析
**分析维度**:
- 数据库查询
- 缓存命中率
- API 响应时间
- 资源使用率

**分析工具**:
```sql
-- 查询计划分析
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM users WHERE email = 'test@example.com';

-- 索引使用情况
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

#### 3. 优化方案
**常见优化**:
- 添加索引
- 优化查询
- 增加缓存
- 数据库分片
- 异步处理

#### 4. 实施验证
**操作步骤**:
1. 在测试环境实施
2. 进行性能测试
3. 对比优化前后
4. 评估优化效果
5. 部署到生产

#### 5. 持续监控
**监控指标**:
- 响应时间（P50, P95, P99）
- 吞吐量（QPS）
- 错误率
- 资源使用率

---

## Handoffs 任务拆分

### 触发条件
- 预估代码 > 200 行
- 涉及 3 个以上文件
- 需要多个步骤
- 依赖其他任务

### 拆分策略

#### 单个大文件（> 500 行）
```
任务: 实现用户管理服务
├─ 子任务1: 生成 User 模型（< 150 行）
├─ 子任务2: 生成 UserRepository（< 150 行）
├─ 子任务3: 生成 UserService（< 200 行）
└─ 子任务4: 生成 UserController（< 200 行）
```

#### 多文件任务
```
任务: 实现订单系统
├─ 子任务1: 实现订单模型和数据访问
├─ 子任务2: 实现订单业务逻辑
├─ 子任务3: 实现订单 API
└─ 子任务4: 实现订单测试
```

### 使用 Handoff Agents
```bash
# 创建任务
python scripts/handoff_manager.py create backend-dev "实现用户管理 API"

# 执行任务
python scripts/handoff_manager.py execute <task-id>

# 查看状态
python scripts/handoff_manager.py status <task-id>
```

---

## 工作流最佳实践

### 1. 始终先设计后编码
- 不要直接开始写代码
- 先设计 API 接口
- 先设计数据库 Schema
- 与相关方确认设计

### 2. 小步快跑，频繁提交
- 每完成一个小功能就提交
- 提交信息清晰明确
- 保持主分支稳定

### 3. 测试驱动开发（TDD）
- 先写测试再写代码
- 保持高测试覆盖率
- 测试即文档

### 4. 代码审查必不可少
- 所有代码必须经过审查
- 认真对待审查意见
- 学习他人的优秀实践

### 5. 持续集成持续部署
- 自动化测试
- 自动化部署
- 快速反馈

### 6. 监控和告警
- 部署后持续监控
- 设置合理的告警阈值
- 快速响应问题

### 7. 文档同步更新
- 代码变更同步更新文档
- API 文档自动生成
- 保持文档的时效性
