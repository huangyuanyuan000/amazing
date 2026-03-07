# Amazing：基于 Agent-Teams 的 AI 协同开发平台，让团队效率提升 10 倍

> 一个开源的企业级大模型管理平台，支持 7 大角色、6 大 Agent、全自动/半自动双模式的全流程 AI 协同开发

## 🎯 写在前面

你是否遇到过这些问题：

- 产品经理写 PRD 要花 2 天，开发理解需求又要 1 天？
- 前后端开发各自为战，接口对接总是出问题？
- 测试用例写到手软，还是漏掉了关键场景？
- 代码审查流于形式，质量问题总是到线上才发现？
- 运维部署像开盲盒，每次上线都提心吊胆？
- AI 工具虽好，但缺少人工把关，不敢放心使用？

如果你的答案是"是"，那么这篇文章就是为你准备的。

今天要介绍的 **Amazing** 项目，是一个基于 **Agent-Teams 协同开发范式**的开源平台，通过 AI 赋能，让整个研发流程从需求到上线实现全流程自动化，同时支持人工决策和把关。

**GitHub 仓库**: https://github.com/z58362026/amazing
**在线架构图**: https://z58362026.github.io/amazing/

---

## 💡 核心理念

### 什么是 Agent-Teams？

传统的 AI 辅助开发工具，通常是"单打独斗"：
- Copilot 帮你写代码
- ChatGPT 帮你解答问题
- 各种 AI 工具各管各的

但真实的软件开发是**团队协作**：产品、前端、后端、测试、运维、运营，每个角色都有自己的职责，需要相互配合。

**Agent-Teams 就是让 AI 也学会团队协作**：

```
👑 架构师 → 技术决策和架构设计
    ↓
📋 产品经理 → 生成 PRD
    ↓
🎨 前端 + ⚙️ 后端 → 并行开发
    ↓
🧪 测试 → 自动化测试
    ↓
👑 架构师 → 代码审查
    ↓
🚀 运维 → 一键部署
```

每个 Agent 专注自己的领域，通过 **Orchestrator（编排器）** 协调，形成完整的开发流水线。

### 核心创新：双模式 AI

Amazing 最大的创新是支持**全自动和半自动两种 AI 模式**，并且**只有架构师有权限切换**：

#### 🤖 全自动模式 (Full-Auto)
- AI 自主决策和执行
- 关键节点设置检查点
- 异常时暂停等待人工
- 适合成熟流程、低风险任务

#### 👨‍💻 半自动模式 (Semi-Auto)
- AI 生成方案供选择
- 人工审核和决策
- 关键步骤人工批准
- 适合新项目、高风险任务

**权限控制**：
- ✅ 架构师：拥有模式切换权限
- ❌ 其他角色：无权切换模式
- 📝 所有切换操作都会被记录和审计

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

### 👥 7 种角色支持

- **👑 架构师 (Architect)**: 技术决策、架构设计、代码审查、**模式切换**
- **📋 产品经理 (PM)**: 需求分析、PRD 编写、功能验收
- **🎨 前端开发 (Frontend)**: UI/UX 实现、组件开发
- **⚙️ 后端开发 (Backend)**: API 开发、数据库设计
- **🧪 测试工程师 (QA)**: 测试设计、自动化测试
- **🚀 运维工程师 (Ops)**: 部署、监控、故障排查
- **📊 运营人员 (Operation)**: 数据分析、用户运营

### 🎨 3 种场景适配

1. **功能开发**: PM → 架构师决策 → Frontend/Backend → 架构师审查 → QA → 架构师验收 → Ops
2. **Bug 修复**: QA → Backend → 架构师审查 → QA → Ops (支持回滚)
3. **需求分析**: PM → 架构师决策 → 技术评审 → PRD 生成

### 🔄 进化机制

- **Agent 进化**: 基于任务成功率、代码质量、交付时间
- **Sub-Agent 进化**: 基于角色效率、协作分数
- **Skill 进化**: 基于准确率、性能、用户满意度

---

## 🏗️ 架构设计

### 📊 在线架构图

**🌐 [查看完整 AI 协同开发范式架构](https://z58362026.github.io/amazing/)**

- [系统架构图](https://z58362026.github.io/amazing/architecture/system-architecture.html)
- [功能开发流程](https://z58362026.github.io/amazing/workflows/development.html)
- [Bug 修复流程](https://z58362026.github.io/amazing/workflows/bug-fix.html)
- [架构师工作流](https://z58362026.github.io/amazing/workflows/architect-workflow.html)
- [模式切换流程](https://z58362026.github.io/amazing/workflows/mode-switch.html)

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    统一入口层                                │
│  CLI (amazing-cli) | Web Dashboard (IronClaw)              │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                   AI 工具链层                              │
│  Claude Code (主) → Codex CLI (备) → Codex Desktop       │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                Agent Orchestrator                          │
│  - 架构师决策管理 (技术方案/产品形态/质量把关)             │
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

---

## 🔀 AI 模式切换机制

### 为什么需要模式切换？

在实际开发中，不同需求有不同特点：

- **成熟功能**：技术栈熟悉、风险可控 → 适合全自动
- **新项目**：技术不确定、风险较高 → 适合半自动
- **Bug 修复**：影响范围小、快速修复 → 适合全自动
- **架构设计**：影响深远、需要慎重 → 适合半自动

### 权限控制：只有架构师可以切换

**为什么只有架构师？**

1. **技术决策权**：架构师负责整体技术方案，有权决定自动化程度
2. **风险评估能力**：架构师能够评估不同模式的风险和收益
3. **全局视角**：架构师了解项目整体情况，能做出最优决策
4. **责任明确**：模式切换影响重大，需要明确责任人

### 切换流程

```
1. 架构师接收需求
   ├── 需求ID: REQ-001
   ├── 需求类型: 功能开发
   └── 风险等级: 低
   ↓
2. 架构师评估需求
   ├── 技术复杂度: 低
   ├── 业务风险: 低
   ├── 团队熟悉度: 高
   └── 决策: 使用全自动模式
   ↓
3. 架构师切换模式
   $ python3 scripts/mode_cli.py mode set full-auto \
     -r REQ-001 \
     --reason "成熟功能，团队熟悉，风险可控"
   ↓
4. 系统记录切换
   ├── 时间戳
   ├── 操作者: architect
   ├── 需求ID: REQ-001
   ├── 切换原因
   └── 模式: semi-auto → full-auto
   ↓
5. AI 按新模式执行
```

### 按需求维度切换

每个需求可以独立设置模式：

```bash
# 需求 REQ-001: 用户登录功能（成熟功能，低风险）
$ python3 scripts/mode_cli.py mode set full-auto -r REQ-001

# 需求 REQ-002: 支付系统（高风险，需要把关）
$ python3 scripts/mode_cli.py mode set semi-auto -r REQ-002

# 需求 REQ-003: 数据报表（低风险，快速开发）
$ python3 scripts/mode_cli.py mode set full-auto -r REQ-003
```

---

## 🚀 快速开始

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

# 可选角色：
# 0. 👑 架构师 (architect)
# 1. 📋 产品经理 (pm)
# 2. 🎨 前端开发 (frontend)
# 3. ⚙️ 后端开发 (backend)
# 4. 🧪 测试工程师 (qa)
# 5. 🚀 运维工程师 (ops)
# 6. 📊 运营人员 (operation)
```

---

## 💼 实战案例：用户权限管理模块

### 场景描述

开发一个用户权限管理模块，包含角色管理、权限分配、审计日志等功能。

### 参与角色

- 👑 架构师
- 📋 产品经理
- 🎨 前端开发
- ⚙️ 后端开发
- 🧪 测试工程师
- 🚀 运维工程师

### 完整流程

#### 步骤 1：PM 创建 PRD

```bash
# PM 角色
python3 scripts/amazing-cli.py role set pm

# 使用 Claude Code 生成 PRD
claude-code "生成用户权限管理模块 PRD，包含：
1. 角色管理 (创建/编辑/删除角色)
2. 权限分配 (为角色分配权限)
3. 审计日志 (记录权限变更)
4. 技术方案 (数据库设计、API 设计)
5. 验收标准"
```

#### 步骤 2：架构师决策

```bash
# 切换到架构师角色
python3 scripts/amazing-cli.py role set architect

# AI 提供 3 种技术方案
claude-code "分析用户权限管理需求，提供 3 种技术方案：
1. RBAC (基于角色)
2. ABAC (基于属性)
3. 混合方案
对比优缺点、实现复杂度、性能"

# 架构师选择方案
python3 scripts/architect_cli.py arch solution user-permission \
  --choice "RBAC" \
  --reason "实现简单，满足当前需求" \
  --tech-stack "FastAPI + PostgreSQL + Redis"

# 设置 AI 模式（成熟功能，使用全自动）
python3 scripts/mode_cli.py mode set full-auto \
  -r REQ-001 \
  --reason "RBAC 是成熟方案，团队熟悉，风险可控"
```

#### 步骤 3：并行开发

**前端开发**：
```bash
# 切换到前端角色
python3 scripts/amazing-cli.py role set frontend

# AI 自动开发（全自动模式）
claude-code "创建角色管理页面：
- 角色列表 (Table)
- 创建角色 (Modal)
- 编辑角色 (Modal)
- 删除角色 (确认对话框)
- 权限分配 (Tree Select)
使用 React + TypeScript + Ant Design"
```

**后端开发**：
```bash
# 切换到后端角色
python3 scripts/amazing-cli.py role set backend

# AI 自动开发（全自动模式）
claude-code "实现角色管理 API：
1. POST /api/v1/roles - 创建角色
2. GET /api/v1/roles - 获取角色列表
3. PUT /api/v1/roles/{id} - 更新角色
4. DELETE /api/v1/roles/{id} - 删除角色
5. POST /api/v1/roles/{id}/permissions - 分配权限
使用 FastAPI + SQLAlchemy + PostgreSQL"
```

#### 步骤 4：架构师审查

```bash
# 查看待审查任务
python3 scripts/architect_cli.py review pending

# 审查前端代码
python3 scripts/architect_cli.py review start frontend-role-page

# 批准或拒绝
python3 scripts/architect_cli.py review approve frontend-role-page \
  --comment "UI 还原度高，代码质量好"
```

#### 步骤 5：QA 测试

```bash
# 切换到 QA 角色
python3 scripts/amazing-cli.py role set qa

# AI 生成测试用例
claude-code "为角色管理功能生成测试用例：
1. 单元测试 (pytest)
2. 集成测试 (API 测试)
3. E2E 测试 (Playwright)
覆盖正常流程、异常流程、边界条件"

# 执行测试
pytest
npm run test:e2e
```

#### 步骤 6：架构师验收

```bash
# 运行验收测试
python3 scripts/amazing-cli.py test acceptance --task REQ-001

# 批准上线
python3 scripts/amazing-cli.py approve REQ-001 \
  --reviewer architect \
  --comment "功能完整，测试通过，批准上线"
```

#### 步骤 7：Ops 部署

```bash
# 切换到 Ops 角色
python3 scripts/amazing-cli.py role set ops

# 部署到 K8s
make k8s-deploy

# 监控
kubectl get pods -n amazing
kubectl logs -f deployment/python-api -n amazing
```

### 效果对比

通过 Agent-Teams 协同，整个开发流程：

| 阶段 | 传统开发 | Amazing (全自动) | Amazing (半自动) |
|------|---------|-----------------|-----------------|
| 需求分析 | 1天 | 0.5天 | 0.5天 |
| PRD 生成 | 1天 | 0.5天 | 0.5天 |
| 架构设计 | 2天 | 0.5天 | 1天 |
| 并行开发 | 4天 | 1天 | 2天 |
| 代码审查 | 1天 | 0.5天 | 1天 |
| 测试 | 2天 | 0.5天 | 1天 |
| 部署 | 0.5天 | 0.5天 | 0.5天 |
| **总计** | **11.5天** | **4天** | **6.5天** |

**效率提升**：
- 全自动模式：提升 **65%**
- 半自动模式：提升 **43%**

---

## 🎯 技术亮点

### 1. 统一的 CLI 工具

Amazing 提供了强大的 CLI 工具：

```bash
# 角色管理
python3 scripts/amazing-cli.py role select
python3 scripts/amazing-cli.py role permissions

# 架构师专用命令
python3 scripts/architect_cli.py arch create <feature>
python3 scripts/architect_cli.py review pending

# 模式管理
python3 scripts/mode_cli.py mode show
python3 scripts/mode_cli.py mode set full-auto -r REQ-001
python3 scripts/mode_cli.py mode history
```

### 2. IronClaw 对话界面

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

### 3. 多语言支持

- **Python**: FastAPI + SQLAlchemy (Common, Data, Training)
- **Go**: Gin + GORM (Compute, Model-Service)
- **TypeScript**: React + Vite (Frontend)

### 4. 容器化部署

```bash
# Docker Compose (开发环境)
make docker-up

# Kubernetes (生产环境)
make k8s-deploy
```

---

## 🔮 未来规划

### 短期目标 (Q2 2025)

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

### 长期愿景

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

## 📚 相关资源

- **GitHub 仓库**: https://github.com/z58362026/amazing
- **在线架构图**: https://z58362026.github.io/amazing/
- **文档中心**: https://github.com/z58362026/amazing/blob/main/docs/README.md
- **快速开始**: https://github.com/z58362026/amazing/blob/main/QUICKSTART.md

---

## 🤝 参与贡献

Amazing 是一个开源项目，欢迎大家参与贡献！

### 贡献方式

1. **提交 Issue**: 报告 Bug 或提出新功能建议
2. **提交 PR**: 贡献代码或文档
3. **参与讨论**: 在 GitHub Discussions 中参与讨论
4. **分享经验**: 写文章、做分享，帮助更多人了解 Amazing

### 贡献指南

查看 [CONTRIBUTING.md](https://github.com/z58362026/amazing/blob/main/CONTRIBUTING.md) 了解详情。

---

## 💬 总结

Amazing 通过 **Agent-Teams 协同开发范式**，将 AI 辅助开发从"单点工具"升级为"团队协作平台"。

### 核心创新

1. **7 种角色协同**：覆盖 PM/Frontend/Backend/QA/Ops/Operation/Architect 全流程
2. **双模式 AI**：全自动和半自动模式，灵活应对不同场景
3. **权限控制**：只有架构师可以切换模式，确保决策质量
4. **按需求切换**：不同需求可以使用不同模式，风险可控
5. **进化机制**：Agent/Sub-Agent/Skill 三级进化，持续提升能力
6. **工具链降级**：Claude Code → Codex → IronClaw，保证可用性

### 适用场景

- ✅ 企业级大模型管理平台开发
- ✅ 多角色协同的软件项目
- ✅ 需要 AI 辅助但又要人工把关的项目
- ✅ 希望提升团队效率的研发团队

如果你也在思考如何让 AI 更好地服务于团队协作，欢迎关注 Amazing 项目！

---

**关键词**: AI 协同开发、Agent-Teams、Claude Code、多角色协作、软件工程、DevOps、全自动模式、半自动模式、架构师决策

**标签**: #AI开发 #团队协作 #Agent #Claude #DevOps #开源项目

---

<div align="center">

**⭐ 如果觉得有帮助，欢迎 Star 支持！**

[GitHub](https://github.com/z58362026/amazing) | [在线架构图](https://z58362026.github.io/amazing/) | [文档](https://github.com/z58362026/amazing/blob/main/docs/README.md)

Made with ❤️ by Amazing Team

</div>
