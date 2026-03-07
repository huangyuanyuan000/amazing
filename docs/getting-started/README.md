# 🚀 Amazing - 从这里开始

欢迎使用 Amazing 大模型管理平台！

## ✅ 项目已初始化

你的项目已经成功初始化，包含：
- ✅ 前端依赖 (React + TypeScript)
- ✅ Python 后端依赖 (FastAPI)
- ✅ 6 大 Agent 配置
- ✅ 完整文档体系
- ✅ 部署配置

## 📖 快速开始 (3 步)

### 第 1 步: 启动数据库

```bash
# 启动 PostgreSQL + Redis + MongoDB
docker-compose -f docker-compose.dev.yml up -d

# 验证
docker ps
```

### 第 2 步: 启动服务

```bash
# 终端 1: 启动 Python API
cd backend/python
python3 main.py

# 终端 2: 启动前端
cd frontend
npm run dev
```

### 第 3 步: 访问应用

- 前端: http://localhost:3000
- API 文档: http://localhost:8000/docs

## 📚 完整文档

### 新手必读

1. **[环境安装](./docs/INSTALLATION.md)** - 安装 Go、启动数据库
2. **[角色接入](./docs/ROLE_ONBOARDING.md)** - 各工种如何接入
3. **[Claude Code 接入](./docs/CLAUDE_CODE_GUIDE.md)** - 龙虾接入指南

### 角色指南

- [产品经理指南](./docs/guides/pm.md)
- [前端开发指南](./docs/guides/frontend.md)
- [后端开发指南](./docs/guides/backend.md)

### 技术文档

- [架构设计](./docs/architecture/README.md)
- [技术规范](./docs/specs/README.md)
- [部署指南](./docs/deployment/README.md)

### 完整索引

查看 **[文档索引](./docs/INDEX.md)** 获取所有文档列表。

## 🎯 我该做什么？

### 如果你是产品经理

```bash
# 1. 选择角色
python3 scripts/amazing-cli.py role select
# 选择: 1. 产品经理 (pm)

# 2. 创建需求
python3 scripts/amazing-cli.py prd create "用户权限管理模块"

# 3. 使用 Claude Code 生成 PRD
claude "生成 PRD: 用户权限管理模块"
```

详见: [产品经理接入指南](./docs/ROLE_ONBOARDING.md#1-产品经理-pm-接入指南)

### 如果你是前端开发

```bash
# 1. 选择角色
python3 scripts/amazing-cli.py role select
# 选择: 2. 前端开发 (frontend)

# 2. 启动开发服务器
cd frontend
npm run dev

# 3. 使用 Claude Code 开发
claude "创建用户列表组件" --role frontend
```

详见: [前端开发接入指南](./docs/ROLE_ONBOARDING.md#2-前端开发-frontend-接入指南)

### 如果你是后端开发

```bash
# 1. 选择角色
python3 scripts/amazing-cli.py role select
# 选择: 3. 后端开发 (backend)

# 2. 启动开发服务器
cd backend/python
python3 main.py

# 3. 使用 Claude Code 开发
claude "实现用户管理 API" --role backend
```

详见: [后端开发接入指南](./docs/ROLE_ONBOARDING.md#3-后端开发-backend-接入指南)

### 如果你是其他角色

查看 [角色接入指南](./docs/ROLE_ONBOARDING.md) 找到你的角色。

## 🔧 常用命令

```bash
# 查看帮助
make help
python3 scripts/amazing-cli.py --help

# 启动数据库
docker-compose -f docker-compose.dev.yml up -d

# 启动开发环境
make dev

# 选择角色
python3 scripts/amazing-cli.py role select

# 查看状态
python3 scripts/amazing-cli.py status

# 使用 Claude Code
claude "你的任务描述"
```

## 🎉 下一步

1. **阅读文档**: 查看 [文档索引](./docs/INDEX.md)
2. **选择角色**: 运行 `python3 scripts/amazing-cli.py role select`
3. **开始开发**: 使用 Claude Code 协同开发

## 📞 需要帮助？

- 查看 [文档索引](./docs/INDEX.md)
- 运行 `make help` 或 `python3 scripts/amazing-cli.py --help`
- 查看各文档的"常见问题"章节

---

**祝你使用愉快！🚀**
