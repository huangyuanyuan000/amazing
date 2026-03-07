# Amazing 案例集

## 概述

本目录包含 3 个完整的 Amazing 架构案例，每个案例都展示了如何使用 Amazing 快速构建不同类型的应用。

所有案例都支持：
- ✅ 一键本地启动（Docker Compose）
- ✅ 一键 Kubernetes 部署
- ✅ 私有化部署
- ✅ 多数据库支持
- ✅ 完整的监控和日志

---

## 案例列表

### 1. 大模型管理平台

**目录**: `model-platform/`

**产品类型**: AI/ML 平台

**业务 Agent**:
- 💻 算力平台 Agent - GPU/CPU 资源管理
- 📊 数据 Agent - 数据集管理
- 🎓 训练 Agent - 模型训练
- 🚀 模型服务 Agent - 模型部署

**技术栈**:
- 后端：Python + FastAPI
- 数据库：PostgreSQL
- 对象存储：MinIO
- 缓存：Redis
- 队列：RabbitMQ

**快速启动**:
```bash
cd model-platform
make dev
```

**访问地址**:
- 前端：http://localhost:3000
- API：http://localhost:8000-8004

---

### 2. 电商平台

**目录**: `e-commerce/`

**产品类型**: B2C 电商

**业务 Agent**:
- 🛍️ 商品 Agent - 商品管理
- 📦 订单 Agent - 订单和购物车
- 💳 支付 Agent - 支付和结算
- 🚚 物流 Agent - 配送和跟踪

**技术栈**:
- 后端：Python + FastAPI, Go + Gin
- 数据库：PostgreSQL, MySQL
- 搜索：Elasticsearch
- 缓存：Redis
- 队列：RabbitMQ

**快速启动**:
```bash
cd e-commerce
make dev
```

**访问地址**:
- 前端：http://localhost:3000
- API：http://localhost:8000-8004

---

### 3. SaaS 平台

**目录**: `saas-platform/`

**产品类型**: 多租户 SaaS

**业务 Agent**:
- 🏢 租户 Agent - 租户管理
- 📋 项目 Agent - 项目管理
- 👥 协作 Agent - 团队协作
- 📊 分析 Agent - 数据分析

**技术栈**:
- 后端：Python + FastAPI, Node.js + NestJS
- 数据库：PostgreSQL, MongoDB
- 分析：ClickHouse
- 缓存：Redis
- 实时：Socket.io

**快速启动**:
```bash
cd saas-platform
make dev
```

**访问地址**:
- 前端：http://localhost:3000
- API：http://localhost:8000-8004

---

## 案例对比

| 特性 | 大模型平台 | 电商平台 | SaaS 平台 |
|------|-----------|---------|----------|
| **复杂度** | 高 | 中 | 高 |
| **业务 Agent** | 4 个 | 4 个 | 4 个 |
| **数据库** | PostgreSQL | PostgreSQL + MySQL | PostgreSQL + MongoDB |
| **特殊组件** | MinIO, GPU | Elasticsearch | ClickHouse, Socket.io |
| **适用场景** | AI/ML 平台 | 电商系统 | 企业 SaaS |
| **团队规模** | 10-15 人 | 8-12 人 | 10-15 人 |

---

## 通用功能

所有案例都包含以下通用功能：

### 固定 Agent

- **Common Agent**: 用户管理、权限控制、日志审计
- **Review Agent**: 代码审查、安全审查、质量把关

### 固定角色

- 👑 架构师
- 📋 产品经理
- 🎨 前端开发
- ⚙️ 后端开发
- 🧪 测试工程师
- 🚀 运维工程师

### 监控和日志

- Prometheus - 指标监控
- Grafana - 可视化
- ELK Stack - 日志分析（可选）

---

## 部署方式

### 本地开发环境

所有案例都支持一键启动：

```bash
# 进入案例目录
cd <case-name>

# 启动所有服务
make dev

# 查看服务状态
make status

# 查看日志
make logs

# 停止服务
make stop

# 清理环境
make clean
```

### Kubernetes 部署

所有案例都提供完整的 K8s 配置：

```bash
# 部署到 K8s
make k8s-deploy

# 查看部署状态
kubectl get pods -n <namespace>

# 查看服务
kubectl get svc -n <namespace>
```

### 私有化部署

所有案例都支持私有化部署：

```bash
# 运行安装脚本
./deploy/private/install.sh

# 配置参数
vim deploy/private/config.yaml

# 启动服务
./deploy/private/start.sh
```

---

## 目录结构

每个案例都遵循统一的目录结构：

```
<case-name>/
├── README.md                  # 案例说明
├── Makefile                   # 快速命令
├── .env.example               # 环境变量模板
│
├── docs/                      # 文档
│   ├── architecture.md        # 架构设计
│   ├── api.md                 # API 文档
│   └── database.md            # 数据库设计
│
├── backend/                   # 后端服务
│   ├── <agent-1>/
│   ├── <agent-2>/
│   └── ...
│
├── frontend/                  # 前端应用
│   ├── src/
│   └── package.json
│
└── deploy/                    # 部署配置
    ├── local/                 # 本地开发
    │   ├── docker-compose.yml
    │   └── init-db/
    ├── k8s/                   # Kubernetes
    │   ├── namespace.yaml
    │   ├── configmap.yaml
    │   └── *.yaml
    └── private/               # 私有化部署
        ├── install.sh
        └── config.yaml
```

---

## 数据库支持

### PostgreSQL

**使用案例**: 大模型平台、电商平台、SaaS 平台

**特点**:
- 功能强大
- 支持 JSON
- 事务完整
- 扩展性好

### MySQL

**使用案例**: 电商平台（支付服务）

**特点**:
- 使用广泛
- 性能稳定
- 生态丰富

### MongoDB

**使用案例**: SaaS 平台（协作服务）

**特点**:
- Schema 灵活
- 文档型存储
- 水平扩展

### ClickHouse

**使用案例**: SaaS 平台（分析服务）

**特点**:
- 列式存储
- 分析性能高
- 压缩率高

---

## 快速选择

### 我想构建 AI/ML 平台
→ 参考 **大模型管理平台** 案例

### 我想构建电商系统
→ 参考 **电商平台** 案例

### 我想构建企业 SaaS
→ 参考 **SaaS 平台** 案例

### 我想了解多数据库使用
→ 参考 **电商平台** 或 **SaaS 平台** 案例

### 我想了解多租户架构
→ 参考 **SaaS 平台** 案例

---

## 相关文档

- [Amazing 架构理念](../docs/00-overview/architecture.md)
- [快速开始](../docs/01-scaffolding/README.md)
- [Agent-Teams 层](../docs/02-agent-teams/README.md)
- [技术选型层](../docs/04-tech-stack/README.md)

---

## 贡献案例

欢迎贡献新的案例！

**贡献步骤**:
1. Fork 项目
2. 创建案例目录
3. 按照统一结构组织代码
4. 编写完整文档
5. 提交 Pull Request

**案例要求**:
- 完整的 README
- 支持一键启动
- 支持 K8s 部署
- 包含监控配置
- 代码规范

---

<div align="center">

**⭐ 如果觉得有帮助，欢迎 Star 支持！**

Made with ❤️ by Amazing Team

</div>
