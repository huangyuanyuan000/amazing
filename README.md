# Amazing - 大模型管理平台

<div align="center">

![Amazing Logo](https://via.placeholder.com/150x150?text=Amazing)

**基于 Agent-Teams 协同开发范式的企业级大模型管理平台**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Go](https://img.shields.io/badge/go-1.22+-00ADD8.svg)](https://golang.org/)
[![React](https://img.shields.io/badge/react-18+-61DAFB.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/typescript-5.0+-3178C6.svg)](https://www.typescriptlang.org/)

[快速开始](#-快速开始) • [架构设计](#-架构设计) • [文档](#-文档) • [贡献指南](#-贡献)

</div>

---

## 📖 目录

- [项目简介](#-项目简介)
- [核心特性](#-核心特性)
- [架构设计](#-架构设计)
- [技术栈](#-技术栈)
- [快速开始](#-快速开始)
- [使用 IronClaw](#-使用-ironclaw)
- [文档](#-文档)
- [贡献](#-贡献)
- [许可证](#-许可证)

---

## 🎯 项目简介

Amazing 是一个基于 **Agent-Teams 协同开发范式**的企业级大模型管理平台，支持多角色、多场景的 AI 辅助开发。

### 核心理念

- **Agent-Teams**: 6 大领域 Agent 协同工作
- **角色编排**: 支持 PM/Frontend/Backend/QA/Ops/Operation 全流程协作
- **场景适配**: 业务开发、Bug 修复、需求分析、代码审查
- **进化机制**: Agent/Sub-Agent/Skill 三级进化体系
- **工具链降级**: Claude Code → Codex CLI → Codex Desktop → IronClaw

---

## ✨ 核心特性

### 🤖 6 大 Agent 体系

| Agent | 职责 | 技术栈 |
|-------|------|--------|
| **Common** | 通用模块 (用户/权限/日志) | FastAPI + PostgreSQL |
| **Compute** | 算力平台 (GPU/CPU 调度) | Go + Kubernetes |
| **Data** | 数据平台 (数据集/标注) | Python + MinIO |
| **Training** | 训推平台 (训练/推理) | PyTorch + Triton |
| **Model-Service** | 模型服务 (API/版本管理) | Go + gRPC |
| **Review** | 审核 Agent (代码审查/质量) | SonarQube + ESLint |

### 👥 6 种角色支持

- **产品经理 (PM)**: 需求分析、PRD 编写、功能验收
- **前端开发 (Frontend)**: UI/UX 实现、组件开发
- **后端开发 (Backend)**: API 开发、数据库设计
- **测试工程师 (QA)**: 测试设计、自动化测试
- **运维工程师 (Ops)**: 部署、监控、故障排查
- **运营人员 (Operation)**: 数据分析、用户运营

### 🎨 3 种场景适配

1. **功能开发**: PM → Frontend/Backend → QA → Review → Ops
2. **Bug 修复**: QA → Backend → QA → Ops (支持回滚)
3. **需求分析**: PM → 技术评审 → PRD 生成

### 🔄 进化机制

- **Agent 进化**: 基于任务成功率、代码质量、交付时间
- **Sub-Agent 进化**: 基于角色效率、协作分数
- **Skill 进化**: 基于准确率、性能、用户满意度

---

## 🏗️ 架构设计

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    统一入口层                                │
│  CLI (amazing-cli) | Web Dashboard (IronClaw)              │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                   AI 工具链层                              │
│  Claude Code (主) → Codex CLI (备) → IronClaw (可视化)    │
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

### Agent 架构

每个 Agent 包含:
- **Sub-Agents**: PM, Frontend, Backend, QA, Ops, Operation
- **Skills**: 可进化的能力单元
- **Evolution Metrics**: 进化指标监控

```
Agent
├── Sub-Agent (PM)
│   ├── Skills: [prd-generator, requirement-analyzer]
│   └── Tools: [claude-code, codex, ironclaw]
├── Sub-Agent (Frontend)
│   ├── Skills: [react-component, ui-design]
│   └── Tools: [claude-code, codex, ironclaw]
├── Sub-Agent (Backend)
│   ├── Skills: [api-design, database-design]
│   └── Tools: [claude-code, codex, ironclaw]
└── Evolution Engine
    ├── Metrics Collection
    ├── Performance Analysis
    └── Auto Upgrade
```

### 在线架构图

- [系统架构图](https://htmlpreview.github.io/?https://github.com/z58362026/amazing/blob/main/docs/architecture/system-architecture.html)
- [功能开发流程](https://htmlpreview.github.io/?https://github.com/z58362026/amazing/blob/main/docs/workflows/development.html)
- [Bug 修复流程](https://htmlpreview.github.io/?https://github.com/z58362026/amazing/blob/main/docs/workflows/bug-fix.html)

---

## 🛠️ 技术栈

### 前端
- **框架**: React 18 + TypeScript
- **构建**: Vite
- **样式**: TailwindCSS
- **状态**: Zustand
- **HTTP**: Axios
- **UI 库**: Ant Design

### 后端
- **Python**: FastAPI + SQLAlchemy + PostgreSQL
- **Go**: Gin + GORM + gRPC
- **缓存**: Redis
- **消息队列**: RabbitMQ (可选)
- **对象存储**: MinIO

### 基础设施
- **容器**: Docker + Docker Compose
- **编排**: Kubernetes + Helm
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack
- **CI/CD**: GitHub Actions

### AI 工具链
- **主力**: Claude Code (Anthropic)
- **备选**: Codex CLI
- **可视化**: Codex Desktop / IronClaw

---

## 🚀 快速开始

### 前置要求

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- Go 1.22+ (可选)

### 1. 克隆项目

```bash
git clone git@github.com:z58362026/amazing.git
cd amazing
```

### 2. 初始化项目

```bash
# 安装依赖
make init

# 启动数据库 (PostgreSQL + Redis + MongoDB)
docker-compose -f docker-compose.dev.yml up -d
```

### 3. 启动服务

```bash
# 方式 1: 使用 Make (推荐)
make dev

# 方式 2: 手动启动
# 终端 1: Python API
cd backend/python && python3 main.py

# 终端 2: 前端
cd frontend && npm run dev
```

### 4. 访问应用

- **前端**: http://localhost:3000
- **API 文档**: http://localhost:8000/docs
- **Go API**: http://localhost:8080/health

### 5. 选择角色

**方式 1: 对话申请 (推荐)**

```bash
# 交互式对话
python3 scripts/amazing-cli.py role chat

# 直接描述
python3 scripts/amazing-cli.py role chat "我是前端开发"
python3 scripts/amazing-cli.py role chat "我负责后端API"
python3 scripts/amazing-cli.py role chat "我做产品需求"
```

系统会智能识别你的意图并推荐合适的角色。

**方式 2: 直接设置**

```bash
python3 scripts/amazing-cli.py role set pm          # 产品经理
python3 scripts/amazing-cli.py role set frontend    # 前端开发
python3 scripts/amazing-cli.py role set backend     # 后端开发
python3 scripts/amazing-cli.py role set qa          # 测试工程师
python3 scripts/amazing-cli.py role set ops         # 运维工程师
```

**方式 3: 交互选择**

```bash
# 查看所有角色
python3 scripts/amazing-cli.py role list

# 交互式选择
python3 scripts/amazing-cli.py role select
```

---

## 🦞 使用 IronClaw

### 什么是 IronClaw？

IronClaw 是 Amazing 平台的可视化 AI 协同开发工具，提供直观的 Web 界面，支持多角色协作、任务管理、代码审查等功能。

### IronClaw 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    IronClaw Dashboard                        │
│  角色管理 | 任务看板 | 代码审查 | 监控面板 | 文档中心      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    IronClaw API Gateway                     │
│  认证授权 | 权限控制 | 请求路由 | 日志审计                │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    Agent Orchestrator                       │
│  任务分发 | 状态同步 | 进度跟踪 | 结果聚合                │
└─────────────────────────────┬─────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼────────┐  ┌──────▼───────┐
            │  Claude Code   │  │  Codex CLI   │
            │   (AI 引擎)    │  │  (备选引擎)  │
            └────────────────┘  └──────────────┘
```

### 角色申请流程

#### 1. 访问 IronClaw

```bash
# 启动 IronClaw (开发模式)
cd ironclaw
npm run dev

# 访问: http://localhost:3001
```

#### 2. 注册账号

1. 访问 http://localhost:3001/register
2. 填写信息:
   - 用户名
   - 邮箱
   - 密码
   - 所属团队
3. 提交注册

#### 3. 申请角色

**方式 1: Web 界面申请**

1. 登录 IronClaw
2. 进入 "角色管理" 页面
3. 点击 "申请角色"
4. 选择角色 (PM/Frontend/Backend/QA/Ops/Operation)
5. 填写申请理由
6. 提交申请
7. 等待管理员审批

**方式 2: CLI 申请**

```bash
# 申请角色
python3 scripts/amazing-cli.py role apply \
  --role frontend \
  --reason "我是前端开发，负责 UI 实现"

# 查看申请状态
python3 scripts/amazing-cli.py role status
```

#### 4. 角色审批

**管理员操作**:

```bash
# 查看待审批申请
python3 scripts/amazing-cli.py admin role-requests

# 批准申请
python3 scripts/amazing-cli.py admin approve <request-id>

# 拒绝申请
python3 scripts/amazing-cli.py admin reject <request-id> --reason "理由"
```

### IronClaw 对话方式

#### 1. 任务对话

**创建任务**:
```
用户: @IronClaw 创建任务: 实现用户登录功能
IronClaw:
✅ 任务已创建
- 任务 ID: TASK-001
- 标题: 实现用户登录功能
- 分配给: Common Agent
- 优先级: 高
- 预计时间: 2 天

需要我帮你生成详细的技术方案吗？
```

**查询任务**:
```
用户: @IronClaw 查询任务 TASK-001
IronClaw:
📋 任务详情
- ID: TASK-001
- 标题: 实现用户登录功能
- 状态: 进行中
- 负责人: @张三 (Backend)
- 进度: 60%
- 预计完成: 明天 18:00
```

#### 2. 代码对话

**生成代码**:
```
用户: @IronClaw 生成用户登录 API
IronClaw:
✅ 代码已生成

```python
@router.post("/login")
async def login(credentials: LoginRequest):
    user = await authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}
```

已保存到: backend/python/app/api/auth.py
需要我生成对应的测试代码吗？
```

**代码审查**:
```
用户: @IronClaw 审查 backend/python/app/api/auth.py
IronClaw:
🔍 代码审查结果

✅ 优点:
- 使用了异步处理
- 错误处理完善
- 符合 RESTful 规范

⚠️ 建议:
1. 添加请求频率限制 (防止暴力破解)
2. 密码错误时不要暴露用户是否存在
3. 添加日志记录

📊 质量评分: 85/100
```

#### 3. 协作对话

**@提及协作**:
```
用户: @IronClaw @张三 请帮忙实现用户登录的前端页面
IronClaw:
✅ 已通知 @张三 (Frontend)

任务详情:
- 标题: 实现用户登录前端页面
- 关联任务: TASK-001
- 优先级: 高
- 技术要求: React + TypeScript + Ant Design

@张三 会在 30 分钟内响应
```

**团队讨论**:
```
用户: @IronClaw 召集团队讨论用户登录方案
IronClaw:
📢 已创建讨论组

参与者:
- @李四 (PM)
- @张三 (Frontend)
- @王五 (Backend)
- @赵六 (QA)

讨论主题: 用户登录方案
会议室: http://localhost:3001/meeting/001

请大家在 10 分钟内加入
```

#### 4. 智能问答

**技术咨询**:
```
用户: @IronClaw 如何实现 JWT 认证？
IronClaw:
📚 JWT 认证实现方案

1. 安装依赖:
   pip install python-jose[cryptography]

2. 生成 Token:
   [代码示例...]

3. 验证 Token:
   [代码示例...]

4. 最佳实践:
   - Token 有效期: 24 小时
   - 使用 Refresh Token
   - 存储在 HttpOnly Cookie

需要完整的代码示例吗？
```

**问题诊断**:
```
用户: @IronClaw 为什么登录接口返回 500 错误？
IronClaw:
🔍 正在分析日志...

发现问题:
- 错误: psycopg2.OperationalError: could not connect to server
- 原因: 数据库连接失败
- 位置: backend/python/app/core/database.py:15

解决方案:
1. 检查数据库是否启动: docker ps | grep postgres
2. 检查连接配置: cat backend/python/.env
3. 重启数据库: docker restart amazing-postgres

需要我帮你执行这些命令吗？
```

### IronClaw 快捷命令

```bash
# 任务管理
@IronClaw task create <title>          # 创建任务
@IronClaw task list                    # 列出任务
@IronClaw task assign <id> @user       # 分配任务
@IronClaw task close <id>              # 关闭任务

# 代码操作
@IronClaw code generate <description>  # 生成代码
@IronClaw code review <file>           # 代码审查
@IronClaw code refactor <file>         # 代码重构
@IronClaw code test <file>             # 生成测试

# 协作
@IronClaw notify @user <message>       # 通知用户
@IronClaw meeting create <topic>       # 创建会议
@IronClaw discuss <topic>              # 发起讨论

# 查询
@IronClaw status                       # 项目状态
@IronClaw help                         # 帮助信息
@IronClaw docs <topic>                 # 查询文档
```

### IronClaw 权限矩阵

| 角色 | 创建任务 | 分配任务 | 代码审查 | 部署 | 管理用户 |
|------|---------|---------|---------|------|---------|
| PM | ✅ | ✅ | ❌ | ❌ | ❌ |
| Frontend | ✅ | ❌ | ✅ | ✅ | ❌ |
| Backend | ✅ | ❌ | ✅ | ✅ | ❌ |
| QA | ✅ | ❌ | ✅ | ❌ | ❌ |
| Ops | ✅ | ❌ | ✅ | ✅ | ❌ |
| Admin | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 📚 文档

### 新手必读
- [START_HERE.md](./START_HERE.md) - 从这里开始
- [QUICKSTART.md](./QUICKSTART.md) - 快速开始指南
- [docs/INSTALLATION.md](./docs/INSTALLATION.md) - 环境安装

### 接入指南
- [docs/ROLE_ONBOARDING.md](./docs/ROLE_ONBOARDING.md) - 各工种接入指南
- [docs/ROLE_CHAT_GUIDE.md](./docs/ROLE_CHAT_GUIDE.md) - 对话申请角色指南
- [docs/CLAUDE_CODE_GUIDE.md](./docs/CLAUDE_CODE_GUIDE.md) - Claude Code 接入
- [docs/IRONCLAW_GUIDE.md](./docs/IRONCLAW_GUIDE.md) - IronClaw 使用指南

### 技术文档
- [docs/architecture/README.md](./docs/architecture/README.md) - 架构设计
- [docs/specs/README.md](./docs/specs/README.md) - 技术规范
- [docs/deployment/README.md](./docs/deployment/README.md) - 部署指南

### 角色指南
- [docs/guides/pm.md](./docs/guides/pm.md) - 产品经理指南
- [docs/guides/frontend.md](./docs/guides/frontend.md) - 前端开发指南
- [docs/guides/backend.md](./docs/guides/backend.md) - 后端开发指南

### 完整索引
- [docs/INDEX.md](./docs/INDEX.md) - 所有文档索引

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解详情。

### 贡献流程

1. Fork 项目
2. 创建分支 (`git checkout -b feature/amazing-feature`)
3. 提交代码 (`git commit -m 'feat: add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

### 开发规范

- 遵循 [Conventional Commits](https://www.conventionalcommits.org/)
- 代码覆盖率 > 80%
- 通过所有 CI 检查
- 更新相关文档

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](./LICENSE) 文件了解详情。

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=z58362026/amazing&type=Date)](https://star-history.com/#z58362026/amazing&Date)

---

## 📞 联系我们

- **Issues**: https://github.com/z58362026/amazing/issues
- **Discussions**: https://github.com/z58362026/amazing/discussions
- **Email**: 305068308@qq.com

---

<div align="center">

**[⬆ 回到顶部](#amazing---大模型管理平台)**

Made with ❤️ by Amazing Team

</div>
