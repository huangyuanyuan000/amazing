# Amazing 完整操作手册

## 📚 文档索引

### 1. 快速开始
- [QUICKSTART.md](../QUICKSTART.md) - 快速开始指南
- [README.md](../README.md) - 项目概述

### 2. 环境安装
- [INSTALLATION.md](./INSTALLATION.md) - 环境安装指南
  - Go 安装
  - Docker 数据库启动
  - 项目初始化

### 3. 角色接入
- [ROLE_ONBOARDING.md](./ROLE_ONBOARDING.md) - 各工种接入指南
  - 产品经理 (PM)
  - 前端开发 (Frontend)
  - 后端开发 (Backend)
  - 测试工程师 (QA)
  - 运维工程师 (Ops)
  - 运营人员 (Operation)

### 4. Claude Code 接入
- [CLAUDE_CODE_GUIDE.md](./CLAUDE_CODE_GUIDE.md) - Claude Code (龙虾) 接入指南
  - 安装配置
  - 使用方法
  - 场景化使用
  - 与 Agent 集成

### 5. 架构文档
- [architecture/README.md](./architecture/README.md) - 架构设计
  - 系统架构
  - Agent 架构
  - 技术架构
  - 部署架构

### 6. 技术规范
- [specs/README.md](./specs/README.md) - 技术规范
  - 代码风格
  - Git 提交规范
  - API 设计规范
  - 测试规范

### 7. 部署指南
- [deployment/README.md](./deployment/README.md) - 部署指南
  - 本地开发
  - Docker 部署
  - K8s 部署
  - 私有化部署

### 8. 角色指南
- [guides/README.md](./guides/README.md) - 角色指南总览
- [guides/pm.md](./guides/pm.md) - 产品经理指南
- [guides/frontend.md](./guides/frontend.md) - 前端开发指南
- [guides/backend.md](./guides/backend.md) - 后端开发指南

---

## 🚀 快速导航

### 我是新人，如何开始？

1. **安装环境**: 阅读 [INSTALLATION.md](./INSTALLATION.md)
2. **选择角色**: 阅读 [ROLE_ONBOARDING.md](./ROLE_ONBOARDING.md)
3. **配置 Claude Code**: 阅读 [CLAUDE_CODE_GUIDE.md](./CLAUDE_CODE_GUIDE.md)
4. **开始开发**: 阅读对应角色的指南

### 我是产品经理

1. [产品经理接入指南](./ROLE_ONBOARDING.md#1-产品经理-pm-接入指南)
2. [产品经理详细指南](./guides/pm.md)
3. [Claude Code 使用 - PM 场景](./CLAUDE_CODE_GUIDE.md#场景-1-功能开发-pm)

### 我是前端开发

1. [前端开发接入指南](./ROLE_ONBOARDING.md#2-前端开发-frontend-接入指南)
2. [前端开发详细指南](./guides/frontend.md)
3. [Claude Code 使用 - 前端场景](./CLAUDE_CODE_GUIDE.md#场景-2-前端开发)

### 我是后端开发

1. [后端开发接入指南](./ROLE_ONBOARDING.md#3-后端开发-backend-接入指南)
2. [后端开发详细指南](./guides/backend.md)
3. [Claude Code 使用 - 后端场景](./CLAUDE_CODE_GUIDE.md#场景-3-后端开发)

### 我是测试工程师

1. [测试工程师接入指南](./ROLE_ONBOARDING.md#4-测试工程师-qa-接入指南)
2. [测试规范](./specs/README.md#4-测试规范)

### 我是运维工程师

1. [运维工程师接入指南](./ROLE_ONBOARDING.md#5-运维工程师-ops-接入指南)
2. [部署指南](./deployment/README.md)

### 我是运营人员

1. [运营人员接入指南](./ROLE_ONBOARDING.md#6-运营人员-operation-接入指南)

---

## 📖 常见任务

### 启动开发环境

```bash
# 1. 启动数据库
docker-compose -f docker-compose.dev.yml up -d

# 2. 启动后端
cd backend/python && python3 main.py

# 3. 启动前端
cd frontend && npm run dev
```

详见: [QUICKSTART.md](../QUICKSTART.md)

### 创建需求

```bash
# 1. 选择 PM 角色
python3 scripts/amazing-cli.py role select

# 2. 创建 PRD
python3 scripts/amazing-cli.py prd create "功能描述"

# 3. 使用 Claude Code 生成详细 PRD
claude "生成 PRD: 功能描述"
```

详见: [产品经理指南](./guides/pm.md)

### 开发功能

```bash
# 1. 认领任务
python3 scripts/amazing-cli.py task claim <task-id>

# 2. 使用 Claude Code 开发
claude "实现功能: 功能描述" --role frontend

# 3. 提交代码
git add .
git commit -m "feat: 功能描述"
```

详见: [前端开发指南](./guides/frontend.md) / [后端开发指南](./guides/backend.md)

### 修复 Bug

```bash
# 1. 复现 Bug
claude "复现 Bug: Bug 描述" --role qa

# 2. 定位问题
claude "定位问题" --role backend --file path/to/file.py

# 3. 修复代码
claude "修复 Bug" --role backend

# 4. 回归测试
pytest
```

详见: [Bug 修复流程](./CLAUDE_CODE_GUIDE.md#场景-4-bug-修复)

### 部署应用

```bash
# 本地部署
make dev

# Docker 部署
make docker-up

# K8s 部署
make k8s-deploy
```

详见: [部署指南](./deployment/README.md)

---

## 🔧 工具使用

### Amazing CLI

```bash
# 查看帮助
python3 scripts/amazing-cli.py --help

# 选择角色
python3 scripts/amazing-cli.py role select

# 查看任务
python3 scripts/amazing-cli.py tasks

# 查看状态
python3 scripts/amazing-cli.py status
```

### Claude Code

```bash
# 交互式模式
claude

# 命令行模式
claude "任务描述"

# 指定角色
claude "任务描述" --role frontend

# 指定文件
claude "任务描述" --file path/to/file.py
```

详见: [Claude Code 指南](./CLAUDE_CODE_GUIDE.md)

### Make 命令

```bash
# 查看帮助
make help

# 初始化项目
make init

# 启动开发
make dev

# Docker 部署
make docker-up

# K8s 部署
make k8s-deploy
```

---

## 🎯 核心概念

### Agent 体系

- **6 大 Agent**: Common, Compute, Data, Training, Model-Service, Review
- **Sub-Agents**: PM, Frontend, Backend, QA, Ops, Operation
- **Skills**: 可进化的能力单元

详见: [架构设计](./architecture/README.md)

### 工作流

- **功能开发**: PM → Frontend/Backend → QA → Review → Ops
- **Bug 修复**: QA → Backend → QA → Ops
- **需求分析**: PM → 技术评审 → 开发

详见: [工作流文档](./workflows/)

### 工具链

- **Claude Code** (主力)
- **Codex CLI** (备选)
- **Codex Desktop** (可视化)

详见: [Claude Code 指南](./CLAUDE_CODE_GUIDE.md)

---

## 📞 获取帮助

### 文档

- 查看对应角色的文档
- 查看技术规范
- 查看部署指南

### CLI 帮助

```bash
# Amazing CLI
python3 scripts/amazing-cli.py --help

# Claude Code
claude --help

# Make
make help
```

### 常见问题

查看各文档的"常见问题"章节。

---

## 🎉 开始使用

1. **安装环境**: [INSTALLATION.md](./INSTALLATION.md)
2. **选择角色**: [ROLE_ONBOARDING.md](./ROLE_ONBOARDING.md)
3. **配置 Claude Code**: [CLAUDE_CODE_GUIDE.md](./CLAUDE_CODE_GUIDE.md)
4. **开始开发**: 查看对应角色指南

祝你使用愉快！🚀
