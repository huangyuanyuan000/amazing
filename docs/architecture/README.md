# Amazing 架构设计

## 1. 系统架构

### 1.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      用户层                                  │
│  产品经理 | 前端 | 后端 | 测试 | 运维 | 运营                 │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    统一入口层                              │
│  CLI (amazing-cli) | Web Dashboard (OpenClaw)            │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                   AI 工具链层                              │
│  Claude Code (主) → Codex CLI (备) → Codex Desktop       │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                Agent Orchestrator                          │
│  - 角色权限管理                                            │
│  - 场景路由 (开发/修复/分析)                               │
│  - 进化管理 (Agent/Sub-Agent/Skill)                       │
└─────────────────────────────┬─────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌───────▼────────┐   ┌───────▼────────┐
│  Common Agent  │   │ Compute Agent  │   │  Data Agent    │
│  (通用模块)    │   │  (算力平台)    │   │  (数据平台)    │
└───────┬────────┘   └───────┬────────┘   └───────┬────────┘
        │                     │                     │
┌───────▼────────┐   ┌───────▼────────┐   ┌───────▼────────┐
│ Training Agent │   │Model Svc Agent │   │ Review Agent   │
│  (训推平台)    │   │ (模型服务)     │   │   (审核)       │
└────────────────┘   └────────────────┘   └────────────────┘
```

### 1.2 Agent 架构

每个 Agent 包含:
- **Sub-Agents**: PM, Frontend, Backend, QA, Ops, Operation
- **Skills**: 可进化的能力单元
- **Evolution Metrics**: 进化指标监控

```
Agent
├── Sub-Agent (PM)
│   ├── Skills: [prd-generator, requirement-analyzer]
│   └── Tools: [claude-code, codex]
├── Sub-Agent (Frontend)
│   ├── Skills: [react-component, ui-design]
│   └── Tools: [claude-code, codex]
├── Sub-Agent (Backend)
│   ├── Skills: [api-design, database-design]
│   └── Tools: [claude-code, codex]
└── Evolution Engine
    ├── Metrics Collection
    ├── Performance Analysis
    └── Auto Upgrade
```

## 2. 技术架构

### 2.1 前端架构

```
Frontend (React + TypeScript)
├── UI Layer
│   ├── Components (Ant Design)
│   ├── Pages
│   └── Layouts
├── State Management (Zustand)
├── API Layer (Axios)
└── Build Tool (Vite)
```

### 2.2 后端架构

```
Backend
├── Python Services (FastAPI)
│   ├── API Gateway
│   ├── Business Logic
│   ├── ORM (SQLAlchemy)
│   └── Auth (JWT)
└── Go Services
    ├── High Performance APIs
    ├── Resource Scheduler
    └── gRPC Services
```

### 2.3 数据架构

```
Data Layer
├── PostgreSQL (主库)
│   ├── 用户数据
│   ├── 业务数据
│   └── 元数据
├── Redis (缓存)
│   ├── Session
│   ├── Cache
│   └── Queue
├── MongoDB (可选)
│   └── 日志/文档
└── MinIO (对象存储)
    └── 文件/模型
```

## 3. 部署架构

### 3.1 本地开发

```
Local Development
├── Python API (8000)
├── Go API (8080)
├── Frontend (3000)
├── PostgreSQL (5432)
└── Redis (6379)
```

### 3.2 Docker 部署

```
Docker Compose
├── Services
│   ├── python-api
│   ├── go-api
│   ├── frontend
│   ├── postgres
│   └── redis
└── Volumes
    ├── postgres_data
    └── redis_data
```

### 3.3 Kubernetes 部署

```
Kubernetes
├── Namespace: amazing
├── Deployments
│   ├── python-api (2 replicas)
│   ├── go-api (2 replicas)
│   ├── frontend (2 replicas)
│   ├── postgres (1 replica)
│   └── redis (1 replica)
├── Services
│   ├── python-api (ClusterIP)
│   ├── go-api (ClusterIP)
│   ├── frontend (LoadBalancer)
│   ├── postgres (ClusterIP)
│   └── redis (ClusterIP)
└── Storage
    └── postgres-pvc (10Gi)
```

## 4. 工作流架构

### 4.1 功能开发流程

```
1. 需求分析 (PM)
   ↓
2. PRD 生成 (PM + Claude Code)
   ↓
3. 技术评审 (Frontend + Backend)
   ↓
4. 并行开发
   ├── 前端开发 (Frontend + Claude Code)
   └── 后端开发 (Backend + Claude Code)
   ↓
5. 集成测试 (QA + Claude Code)
   ↓
6. 代码审查 (Review Agent)
   ↓
7. 部署上线 (Ops + Claude Code)
```

### 4.2 Bug 修复流程

```
1. Bug 报告 (QA/User)
   ↓
2. Bug 复现 (QA + Claude Code)
   ↓
3. 问题定位 (Backend + Claude Code)
   ↓
4. 代码修复 (Backend + Claude Code)
   ↓
5. 回归测试 (QA + Claude Code)
   ↓
6. 热修复部署 (Ops + Claude Code)
   ↓
7. 回滚机制 (如果失败)
```

### 4.3 需求分析流程

```
1. 需求收集 (PM)
   ↓
2. 需求分析 (PM + Claude Code)
   ├── 功能拆解
   ├── 优先级排序
   └── 可行性评估
   ↓
3. PRD 生成 (PM + Claude Code)
   ├── 使用 prd-template.md
   ├── 自动填充内容
   └── 生成技术方案
   ↓
4. 技术评审 (All Roles)
   ↓
5. 进入开发流程
```

## 5. 进化机制

### 5.1 Agent 进化

```
Agent Evolution
├── Metrics Collection
│   ├── Task Success Rate
│   ├── Code Quality Score
│   └── Delivery Time
├── Performance Analysis
│   ├── Threshold Check
│   └── Trend Analysis
└── Auto Upgrade
    ├── Capability Enhancement
    └── Version Control
```

### 5.2 Sub-Agent 进化

```
Sub-Agent Evolution
├── Role Efficiency Metrics
├── Collaboration Score
└── Skill Improvement
```

### 5.3 Skill 进化

```
Skill Evolution
├── Accuracy Metrics
├── Performance Metrics
├── User Satisfaction
└── Version Management
```

## 6. 安全架构

```
Security
├── Authentication
│   ├── JWT Token
│   └── OAuth2
├── Authorization
│   ├── RBAC
│   └── Permission Matrix
├── Data Security
│   ├── Encryption at Rest
│   └── Encryption in Transit
└── Audit
    ├── Operation Logs
    └── Access Logs
```

## 7. 监控架构

```
Monitoring
├── Application Monitoring
│   ├── Prometheus
│   └── Grafana
├── Log Management
│   ├── ELK Stack
│   └── Loki
├── Tracing
│   └── Jaeger
└── Alerting
    └── AlertManager
```
