# Amazing 项目初始化架构

## 概述

本文档描述 Amazing 项目的完整初始化架构，包括 backend、frontend、scripts、infra 等所有组件。

这是基于大模型管理平台的早期架构设计，经过优化后形成的通用项目模板。

---

## 目录结构

```
project-root/
├── .agents/                    # Agent 配置
│   ├── common/                # Common Agent（固定）
│   ├── review/                # Review Agent（固定）
│   ├── compute/               # 业务 Agent 1
│   ├── data/                  # 业务 Agent 2
│   ├── training/              # 业务 Agent 3
│   └── model-service/         # 业务 Agent 4
│
├── .claude/                   # Claude 配置
│   ├── config.json           # Claude 配置
│   ├── settings.json         # 设置
│   └── roles/                # 角色配置
│       └── config.json
│
├── backend/                   # 后端服务
│   ├── common/               # 通用服务（Python）
│   │   ├── app/
│   │   │   ├── api/         # API 路由
│   │   │   ├── models/      # 数据模型
│   │   │   ├── services/    # 业务逻辑
│   │   │   └── utils/       # 工具函数
│   │   ├── tests/           # 测试
│   │   ├── requirements.txt # 依赖
│   │   ├── Dockerfile       # Docker 配置
│   │   └── main.py          # 入口文件
│   │
│   ├── compute/              # 算力服务（Python）
│   ├── data/                 # 数据服务（Python）
│   ├── training/             # 训练服务（Python）
│   └── model-service/        # 模型服务（Go）
│       ├── cmd/
│       ├── internal/
│       ├── pkg/
│       ├── Dockerfile
│       └── go.mod
│
├── frontend/                  # 前端应用
│   ├── public/
│   ├── src/
│   │   ├── pages/           # 页面
│   │   │   ├── compute/    # 算力管理
│   │   │   ├── data/       # 数据管理
│   │   │   ├── training/   # 训练管理
│   │   │   └── model/      # 模型管理
│   │   ├── components/      # 组件
│   │   ├── services/        # API 服务
│   │   ├── stores/          # 状态管理
│   │   ├── utils/           # 工具函数
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── scripts/                   # 脚本工具
│   ├── amazing-cli.py        # 主 CLI 工具
│   ├── architect_cli.py      # 架构师 CLI
│   ├── mode_cli.py           # 模式管理 CLI
│   ├── deploy.sh             # 部署脚本
│   └── init.sh               # 初始化脚本
│
├── infra/                     # 基础设施
│   ├── docker/               # Docker 配置
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   └── docker-compose.prod.yml
│   ├── k8s/                  # Kubernetes 配置
│   │   ├── namespace.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   ├── postgres.yaml
│   │   ├── redis.yaml
│   │   ├── common.yaml
│   │   ├── compute.yaml
│   │   ├── data.yaml
│   │   ├── training.yaml
│   │   ├── model-service.yaml
│   │   ├── frontend.yaml
│   │   └── ingress.yaml
│   └── terraform/            # Terraform 配置
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── docs/                      # 文档
│   ├── architecture.md       # 架构设计
│   ├── api.md                # API 文档
│   └── deployment.md         # 部署文档
│
├── .env.example              # 环境变量模板
├── .gitignore
├── Makefile                  # 快速命令
├── README.md
└── amazing.config.json       # Amazing 配置
```

---

## Backend 架构

### Python 服务结构

```
backend/<service-name>/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用
│   ├── config.py            # 配置
│   ├── database.py          # 数据库连接
│   │
│   ├── api/                 # API 路由
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── users.py
│   │   │   │   └── resources.py
│   │   │   └── router.py
│   │   └── deps.py          # 依赖注入
│   │
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── resource.py
│   │
│   ├── schemas/             # Pydantic 模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── resource.py
│   │
│   ├── services/            # 业务逻辑
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── resource_service.py
│   │
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── security.py
│       └── helpers.py
│
├── tests/                   # 测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   └── test_services/
│
├── requirements.txt         # 依赖
├── requirements-dev.txt     # 开发依赖
├── Dockerfile
├── .dockerignore
└── README.md
```

### Go 服务结构

```
backend/<service-name>/
├── cmd/
│   └── server/
│       └── main.go          # 入口文件
│
├── internal/                # 内部包
│   ├── api/                # API 处理
│   │   ├── handler/
│   │   ├── middleware/
│   │   └── router/
│   ├── service/            # 业务逻辑
│   ├── repository/         # 数据访问
│   └── model/              # 数据模型
│
├── pkg/                     # 公共包
│   ├── config/
│   ├── database/
│   └── utils/
│
├── go.mod
├── go.sum
├── Dockerfile
└── README.md
```

---

## Frontend 架构

### React + TypeScript 结构

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
│
├── src/
│   ├── pages/               # 页面
│   │   ├── Home/
│   │   │   ├── index.tsx
│   │   │   └── styles.ts
│   │   ├── Compute/
│   │   ├── Data/
│   │   ├── Training/
│   │   └── Model/
│   │
│   ├── components/          # 组件
│   │   ├── Layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── Common/
│   │   │   ├── Button.tsx
│   │   │   ├── Table.tsx
│   │   │   └── Modal.tsx
│   │   └── Business/
│   │
│   ├── services/            # API 服务
│   │   ├── api.ts          # API 客户端
│   │   ├── auth.ts         # 认证服务
│   │   ├── compute.ts      # 算力服务
│   │   ├── data.ts         # 数据服务
│   │   └── training.ts     # 训练服务
│   │
│   ├── stores/              # 状态管理（Zustand）
│   │   ├── useAuthStore.ts
│   │   ├── useComputeStore.ts
│   │   └── useDataStore.ts
│   │
│   ├── hooks/               # 自定义 Hooks
│   │   ├── useAuth.ts
│   │   └── useApi.ts
│   │
│   ├── utils/               # 工具函数
│   │   ├── format.ts
│   │   └── validate.ts
│   │
│   ├── types/               # 类型定义
│   │   ├── api.ts
│   │   └── models.ts
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── vite-env.d.ts
│
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .eslintrc.js
├── .prettierrc
└── README.md
```

---

## Scripts 工具

### amazing-cli.py

主 CLI 工具，提供项目管理功能：

```python
#!/usr/bin/env python3
"""
Amazing CLI - 主命令行工具

功能：
- 项目初始化
- 角色管理
- Agent 管理
- 开发环境管理
"""

import click

@click.group()
def cli():
    """Amazing CLI - AI 范式架构平台"""
    pass

@cli.command()
@click.argument('project_name')
@click.option('--template', help='使用模板')
def init(project_name, template):
    """初始化新项目"""
    pass

@cli.group()
def role():
    """角色管理"""
    pass

@role.command()
def select():
    """选择角色"""
    pass

@cli.group()
def agent():
    """Agent 管理"""
    pass

@agent.command()
def list():
    """列出所有 Agent"""
    pass

if __name__ == '__main__':
    cli()
```

### architect_cli.py

架构师专用 CLI：

```python
#!/usr/bin/env python3
"""
Architect CLI - 架构师命令行工具

功能：
- 架构设计
- 代码审查
- 技术决策
- 质量把关
"""

import click

@click.group()
def cli():
    """Architect CLI - 架构师工具"""
    pass

@cli.group()
def arch():
    """架构管理"""
    pass

@arch.command()
@click.argument('feature')
def create(feature):
    """创建架构设计"""
    pass

@cli.group()
def review():
    """代码审查"""
    pass

@review.command()
def pending():
    """查看待审查任务"""
    pass

if __name__ == '__main__':
    cli()
```

### mode_cli.py

模式管理 CLI：

```python
#!/usr/bin/env python3
"""
Mode CLI - AI 模式管理工具

功能：
- 模式切换（全自动/半自动）
- 模式历史
- 模式配置
"""

import click

@click.group()
def cli():
    """Mode CLI - 模式管理工具"""
    pass

@cli.group()
def mode():
    """模式管理"""
    pass

@mode.command()
def show():
    """显示当前模式"""
    pass

@mode.command()
@click.argument('mode_name')
@click.option('-r', '--requirement-id', required=True)
@click.option('--reason', required=True)
def set(mode_name, requirement_id, reason):
    """切换模式"""
    pass

@mode.command()
def history():
    """查看切换历史"""
    pass

if __name__ == '__main__':
    cli()
```

---

## Infra 基础设施

### Docker Compose

**docker-compose.yml** - 本地开发环境：

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: amazing
      POSTGRES_PASSWORD: amazing123
      POSTGRES_DB: amazing
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  common-service:
    build: ../backend/common
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis

  frontend:
    build: ../frontend
    ports:
      - "3000:3000"
    depends_on:
      - common-service

volumes:
  postgres_data:
```

### Kubernetes

**namespace.yaml**:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: amazing
```

**configmap.yaml**:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: amazing-config
  namespace: amazing
data:
  DATABASE_HOST: postgres
  REDIS_HOST: redis
```

---

## 配置文件

### amazing.config.json

```json
{
  "project": {
    "name": "my-project",
    "version": "1.0.0"
  },
  "architecture": {
    "pattern": "agent-teams",
    "mode": "semi-auto"
  },
  "agents": {
    "fixed": ["common", "review"],
    "business": [
      {
        "name": "compute",
        "techStack": {
          "backend": "Python + FastAPI",
          "database": "PostgreSQL"
        }
      }
    ]
  },
  "roles": [
    "architect",
    "pm",
    "frontend",
    "backend",
    "qa",
    "ops"
  ]
}
```

---

## 使用方式

### 1. 初始化项目

```bash
# 使用 CLI 初始化
amazing-cli init my-project --template model-platform

# 或手动复制模板
cp -r templates/project-init my-project
cd my-project
```

### 2. 配置环境

```bash
# 复制环境变量
cp .env.example .env

# 编辑配置
vim .env
```

### 3. 启动开发环境

```bash
# 使用 Docker Compose
docker-compose -f infra/docker/docker-compose.yml up

# 或使用 Makefile
make dev
```

### 4. 部署到 K8s

```bash
# 部署所有服务
kubectl apply -f infra/k8s/

# 或使用 Makefile
make k8s-deploy
```

---

## 相关文档

- [项目模板说明](../templates/README.md)
- [Backend 开发指南](./backend-guide.md)
- [Frontend 开发指南](./frontend-guide.md)
- [部署指南](./deployment-guide.md)
