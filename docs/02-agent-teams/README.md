# 第二层：Agent-Teams 层（组织形态层）

## 概述

Agent-Teams 层定义了团队的**组织形态**，包括固定角色、固定部门和协作机制。

这是 Amazing 架构的基础层，就像公司的组织架构一样。

---

## 核心组成

### 1. 固定角色（跨部门）

这些角色存在于任何软件团队中：

| 角色 | 英文 | 职责 | 为什么固定？ |
|------|------|------|-------------|
| 👑 架构师 | Architect | 技术决策、架构设计、质量把关 | 任何项目都需要技术决策者 |
| 📋 产品经理 | PM | 需求分析、产品规划、功能验收 | 任何项目都需要需求管理 |
| 🎨 前端开发 | Frontend | UI/UX 实现、组件开发 | 现代应用都需要前端界面 |
| ⚙️ 后端开发 | Backend | API 开发、业务逻辑、数据库 | 任何应用都需要后端服务 |
| 🧪 测试工程师 | QA | 测试设计、质量保证、Bug 追踪 | 质量保证是必需的 |
| 🚀 运维工程师 | Ops | 部署、监控、故障排查 | 应用需要部署和维护 |

**这些角色是固定的，因为它们是软件开发的基本分工。**

### 2. 固定部门（通用职能）

这些部门提供通用能力，就像公司的 HR、财务、IT 部门：

#### Common Agent（通用部门）

**职责**：
- 用户管理
- 权限控制
- 日志审计
- 配置管理

**为什么固定？**
- 任何系统都需要用户管理
- 任何系统都需要权限控制
- 这些是通用能力，不属于特定业务

**类比**：
- 就像公司的 HR 部门（管理员工）
- 就像公司的 IT 部门（管理系统）

#### Review Agent（质量审核部门）

**职责**：
- 代码审查
- 安全审查
- 性能审查
- 合规检查

**为什么固定？**
- 任何系统都需要质量把控
- 审核是独立的职能
- 需要统一的标准和流程

**类比**：
- 就像公司的质量管理部门
- 就像公司的审计部门

### 3. 业务 Agent（动态创建）

业务 Agent 是根据**产品形态**动态创建的，对应业务部门。

**示例：大模型管理平台**

```
算力平台 Agent（算力业务部门）
├── PM Sub-Agent（产品经理）
├── Frontend Sub-Agent（前端开发）
├── Backend Sub-Agent（后端开发）
├── QA Sub-Agent（测试工程师）
└── Ops Sub-Agent（运维工程师）

数据 Agent（数据业务部门）
├── PM Sub-Agent
├── Frontend Sub-Agent
├── Backend Sub-Agent
├── QA Sub-Agent
└── Ops Sub-Agent

训练 Agent（训练业务部门）
├── PM Sub-Agent
├── Frontend Sub-Agent
├── Backend Sub-Agent
├── QA Sub-Agent
└── Ops Sub-Agent

模型服务 Agent（服务业务部门）
├── PM Sub-Agent
├── Frontend Sub-Agent
├── Backend Sub-Agent
├── QA Sub-Agent
└── Ops Sub-Agent
```

**这就像真实的公司组织结构**：
- 有通用部门（HR、财务、IT）→ Common Agent、Review Agent
- 有业务部门（销售、市场、产品）→ Business Agents
- 每个部门都有不同角色的人 → Sub-Agents

---

## 组织结构图

```
Amazing 组织结构

├── 固定部门（通用职能）
│   ├── Common Agent（通用部门）
│   │   ├── PM Sub-Agent
│   │   ├── Frontend Sub-Agent
│   │   ├── Backend Sub-Agent
│   │   ├── QA Sub-Agent
│   │   └── Ops Sub-Agent
│   │
│   └── Review Agent（审核部门）
│       ├── QA Sub-Agent（质量审查）
│       └── Architect Sub-Agent（架构审查）
│
└── 业务部门（动态创建）
    ├── 业务 Agent 1
    │   ├── PM Sub-Agent
    │   ├── Frontend Sub-Agent
    │   ├── Backend Sub-Agent
    │   ├── QA Sub-Agent
    │   └── Ops Sub-Agent
    │
    ├── 业务 Agent 2
    │   └── ...
    │
    └── 业务 Agent N
        └── ...
```

---

## 协作机制

### 1. 角色权限矩阵

| 角色 | 查看代码 | 编写代码 | 审查代码 | 部署 | 切换模式 |
|------|---------|---------|---------|------|---------|
| 架构师 | ✅ | ✅ | ✅ | ✅ | ✅ |
| PM | ✅ | ❌ | ❌ | ❌ | ❌ |
| Frontend | ✅ | ✅ | ❌ | ❌ | ❌ |
| Backend | ✅ | ✅ | ❌ | ❌ | ❌ |
| QA | ✅ | ✅ | ✅ | ❌ | ❌ |
| Ops | ✅ | ❌ | ❌ | ✅ | ❌ |

### 2. 工作流程

**功能开发流程**：

```
1. PM 创建需求
   ↓
2. 架构师决策（选择 AI 模式）
   ↓
3. Frontend + Backend 并行开发
   ↓
4. 架构师审查代码
   ↓
5. QA 测试
   ↓
6. 架构师验收
   ↓
7. Ops 部署
```

### 3. 决策机制

**架构师主导**：
- 技术方案决策
- 业务模块划分
- 技术栈选型
- AI 模式切换
- 代码质量把关

**为什么架构师主导？**
- 有全局视角
- 懂技术和业务
- 能评估风险
- 负责架构质量

---

## Sub-Agent 说明

### 什么是 Sub-Agent？

Sub-Agent 是**角色在具体业务部门的实现**。

**示例**：

```
算力平台 Agent 的 Backend Sub-Agent：

角色：后端开发
部门：算力平台
职责：
├── 实现算力管理 API
├── 设计数据库表结构
├── 编写业务逻辑
└── 编写单元测试

技术栈：
├── Python + FastAPI
├── PostgreSQL
└── Redis
```

### Sub-Agent 的特点

1. **角色固定**：PM、Frontend、Backend、QA、Ops
2. **部门动态**：属于哪个业务 Agent
3. **技术实现**：使用具体的技术栈
4. **独立工作**：在自己的领域内工作
5. **协作配合**：与其他 Sub-Agent 协作

---

## 如何创建业务 Agent？

### 方法 1：使用 Amazing CLI（推荐）

```bash
# 初始化项目时，AI 会推荐业务划分
amazing-cli init my-project

# 或者后续添加
amazing-cli agent create monitoring --description "监控告警"
```

### 方法 2：手动创建

1. 在 `.agents/` 目录下创建新目录
2. 创建 `config.json` 配置文件
3. 创建 `prompt.md` 定义 Agent 行为
4. 创建 `sub-agents/` 目录
5. 为每个角色创建 Sub-Agent 配置

**详见**：[业务 Agent 创建指南](./business-agents/create-guide.md)

---

## 最佳实践

### 1. 业务 Agent 的划分原则

**好的划分**：
- ✅ 职责清晰，边界明确
- ✅ 高内聚，低耦合
- ✅ 易于扩展和维护
- ✅ 符合团队结构

**不好的划分**：
- ❌ 职责模糊，边界不清
- ❌ 相互依赖，耦合严重
- ❌ 难以扩展
- ❌ 与团队结构不符

### 2. 团队规模建议

| 业务 Agent 数量 | 团队规模 | 说明 |
|----------------|---------|------|
| 2-3 个 | 5-10 人 | 小型团队 |
| 4-6 个 | 10-20 人 | 中型团队 |
| 7-10 个 | 20-50 人 | 大型团队 |

**原则**：
- 每个业务 Agent 对应一个小团队（2-5 人）
- 团队包含不同角色（PM、开发、测试、运维）
- 团队相对独立，减少沟通成本

### 3. 命名规范

**业务 Agent 命名**：
- 使用业务领域名称
- 简洁明了
- 避免技术术语

**示例**：
- ✅ `compute`（算力）
- ✅ `data`（数据）
- ✅ `training`（训练）
- ❌ `gpu-scheduler`（太技术化）
- ❌ `ml-platform`（太宽泛）

---

## 相关文档

- [固定 Agent 说明](./fixed-agents/README.md)
- [业务 Agent 创建指南](./business-agents/create-guide.md)
- [固定角色说明](./roles/README.md)
- [Sub-Agent 层说明](../03-sub-agents/README.md)
