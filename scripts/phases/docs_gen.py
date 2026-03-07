#!/usr/bin/env python3
"""
Phase 7: 文档生成

生成项目文档、API 文档和开发指南
"""

from pathlib import Path
from typing import Dict


def execute(context: Dict) -> Dict:
    """执行文档生成"""
    project_path = context["project_path"]
    project_name = context["project_name"]
    product_description = context["product_description"]
    phase_results = context["phase_results"]

    # 获取业务模块和技术栈
    business_agents = phase_results.get("business-agent-gen", {}).get("business_agents", [])
    tech_stack = phase_results.get("business-agent-gen", {}).get("tech_stack", {})
    api_endpoints = phase_results.get("backend-gen", {}).get("api_endpoints", [])

    print("📚 生成项目文档...")

    docs_path = project_path / "docs"
    generated_docs = []

    # 生成 README
    generate_readme(project_path, project_name, product_description, business_agents, tech_stack)
    generated_docs.append("README.md")

    # 生成 API 文档
    generate_api_docs(docs_path, business_agents, api_endpoints)
    generated_docs.append("docs/api.md")

    # 生成架构文档
    generate_architecture_docs(docs_path, project_name, business_agents, tech_stack)
    generated_docs.append("docs/architecture.md")

    # 生成开发指南
    generate_development_guide(docs_path, tech_stack)
    generated_docs.append("docs/development.md")

    # 生成部署文档
    generate_deployment_guide(docs_path, project_name)
    generated_docs.append("docs/deployment.md")

    # 生成 CLAUDE.md
    generate_claude_md(project_path, project_name, product_description, business_agents)
    generated_docs.append("CLAUDE.md")

    print(f"\n✅ 已生成 {len(generated_docs)} 个文档")

    return {
        "generated_docs": generated_docs
    }


def generate_readme(project_path: Path, project_name: str, product_description: str,
                    business_agents: list, tech_stack: dict):
    """生成 README"""
    backend = tech_stack.get("backend", "Python/FastAPI")
    frontend = tech_stack.get("frontend", "React")
    database = tech_stack.get("database", "PostgreSQL")

    agents_list = "\n".join([f"- **{agent['displayName']}**: {agent['description']}"
                             for agent in business_agents])

    content = f'''# {project_name}

## 项目简介

{product_description}

## 技术栈

- **后端**: {backend}
- **前端**: {frontend}
- **数据库**: {database}
- **部署**: Docker + Kubernetes

## 业务模块

{agents_list}

## 快速开始

### 本地开发

```bash
# 启动开发环境
make dev
```

访问地址:
- 前端: http://localhost:3000
- 后端: http://localhost:8000
- API 文档: http://localhost:8000/docs

### Docker 部署

```bash
# 构建并启动
make docker

# 查看状态
make status

# 查看日志
docker-compose logs -f
```

### Kubernetes 部署

```bash
# 部署到 K8s
make k8s

# 查看状态
kubectl get pods -n {project_name}
```

## 项目结构

```
{project_name}/
├── .agents/              # 业务 Agent
├── .claude/              # 角色和权限配置
├── src/
│   ├── backend/          # 后端代码
│   └── frontend/         # 前端代码
├── deploy/
│   ├── docker/           # Docker 配置
│   ├── k8s/              # Kubernetes 配置
│   └── offline/          # 离线部署
├── docs/                 # 文档
├── tests/                # 测试
└── Makefile              # 常用命令
```

## 开发规范

- [代码规范](docs/standards/code.md)
- [Git 规范](docs/standards/git.md)
- [API 规范](docs/standards/api.md)
- [测试规范](docs/standards/testing.md)

## 相关文档

- [架构设计](docs/architecture.md)
- [API 文档](docs/api.md)
- [开发指南](docs/development.md)
- [部署指南](docs/deployment.md)

## 许可证

MIT
'''

    with open(project_path / "README.md", "w") as f:
        f.write(content)
    print("  ✓ README.md")


def generate_api_docs(docs_path: Path, business_agents: list, api_endpoints: list):
    """生成 API 文档"""
    api_sections = []

    for agent in business_agents:
        agent_name = agent["name"]
        display_name = agent["displayName"]

        section = f'''## {display_name}

### 列表查询

```http
GET /api/v1/{agent_name}?page=1&size=10
```

**响应**
```json
{{
  "items": [
    {{
      "id": 1,
      "name": "示例",
      "created_at": "2024-01-01T00:00:00Z"
    }}
  ],
  "total": 100,
  "page": 1,
  "size": 10
}}
```

### 详情查询

```http
GET /api/v1/{agent_name}/{{id}}
```

**响应**
```json
{{
  "id": 1,
  "name": "示例",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}}
```

### 创建

```http
POST /api/v1/{agent_name}
Content-Type: application/json

{{
  "name": "新建示例"
}}
```

**响应**
```json
{{
  "id": 2,
  "name": "新建示例",
  "created_at": "2024-01-01T00:00:00Z"
}}
```

### 更新

```http
PUT /api/v1/{agent_name}/{{id}}
Content-Type: application/json

{{
  "name": "更新后的名称"
}}
```

### 删除

```http
DELETE /api/v1/{agent_name}/{{id}}
```

**响应**
```json
{{
  "message": "删除成功"
}}
```
'''
        api_sections.append(section)

    content = f'''# API 文档

## 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: Bearer Token
- **Content-Type**: `application/json`

## 认证

所有 API 请求需要在 Header 中携带 Token:

```http
Authorization: Bearer <your-token>
```

## 通用响应格式

### 成功响应

```json
{{
  "code": 0,
  "message": "success",
  "data": {{}}
}}
```

### 错误响应

```json
{{
  "code": 400,
  "message": "错误信息",
  "detail": "详细错误描述"
}}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## API 列表

{chr(10).join(api_sections)}

## 分页参数

所有列表接口支持分页参数:

- `page`: 页码，从 1 开始
- `size`: 每页数量，默认 10，最大 100

## 排序参数

支持通过 `order_by` 参数排序:

```http
GET /api/v1/users?order_by=created_at:desc
```

## 过滤参数

支持字段过滤:

```http
GET /api/v1/users?name=john&status=active
```
'''

    with open(docs_path / "api.md", "w") as f:
        f.write(content)
    print("  ✓ api.md")


def generate_architecture_docs(docs_path: Path, project_name: str, business_agents: list, tech_stack: dict):
    """生成架构文档"""
    agents_desc = "\n".join([f"### {agent['displayName']}\n\n{agent['description']}\n"
                             for agent in business_agents])

    content = f'''# 架构设计

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐
│   前端      │────▶│   后端      │────▶│   数据库     │
│   React     │     │   FastAPI   │     │  PostgreSQL  │
└─────────────┘     └─────────────┘     └──────────────┘
                          │
                          ▼
                    ┌─────────────┐
                    │    Redis    │
                    └─────────────┘
```

## 技术选型

### 后端

- **语言**: {tech_stack.get("backend", "Python")}
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **异步**: asyncio + aiohttp

### 前端

- **框架**: {tech_stack.get("frontend", "React")}
- **UI 库**: Ant Design
- **状态管理**: Zustand
- **路由**: React Router
- **构建工具**: Vite

### 数据库

- **主库**: {tech_stack.get("database", "PostgreSQL")}
- **缓存**: Redis
- **搜索**: Elasticsearch (可选)

### 部署

- **容器化**: Docker
- **编排**: Kubernetes
- **CI/CD**: GitHub Actions
- **监控**: Prometheus + Grafana

## 业务模块

{agents_desc}

## 数据模型

### 通用字段

所有表都包含以下字段:

- `id`: 主键
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `deleted_at`: 软删除时间 (可选)

### 关系设计

- 使用外键约束保证数据完整性
- 多对多关系使用中间表
- 支持软删除

## 安全设计

### 认证

- JWT Token 认证
- Token 过期时间: 24 小时
- Refresh Token 机制

### 权限

- 基于 IronClaw 权限体系
- 角色-权限模型
- 细粒度权限控制

### 数据安全

- 密码使用 bcrypt 加密
- 敏感数据加密存储
- SQL 注入防护
- XSS 防护

## 性能优化

### 缓存策略

- Redis 缓存热点数据
- 缓存过期时间: 5 分钟
- 缓存更新策略: Write-Through

### 数据库优化

- 索引优化
- 查询优化
- 连接池管理
- 读写分离 (可选)

### 前端优化

- 代码分割
- 懒加载
- CDN 加速
- 图片优化

## 可扩展性

### 水平扩展

- 无状态服务设计
- 支持多实例部署
- 负载均衡

### 垂直扩展

- 资源配置可调
- 支持 GPU 加速 (AI 场景)

## 监控告警

### 指标监控

- 请求量、响应时间
- 错误率
- 资源使用率

### 日志

- 结构化日志
- 日志聚合
- 日志分析

### 告警

- 阈值告警
- 异常告警
- 通知渠道: 邮件、钉钉、企业微信
'''

    with open(docs_path / "architecture.md", "w") as f:
        f.write(content)
    print("  ✓ architecture.md")


def generate_development_guide(docs_path: Path, tech_stack: dict):
    """生成开发指南"""
    content = '''# 开发指南

## 环境准备

### 必需软件

- Python 3.11+
- Node.js 20+
- Docker 24+
- PostgreSQL 15+
- Redis 7+

### 推荐工具

- VS Code / PyCharm
- Postman / Insomnia
- DBeaver / pgAdmin

## 安装依赖

### 后端

```bash
cd src/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### 前端

```bash
cd src/frontend
npm install
```

## 数据库初始化

```bash
# 创建数据库
createdb myapp

# 运行迁移
cd src/backend
alembic upgrade head

# 初始化数据
python scripts/init_data.py
```

## 运行项目

### 后端

```bash
cd src/backend
uvicorn main:app --reload --port 8000
```

访问 API 文档: http://localhost:8000/docs

### 前端

```bash
cd src/frontend
npm run dev
```

访问前端: http://localhost:3000

## 开发流程

### 1. 创建功能分支

```bash
git checkout -b feature/your-feature
```

### 2. 开发

- 编写代码
- 编写测试
- 运行测试

### 3. 提交代码

```bash
git add .
git commit -m "feat: 添加新功能"
```

遵循 Conventional Commits 规范:
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具

### 4. 创建 Pull Request

- 推送到远程分支
- 创建 PR
- 等待代码审查
- 合并到主分支

## 代码规范

### Python

使用 black + ruff:

```bash
# 格式化
black src/backend

# 检查
ruff check src/backend
```

### TypeScript

使用 eslint + prettier:

```bash
# 格式化
npm run format

# 检查
npm run lint
```

## 测试

### 后端测试

```bash
cd src/backend
pytest tests/ -v
```

### 前端测试

```bash
cd src/frontend
npm run test
```

### 集成测试

```bash
make test
```

## 调试

### 后端调试

VS Code launch.json:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--reload"],
      "cwd": "${workspaceFolder}/src/backend"
    }
  ]
}
```

### 前端调试

浏览器开发者工具 + React DevTools

## 常见问题

### 数据库连接失败

检查 DATABASE_URL 环境变量是否正确

### 端口被占用

修改配置文件中的端口号

### 依赖安装失败

清理缓存后重试:
```bash
pip cache purge
npm cache clean --force
```
'''

    with open(docs_path / "development.md", "w") as f:
        f.write(content)
    print("  ✓ development.md")


def generate_deployment_guide(docs_path: Path, project_name: str):
    """生成部署文档"""
    content = f'''# 部署指南

## Docker 部署

### 前置条件

- Docker 20.10+
- Docker Compose 2.0+

### 部署步骤

1. 克隆代码

```bash
git clone <repository-url>
cd {project_name}
```

2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库密码等
```

3. 启动服务

```bash
make docker
```

4. 查看状态

```bash
make status
```

5. 访问应用

- 前端: http://localhost
- 后端: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 管理命令

```bash
# 查看日志
docker-compose logs -f

# 重启服务
docker-compose restart

# 停止服务
docker-compose down

# 清理数据
docker-compose down -v
```

## Kubernetes 部署

### 前置条件

- Kubernetes 1.24+
- kubectl
- Helm 3+ (可选)

### 部署步骤

1. 创建命名空间

```bash
kubectl create namespace {project_name}
```

2. 配置 Secrets

```bash
# 复制模板
cp deploy/k8s/secrets.yaml.template deploy/k8s/secrets.yaml

# 编辑 secrets.yaml，填入实际密码
vim deploy/k8s/secrets.yaml

# 应用配置
kubectl apply -f deploy/k8s/secrets.yaml
```

3. 部署应用

```bash
kubectl apply -f deploy/k8s/
```

4. 查看状态

```bash
kubectl get pods -n {project_name}
kubectl get svc -n {project_name}
```

5. 访问应用

```bash
# 获取 LoadBalancer IP
kubectl get svc frontend -n {project_name}
```

### 管理命令

```bash
# 查看日志
kubectl logs -f <pod-name> -n {project_name}

# 进入容器
kubectl exec -it <pod-name> -n {project_name} -- /bin/bash

# 扩容
kubectl scale deployment backend --replicas=5 -n {project_name}

# 更新镜像
kubectl set image deployment/backend backend=myapp/backend:v2 -n {project_name}

# 回滚
kubectl rollout undo deployment/backend -n {project_name}
```

## 离线部署

### 构建离线包

```bash
make offline
```

生成的离线包: `deploy/offline/{project_name}-offline.tar.gz`

### 安装

1. 上传离线包到目标服务器

2. 解压

```bash
tar -xzf {project_name}-offline.tar.gz
cd offline-package
```

3. 运行安装脚本

```bash
bash install.sh
```

4. 访问应用

http://localhost

## 生产环境配置

### 环境变量

```bash
# 数据库
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Redis
REDIS_URL=redis://host:6379

# 密钥
SECRET_KEY=your-secret-key

# 日志级别
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=https://yourdomain.com
```

### 资源配置

推荐配置:

- **后端**: 2 CPU, 4GB 内存
- **前端**: 1 CPU, 2GB 内存
- **数据库**: 4 CPU, 8GB 内存
- **Redis**: 1 CPU, 2GB 内存

### 备份策略

#### 数据库备份

```bash
# 每日备份
0 2 * * * pg_dump -U admin {project_name} > backup_$(date +\%Y\%m\%d).sql

# 保留 7 天
find /backup -name "backup_*.sql" -mtime +7 -delete
```

#### 文件备份

```bash
# 备份上传文件
tar -czf uploads_$(date +\%Y\%m\%d).tar.gz /app/uploads
```

### 监控

#### Prometheus

```yaml
scrape_configs:
  - job_name: '{project_name}'
    static_configs:
      - targets: ['backend:8000']
```

#### Grafana

导入预置的 Dashboard: `deploy/monitoring/grafana-dashboard.json`

### 日志

#### 日志收集

使用 Fluentd 收集日志到 Elasticsearch

#### 日志查询

Kibana: http://kibana.yourdomain.com

## 故障排查

### 服务无法启动

1. 检查日志
2. 检查端口占用
3. 检查环境变量
4. 检查数据库连接

### 性能问题

1. 查看资源使用率
2. 分析慢查询
3. 检查缓存命中率
4. 优化数据库索引

### 数据库连接池耗尽

增加连接池大小:

```python
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_MAX_OVERFLOW = 40
```
'''

    with open(docs_path / "deployment.md", "w") as f:
        f.write(content)
    print("  ✓ deployment.md")


def generate_claude_md(project_path: Path, project_name: str, product_description: str, business_agents: list):
    """生成 CLAUDE.md"""
    agents_list = "\n".join([f"- **{agent['name']}**: {agent['displayName']} - {agent['description']}"
                             for agent in business_agents])

    content = f'''# {project_name}

## 项目概述

{product_description}

## 业务模块

{agents_list}

## 开发规范

### Git 规范

遵循 Conventional Commits:
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具

### 代码规范

- Python: black + ruff
- TypeScript: eslint + prettier
- 测试覆盖率 > 80%

### API 规范

- RESTful 风格
- 统一响应格式
- OpenAPI 3.0 文档

## 角色权限

基于 IronClaw 权限体系，详见 `.claude/ironclaw/permissions.yml`

## 常用命令

```bash
# 开发
make dev

# 部署
make docker
make k8s

# 测试
make test
```
'''

    with open(project_path / "CLAUDE.md", "w") as f:
        f.write(content)
    print("  ✓ CLAUDE.md")
