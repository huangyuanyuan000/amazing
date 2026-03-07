# Amazing - AI 驱动的企业级脚手架框架

> 📖 **[在线架构图](https://z58362026.github.io/amazing/)** - 查看完整的架构设计和能力体系

<div align="center">

![Amazing Logo](https://via.placeholder.com/150x150?text=Amazing)

**一条命令初始化企业级项目，内置 AI Coding 范式 + 完整规范体系 + 全栈监控 + Handoffs 引擎**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#)

[快速开始](#-快速开始) • [核心能力](#-核心能力) • [架构设计](#-架构设计) • [使用指南](#-使用指南)

</div>

---

## 🎯 Amazing 是什么

Amazing 是一个**企业级 AI Coding 脚手架框架**。

**不是**：代码生成器、模板复制工具
**而是**：一套完整的 AI 协同开发范式 + 企业级规范体系

通过一条命令或一段对话描述业务需求，即可初始化一个具备全套 AI 开发能力、完整规范体系和全栈监控的企业级项目。

### 核心特点

- 🏗️ **架构驱动**：基于 9 大业务流程（产品分析→技术架构→代码开发→测试→部署→运营→审查→Bug 修复→进化）
- 🤖 **AI 原生**：内置 7 个固定角色 + 11 个核心 Agent + 动态业务 Agent + Handoffs 引擎
- 🧠 **技能复用**：23 个 Skill 技能库（架构/开发/数据库/测试/运维/安全/运营），按角色权限加载
- 📋 **规范完整**：内置代码/Git/API/测试完整规范体系，支持自动化检查
- 📊 **监控完善**：内置 Monitoring Agent（日志/指标/追踪/告警），实现全栈可观测性
- 🔐 **权限治理**：每个角色独立的 IronClaw 实例，严格的权限边界和工作流
- 📦 **开箱即用**：初始化即部署就绪（本地/Docker/K8s/离线）
- 🔄 **任务拆分**：Handoffs 引擎防止上下文溢出（单文件 < 200 行）

---

## 🚀 快速开始

### 1. 克隆脚手架

```bash
git clone https://github.com/z58362026/amazing.git
cd amazing
```

### 2. 初始化项目

```bash
# 方式一：标准项目（推荐）
python3 scripts/init.py my-project

# 方式二：AI 平台项目（包含所有业务 Agent）
python3 scripts/init.py my-ai-platform \
  --business-agents=compute,data,training,model-service

# 方式三：特定业务项目
python3 scripts/init.py my-data-platform --business-agents=data

# 方式四：交互式
python3 scripts/init.py my-project --interactive

# 方式五：从案例初始化
python3 scripts/init.py my-project --from-example=model-platform
```

### 3. 进入项目

```bash
cd my-project

# 查看项目结构
tree -L 2

# 一键启动
make dev
```

---

## 💎 核心能力

### 1. 完整的规范体系 ✨ NEW

初始化项目自动应用完整的开发规范：

| 规范类型 | 内容 | 自动化检查 |
|---------|------|-----------|
| **代码规范** | Python (PEP 8) + TypeScript (Airbnb) | black, ruff, eslint, prettier |
| **Git 规范** | Git Flow + Conventional Commits | commit-msg hook |
| **API 规范** | RESTful + OpenAPI 3.0 | OpenAPI 文档验证 |
| **测试规范** | 测试金字塔 + 覆盖率要求 | pytest, jest (覆盖率检查) |

**规范文件位置**：`standards/`
- `standards/code/` - 代码规范（Python/TypeScript/Go）
- `standards/git/` - Git 工作流规范
- `standards/api/` - API 设计规范
- `standards/testing/` - 测试规范

### 2. 全栈监控能力 ✨ NEW

内置 Monitoring Agent，实现完整的可观测性：

| 监控维度 | 工具链 | 能力 |
|---------|--------|------|
| **日志管理** | ELK Stack / Loki | 日志收集、解析、查询、告警 |
| **指标监控** | Prometheus + Grafana | RED/USE 方法、仪表盘、告警规则 |
| **链路追踪** | Jaeger / Tempo | 分布式追踪、性能分析、依赖分析 |
| **告警管理** | Alertmanager | 告警分级、路由、聚合、值班管理 |

**Monitoring Agent 位置**：`.agents/monitoring/`
- `log-agent` - 日志收集与分析
- `metrics-agent` - 指标监控
- `trace-agent` - 链路追踪
- `alert-agent` - 告警管理
- `orchestrator` - 监控编排

### 3. 完整的角色体系 ✨ NEW

7 个角色，每个角色包含详细的定义、约束和工作流：

| 角色 | 职责 | 工作流数量 | 文件位置 |
|------|------|-----------|---------|
| **架构师** | 架构设计、技术选型、技术决策 | 7 个 | `.claude/roles/architect/` |
| **产品经理** | 需求分析、PRD 编写、功能验收 | 7 个 | `.claude/roles/product-manager/` |
| **前端开发** | UI 开发、组件开发、性能优化 | 5 个 | `.claude/roles/frontend-dev/` |
| **后端开发** | API 开发、数据库设计、服务开发 | 4 个 | `.claude/roles/backend-dev/` |
| **测试工程师** | 测试设计、自动化测试、性能测试 | 5 个 | `.claude/roles/test-engineer/` |
| **运维工程师** | 部署、监控配置、故障排查 | 7 个 | `.claude/roles/devops-engineer/` |
| **运营人员** | 数据分析、配置管理、用户运营 | 6 个 | `.claude/roles/operations/` |

每个角色包含：
- `role.md` - 角色定位、职责、权限、技术栈
- `constraints.md` - 权限边界、质量标准、时间约束
- `workflows.md` - 详细的工作流（步骤 + 检查点 + 时间估算）

### 4. 11 个核心 Agent

| Agent | 职责 | Sub-Agents | 状态 |
|-------|------|-----------|------|
| **Common** | 用户管理、权限控制、日志审计 | 5 个 | ✅ |
| **Review** | 代码审查、质量把控、合规检查 | 5 个 | ✅ |
| **Architect** | 架构设计、技术选型、决策管理 | 4 个 | ✅ NEW |
| **Database** | Schema 设计、迁移管理、查询优化 | 5 个 | ✅ NEW |
| **Deployment** | Docker/K8s 部署、CI/CD 配置 | 5 个 | ✅ NEW |
| **Evolution** | 变更影响分析、依赖追踪、模式学习 | 5 个 | ✅ NEW |
| **Monitoring** | 日志/指标/追踪/告警 | 5 个 | ✅ NEW |
| **Compute** | GPU/CPU 资源管理、集群调度 | 5 个 | 📦 模板 |
| **Data** | 数据集管理、数据处理、标注工具 | 5 个 | 📦 模板 |
| **Training** | 模型训练、推理部署、实验管理 | 5 个 | 📦 模板 |
| **Model Service** | 模型 API 服务、版本管理、监控 | 5 个 | 📦 模板 |

**说明**：
- ✅ 核心 Agent：所有项目默认包含
- 📦 业务 Agent 模板：按需选择（`--business-agents` 参数）

### 5. 业务 Agent 模板 ✨ NEW

4 个可选的业务 Agent 模板，支持按需选择和组合：

```bash
# AI 平台完整方案
python3 scripts/init.py my-ai-platform \
  --business-agents=compute,data,training,model-service

# 数据处理平台
python3 scripts/init.py my-data-platform --business-agents=data

# 模型服务平台
python3 scripts/init.py my-model-platform \
  --business-agents=training,model-service
```

**模板位置**：`templates/business-agents/`

### 6. Skill 技能库 ✨ NEW

23 个可复用的 Skill，按角色职责分为 8 大类，供 Agent 和 Handoff 调用：

| 分类 | Skills | 核心能力 |
|------|--------|---------|
| **架构设计** | architecture-design, tech-selection, api-design | 架构模式选择、技术选型评估、RESTful API 规范 |
| **开发** | react-component, state-management, microservice, auth-implement | React 组件规范、状态管理方案、微服务设计、认证授权 |
| **数据库** | database-design, db-migration, query-optimization | Schema 设计、零停机迁移、查询优化 |
| **测试** | test-design, test-automation, performance-test | 测试金字塔、自动化框架、性能测试方案 |
| **运维** | docker-deploy, k8s-deploy, ci-cd-pipeline, monitoring-setup | Docker 构建、K8s 部署策略、CI/CD 流水线、Prometheus 监控 |
| **安全** | security-audit, code-review-checklist | OWASP Top 10 检查、代码审查五维度 |
| **运营** | data-analysis, config-management | 数据分析方法论、功能灰度/A/B 测试 |
| **初始化** | init-project | 对话式项目初始化 |

**角色绑定**：每个角色只能使用授权范围内的 Skill，通过 `/init-role` 命令加载

```bash
/init-role frontend-dev
# → 自动加载：react-component, state-management 等前端 Skills
# → 权限限制：不能调用 docker-deploy, k8s-deploy 等运维 Skills
```

**工具链切换**：通过 `/switch-tool` 在不同 AI 工具间无缝切换

```bash
/switch-tool claude    # Claude Code CLI（默认）
/switch-tool codex     # Codex CLI（本地降级方案）
```

**Skill 位置**：`.claude/skills/`

### 7. Handoffs 引擎

防止上下文溢出的任务拆分系统：

- **9 条 Handoff Chain**：覆盖完整业务流程
- **任务拆分规则**：单文件 < 200 行，单任务 < 5 个文件
- **状态管理**：任务状态持久化，支持暂停/恢复/回滚
- **依赖追踪**：自动识别任务依赖关系

### 8. IronClaw 权限治理

每个角色独立的权限实例：

- **7 个角色实例**：独立的权限配置
- **严格的权限边界**：只能访问授权的资源
- **审计日志**：所有操作可追溯
- **工作流约束**：关键操作必须审批

---

## 📦 脚手架能力

### 1. 初始化能力

| 能力 | 说明 | 命令 |
|------|------|------|
| **标准初始化** | 生成标准企业级项目 | `python3 scripts/init.py my-project` |
| **业务 Agent 选择** | 选择特定业务 Agent | `--business-agents=compute,data` |
| **交互式初始化** | 通过对话描述需求 | `--interactive` |
| **模板初始化** | 从预置模板快速开始 | `--template=ai-platform` |
| **案例初始化** | 从成功案例复制架构 | `--from-example=model-platform` |

### 2. 架构生成能力

初始化时自动生成：

- ✅ **完整规范体系**（代码/Git/API/测试）
- ✅ **Monitoring Agent 配置**（日志/指标/追踪/告警）
- ✅ **7 个角色完整定义**（role + constraints + workflows）
- ✅ **11 个核心 Agent**（含 29 个 Sub-Agents）
- ✅ **23 个 Skill 技能库**（8 大分类，按角色权限加载）
- ✅ **9 条 Handoff Chain 配置**（完整业务流程）
- ✅ **7 个独立 IronClaw 实例**（权限治理）
- ✅ **Handoffs 引擎**（任务拆分系统）
- ✅ **业务 Agent**（根据需求动态生成）
- ✅ **部署配置**（Docker/K8s/离线）

### 3. 开发能力

生成的项目具备：

| 能力 | 说明 |
|------|------|
| **热重载开发** | 代码修改自动重启 |
| **自动迁移** | 数据库 Schema 自动同步 |
| **代码检查** | Lint + 类型检查 + 测试 |
| **API 文档** | 自动生成 OpenAPI 文档 |
| **监控仪表盘** | Grafana 仪表盘自动配置 |

### 4. 部署能力

| 部署方式 | 说明 | 命令 |
|---------|------|------|
| **本地开发** | 热重载 + 自动迁移 | `make dev` |
| **Docker** | Docker Compose 一键部署 | `make docker` |
| **Kubernetes** | K8s 集群部署 + HPA | `make k8s` |
| **离线部署** | 私有化部署包 | `make offline` |

---

## 🏗️ 架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                     Amazing Framework                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Standards  │  │  Monitoring  │  │    Roles     │     │
│  │   规范体系    │  │   监控体系    │  │   角色体系    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              23 Skills (8 Categories)               │  │
│  │  架构 │ 开发 │ 数据库 │ 测试 │ 运维 │ 安全 │ 运营   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              11 Core Agents (29 Sub-Agents)          │  │
│  │  Common │ Review │ Architect │ Database │ Deployment │  │
│  │  Evolution │ Monitoring │ + 4 Business Agent 模板    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Handoffs Engine (9 Chains)                   │  │
│  │  任务拆分 │ 状态管理 │ 依赖追踪 │ 自动恢复            │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         IronClaw (7 Role Instances)                  │  │
│  │  权限治理 │ 审计日志 │ 工作流约束                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 核心组件

#### 1. Standards 规范体系
- **代码规范**：Python/TypeScript/Go
- **Git 规范**：Git Flow + Conventional Commits
- **API 规范**：RESTful + OpenAPI 3.0
- **测试规范**：测试金字塔 + 覆盖率要求

#### 2. Monitoring 监控体系
- **日志管理**：ELK Stack / Loki
- **指标监控**：Prometheus + Grafana
- **链路追踪**：Jaeger / Tempo
- **告警管理**：Alertmanager

#### 3. Roles 角色体系
- **7 个角色**：architect, product-manager, frontend-dev, backend-dev, test-engineer, devops-engineer, operations
- **每个角色 3 个文件**：role.md, constraints.md, workflows.md
- **40+ 工作流**：覆盖开发全生命周期

#### 4. Agents 体系
- **11 个核心 Agent**：29 个 Sub-Agents
- **4 个业务 Agent 模板**：按需选择

#### 5. Skills 技能库
- **23 个 Skill**：8 大分类（架构/开发/数据库/测试/运维/安全/运营/初始化）
- **角色绑定**：按权限加载，前端只能用前端 Skill，运维只能用运维 Skill
- **进化能力**：每个 Skill 内置指标跟踪，持续优化
- **Commands**：`/init-role` 加载角色技能，`/switch-tool` 切换 AI 工具链

#### 6. Handoffs 引擎
- **9 条 Handoff Chain**：完整业务流程
- **任务拆分**：防止上下文溢出
- **状态管理**：支持暂停/恢复/回滚

#### 7. IronClaw 权限治理
- **7 个角色实例**：独立权限配置
- **审计日志**：所有操作可追溯
- **工作流约束**：关键操作必须审批

---

## 📖 使用指南

### 初始化项目

#### 1. 标准项目
```bash
python3 scripts/init.py my-project
```

生成的项目包含：
- ✅ 完整规范体系（standards/）
- ✅ Monitoring Agent 配置
- ✅ 7 个角色完整定义
- ✅ 11 个核心 Agent
- ✅ 23 个 Skill 技能库
- ✅ Handoffs 引擎
- ✅ IronClaw 权限治理

#### 2. AI 平台项目
```bash
python3 scripts/init.py my-ai-platform \
  --business-agents=compute,data,training,model-service
```

额外包含：
- ✅ Compute Agent（GPU/CPU 资源管理）
- ✅ Data Agent（数据集管理）
- ✅ Training Agent（模型训练）
- ✅ Model Service Agent（模型服务）

#### 3. 特定业务项目
```bash
# 数据平台
python3 scripts/init.py my-data-platform --business-agents=data

# 算力平台
python3 scripts/init.py my-compute-platform --business-agents=compute

# 训练平台
python3 scripts/init.py my-training-platform --business-agents=training,model-service
```

### 开发流程

#### 1. 本地开发

```bash
cd my-project

# 启动开发环境
make dev

# 代码检查
make lint

# 运行测试
make test

# 查看监控
open http://localhost:3000  # Grafana
```

#### 2. 任务管理

```bash
# 创建任务
python scripts/handoff_manager.py run --task="开发用户管理" --mode=auto

# 查看任务状态
python scripts/handoff_manager.py status <task-id>

# 暂停任务
python scripts/handoff_manager.py pause <task-id>

# 恢复任务
python scripts/handoff_manager.py resume <task-id>

# 回滚任务
python scripts/handoff_manager.py rollback <task-id> --to=<handoff-id>
```

#### 3. 部署

```bash
# Docker 部署
make docker

# Kubernetes 部署
make k8s

# 生成离线部署包
make offline
```

#### 4. 查看规范

```bash
# 查看代码规范
cat standards/code/python.md
cat standards/code/typescript.md

# 查看 Git 规范
cat standards/git/workflow.md

# 查看 API 规范
cat standards/api/restful.md

# 查看测试规范
cat standards/testing/testing-standards.md
```

#### 5. 查看角色定义

```bash
# 查看架构师角色
cat .claude/roles/architect/role.md
cat .claude/roles/architect/constraints.md
cat .claude/roles/architect/workflows.md

# 查看其他角色
ls .claude/roles/
```

#### 6. 查看监控配置

```bash
# 查看 Monitoring Agent
cat .agents/monitoring/agent.md

# 查看 Sub-Agents
ls .agents/monitoring/sub-agents/
```

---

## 📚 文档

- [在线架构图](https://z58362026.github.io/amazing/) - 完整的架构设计
- [CLAUDE.md](CLAUDE.md) - 项目配置和规范
- [Standards 规范](standards/) - 代码/Git/API/测试规范
- [Roles 角色](. claude/roles/) - 7 个角色完整定义
- [Agents 体系](.agents/) - 11 个核心 Agent
- [Skills 技能库](.claude/skills/) - 23 个可复用 Skill
- [Business Agent 模板](templates/business-agents/) - 4 个业务 Agent 模板

---

## 🎨 示例

### 大模型管理平台

完整的案例实现：

```bash
cd examples/model-platform

# 查看项目结构
tree -L 2

# 查看角色配置
ls .claude/roles/

# 查看 Handoffs 配置
ls .agents/handoffs/

# 查看部署配置
ls deploy/k8s/
ls deploy/offline/
```

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

**联系方式**：
- GitHub Issues: https://github.com/z58362026/amazing/issues
- Email: 305068308@qq.com

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**[⬆ 回到顶部](#amazing---ai-驱动的企业级脚手架框架)**

Made with ❤️ by Amazing Team

</div>
