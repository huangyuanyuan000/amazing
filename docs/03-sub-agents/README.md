# Sub-Agent 层说明

## 概述

Sub-Agent 是**角色在具体业务部门的实现**。

每个业务 Agent（业务部门）都包含多个 Sub-Agent，对应不同的角色。

---

## 什么是 Sub-Agent？

### 定义

```
Sub-Agent = 角色 + 业务部门 + 技术实现
```

**示例**：

```
算力平台 Agent 的 Backend Sub-Agent

角色：后端开发（Backend）
部门：算力平台（Compute Agent）
技术实现：Python + FastAPI

职责：
├── 实现算力管理 API
├── 设计数据库表结构
├── 编写业务逻辑
└── 编写单元测试
```

### 与 Agent 的关系

```
业务 Agent（业务部门）
├── PM Sub-Agent（产品经理）
├── Frontend Sub-Agent（前端开发）
├── Backend Sub-Agent（后端开发）
├── QA Sub-Agent（测试工程师）
└── Ops Sub-Agent（运维工程师）
```

**类比**：
- **Agent** = 公司的一个业务部门（如销售部）
- **Sub-Agent** = 部门里的某个角色（如销售部的产品经理）

---

## Sub-Agent 的特点

### 1. 角色固定

Sub-Agent 的角色是固定的：
- PM Sub-Agent
- Frontend Sub-Agent
- Backend Sub-Agent
- QA Sub-Agent
- Ops Sub-Agent

### 2. 部门动态

Sub-Agent 属于哪个业务部门是动态的：
- 算力平台的 Backend Sub-Agent
- 数据管理的 Backend Sub-Agent
- 训练管理的 Backend Sub-Agent

### 3. 技术实现

每个 Sub-Agent 使用具体的技术栈：
- 算力平台的 Backend：Python + FastAPI
- 模型服务的 Backend：Go + Gin

### 4. 独立工作

每个 Sub-Agent 在自己的领域内独立工作：
- Frontend Sub-Agent 负责 UI 开发
- Backend Sub-Agent 负责 API 开发
- 互不干扰

### 5. 协作配合

Sub-Agent 之间需要协作：
- Frontend 和 Backend 对接 API
- Backend 和 QA 对接测试
- QA 和 Ops 对接部署

---

## Sub-Agent 配置

### 配置文件结构

```
.agents/
└── compute/                    # 业务 Agent
    ├── config.json            # Agent 配置
    ├── prompt.md              # Agent Prompt
    └── sub-agents/            # Sub-Agent 配置
        ├── pm.json            # PM Sub-Agent
        ├── frontend.json      # Frontend Sub-Agent
        ├── backend.json       # Backend Sub-Agent
        ├── qa.json            # QA Sub-Agent
        └── ops.json           # Ops Sub-Agent
```

### Sub-Agent 配置示例

**backend.json**：

```json
{
  "role": "backend",
  "agent": "compute",
  "displayName": "算力平台后端开发",
  "description": "负责算力平台的后端 API 开发",
  "techStack": {
    "language": "Python",
    "framework": "FastAPI",
    "database": "PostgreSQL",
    "cache": "Redis",
    "queue": "RabbitMQ"
  },
  "responsibilities": [
    "实现算力管理 API",
    "设计数据库表结构",
    "编写业务逻辑",
    "编写单元测试",
    "编写 API 文档"
  ],
  "outputs": [
    "API 代码",
    "数据库设计",
    "API 文档",
    "单元测试"
  ],
  "collaborations": [
    {
      "with": "frontend",
      "interface": "REST API",
      "description": "提供 API 接口给前端调用"
    },
    {
      "with": "qa",
      "interface": "测试环境",
      "description": "提供测试环境和测试数据"
    }
  ]
}
```

---

## Sub-Agent 工作流程

### 1. 接收任务

```
PM Sub-Agent 创建需求
    ↓
架构师决策（选择 AI 模式）
    ↓
Backend Sub-Agent 接收任务
```

### 2. 执行任务

**全自动模式**：
```
Backend Sub-Agent
├── AI 分析需求
├── AI 设计 API
├── AI 生成代码
├── AI 编写测试
└── 提交审查
```

**半自动模式**：
```
Backend Sub-Agent
├── AI 生成多种方案
├── 架构师选择方案
├── AI 生成代码草稿
├── 架构师审查代码
└── 架构师批准
```

### 3. 协作对接

```
Backend Sub-Agent 完成 API
    ↓
Frontend Sub-Agent 对接 API
    ↓
QA Sub-Agent 测试功能
    ↓
Ops Sub-Agent 部署上线
```

---

## Sub-Agent 编排

### 串行编排

任务按顺序执行：

```
PM Sub-Agent（需求分析）
    ↓
Backend Sub-Agent（API 开发）
    ↓
Frontend Sub-Agent（UI 开发）
    ↓
QA Sub-Agent（测试）
    ↓
Ops Sub-Agent（部署）
```

**适用场景**：
- 任务有明确的依赖关系
- 后续任务依赖前面的输出

### 并行编排

任务同时执行：

```
PM Sub-Agent（需求分析）
    ↓
┌───────────────┬───────────────┐
Frontend        Backend         Database
Sub-Agent       Sub-Agent       Design
    └───────────────┴───────────────┘
                ↓
        QA Sub-Agent（测试）
                ↓
        Ops Sub-Agent（部署）
```

**适用场景**：
- 任务相对独立
- 可以并行开发提高效率

### 混合编排

串行和并行结合：

```
PM Sub-Agent（需求分析）
    ↓
架构师决策（技术方案）
    ↓
┌───────────────┬───────────────┐
Frontend        Backend
Sub-Agent       Sub-Agent
    └───────────────┴───────────────┘
                ↓
        架构师审查（代码审查）
                ↓
        QA Sub-Agent（测试）
                ↓
        架构师验收（质量验收）
                ↓
        Ops Sub-Agent（部署）
```

**适用场景**：
- 大部分实际项目
- 既有并行又有串行

---

## Sub-Agent 通信

### 1. API 接口

Frontend 和 Backend 通过 API 通信：

```
Frontend Sub-Agent
    ↓ HTTP Request
Backend Sub-Agent
    ↓ HTTP Response
Frontend Sub-Agent
```

### 2. 文档共享

通过文档传递信息：

```
PM Sub-Agent
    ↓ PRD 文档
Backend Sub-Agent
    ↓ API 文档
Frontend Sub-Agent
```

### 3. 代码仓库

通过 Git 协作：

```
Backend Sub-Agent
    ↓ git push
Code Repository
    ↓ git pull
Frontend Sub-Agent
```

### 4. 消息队列

通过消息队列异步通信：

```
Backend Sub-Agent
    ↓ 发送消息
Message Queue
    ↓ 接收消息
QA Sub-Agent
```

---

## 最佳实践

### 1. 明确职责边界

**好的划分**：
- ✅ Frontend 负责 UI，Backend 负责 API
- ✅ Backend 负责业务逻辑，Database 负责数据存储
- ✅ QA 负责测试，Ops 负责部署

**不好的划分**：
- ❌ Frontend 直接操作数据库
- ❌ Backend 包含 UI 逻辑
- ❌ 职责重叠，边界不清

### 2. 定义清晰的接口

**API 接口**：
- 使用 OpenAPI 规范
- 明确请求和响应格式
- 提供完整的 API 文档

**数据接口**：
- 定义数据模型
- 明确数据格式
- 提供数据字典

### 3. 保持独立性

**原则**：
- 每个 Sub-Agent 应该能独立开发
- 减少相互依赖
- 通过接口通信

**好处**：
- 并行开发
- 易于测试
- 易于维护

### 4. 统一技术栈

**建议**：
- 同一业务 Agent 的 Sub-Agent 使用相同技术栈
- 统一的代码规范
- 统一的开发工具

**好处**：
- 降低学习成本
- 便于人员流动
- 易于维护

---

## 示例：算力平台 Agent

### 组织结构

```
算力平台 Agent（业务部门）
├── PM Sub-Agent（产品经理）
│   ├── 职责：需求分析、PRD 编写
│   └── 输出：PRD 文档、原型设计
│
├── Frontend Sub-Agent（前端开发）
│   ├── 技术栈：React + TypeScript
│   ├── 职责：UI 开发、组件开发
│   └── 输出：前端代码、UI 组件
│
├── Backend Sub-Agent（后端开发）
│   ├── 技术栈：Python + FastAPI
│   ├── 职责：API 开发、业务逻辑
│   └── 输出：API 代码、数据库设计
│
├── QA Sub-Agent（测试工程师）
│   ├── 技术栈：Pytest + Playwright
│   ├── 职责：测试设计、自动化测试
│   └── 输出：测试用例、测试报告
│
└── Ops Sub-Agent（运维工程师）
    ├── 技术栈：Docker + Kubernetes
    ├── 职责：部署、监控
    └── 输出：部署配置、监控配置
```

### 工作流程

```
1. PM Sub-Agent 创建需求
   ├── 分析用户需求
   ├── 编写 PRD
   └── 设计原型

2. 架构师决策
   ├── 评估技术方案
   ├── 选择 AI 模式
   └── 批准开始开发

3. Frontend + Backend 并行开发
   ├── Frontend：开发 UI 界面
   ├── Backend：开发 API 接口
   └── 通过 API 文档对接

4. 架构师审查
   ├── 审查前端代码
   ├── 审查后端代码
   └── 批准进入测试

5. QA Sub-Agent 测试
   ├── 编写测试用例
   ├── 执行自动化测试
   └── 提交测试报告

6. 架构师验收
   ├── 验收功能
   ├── 验收质量
   └── 批准上线

7. Ops Sub-Agent 部署
   ├── 部署到测试环境
   ├── 部署到生产环境
   └── 配置监控告警
```

---

## 相关文档

- [Agent-Teams 层说明](../02-agent-teams/README.md)
- [技术选型层说明](../04-tech-stack/README.md)
- [工作流程说明](../05-workflows/development.md)
