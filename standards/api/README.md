# API 设计规范

## RESTful + OpenAPI 3.0

### 统一响应格式
```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "request_id": "uuid"
  }
}
```

### 错误响应
```json
{
  "code": 40001,
  "message": "Validation failed",
  "errors": [
    {"field": "email", "message": "Invalid email format"}
  ],
  "meta": {
    "request_id": "uuid"
  }
}
```

### 错误码规范
| 范围 | 类型 | 示例 |
|------|------|------|
| 0 | 成功 | 0 |
| 40000-40099 | 参数错误 | 40001 参数校验失败 |
| 40100-40199 | 认证错误 | 40101 Token 过期 |
| 40300-40399 | 权限错误 | 40301 无权访问 |
| 40400-40499 | 资源不存在 | 40401 用户不存在 |
| 50000-50099 | 服务器错误 | 50001 数据库异常 |

### URL 规范
```
GET    /api/v1/users          # 列表
POST   /api/v1/users          # 创建
GET    /api/v1/users/{id}     # 详情
PUT    /api/v1/users/{id}     # 更新
DELETE /api/v1/users/{id}     # 删除
POST   /api/v1/users/{id}/actions/disable  # 特殊操作
```

### 分页参数
```
GET /api/v1/users?page=1&page_size=20&sort=-created_at&filter[role]=admin
```

### FastAPI 模板
```python
from fastapi import APIRouter, Query, Path
from app.schemas.common import PageResponse, ErrorResponse

router = APIRouter(prefix="/api/v1")

@router.get(
    "/users",
    response_model=PageResponse[UserResponse],
    responses={401: {"model": ErrorResponse}},
    summary="获取用户列表",
    tags=["用户管理"],
)
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
):
    ...
```

### 版本管理
- URL 路径版本: `/api/v1/`, `/api/v2/`
- 新版本必须向后兼容，或提供迁移指南
- 旧版本最少维护 2 个大版本周期
