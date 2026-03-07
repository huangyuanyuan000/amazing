# Init Project Skill - 对话式项目初始化

## 功能描述
通过自然语言对话，智能初始化项目架构。

## 触发方式
```bash
/init-project
```

或直接对话：
```
初始化一个电商平台项目...
创建一个 SaaS 平台...
我要做一个 IoT 管理系统...
```

## 对话流程

### 1. 需求收集
```
🤖: 请描述你的项目需求：
- 项目类型（电商/SaaS/AI 平台/IoT/其他）
- 核心功能模块
- 技术栈偏好（如有）
- 部署环境（本地/Docker/K8s/离线）
- 数据库选择（如有）

👤: 我要做一个电商平台，需要：
- 用户系统、商品管理、订单系统、支付系统
- 使用 Python + React
- 支持 Docker 和 K8s 部署
- 使用 PostgreSQL 数据库
```

### 2. 架构生成
```
🤖: 正在生成项目架构...

✅ 项目架构已生成：
- 技术栈: Python (FastAPI) + React + TypeScript
- 数据库: PostgreSQL + Redis
- 部署: Docker Compose + Kubernetes
- 业务模块:
  - user: 用户系统
  - product: 商品管理
  - order: 订单系统
  - payment: 支付系统

是否确认？(y/n)
```

### 3. 项目初始化
```
👤: y

🤖: 正在初始化项目...
✅ 项目初始化完成！

项目路径: ./my-ecommerce
启动方式:
  - 本地开发: cd my-ecommerce && make dev
  - Docker 部署: cd my-ecommerce && make docker
  - K8s 部署: cd my-ecommerce && make k8s
```

## 智能能力

### 1. 需求理解
- 自然语言解析
- 业务模块识别
- 技术栈推荐

### 2. 架构设计
- 根据需求自动选择技术栈
- 自动设计数据库 Schema
- 自动生成 API 接口
- 自动配置部署方案

### 3. 代码生成
- 生成项目骨架
- 生成业务模块代码
- 生成测试用例
- 生成部署配置

### 4. 最佳实践
- 应用开发规范
- 配置 CI/CD
- 添加监控告警
- 配置进化能力

## 示例对话

### 示例 1: AI 平台
```
👤: 初始化一个大模型管理平台，需要算力管理、数据管理、模型训练、模型服务

🤖: 正在分析需求...

建议架构：
- 技术栈: Python (FastAPI) + Go (高性能服务) + React
- 数据库: PostgreSQL (主库) + MongoDB (日志) + Redis (缓存)
- 部署: Kubernetes (推荐，支持 GPU 调度)
- 业务模块:
  - compute: 算力平台 (Go)
  - data: 数据平台 (Python)
  - training: 训推平台 (Python + Go)
  - model-service: 模型服务 (Go)

是否确认？
```

### 示例 2: SaaS 平台
```
👤: 创建一个 SaaS 平台，需要多租户、权限管理、数据隔离

🤖: 正在分析需求...

建议架构：
- 技术栈: Python (FastAPI) + React + TypeScript
- 数据库: PostgreSQL (支持 Schema 隔离)
- 部署: Docker Compose + Kubernetes
- 业务模块:
  - tenant: 租户管理
  - auth: 认证授权
  - user: 用户管理
  - billing: 计费系统

特性：
- 多租户架构（Schema 隔离）
- RBAC 权限模型
- 数据加密
- 审计日志

是否确认？
```

## 配置

### 模板映射
```yaml
# .claude/skills/init-project/templates.yml
keywords:
  电商|e-commerce|商城:
    template: e-commerce
    modules: [user, product, order, payment]

  AI平台|大模型|LLM:
    template: ai-platform
    modules: [compute, data, training, model-service]

  SaaS|多租户:
    template: saas-platform
    modules: [tenant, auth, user, billing]

  IoT|物联网:
    template: iot-platform
    modules: [device, data, rule, alert]
```

### 技术栈推荐
```yaml
# .claude/skills/init-project/tech-stack.yml
rules:
  - condition: 高性能|大并发|实时
    backend: Go
    database: PostgreSQL + Redis

  - condition: AI|机器学习|深度学习
    backend: Python
    database: PostgreSQL + MongoDB

  - condition: 快速开发|原型
    backend: Python (FastAPI)
    database: SQLite (dev) + PostgreSQL (prod)
```

## 进化能力
- 学习用户偏好
- 优化架构推荐
- 积累最佳实践
- 自动更新模板
