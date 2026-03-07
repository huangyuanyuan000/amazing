# Amazing 快速开始

## ✅ 项目已初始化

### 已安装组件

- ✅ 前端依赖 (Node.js)
- ✅ Python 后端依赖 (FastAPI)
- ⚠️  Go 后端 (未安装 Go，可选)

### 项目结构

```
amazing/
├── .agents/              # 6 个 Agent 配置
├── .claude/             # Claude Code 配置
├── backend/             # 后端服务
│   ├── python/          # FastAPI (已就绪)
│   └── go/              # Go 服务 (需要安装 Go)
├── frontend/            # React 前端 (已就绪)
├── infra/               # 基础设施配置
├── docs/                # 完整文档
└── scripts/             # 工具脚本
```

## 🚀 启动服务

### 方式 1: 本地开发 (推荐)

```bash
# 启动 Python API (端口 8000)
cd backend/python
python3 main.py

# 新终端: 启动前端 (端口 3000)
cd frontend
npm run dev
```

访问:
- 前端: http://localhost:3000
- API 文档: http://localhost:8000/docs

### 方式 2: Docker (完整环境)

```bash
# 启动所有服务
make docker-up

# 查看日志
cd infra/docker
docker-compose logs -f

# 停止服务
make docker-down
```

### 方式 3: Kubernetes

```bash
# 部署到 K8s
make k8s-deploy

# 查看状态
kubectl get pods -n amazing
```

## 📖 使用 Agent-Teams

### 1. 选择角色

```bash
# 使用 CLI
python3 scripts/amazing-cli.py role select

# 可选角色:
# - pm (产品经理)
# - frontend (前端开发)
# - backend (后端开发)
# - qa (测试工程师)
# - ops (运维工程师)
# - operation (运营人员)
```

### 2. 创建需求

```bash
# 创建 PRD
python3 scripts/amazing-cli.py prd create "用户权限管理模块"
```

### 3. 分配任务

```bash
# 分配给 Agent
python3 scripts/amazing-cli.py agent assign common --task prd-001
```

### 4. 查看状态

```bash
# 查看项目状态
python3 scripts/amazing-cli.py status
```

## 🔧 工具链

### Claude Code (主力)

```bash
# 使用 Claude Code 开发
claude-code "实现用户登录功能"
```

### Codex CLI (备选)

```bash
# 使用 Codex CLI
codex "实现用户登录功能"
```

### Codex Desktop (可视化)

打开 Codex Desktop，选择角色，进行可视化操作。

## 📚 文档

- [架构设计](./docs/architecture/README.md)
- [技术规范](./docs/specs/README.md)
- [角色指南](./docs/guides/README.md)
- [部署指南](./docs/deployment/README.md)

## 🎯 核心特性

1. **6 大 Agent**: Common, Compute, Data, Training, Model-Service, Review
2. **6 种角色**: PM, Frontend, Backend, QA, Ops, Operation
3. **3 种场景**: 功能开发、Bug 修复、需求分析
4. **进化机制**: Agent/Sub-Agent/Skill 三级进化
5. **工具链降级**: Claude Code → Codex CLI → Codex Desktop

## ⚙️ 可选配置

### 安装 Go (可选)

```bash
# macOS
brew install go

# 然后重新初始化
make init
```

### 安装数据库依赖 (可选)

```bash
# 安装 PostgreSQL 客户端
brew install postgresql

# 安装 Python 数据库依赖
cd backend/python
python3 -m pip install -r requirements-optional.txt
```

## 🐛 故障排查

### 端口被占用

```bash
# 查看端口占用
lsof -i :3000
lsof -i :8000

# 杀死进程
kill -9 <PID>
```

### Python 依赖问题

```bash
# 升级 pip
python3 -m pip install --upgrade pip

# 重新安装依赖
cd backend/python
python3 -m pip install -r requirements.txt
```

## 📞 获取帮助

```bash
# 查看帮助
make help
python3 scripts/amazing-cli.py --help
```

## 🎉 下一步

1. 阅读[角色指南](./docs/guides/README.md)了解你的角色
2. 查看[技术规范](./docs/specs/README.md)了解开发规范
3. 开始使用 Agent-Teams 协同开发！
