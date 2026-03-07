# 大模型管理平台 - AI Coding 规范

## 项目概述
大模型管理平台（Amazing Model Platform），提供完整的大模型生命周期管理能力。

## 业务模块

### 1. 通用功能（Common）
- **用户管理**：用户注册、登录、权限管理
- **权限控制**：RBAC 权限模型、资源隔离
- **日志审计**：操作日志、审计追踪

### 2. 算力平台（Compute）
- **资源管理**：GPU/CPU 资源池管理
- **任务调度**：智能调度、资源分配
- **监控告警**：资源监控、异常告警

### 3. 数据平台（Data）
- **数据集管理**：数据集上传、版本管理
- **数据标注**：标注任务、质量控制
- **数据质量**：数据清洗、质量评估

### 4. 训推平台（Training）
- **模型训练**：训练任务管理、分布式训练
- **实验管理**：实验追踪、参数管理
- **超参调优**：自动调参、最优模型选择

### 5. 模型服务（Model Service）
- **模型部署**：一键部署、版本管理
- **推理服务**：高性能推理、负载均衡
- **模型监控**：性能监控、质量监控

### 6. 运营管理（Operations）
- **数据分析**：用户分析、资源分析
- **用户运营**：用户画像、运营活动
- **系统配置**：系统参数、功能开关

### 7. API 开放平台（API Gateway）
- **API 管理**：API 注册、文档生成
- **限流鉴权**：流量控制、身份验证
- **API 监控**：调用统计、性能监控

## 技术架构

### 后端技术栈
- **Python (FastAPI)**：通用功能、数据平台、训推平台
- **Go (Gin)**：算力平台、模型服务、API 网关（高性能）

### 前端技术栈
- **React 18**：UI 框架
- **TypeScript**：类型安全
- **Vite**：构建工具
- **Ant Design**：UI 组件库

### 数据库
- **PostgreSQL 14+**：主数据库（用户、资源、任务）
- **MongoDB 5+**：日志存储（操作日志、训练日志）
- **Redis 7+**：缓存（会话、配置、队列）

### 基础设施
- **Kubernetes**：容器编排
- **Docker**：容器化
- **Helm**：应用部署
- **Prometheus + Grafana**：监控告警

## 目录结构

```
model-platform/
├── CLAUDE.md                     # 项目配置
├── README.md                     # 项目说明
├── Makefile                      # 快捷命令
│
├── .claude/                      # Claude 配置
│   ├── roles/                    # 角色配置
│   ├── ironclaw/                 # 权限配置
│   └── skills/                   # 技能配置
│
├── .agents/                      # 业务 Agent
│   ├── common/                   # 通用功能
│   ├── compute/                  # 算力平台
│   ├── data/                     # 数据平台
│   ├── training/                 # 训推平台
│   ├── model-service/            # 模型服务
│   ├── operations/               # 运营管理
│   └── api-gateway/              # API 网关
│
├── src/                          # 源代码
│   ├── backend/                  # 后端代码
│   │   ├── common/               # 通用模块（Python）
│   │   ├── data/                 # 数据平台（Python）
│   │   ├── training/             # 训推平台（Python）
│   │   ├── compute/              # 算力平台（Go）
│   │   ├── model-service/        # 模型服务（Go）
│   │   └── api-gateway/          # API 网关（Go）
│   │
│   ├── frontend/                 # 前端代码
│   │   ├── src/
│   │   │   ├── pages/            # 页面
│   │   │   ├── components/       # 组件
│   │   │   ├── services/         # API 服务
│   │   │   └── utils/            # 工具函数
│   │   ├── package.json
│   │   └── vite.config.ts
│   │
│   └── shared/                   # 共享代码
│       ├── types/                # 类型定义
│       └── constants/            # 常量定义
│
├── deploy/                       # 部署配置
│   ├── local/                    # 本地开发
│   │   ├── docker-compose.yml
│   │   └── .env.example
│   ├── docker/                   # Docker 部署
│   │   ├── docker-compose.yml
│   │   └── Dockerfile.*
│   ├── k8s/                      # Kubernetes 部署
│   │   ├── base/                 # 基础配置
│   │   ├── overlays/             # 环境配置
│   │   └── helm/                 # Helm Charts
│   └── offline/                  # 离线部署
│       └── install.sh
│
├── docs/                         # 文档
│   ├── architecture/             # 架构文档
│   ├── api/                      # API 文档
│   ├── deployment/               # 部署文档
│   └── development/              # 开发文档
│
├── tests/                        # 测试
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   └── e2e/                      # E2E 测试
│
└── scripts/                      # 脚本
    ├── init-db.sh                # 初始化数据库
    ├── migrate.sh                # 数据迁移
    └── deploy.sh                 # 部署脚本
```

## 部署配置

### 本地开发
```bash
make dev
```
- 使用 SQLite（开发数据库）
- 使用本地 Redis
- 热重载开发

### Docker 部署
```bash
make docker
```
- PostgreSQL + MongoDB + Redis
- 所有服务容器化
- 一键启动

### Kubernetes 部署
```bash
make k8s
```
- 生产级集群部署
- 自动扩缩容
- 高可用配置

### 离线部署
```bash
make offline
```
- 打包所有依赖
- 私有化部署
- 无需外网

## 数据库配置

### PostgreSQL（主库）
```yaml
database:
  host: postgres
  port: 5432
  database: model_platform
  schemas:
    - users          # 用户表
    - resources      # 资源表
    - datasets       # 数据集表
    - training_jobs  # 训练任务表
    - models         # 模型表
```

### MongoDB（日志）
```yaml
mongodb:
  host: mongodb
  port: 27017
  database: logs
  collections:
    - operation_logs  # 操作日志
    - training_logs   # 训练日志
    - api_logs        # API 日志
```

### Redis（缓存）
```yaml
redis:
  host: redis
  port: 6379
  databases:
    0: session       # 会话缓存
    1: config        # 配置缓存
    2: queue         # 任务队列
```

## 进化配置

### 影响分析规则
```yaml
impact_rules:
  - source: common/auth
    targets: [compute, data, training, model-service, operations, api-gateway]
    action: notify

  - source: compute/resources
    targets: [training, model-service]
    action: auto_update

  - source: data/datasets
    targets: [training]
    action: notify

  - source: training/models
    targets: [model-service]
    action: auto_update

  - source: model-service/api
    targets: [api-gateway, operations]
    action: notify
```

### 通知规则
```yaml
notification_rules:
  - trigger: api_change
    notify: [frontend-dev, api-gateway-dev]
    channels: [slack, email]

  - trigger: database_schema_change
    notify: [backend-dev, devops-engineer]
    channels: [slack, email]

  - trigger: deployment_config_change
    notify: [devops-engineer]
    channels: [slack]

  - trigger: business_logic_change
    notify: [product-manager, test-engineer]
    channels: [email]
```

## 开发规范

继承框架规范，详见 `../../standards/`

### 额外规范
- **API 版本**：使用 `/api/v1/` 前缀
- **错误码**：统一错误码体系（10000-99999）
- **日志格式**：JSON 格式，包含 trace_id
- **监控指标**：Prometheus 格式

## AI 工具链

- **Claude Code CLI**：主力开发工具
- **Codex CLI**：本地降级方案
- **Codex Desktop**：可视化操作
