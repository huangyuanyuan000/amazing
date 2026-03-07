# SaaS 平台案例

## 项目概述

这是一个基于 Amazing 架构的多租户 SaaS 平台完整案例，展示如何使用 Amazing 快速构建企业级 SaaS 系统。

## 产品形态

### 产品描述

```
我要构建一个多租户 SaaS 平台，提供企业级项目管理和协作工具。

目标用户：
- 企业管理员（租户管理）
- 项目经理（项目管理）
- 团队成员（任务协作）

使用场景：
- 企业注册和订阅
- 项目管理
- 团队协作
- 数据分析

核心功能包括：

1. 租户管理
   - 租户注册和认证
   - 租户配置
   - 数据隔离
   - 租户计费

2. 项目管理
   - 项目创建和管理
   - 任务分配和跟踪
   - 里程碑管理
   - 甘特图

3. 团队协作
   - 团队成员管理
   - 实时通讯
   - 文档共享
   - 评论和讨论

4. 数据分析
   - 项目统计
   - 团队效率分析
   - 自定义报表
   - 数据导出

5. 计费管理
   - 订阅计划
   - 使用量统计
   - 账单生成
   - 支付集成

技术要求：
- 多租户架构
- 数据隔离
- 高可用
- 可扩展

预期规模：
- 租户数：100 - 10000
- 用户数：1000 - 100000
- 项目数：10000 - 1000000
```

## 业务划分

### AI 推荐方案

**方案 A：按功能模块划分（推荐）**

```
├── 租户 Agent - 租户管理
│   ├── 租户注册和认证
│   ├── 租户配置
│   ├── 数据隔离
│   └── 租户计费
│
├── 项目 Agent - 项目管理
│   ├── 项目创建和管理
│   ├── 任务分配和跟踪
│   ├── 里程碑管理
│   └── 甘特图
│
├── 协作 Agent - 团队协作
│   ├── 团队成员管理
│   ├── 实时通讯
│   ├── 文档共享
│   └── 评论和讨论
│
└── 分析 Agent - 数据分析
    ├── 项目统计
    ├── 团队效率分析
    ├── 自定义报表
    └── 数据导出
```

## 技术架构

### 技术栈选择

#### 租户 Agent
```json
{
  "backend": "Python + FastAPI",
  "database": "PostgreSQL (多租户模式)",
  "cache": "Redis",
  "auth": "JWT + OAuth2"
}
```

#### 项目 Agent
```json
{
  "backend": "Python + FastAPI",
  "database": "PostgreSQL",
  "cache": "Redis",
  "queue": "RabbitMQ"
}
```

#### 协作 Agent
```json
{
  "backend": "Node.js + NestJS",
  "database": "MongoDB",
  "cache": "Redis",
  "realtime": "Socket.io"
}
```

#### 分析 Agent
```json
{
  "backend": "Python + FastAPI",
  "database": "PostgreSQL",
  "cache": "Redis",
  "analytics": "ClickHouse"
}
```

### 多租户架构

#### 数据隔离策略

**方案 1：共享数据库，共享 Schema（推荐）**

```sql
-- 所有表都包含 tenant_id
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    tenant_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tenant_id (tenant_id)
);

-- 行级安全策略（RLS）
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON projects
    USING (tenant_id = current_setting('app.current_tenant')::int);
```

**方案 2：共享数据库，独立 Schema**

```sql
-- 为每个租户创建独立 Schema
CREATE SCHEMA tenant_1;
CREATE SCHEMA tenant_2;

-- 在租户 Schema 中创建表
CREATE TABLE tenant_1.projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 部署方式

### 本地开发环境

```bash
# 进入项目目录
cd examples/saas-platform

# 启动所有服务
make dev

# 或使用 Docker Compose
docker-compose -f deploy/local/docker-compose.yml up
```

**访问地址**：
- 前端：http://localhost:3000
- 租户服务：http://localhost:8001
- 项目服务：http://localhost:8002
- 协作服务：http://localhost:8003
- 分析服务：http://localhost:8004

### Kubernetes 部署

```bash
# 部署到 K8s
make k8s-deploy

# 或手动部署
kubectl apply -f deploy/k8s/
```

### 私有化部署

```bash
# 使用私有化部署脚本
./deploy/private/install.sh

# 配置私有化参数
vim deploy/private/config.yaml
```

## 核心功能

### 租户注册流程

```
1. 企业注册
   ├── 填写企业信息
   ├── 选择订阅计划
   └── 创建管理员账号
   ↓
2. 租户初始化
   ├── 创建租户数据库/Schema
   ├── 初始化租户配置
   └── 分配资源配额
   ↓
3. 开始使用
   ├── 邀请团队成员
   ├── 创建项目
   └── 开始协作
```

### 数据隔离

```python
# 中间件：设置当前租户
@app.middleware("http")
async def tenant_middleware(request: Request, call_next):
    tenant_id = get_tenant_from_request(request)

    # 设置租户上下文
    set_current_tenant(tenant_id)

    # 设置数据库会话变量
    await db.execute(
        f"SET app.current_tenant = {tenant_id}"
    )

    response = await call_next(request)
    return response
```

### 计费管理

```
订阅计划：
├── 免费版
│   ├── 5 个用户
│   ├── 10 个项目
│   └── 1GB 存储
│
├── 专业版（$29/月）
│   ├── 50 个用户
│   ├── 100 个项目
│   └── 10GB 存储
│
└── 企业版（$99/月）
    ├── 无限用户
    ├── 无限项目
    └── 100GB 存储
```

## 目录结构

```
saas-platform/
├── docs/
│   ├── README.md              # 本文档
│   ├── architecture.md        # 架构设计
│   ├── multi-tenancy.md       # 多租户设计
│   └── api.md                 # API 文档
│
├── backend/
│   ├── tenant/                # 租户服务
│   ├── project/               # 项目服务
│   ├── collaboration/         # 协作服务
│   └── analytics/             # 分析服务
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── tenant/       # 租户管理
│   │   │   ├── project/      # 项目管理
│   │   │   ├── team/         # 团队协作
│   │   │   └── analytics/    # 数据分析
│   │   └── components/
│   └── package.json
│
├── deploy/
│   ├── local/
│   │   ├── docker-compose.yml
│   │   └── Makefile
│   ├── k8s/
│   │   ├── tenant.yaml
│   │   ├── project.yaml
│   │   ├── collaboration.yaml
│   │   └── analytics.yaml
│   └── private/
│       ├── install.sh
│       └── config.yaml
│
├── .env.example
├── Makefile
└── README.md
```

## 性能指标

### 目标指标

- **租户数**：10000+
- **并发用户**：50000+
- **QPS**：10000+
- **响应时间**：< 100ms
- **可用性**：99.95%

### 优化措施

1. **多租户优化**
   - 租户数据缓存
   - 连接池隔离
   - 资源配额限制

2. **数据库优化**
   - 分区表
   - 索引优化
   - 查询优化

3. **缓存策略**
   - 租户配置缓存
   - 用户会话缓存
   - 查询结果缓存

## 相关文档

- [架构设计](./architecture.md)
- [多租户设计](./multi-tenancy.md)
- [API 文档](./api.md)
- [部署指南](./deployment.md)
