# RESTful API 设计规范

基于 REST 架构风格和 OpenAPI 3.0 标准。

## 1. URL 设计

### 资源命名
```
✅ 使用名词复数
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}

❌ 不要使用动词
GET /api/v1/getUsers
POST /api/v1/createUser
```

### 嵌套资源
```
✅ 最多两层嵌套
GET /api/v1/users/{userId}/orders
GET /api/v1/users/{userId}/orders/{orderId}

❌ 避免过深嵌套
GET /api/v1/users/{userId}/orders/{orderId}/items/{itemId}/reviews
```

### 版本控制
```
✅ URL 路径版本
/api/v1/users
/api/v2/users

✅ 请求头版本（可选）
Accept: application/vnd.api+json; version=1
```

## 2. HTTP 方法

| 方法 | 用途 | 幂等性 | 安全性 |
|------|------|--------|--------|
| GET | 查询资源 | ✅ | ✅ |
| POST | 创建资源 | ❌ | ❌ |
| PUT | 全量更新 | ✅ | ❌ |
| PATCH | 部分更新 | ❌ | ❌ |
| DELETE | 删除资源 | ✅ | ❌ |

### 使用示例
```
GET    /api/v1/users          # 获取用户列表
POST   /api/v1/users          # 创建用户
GET    /api/v1/users/123      # 获取用户详情
PUT    /api/v1/users/123      # 全量更新用户
PATCH  /api/v1/users/123      # 部分更新用户
DELETE /api/v1/users/123      # 删除用户
```

## 3. 状态码

### 成功响应
| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 OK | 成功 | GET/PUT/PATCH/DELETE 成功 |
| 201 Created | 已创建 | POST 创建成功 |
| 204 No Content | 无内容 | DELETE 成功且无返回内容 |

### 客户端错误
| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 400 Bad Request | 请求错误 | 参数校验失败 |
| 401 Unauthorized | 未认证 | Token 无效/过期 |
| 403 Forbidden | 无权限 | 权限不足 |
| 404 Not Found | 未找到 | 资源不存在 |
| 409 Conflict | 冲突 | 资源已存在 |
| 422 Unprocessable Entity | 不可处理 | 业务逻辑错误 |
| 429 Too Many Requests | 请求过多 | 触发限流 |

### 服务器错误
| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 500 Internal Server Error | 服务器错误 | 内部异常 |
| 502 Bad Gateway | 网关错误 | 上游服务异常 |
| 503 Service Unavailable | 服务不可用 | 服务维护 |

## 4. 统一响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 123,
    "username": "testuser",
    "email": "test@example.com"
  },
  "meta": {
    "timestamp": "2024-01-01T10:00:00Z",
    "request_id": "req-abc123"
  }
}
```

### 列表响应
```json
{
  "code": 200,
  "message": "success",
  "data": [
    {"id": 1, "username": "user1"},
    {"id": 2, "username": "user2"}
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    },
    {
      "field": "password",
      "message": "Password must be at least 8 characters"
    }
  ],
  "meta": {
    "timestamp": "2024-01-01T10:00:00Z",
    "request_id": "req-abc123"
  }
}
```

## 5. 查询参数

### 分页
```
GET /api/v1/users?page=1&page_size=20
```

### 排序
```
GET /api/v1/users?sort=created_at        # 升序
GET /api/v1/users?sort=-created_at       # 降序（- 前缀）
GET /api/v1/users?sort=name,-created_at  # 多字段排序
```

### 过滤
```
GET /api/v1/users?status=active
GET /api/v1/users?role=admin&status=active
GET /api/v1/users?created_at_gte=2024-01-01  # 大于等于
GET /api/v1/users?created_at_lt=2024-12-31   # 小于
```

### 字段选择
```
GET /api/v1/users?fields=id,username,email
```

### 搜索
```
GET /api/v1/users?q=john
GET /api/v1/users?search=john&search_fields=username,email
```

## 6. 请求体

### JSON 格式
```json
POST /api/v1/users
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepass123",
  "role": "user"
}
```

### 文件上传
```
POST /api/v1/users/avatar
Content-Type: multipart/form-data

file: [binary data]
```

## 7. 认证与授权

### Bearer Token
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### API Key
```
X-API-Key: your-api-key-here
```

### 权限检查
```json
{
  "code": 403,
  "message": "Insufficient permissions",
  "errors": [
    {
      "required_permission": "users:delete",
      "user_permissions": ["users:read", "users:write"]
    }
  ]
}
```

## 8. 限流

### 响应头
```
X-RateLimit-Limit: 1000        # 限制总数
X-RateLimit-Remaining: 999     # 剩余次数
X-RateLimit-Reset: 1640995200  # 重置时间（Unix 时间戳）
```

### 超限响应
```json
{
  "code": 429,
  "message": "Rate limit exceeded",
  "meta": {
    "retry_after": 60
  }
}
```

## 9. 批量操作

### 批量创建
```json
POST /api/v1/users/batch
{
  "users": [
    {"username": "user1", "email": "user1@example.com"},
    {"username": "user2", "email": "user2@example.com"}
  ]
}

Response:
{
  "code": 201,
  "data": {
    "created": 2,
    "failed": 0,
    "results": [
      {"id": 1, "username": "user1"},
      {"id": 2, "username": "user2"}
    ]
  }
}
```

### 批量删除
```json
DELETE /api/v1/users/batch
{
  "ids": [1, 2, 3]
}
```

## 10. 异步操作

### 长时间任务
```
POST /api/v1/reports/generate
Response: 202 Accepted
{
  "code": 202,
  "message": "Task accepted",
  "data": {
    "task_id": "task-abc123",
    "status": "pending",
    "status_url": "/api/v1/tasks/task-abc123"
  }
}

GET /api/v1/tasks/task-abc123
{
  "code": 200,
  "data": {
    "task_id": "task-abc123",
    "status": "completed",
    "result_url": "/api/v1/reports/report-xyz789"
  }
}
```

## 11. HATEOAS（可选）

```json
{
  "code": 200,
  "data": {
    "id": 123,
    "username": "testuser",
    "email": "test@example.com"
  },
  "links": {
    "self": "/api/v1/users/123",
    "orders": "/api/v1/users/123/orders",
    "update": "/api/v1/users/123",
    "delete": "/api/v1/users/123"
  }
}
```

## 12. OpenAPI 3.0 文档

```yaml
openapi: 3.0.3
info:
  title: Amazing API
  version: 1.0.0
  description: Amazing 框架 API 文档

servers:
  - url: https://api.example.com/v1
    description: 生产环境
  - url: https://api-dev.example.com/v1
    description: 开发环境

paths:
  /users:
    get:
      summary: 获取用户列表
      tags: [Users]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: page_size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        username:
          type: string
        email:
          type: string
          format: email
      required:
        - username
        - email

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

## 13. 最佳实践

- ✅ 使用 HTTPS
- ✅ 使用 JSON 作为默认格式
- ✅ 提供完整的 OpenAPI 文档
- ✅ 实现 CORS 支持
- ✅ 记录所有 API 请求日志
- ✅ 实现请求 ID 追踪
- ✅ 提供 API 版本管理
- ✅ 实现限流保护
- ✅ 返回有意义的错误信息
- ✅ 支持 gzip 压缩

## 14. 禁止事项

- ❌ 在 URL 中暴露敏感信息
- ❌ 返回详细的错误堆栈（生产环境）
- ❌ 使用 GET 请求修改数据
- ❌ 忽略 HTTP 状态码语义
- ❌ 不一致的响应格式
- ❌ 缺少认证和授权
- ❌ 不实现限流
- ❌ 缺少 API 文档
