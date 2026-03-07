# API Gateway Agent - API 开放平台

## 职责
负责 API 管理、限流鉴权、API 监控等，提供统一的 API 网关服务。

## 核心功能

### 1. API 管理
- API 注册：自动发现、手动注册
- API 文档：自动生成 OpenAPI 文档
- API 版本：版本管理、兼容性检查

### 2. 限流鉴权
- 流量控制：QPS 限流、并发限流
- 身份验证：API Key、JWT Token
- 权限控制：基于角色的访问控制

### 3. API 监控
- 调用统计：调用次数、成功率、响应时间
- 性能监控：P50/P95/P99 延迟
- 异常告警：错误率告警、超时告警

### 4. 协议转换
- HTTP/HTTPS
- gRPC
- WebSocket

## 技术栈
- **后端**: Go (Gin)
- **网关**: Kong / Traefik
- **监控**: Prometheus + Grafana

## API 接口

### API 管理
- `POST /api/v1/gateway/apis` - 注册 API
- `GET /api/v1/gateway/apis` - 获取 API 列表
- `GET /api/v1/gateway/apis/{id}/docs` - API 文档

### 限流鉴权
- `POST /api/v1/gateway/keys` - 创建 API Key
- `POST /api/v1/gateway/rate-limits` - 配置限流
- `POST /api/v1/gateway/auth` - 验证身份

### API 监控
- `GET /api/v1/gateway/metrics` - 获取指标
- `GET /api/v1/gateway/logs` - 获取日志
- `POST /api/v1/gateway/alerts` - 配置告警

## 数据模型

### API 定义
```go
type API struct {
    ID          string    `json:"id"`
    Name        string    `json:"name"`
    Path        string    `json:"path"`
    Method      string    `json:"method"`
    Service     string    `json:"service"`
    Version     string    `json:"version"`
    RateLimit   int       `json:"rate_limit"`
    CreatedAt   time.Time `json:"created_at"`
}
```

### API Key
```go
type APIKey struct {
    Key         string    `json:"key"`
    UserID      string    `json:"user_id"`
    Permissions []string  `json:"permissions"`
    RateLimit   int       `json:"rate_limit"`
    ExpiresAt   time.Time `json:"expires_at"`
}
```

### API 指标
```go
type APIMetrics struct {
    API         string  `json:"api"`
    Requests    int64   `json:"requests"`
    Errors      int64   `json:"errors"`
    AvgLatency  float64 `json:"avg_latency"`
    P95Latency  float64 `json:"p95_latency"`
}
```

## Sub-Agents

### Router Agent
负责请求路由和转发。

### Auth Agent
负责身份验证和权限控制。

### Monitor Agent
负责 API 监控和告警。

## 路由规则

```yaml
routes:
  - path: /api/v1/compute/*
    service: compute-service
    rate_limit: 1000

  - path: /api/v1/data/*
    service: data-service
    rate_limit: 500

  - path: /api/v1/training/*
    service: training-service
    rate_limit: 200

  - path: /api/v1/models/*
    service: model-service
    rate_limit: 1000

  - path: /api/v1/operations/*
    service: operations-service
    rate_limit: 100
```

## 限流策略

```yaml
rate_limits:
  # 全局限流
  global:
    qps: 10000
    concurrent: 1000

  # 用户限流
  per_user:
    qps: 100
    concurrent: 10

  # API 限流
  per_api:
    compute: 1000
    data: 500
    training: 200
    models: 1000
```

## 依赖关系
- 依赖 Common Agent（用户、权限）
- 路由到所有业务模块
- 被外部客户端调用

## 监控指标
- 总请求数
- 错误率
- 平均响应时间
- P95/P99 延迟
- 限流触发次数
