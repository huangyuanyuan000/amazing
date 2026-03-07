# 技术规范

## 1. 代码风格规范

### 1.1 Python 规范

**工具**: black + ruff

**规则**:
- 使用 black 格式化代码
- 行长度: 88 字符
- 使用 type hints
- 遵循 PEP 8

**示例**:
```python
from typing import List, Optional

def get_users(
    limit: int = 10,
    offset: int = 0,
    status: Optional[str] = None
) -> List[dict]:
    """获取用户列表"""
    pass
```

### 1.2 Go 规范

**工具**: gofmt + golangci-lint

**规则**:
- 使用 gofmt 格式化
- 遵循 Effective Go
- 错误处理必须显式
- 使用 context 传递上下文

**示例**:
```go
func GetUsers(ctx context.Context, limit, offset int) ([]User, error) {
    // implementation
    return users, nil
}
```

### 1.3 TypeScript 规范

**工具**: eslint + prettier

**规则**:
- 使用 prettier 格式化
- 严格模式 (strict: true)
- 使用函数式组件
- Props 必须定义类型

**示例**:
```typescript
interface UserListProps {
  users: User[]
  onSelect: (user: User) => void
}

export const UserList: React.FC<UserListProps> = ({ users, onSelect }) => {
  return <div>{/* ... */}</div>
}
```

## 2. Git 提交规范

### 2.1 Conventional Commits

**格式**: `<type>(<scope>): <subject>`

**类型**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `refactor`: 代码重构
- `test`: 测试相关
- `ci`: CI/CD 相关
- `chore`: 其他修改

**示例**:
```
feat(auth): 添加 JWT 认证
fix(api): 修复用户查询接口 500 错误
docs(readme): 更新部署文档
refactor(user): 重构用户服务代码
test(auth): 添加认证模块单元测试
```

### 2.2 分支规范

```
main          - 生产分支
develop       - 开发分支
feature/*     - 功能分支
bugfix/*      - Bug 修复分支
hotfix/*      - 热修复分支
release/*     - 发布分支
```

## 3. API 设计规范

### 3.1 RESTful API

**URL 设计**:
```
GET    /api/v1/users          - 获取用户列表
GET    /api/v1/users/:id      - 获取单个用户
POST   /api/v1/users          - 创建用户
PUT    /api/v1/users/:id      - 更新用户
DELETE /api/v1/users/:id      - 删除用户
```

**响应格式**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "name": "张三"
  }
}
```

**错误响应**:
```json
{
  "code": 400,
  "message": "参数错误",
  "errors": [
    {
      "field": "email",
      "message": "邮箱格式不正确"
    }
  ]
}
```

### 3.2 OpenAPI 规范

所有 API 必须提供 OpenAPI 3.0 文档:

```yaml
openapi: 3.0.0
info:
  title: Amazing API
  version: 1.0.0
paths:
  /api/v1/users:
    get:
      summary: 获取用户列表
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: 成功
```

## 4. 测试规范

### 4.1 单元测试

**覆盖率要求**: > 80%

**Python (Pytest)**:
```python
def test_create_user():
    user = create_user(name="张三", email="test@example.com")
    assert user.name == "张三"
    assert user.email == "test@example.com"
```

**Go**:
```go
func TestCreateUser(t *testing.T) {
    user, err := CreateUser("张三", "test@example.com")
    assert.NoError(t, err)
    assert.Equal(t, "张三", user.Name)
}
```

**TypeScript (Jest)**:
```typescript
describe('UserList', () => {
  it('should render users', () => {
    const users = [{ id: 1, name: '张三' }]
    render(<UserList users={users} />)
    expect(screen.getByText('张三')).toBeInTheDocument()
  })
})
```

### 4.2 集成测试

**要求**:
- 所有 API 必须有集成测试
- 测试覆盖正常流程和异常流程
- 使用测试数据库

**示例**:
```python
@pytest.mark.asyncio
async def test_user_api(client):
    # 创建用户
    response = await client.post("/api/v1/users", json={
        "name": "张三",
        "email": "test@example.com"
    })
    assert response.status_code == 200

    # 获取用户
    user_id = response.json()["data"]["id"]
    response = await client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
```

## 5. CI/CD 规范

### 5.1 GitHub Actions

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: make test
      - name: Run lint
        run: make lint
```

### 5.2 部署流程

```
1. 代码提交 → 2. CI 检查 → 3. 构建镜像 → 4. 部署到环境
```

**环境**:
- `dev`: 开发环境 (自动部署)
- `staging`: 预发布环境 (手动部署)
- `prod`: 生产环境 (手动部署 + 审批)

## 6. 文档规范

### 6.1 代码注释

**Python**:
```python
def create_user(name: str, email: str) -> User:
    """创建用户

    Args:
        name: 用户名
        email: 邮箱

    Returns:
        User: 创建的用户对象

    Raises:
        ValueError: 参数不合法
    """
    pass
```

**Go**:
```go
// CreateUser 创建用户
// 参数:
//   - name: 用户名
//   - email: 邮箱
// 返回:
//   - User: 创建的用户对象
//   - error: 错误信息
func CreateUser(name, email string) (*User, error) {
    // implementation
}
```

### 6.2 README 规范

每个模块必须有 README.md:

```markdown
# 模块名称

## 功能描述

## 技术栈

## 快速开始

## API 文档

## 测试

## 部署
```

### 6.3 API 文档

使用 Swagger UI 提供交互式 API 文档:
- Python: FastAPI 自动生成
- Go: 使用 swaggo/swag

## 7. 安全规范

### 7.1 认证授权

- 使用 JWT Token
- Token 有效期: 24 小时
- Refresh Token 有效期: 7 天
- 敏感操作需要二次验证

### 7.2 数据安全

- 密码使用 bcrypt 加密
- 敏感数据加密存储
- HTTPS 传输
- SQL 注入防护
- XSS 防护

### 7.3 代码安全

- 定期扫描依赖漏洞
- 使用 SAST 工具
- Code Review 必须通过

## 8. 性能规范

### 8.1 API 性能

- 响应时间: < 200ms (P95)
- QPS: > 1000
- 错误率: < 0.1%

### 8.2 前端性能

- FCP: < 1.5s
- LCP: < 2.5s
- TTI: < 3.5s
- Bundle Size: < 500KB

### 8.3 数据库性能

- 查询时间: < 100ms
- 索引覆盖率: > 90%
- 慢查询监控

## 9. 日志规范

### 9.1 日志级别

- `DEBUG`: 调试信息
- `INFO`: 一般信息
- `WARNING`: 警告信息
- `ERROR`: 错误信息
- `CRITICAL`: 严重错误

### 9.2 日志格式

```json
{
  "timestamp": "2024-03-07T10:00:00Z",
  "level": "INFO",
  "service": "python-api",
  "message": "User created",
  "user_id": 123,
  "trace_id": "abc123"
}
```

## 10. 监控规范

### 10.1 指标监控

- CPU 使用率
- 内存使用率
- 磁盘使用率
- 网络流量
- API 响应时间
- 错误率

### 10.2 告警规则

- CPU > 80%: 警告
- 内存 > 85%: 警告
- 错误率 > 1%: 严重
- API 响应时间 > 1s: 警告
