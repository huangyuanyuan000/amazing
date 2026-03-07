# 大模型管理平台

完整的大模型生命周期管理平台，包含算力管理、数据管理、训推一体、模型服务等核心能力。

## 🎯 功能模块

### 1. 通用功能（Common）
- 用户管理、权限控制、日志审计

### 2. 算力平台（Compute）
- GPU/CPU 资源管理、任务调度、监控告警

### 3. 数据平台（Data）
- 数据集管理、数据标注、数据质量

### 4. 训推平台（Training）
- 模型训练、实验管理、超参调优

### 5. 模型服务（Model Service）
- 模型部署、推理服务、版本管理

### 6. 运营管理（Operations）
- 数据分析、用户运营、系统配置

### 7. API 开放平台（API Gateway）
- API 管理、限流鉴权、API 监控

## 🏗️ 技术架构

### 后端
- **Python (FastAPI)**: Common、Data、Training
- **Go (Gin)**: Compute、Model Service、API Gateway

### 前端
- **React 18 + TypeScript + Vite**
- **Ant Design**

### 数据库
- **PostgreSQL 14+**: 主数据库
- **MongoDB 5+**: 日志存储
- **Redis 7+**: 缓存

### 基础设施
- **Kubernetes + Docker + Helm**
- **Prometheus + Grafana**

## 🚀 快速开始

### 前置要求
- Docker & Docker Compose
- Python 3.11+
- Go 1.21+
- Node.js 18+

### 本地开发

```bash
# 1. 启动数据库
make dev

# 2. 访问服务
# - 前端: http://localhost:3000
# - API 网关: http://localhost:8000
# - API 文档: http://localhost:8000/docs

# 3. 默认账号
# - 管理员: admin / admin123
# - 测试用户: testuser / user123
```

### Docker 部署

```bash
# 构建并启动所有服务
make docker

# 访问服务
# - 前端: http://localhost:3000
# - API 网关: http://localhost:8000
# - Grafana: http://localhost:3001 (admin/admin)
```

### Kubernetes 部署

```bash
# 部署到 K8s 集群
make k8s

# 查看服务状态
kubectl get pods -n model-platform

# 获取访问地址
kubectl get ingress -n model-platform
```

## 📁 目录结构

```
model-platform/
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
│   │   ├── common/               # Python
│   │   ├── data/                 # Python
│   │   ├── training/             # Python
│   │   ├── compute/              # Go
│   │   ├── model-service/        # Go
│   │   └── api-gateway/          # Go
│   └── frontend/                 # 前端代码
│
├── deploy/                       # 部署配置
│   ├── local/                    # 本地开发
│   ├── docker/                   # Docker 部署
│   ├── k8s/                      # K8s 部署
│   └── offline/                  # 离线部署
│
├── docs/                         # 文档
├── tests/                        # 测试
├── scripts/                      # 脚本
├── Makefile                      # 快捷命令
└── README.md                     # 本文档
```

## 🔧 开发指南

### 后端开发

```bash
# Python 服务
cd src/backend/common
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001

# Go 服务
cd src/backend/compute
go mod download
go run main.go
```

### 前端开发

```bash
cd src/frontend
npm install
npm run dev
```

### 运行测试

```bash
# 所有测试
make test

# 单元测试
pytest tests/unit/

# 集成测试
pytest tests/integration/

# E2E 测试
cd tests/e2e && npm run test
```

### 代码检查

```bash
# 所有代码检查
make lint

# Python
black . && ruff check .

# Go
gofmt -w . && golangci-lint run

# TypeScript
npm run lint
```

## 📊 监控

### Grafana 仪表板
- 访问: http://localhost:3001
- 账号: admin / admin
- 预置仪表板:
  - 系统概览
  - 资源监控
  - 任务监控
  - API 监控

### Prometheus
- 访问: http://localhost:9090
- 指标查询和告警配置

## 🔐 权限管理

### 角色申请

```bash
# 申请后端开发角色
python3 scripts/ironclaw.py request-role \
  --role=backend-dev \
  --reason="加入后端团队"

# 架构师审批
python3 scripts/ironclaw.py list-requests
python3 scripts/ironclaw.py approve-request --id=REQ-001
```

### 权限级别
- **Admin（架构师）**: 全局权限
- **Manager（产品经理）**: 管理权限
- **Operator（运维工程师）**: 执行权限
- **Developer（开发/测试）**: 读写权限
- **Viewer（运营人员）**: 只读权限

## 📖 文档

- [架构文档](docs/architecture/)
- [API 文档](docs/api/)
- [部署文档](docs/deployment/)
- [开发文档](docs/development/)

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](../../CONTRIBUTING.md)

## 📄 许可证

MIT License
