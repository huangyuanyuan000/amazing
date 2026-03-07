# API 设计规范

本目录包含 Amazing 框架的 API 设计规范标准。

## 规范文件

- `restful.md` - RESTful API 设计规范
- `graphql.md` - GraphQL API 设计规范（待补充）
- `grpc.md` - gRPC API 设计规范（待补充）
- `websocket.md` - WebSocket 设计规范（待补充）

## 核心原则

1. **一致性** - 所有 API 遵循统一的设计模式
2. **可预测性** - URL 和响应格式符合直觉
3. **版本化** - 支持 API 版本管理
4. **文档化** - 提供完整的 OpenAPI 文档
5. **安全性** - 认证、授权、限流、HTTPS

## 快速参考

### URL 设计
```
GET    /api/v1/users          # 列表
POST   /api/v1/users          # 创建
GET    /api/v1/users/{id}     # 详情
PUT    /api/v1/users/{id}     # 更新
DELETE /api/v1/users/{id}     # 删除
```

### 统一响应
```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "meta": {}
}
```
