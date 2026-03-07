# API Design Skill - RESTful API 设计规范

## 功能描述
提供 RESTful API 设计规范、OpenAPI 3.0 模板和接口设计最佳实践。

## 触发方式
- 新 API 端点设计
- API 版本升级
- API 文档生成

## 核心内容

### 1. URL 设计规范
```
GET    /api/v1/users          # 列表
POST   /api/v1/users          # 创建
GET    /api/v1/users/{id}     # 详情
PUT    /api/v1/users/{id}     # 全量更新
PATCH  /api/v1/users/{id}     # 部分更新
DELETE /api/v1/users/{id}     # 删除
```

### 2. 统一响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "meta": { "page": 1, "page_size": 20, "total": 100 }
}
```

### 3. 错误码规范
| 状态码 | 含义 | 使用场景 |
|--------|------|----------|
| 200 | 成功 | GET/PUT/PATCH/DELETE 成功 |
| 201 | 已创建 | POST 创建成功 |
| 400 | 请求错误 | 参数校验失败 |
| 401 | 未认证 | Token 无效/过期 |
| 403 | 无权限 | 权限不足 |
| 404 | 未找到 | 资源不存在 |
| 422 | 不可处理 | 业务逻辑错误 |
| 500 | 服务器错误 | 内部异常 |

### 4. 版本管理
- URL 路径版本: `/api/v1/`, `/api/v2/`
- 向后兼容: 新增字段不影响旧版本
- 废弃通知: 提前 2 个版本通知

## 示例
### OpenAPI 3.0 模板
```yaml
openapi: "3.0.3"
info:
  title: "API 名称"
  version: "1.0.0"
paths:
  /api/v1/users:
    get:
      summary: "获取用户列表"
      parameters:
        - name: page
          in: query
          schema: { type: integer, default: 1 }
      responses:
        "200":
          description: "成功"
```

## 进化能力
- API 设计模式库持续扩充
- 从 API 使用数据优化设计
- 自动生成 API 文档
