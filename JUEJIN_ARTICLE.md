# Amazing：基于 Agent-Teams 的 AI 协同开发平台

## 前言

在 AI 辅助开发的浪潮中，我们看到了 GitHub Copilot、Cursor、Claude Code 等工具的崛起。但这些工具大多聚焦于单一开发者的编码效率提升，而忽略了软件开发的本质——**团队协作**。

Amazing 项目诞生于这样的思考：**能否让 AI 不仅仅是代码助手，而是成为整个研发团队的协作伙伴？**

本文将深入介绍 Amazing 的设计理念、架构实现，以及如何通过 Agent-Teams 范式重新定义 AI 辅助开发。

---

## 一、为什么需要 Agent-Teams？

### 1.1 传统 AI 辅助开发的局限

当前主流的 AI 开发工具存在以下问题：

1. **单点能力**：只能辅助编码，无法覆盖需求分析、测试、部署等环节
2. **角色单一**：只服务于开发者，PM、QA、运维无法受益
3. **缺乏协作**：无法支持多角色协同，团队沟通成本依然很高
4. **场景固定**：只适合功能开发，Bug 修复、需求分析等场景支持不足

### 1.2 Agent-Teams 的核心思想

Amazing 提出的 Agent-Teams 范式包含三个核心要素：

```
┌─────────────────────────────────────────────────┐
│              Agent-Teams 范式                    │
├─────────────────────────────────────────────────┤
│  1. 多角色协同 (PM/Frontend/Backend/QA/Ops)    │
│  2. 场景适配 (开发/修复/分析/审查)              │
│  3. 进化机制 (Agent/Sub-Agent/Skill 三级进化)   │
└─────────────────────────────────────────────────┘
```

**核心优势**：
- 覆盖软件开发全生命周期
- 支持多角色并行协作
- 根据场景自动编排工作流
- 持续学习和进化

---

## 二、Amazing 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────┐
│                   用户层                         │
│  PM | Frontend | Backend | QA | Ops | Operation │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              统一入口层                          │
│  CLI (amazing-cli) | Web (IronClaw)            │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              AI 工具链层                         │
│  Claude Code → Codex CLI → Codex Desktop       │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│           Agent Orchestrator                    │
│  角色权限 | 场景路由 | 进化管理                 │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
┌───────▼───┐ ┌───▼────┐ ┌──▼──────┐
│  Common   │ │Compute │ │  Data   │
│  Agent    │ │ Agent  │ │ Agent   │
└───────────┘ └────────┘ └─────────┘
```

### 2.2 六大 Agent 体系

Amazing 将企业级大模型管理平台拆分为 6 个领域 Agent：

| Agent | 职责 | 技术栈 | Sub-Agent 示例 |
|-------|------|--------|---------------|
| **Common** | 用户/权限/日志 | FastAPI + PostgreSQL | PM, Frontend, Backend |
| **Compute** | GPU/CPU 调度 | Go + Kubernetes | Ops |
| **Data** | 数据集/标注 | Python + MinIO | Operation |
| **Training** | 训练/推理 | PyTorch + Triton | Backend |
| **Model-Service** | API/版本管理 | Go + gRPC | Backend |
| **Review** | 代码审查/质量 | SonarQube + ESLint | QA |

每个 Agent 负责一个独立的业务领域，内部包含多个 Sub-Agent（对应不同角色）。

### 2.3 角色与权限

Amazing 支持 6 种角色，每种角色有明确的权限边界：

```python
# 角色权限矩阵
ROLE_PERMISSIONS = {
    "pm": {
        "create_prd": True,
        "approve_feature": True,
        "code_development": False,
        "deployment": False
    },
    "frontend": {
        "ui_development": True,
        "component_creation": True,
        "backend_development": False,
        "database_operation": False
    },
    "backend": {
        "api_development": True,
        "database_design": True,
        "frontend_development": False,
        "production_deployment": False
    },
    "qa": {
        "test_design": True,
        "bug_report": True,
        "code_development": False,
        "deployment": False
    },
    "ops": {
        "deployment": True,
        "monitoring": True,
        "code_development": False,
        "requirement_change": False
    },
    "operation": {
        "data_analysis": True,
        "config_management": True,
        "code_development": False,
        "database_modification": False
    }
}
```

---

## 三、核心功能实现

### 3.1 角色申请与管理

用户可以通过 CLI 或 Web 界面申请角色：

**CLI 方式**：
```bash
# 申请前端开发角色
python3 scripts/amazing-cli.py role apply \
  --role frontend \
  --reason "负责 UI 实现"

# 查看申请状态
python3 scripts/amazing-cli.py role status
```

**Web 方式（IronClaw）**：
```
用户: @IronClaw 我想申请前端开发角色
IronClaw:
✅ 角色申请已提交
- 角色: Frontend Developer
- 申请时间: 2025-03-15 10:30
- 状态: 待审批
- 预计审批时间: 1 个工作日

管理员会尽快处理您的申请，请耐心等待。
```

### 3.2 场景化工作流

Amazing 支持 3 种典型场景，每种场景有不同的工作流：

#### 场景 1：功能开发

```
PM (需求分析)
  → Frontend/Backend (并行开发)
    → QA (测试)
      → Review Agent (代码审查)
        → Ops (部署)
```

**示例**：
```bash
# PM 创建 PRD
python3 scripts/amazing-cli.py prd create "用户权限管理"

# 分配给开发团队
python3 scripts/amazing-cli.py agent assign common --task prd-001

# Frontend 开发 UI
claude-code "创建用户列表组件，支持分页和搜索"

# Backend 开发 API
claude-code "实现用户 CRUD API，使用 FastAPI"

# QA 测试
python3 scripts/amazing-cli.py test acceptance --task prd-001

# Ops 部署
make k8s-deploy
```

#### 场景 2：Bug 修复

```
QA (发现 Bug)
  → Backend (修复)
    → QA (验证)
      → Ops (热修复部署，支持回滚)
```

#### 场景 3：需求分析

```
PM (需求输入)
  → 技术评审 (Frontend + Backend)
    → PRD 生成
      → 任务拆分
```

### 3.3 AI 工具链降级

Amazing 支持多种 AI 工具，并提供自动降级机制：

```
Claude Code (首选)
  ↓ (不可用时)
Codex CLI (备选)
  ↓ (不可用时)
Codex Desktop (可视化)
  ↓ (不可用时)
IronClaw (Web 界面)
```

**使用示例**：
```bash
# 优先使用 Claude Code
claude-code "实现用户登录功能"

# 降级到 Codex CLI
codex "实现用户登录功能"

# 降级到 IronClaw
# 访问 http://localhost:3001
# 输入: @IronClaw 实现用户登录功能
```

---

## 四、进化机制

### 4.1 三级进化体系

Amazing 实现了 Agent/Sub-Agent/Skill 三级进化：

```
┌─────────────────────────────────────┐
│         Agent 进化                   │
│  基于: 任务成功率、代码质量、交付时间 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│       Sub-Agent 进化                 │
│  基于: 角色效率、协作分数            │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│         Skill 进化                   │
│  基于: 准确率、性能、用户满意度      │
└─────────────────────────────────────┘
```

### 4.2 进化指标

**Agent 级别**：
- 任务成功率 (>90% 升级)
- 代码质量评分 (SonarQube)
- 平均交付时间

**Sub-Agent 级别**：
- 角色任务完成率
- 协作响应时间
- 代码审查通过率

**Skill 级别**：
- 功能准确率
- 执行性能
- 用户满意度评分

### 4.3 进化示例

```python
# Agent 进化配置
AGENT_EVOLUTION = {
    "common": {
        "level": 2,
        "metrics": {
            "task_success_rate": 0.92,
            "code_quality_score": 85,
            "avg_delivery_time": "2.5 days"
        },
        "next_level_requirements": {
            "task_success_rate": 0.95,
            "code_quality_score": 90
        }
    }
}
```

---

## 五、实战案例

### 5.1 案例：实现用户权限管理模块

**参与角色**：PM、Frontend、Backend、QA、Ops

**工作流程**：

#### 步骤 1：PM 创建 PRD

```bash
# PM 角色
python3 scripts/amazing-cli.py role select
# 选择: 1. 产品经理 (pm)

# 使用 Claude Code 生成 PRD
claude-code "生成用户权限管理模块 PRD，包含：
1. 角色管理 (创建/编辑/删除角色)
2. 权限分配 (为角色分配权限)
3. 审计日志 (记录权限变更)
4. 技术方案 (数据库设计、API 设计)
5. 验收标准"
```

#### 步骤 2：Frontend 开发 UI

```bash
# Frontend 角色
python3 scripts/amazing-cli.py role select
# 选择: 2. 前端开发 (frontend)

# 开发角色管理页面
claude-code "创建 RoleManagement 组件：
- 角色列表 (Table)
- 创建角色 (Modal)
- 编辑角色 (Modal)
- 删除角色 (确认对话框)
- 权限分配 (Tree Select)
使用 React + TypeScript + Ant Design"
```

#### 步骤 3：Backend 开发 API

```bash
# Backend 角色
python3 scripts/amazing-cli.py role select
# 选择: 3. 后端开发 (backend)

# 开发 API
claude-code "实现角色管理 API：
1. POST /api/v1/roles - 创建角色
2. GET /api/v1/roles - 获取角色列表
3. PUT /api/v1/roles/{id} - 更新角色
4. DELETE /api/v1/roles/{id} - 删除角色
5. POST /api/v1/roles/{id}/permissions - 分配权限
使用 FastAPI + SQLAlchemy + PostgreSQL"
```

#### 步骤 4：QA 测试

```bash
# QA 角色
python3 scripts/amazing-cli.py role select
# 选择: 4. 测试工程师 (qa)

# 生成测试用例
claude-code "为角色管理功能生成测试用例：
1. 单元测试 (pytest)
2. 集成测试 (API 测试)
3. E2E 测试 (Playwright)
覆盖正常流程、异常流程、边界条件"

# 执行测试
pytest
npm run test:e2e
```

#### 步骤 5：Ops 部署

```bash
# Ops 角色
python3 scripts/amazing-cli.py role select
# 选择: 5. 运维工程师 (ops)

# 部署到 K8s
make k8s-deploy

# 监控
kubectl get pods -n amazing
kubectl logs -f deployment/python-api -n amazing
```

### 5.2 协作效果

通过 Agent-Teams 协同，整个开发流程：

- **需求分析**: 1 天 (PM + Claude Code)
- **并行开发**: 2 天 (Frontend + Backend 同时进行)
- **测试**: 1 天 (QA + 自动化测试)
- **部署**: 0.5 天 (Ops + K8s)

**总计**: 4.5 天完成，相比传统开发（约 10 天）效率提升 **55%**。

---

## 六、技术亮点

### 6.1 统一的 CLI 工具

Amazing 提供了强大的 CLI 工具 `amazing-cli.py`：

```bash
# 角色管理
python3 scripts/amazing-cli.py role select
python3 scripts/amazing-cli.py role permissions

# 任务管理
python3 scripts/amazing-cli.py tasks --role frontend
python3 scripts/amazing-cli.py task claim <task-id>

# PRD 管理
python3 scripts/amazing-cli.py prd create "功能名称"
python3 scripts/amazing-cli.py prd list

# Agent 管理
python3 scripts/amazing-cli.py agent assign common --task prd-001
python3 scripts/amazing-cli.py status
```

### 6.2 IronClaw 对话界面

IronClaw 是 Amazing 的 Web 界面，支持自然语言交互：

```
用户: @IronClaw 创建任务: 实现用户登录功能
IronClaw:
✅ 任务已创建
- 任务 ID: TASK-001
- 分配给: Common Agent
- 优先级: 高
- 预计时间: 2 天

需要我帮你生成技术方案吗？
```

### 6.3 多语言支持

- **Python**: FastAPI + SQLAlchemy (Common, Data, Training)
- **Go**: Gin + GORM (Compute, Model-Service)
- **TypeScript**: React + Vite (Frontend)

### 6.4 容器化部署

```bash
# Docker Compose (开发环境)
make docker-up

# Kubernetes (生产环境)
make k8s-deploy
```

---

## 七、未来规划

### 7.1 短期目标 (Q2 2025)

1. **完善 6 大 Agent**
   - Common Agent (已完成 80%)
   - Compute Agent (规划中)
   - Data Agent (规划中)

2. **增强 IronClaw**
   - 实时协作
   - 语音交互
   - 移动端支持

3. **进化机制落地**
   - Agent 自动升级
   - Skill 市场

### 7.2 长期愿景

1. **开放生态**
   - 支持第三方 Agent
   - Skill 插件市场
   - 社区贡献

2. **跨平台支持**
   - GitLab 集成
   - Jira 集成
   - Slack 集成

3. **企业级特性**
   - 多租户
   - SSO 认证
   - 审计日志

---

## 八、总结

Amazing 通过 Agent-Teams 范式，将 AI 辅助开发从"单点工具"升级为"团队协作平台"。核心创新点：

1. **多角色协同**：覆盖 PM/Frontend/Backend/QA/Ops/Operation 全流程
2. **场景适配**：支持功能开发、Bug 修复、需求分析等多种场景
3. **进化机制**：Agent/Sub-Agent/Skill 三级进化，持续提升能力
4. **工具链降级**：Claude Code → Codex → IronClaw，保证可用性

如果你也在思考如何让 AI 更好地服务于团队协作，欢迎关注 Amazing 项目：

- **GitHub**: https://github.com/z58362026/amazing
- **在线架构图**: https://z58362026.github.io/amazing/
- **文档**: 项目 `docs/` 目录

期待与你一起探索 AI 协同开发的未来！

---

## 附录：快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Docker
- Kubernetes (可选)

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/z58362026/amazing.git
cd amazing

# 2. 安装依赖
make install

# 3. 启动服务
make dev

# 4. 访问 IronClaw
open http://localhost:3001
```

### 选择角色

```bash
# 选择你的角色
python3 scripts/amazing-cli.py role select

# 查看权限
python3 scripts/amazing-cli.py role permissions
```

### 开始工作

```bash
# 查看可用任务
python3 scripts/amazing-cli.py tasks

# 认领任务
python3 scripts/amazing-cli.py task claim <task-id>

# 使用 Claude Code 开发
claude-code "你的需求"
```

---

**关键词**: AI 协同开发、Agent-Teams、Claude Code、多角色协作、软件工程、DevOps

**标签**: #AI开发 #团队协作 #Agent #Claude #DevOps
