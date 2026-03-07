# Amazing：让 AI 真正能开发企业级项目的框架

> 📖 **[完整架构文档](https://z58362026.github.io/amazing/)** | **[GitHub 仓库](https://github.com/z58362026/amazing)**

## 核心问题

用 AI 开发复杂项目时的四大痛点：

- 💥 **上下文溢出** - 一次生成太多代码导致 AI 卡死
- 🔄 **重复劳动** - 每次都要重新描述项目结构和技术栈
- 🏗️ **架构混乱** - 缺乏统一的项目结构和开发规范
- 🤖 **权限失控** - AI 可以随意修改任何代码

**核心洞察**：AI 开发的瓶颈不是 AI 能力，而是缺少一套完整的协同开发范式。

Amazing 就是这套范式的实现。

---

## 解决方案

Amazing 是一套 **AI 协同开发范式**，一条命令初始化企业级项目：

```bash
python3 scripts/init.py my-project \
  --description="电商平台：用户、商品、订单、支付"
```

自动生成：
- 🏗️ 9 大业务流程（产品→架构→开发→测试→部署→运营→审查→修复→进化）
- 👥 7 个角色 + 独立权限实例
- 🤖 55 个 Handoff Agents
- 🧠 23 个可复用 Skills（架构/开发/测试/运维/安全/运营）
- 📦 开箱即用的部署配置

> 详细使用方式见 [在线文档](https://z58362026.github.io/amazing/)

---

## 四大核心创新

### 1. Handoffs 任务拆分 - 解决上下文溢出

**核心机制**：
```
大任务 → 自动拆分 → 逐个执行（< 200行/个）→ 状态保存 → 支持恢复
```

**实际效果**：
```bash
# 开发用户管理模块 → 自动拆分为 7 个子任务
python scripts/handoff_manager.py run --task="开发用户管理模块"

# 输出：
# [1/7] 数据模型生成 ✓
# [2/7] API 端点生成 ✓
# [3/7] 后端服务生成 ✓
# [4/7] 前端 API 服务层 ✓
# [5/7] 前端状态管理 ✓
# [6/7] 前端页面生成 ✓
# [7/7] 前端组件生成 ✓
```

> 详细原理见 [Handoffs 架构文档](https://z58362026.github.io/amazing/handoffs-architecture.html)

### 2. IronClaw 权限实例 - 解决权限失控

**核心机制**：每个角色一个独立的 IronClaw 权限实例

```yaml
# 前端开发权限示例
permissions:
  read: [docs/, src/frontend/, tests/frontend/]
  write: [src/frontend/, tests/frontend/]
  create: [frontend-components, frontend-pages]

restrictions:
  - 不能修改后端代码
  - 不能修改部署配置
  - 不能创建/修改角色
```

> 完整权限配置见 [GitHub 仓库](https://github.com/z58362026/amazing/tree/main/.claude/ironclaw)

### 3. 智能初始化编排器 - 解决重复劳动

**核心能力**：
```
业务描述 → 领域分析 → 模块拆分 → 技术选型 → 架构设计 → 脚手架生成
```

自动推断：
- 技术栈（Python/Go/Node.js/Java）
- 数据库（PostgreSQL/MySQL/MongoDB/Redis）
- 部署方式（Docker/K8s/离线）
- 模块划分（user/product/order/payment...）

> 编排器实现见 [scripts/orchestrator.py](https://github.com/z58362026/amazing/blob/main/scripts/orchestrator.py)

### 4. 九大业务流程链 - 解决流程缺失

| 链路 | 说明 | Handoffs |
|------|------|----------|
| **product-analysis** | 产品分析链 | 5 个 |
| **tech-architecture** | 技术架构链 | 6 个 |
| **code-generation** | 代码开发链 | 7 个 |
| **testing** | 测试链 | 6 个 |
| **bug-fix** | Bug 修复链 | 6 个 |
| **deployment** | 部署运维链 | 4 个 |
| **operations** | 运营链 | 4 个 |
| **code-review** | 代码审查链 | 3 个 |
| **evolution** | 进化迭代链 | 4 个 |

> 完整流程配置见 [在线架构图](https://z58362026.github.io/amazing/)

---

## Agent 体系架构

Amazing 采用三层 Agent 架构：

### 固定 Agent��6个）- 框架级通用能力

| Agent | 职责 | 典型能力 |
|-------|------|---------|
| **common** | 通用功能 | 认证、配置、网关、通知 |
| **database** | 数据库适配 | 多数据库支持、迁移、查询优化 |
| **deployment** | 部署能力 | Docker、K8s、CI/CD |
| **monitoring** | 监控告警 | 日志、指标、链路追踪 |
| **evolution** | 进化分析 | 模式检测、影响分析、自动优化 |
| **review** | 代码审查 | 代码质量、安全、性能审查 |

### 业务 Agent - 根据需求动态生成

初始化时根据业务描述自动生成，例如电商平台：
- **user** Agent（用户管理）→ auth-agent, profile-agent
- **product** Agent（商品管理）→ catalog-agent, inventory-agent
- **order** Agent（订单管理）→ order-agent, fulfillment-agent
- **payment** Agent（支付管理）→ payment-agent, refund-agent

### Handoff Agents（55个）- 任务执行单元

按 9 条业务链路组织，每个 Handoff 生成代码 < 200 行。

> 完整 Agent 体系见 [Agent Teams 文档](https://z58362026.github.io/amazing/02-agent-teams/)

---

## Skill 体系：23 个可复用技能库

Skill 是 Agent 和 Handoff 调用的**方法论和规范库**，按角色职责分为 8 大类：

| 分类 | Skills | 核心能力 |
|------|--------|---------|
| **架构设计** | architecture-design, tech-selection, api-design | 架构模式选择、技术选型评估、RESTful API 规范 |
| **开发** | react-component, state-management, microservice, auth-implement | React 组件规范、状态管理方案、微服务设计、认证授权 |
| **数据库** | database-design, db-migration, query-optimization | Schema 设计、零停机迁移、查询优化 |
| **测试** | test-design, test-automation, performance-test | 测试金字塔、自动化框架、性能测试方案 |
| **运维** | docker-deploy, k8s-deploy, ci-cd-pipeline, monitoring-setup | Docker 多阶段构建、K8s 部署策略、CI/CD 流水线、Prometheus 监控 |
| **安全** | security-audit, code-review-checklist | OWASP Top 10 检查、代码审查五维度 |
| **运营** | data-analysis, config-management | 数据分析方法论、功能灰度/A/B 测试 |
| **初始化** | init-project | 对话式项目初始化 |

### Skill 与角色绑定

每个角色只能使用授权范围内的 Skill，通过 `/init-role` 命令加载：

```bash
/init-role frontend-dev
# → 自动加载：react-component, state-management 等前端 Skills
# → 权限限制：不能调用 docker-deploy, k8s-deploy 等运维 Skills
```

### Skill 进化能力

每个 Skill 内置进化机制，通过指标跟踪持续优化：
- 架构模式库从项目实践中验证效果
- 测试模式从 Bug 中反推缺失用例
- CI/CD 模板持续缩短执行时间

### 工具链切换

通过 `/switch-tool` 命令在不同 AI 工具间无缝切换：

```bash
/switch-tool claude    # Claude Code CLI（默认，最强能力）
/switch-tool codex     # Codex CLI（本地降级方案）
```

> 完整 Skill 配置见 [GitHub 仓库](https://github.com/z58362026/amazing/tree/main/.claude/skills)

---

## 实战案例：大模型管理平台

用 Amazing 开发完整的大模型管理平台：

```bash
# 1. 初始化项目（1 分钟）
python3 scripts/init.py model-platform \
  --description="大模型管理平台"

# 2. 产品分析（5 分钟）
python scripts/handoff_manager.py run \
  --task="分析大模型平台需求" \
  --chain=product-analysis

# 3. 代码开发（按模块）
python scripts/handoff_manager.py run \
  --task="开发用户管理模块" \
  --chain=code-generation

# 4. 一键部署
make docker  # 或 make k8s
```

### 开发效率对比

| 阶段 | 传统开发 | Amazing | 提升 |
|------|---------|---------|------|
| 项目初始化 | 2-3 天 | 1 分钟 | **99%** |
| 产品分析 | 1-2 天 | 5 分钟 | **99%** |
| 技术架构 | 3-5 天 | 10 分钟 | **99%** |
| 代码开发 | 2-3 周 | 2-3 天 | **90%** |
| 测试编写 | 1 周 | 1 天 | **85%** |
| 部署配置 | 2-3 天 | 1 小时 | **95%** |

**总体提升：约 90%**

> 完整案例见 [大模型平台案例](https://z58362026.github.io/amazing/06-examples/model-platform/)

---

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/z58362026/amazing.git
cd amazing
```

### 2. 初始化项目
```bash
python3 scripts/init.py my-project \
  --description="你的项目描述"
```

### 3. 开始开发
```bash
cd my-project

# 产品分析
python scripts/handoff_manager.py run \
  --task="分析需求" \
  --chain=product-analysis

# 代码开发
python scripts/handoff_manager.py run \
  --task="开发模块" \
  --chain=code-generation

# 启动开发环境
make dev
```

> 详细教程见 [快速开始文档](https://z58362026.github.io/amazing/00-overview/)

---

## 与其他方案对比

| 特性 | Amazing | 传统脚手架 | AI 直接生成 |
|------|---------|-----------|------------|
| **上下文溢出** | ✅ 解决 | N/A | ❌ 存在 |
| **权限控制** | ✅ 严格 | ❌ 无 | ❌ 无 |
| **完整流程** | ✅ 9 大流程 | ❌ 仅初始化 | ❌ 仅代码 |
| **任务拆分** | ✅ 自动 | ❌ 无 | ❌ 手动 |
| **文档生成** | ✅ 自动 | ❌ 手动 | ❌ 缺失 |
| **多数据库** | ✅ 支持 | ❌ 单一 | ❌ 单一 |
| **技能复用** | ✅ 23 个 Skill | ❌ 无 | ❌ 无 |
| **进化能力** | ✅ 支持 | ❌ 无 | ❌ 无 |
| **部署就绪** | ✅ 开箱即用 | ⚠️ 需配置 | ❌ 缺失 |

---

## 核心价值

Amazing 解决了 AI 开发的核心痛点：

1. ✅ **重复劳动** → 智能初始化编排器
2. ✅ **上下文溢出** → Handoffs 任务拆分
3. ✅ **权限失控** → 独立 IronClaw 实例
4. ✅ **流程缺失** → 9 大业务流程链
5. ✅ **经验沉淀** → 23 个可复用 Skill 技能库

通过 Amazing，你可以：
- 🚀 **10 倍提升**开发效率
- 📚 **自动生成**完整文档
- 🏗️ **标准化**项目架构
- 🔐 **严格控制**权限边界
- 🔄 **持续进化**AI 能力

---

## 相关链接

- **GitHub 仓库**：https://github.com/z58362026/amazing
- **在线架构图**：https://z58362026.github.io/amazing/
- **问题反馈**：https://github.com/z58362026/amazing/issues

---

**如果觉得有帮助，欢迎 Star ⭐ 支持一下！**
