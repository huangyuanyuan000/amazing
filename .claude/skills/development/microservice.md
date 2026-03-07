# Microservice Skill - 微服务设计模式

## 功能描述
提供微服务架构设计模式、服务拆分策略和通信方案。

## 触发方式
- 微服务架构设计
- 单体拆分
- 服务间通信设计

## 核心内容

### 1. 服务拆分原则
- **单一职责**: 每个服务只做一件事
- **业务边界**: 按领域驱动设计（DDD）划分
- **数据自治**: 每个服务拥有自己的数据库
- **独立部署**: 服务可独立构建、测试、部署

### 2. 通信模式
| 模式 | 协议 | 适用场景 |
|------|------|----------|
| 同步 REST | HTTP/JSON | CRUD 操作 |
| 同步 gRPC | HTTP/2 + Protobuf | 高性能内部调用 |
| 异步消息 | RabbitMQ/Kafka | 事件驱动、解耦 |
| 事件溯源 | Event Store | 审计、回溯 |

### 3. 关键模式
- **API Gateway**: 统一入口，路由、限流、认证
- **服务发现**: Consul/K8s Service
- **熔断器**: Circuit Breaker
- **分布式追踪**: Jaeger/Zipkin
- **配置中心**: Consul/Apollo/Nacos

### 4. 数据一致性
- **Saga 模式**: 编排式/协调式事务
- **最终一致性**: 事件驱动 + 补偿机制
- **TCC**: Try-Confirm-Cancel

## 示例
### 电商微服务拆分
```
API Gateway
├── 用户服务 (PostgreSQL)
├── 商品服务 (PostgreSQL + ES)
├── 订单服务 (PostgreSQL)
├── 支付服务 (PostgreSQL)
└── 消息队列 (RabbitMQ)
```

## 进化能力
- 服务拆分策略持续优化
- 通信模式最佳实践积累
- 故障模式学习
