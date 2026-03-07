# 业务 Agent 创建指南

## 概述

业务 Agent 是根据产品形态动态创建的，对应业务部门。

本指南介绍如何创建和配置业务 Agent。

---

## 创建方式

### 方式 1：使用 Amazing CLI（推荐）

```bash
# 初始化项目时自动创建
amazing-cli init my-project

# 或后续添加
amazing-cli agent create <agent-name> \
  --description "Agent 描述" \
  --tech-stack "Python + FastAPI"
```

### 方式 2：手动创建

按照以下步骤手动创建业务 Agent。

---

## 创建步骤

### 步骤 1：创建目录结构

```bash
mkdir -p .agents/<agent-name>/{sub-agents,prompts}
```

**示例**：创建算力平台 Agent

```bash
mkdir -p .agents/compute/{sub-agents,prompts}
```

### 步骤 2：创建 Agent 配置

创建 `.agents/<agent-name>/config.json`：

```json
{
  "name": "compute",
  "type": "business",
  "displayName": "算力平台",
  "description": "负责 GPU/CPU 资源的管理、调度和监控",
  "version": "1.0.0",
  "techStack": {
    "backend": {
      "language": "Python",
      "framework": "FastAPI",
      "version": "3.11+"
    },
    "database": {
      "type": "PostgreSQL",
      "version": "15+"
    },
    "cache": {
      "type": "Redis",
      "version": "7+"
    },
    "queue": {
      "type": "RabbitMQ",
      "version": "3.12+"
    }
  },
  "services": [
    {
      "name": "resource",
      "description": "资源管理服务",
      "api": "/api/v1/compute/resources"
    },
    {
      "name": "scheduler",
      "description": "资源调度服务",
      "api": "/api/v1/compute/scheduler"
    },
    {
      "name": "monitor",
      "description": "资源监控服务",
      "api": "/api/v1/compute/monitor"
    }
  ],
  "dependencies": {
    "common": ["user", "permission", "audit"],
    "review": ["code_review", "security_scan"]
  },
  "subAgents": [
    "pm",
    "frontend",
    "backend",
    "qa",
    "ops"
  ]
}
```

### 步骤 3：创建 Sub-Agent 配置

为每个角色创建 Sub-Agent 配置。

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
    "实现资源管理 API",
    "实现资源调度逻辑",
    "实现监控数据采集",
    "设计数据库表结构",
    "编写单元测试"
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
      "description": "提供 API 接口"
    },
    {
      "with": "qa",
      "interface": "测试环境",
      "description": "提供测试环境"
    }
  ]
}
```

**frontend.json**：

```json
{
  "role": "frontend",
  "agent": "compute",
  "displayName": "算力平台前端开发",
  "description": "负责算力平台的前端 UI 开发",
  "techStack": {
    "framework": "React",
    "language": "TypeScript",
    "ui": "Ant Design",
    "stateManagement": "Zustand"
  },
  "responsibilities": [
    "实现资源列表页面",
    "实现资源详情页面",
    "实现监控大屏",
    "实现资源调度界面",
    "编写组件测试"
  ],
  "outputs": [
    "前端代码",
    "UI 组件",
    "页面文档",
    "组件测试"
  ],
  "collaborations": [
    {
      "with": "backend",
      "interface": "REST API",
      "description": "调用后端 API"
    },
    {
      "with": "pm",
      "interface": "原型设计",
      "description": "根据原型开发"
    }
  ]
}
```

类似地创建 `pm.json`、`qa.json`、`ops.json`。

### 步骤 4：创建 Agent Prompt

创建 `.agents/<agent-name>/prompt.md`：

```markdown
# 算力平台 Agent Prompt

## 角色定位

你是算力平台 Agent，负责 GPU/CPU 资源的管理、调度和监控。

## 核心职责

1. **资源管理**
   - 管理 GPU/CPU 资源池
   - 资源的增删改查
   - 资源状态管理

2. **资源调度**
   - 根据需求分配资源
   - 资源调度算法
   - 资源回收和释放

3. **资源监控**
   - 实时监控资源使用情况
   - 资源告警
   - 资源使用统计

## 技术栈

- 后端：Python + FastAPI
- 数据库：PostgreSQL
- 缓存：Redis
- 队列：RabbitMQ

## API 设计原则

1. RESTful 风格
2. 统一的响应格式
3. 完整的错误处理
4. API 版本控制

## 数据库设计原则

1. 合理的表结构设计
2. 适当的索引
3. 外键约束
4. 数据完整性

## 代码规范

1. 遵循 PEP 8
2. 类型注解
3. 文档字符串
4. 单元测试覆盖率 > 80%

## 协作方式

- 与 Common Agent 集成用户和权限
- 与 Review Agent 集成代码审查
- 与其他业务 Agent 通过 API 通信
```

### 步骤 5：创建目录结构

创建代码目录：

```bash
mkdir -p backend/<agent-name>/{app/{api,models,services,utils},tests}
mkdir -p frontend/src/pages/<agent-name>
```

### 步骤 6：更新项目配置

更新 `amazing.config.json`：

```json
{
  "agents": {
    "business": [
      {
        "name": "compute",
        "displayName": "算力平台",
        "description": "GPU/CPU 资源管理",
        "techStack": {
          "backend": "Python + FastAPI",
          "database": "PostgreSQL"
        }
      }
    ]
  }
}
```

---

## 配置模板

### 最小配置

```json
{
  "name": "agent-name",
  "type": "business",
  "displayName": "Agent 显示名称",
  "description": "Agent 描述",
  "techStack": {
    "backend": "Python + FastAPI",
    "database": "PostgreSQL"
  },
  "subAgents": ["pm", "frontend", "backend", "qa", "ops"]
}
```

### 完整配置

```json
{
  "name": "agent-name",
  "type": "business",
  "displayName": "Agent 显示名称",
  "description": "Agent 详细描述",
  "version": "1.0.0",
  "techStack": {
    "backend": {
      "language": "Python",
      "framework": "FastAPI",
      "version": "3.11+"
    },
    "frontend": {
      "framework": "React",
      "language": "TypeScript"
    },
    "database": {
      "type": "PostgreSQL",
      "version": "15+"
    },
    "cache": {
      "type": "Redis",
      "version": "7+"
    }
  },
  "services": [
    {
      "name": "service-name",
      "description": "服务描述",
      "api": "/api/v1/agent/service"
    }
  ],
  "dependencies": {
    "common": ["user", "permission"],
    "review": ["code_review"]
  },
  "subAgents": ["pm", "frontend", "backend", "qa", "ops"],
  "metadata": {
    "owner": "team-name",
    "created": "2025-03-15",
    "updated": "2025-03-15"
  }
}
```

---

## 最佳实践

### 1. 命名规范

**Agent 名称**：
- 使用小写字母
- 使用连字符分隔
- 简洁明了

```
✅ compute
✅ data-management
✅ model-service

❌ ComputeAgent
❌ data_management
❌ ms
```

### 2. 职责单一

每个 Agent 只负责一个业务领域：

```
✅ compute Agent - 只负责算力管理
✅ data Agent - 只负责数据管理

❌ resource Agent - 既管理算力又管理数据
```

### 3. 依赖最小化

尽量减少 Agent 之间的依赖：

```
✅ 通过 API 通信
✅ 异步消息队列

❌ 直接访问其他 Agent 的数据库
❌ 紧密耦合
```

### 4. 文档完善

每个 Agent 都应该有：
- ✅ config.json（配置）
- ✅ prompt.md（Prompt）
- ✅ README.md（说明文档）
- ✅ API 文档

---

## 常见问题

### Q1: Agent 之间如何通信？

**答**：通过 REST API 或消息队列。

```python
# Agent A 调用 Agent B 的 API
import httpx

response = httpx.get("http://agent-b/api/v1/resource")
data = response.json()
```

### Q2: 如何处理 Agent 之间的数据共享？

**答**：通过 API 获取，不要直接访问数据库。

```
✅ Agent A 调用 Agent B 的 API 获取数据
❌ Agent A 直接查询 Agent B 的数据库
```

### Q3: Agent 可以删除吗？

**答**：可以，但要注意依赖关系。

```bash
# 删除 Agent
amazing-cli agent delete <agent-name>

# 会检查是否有其他 Agent 依赖
```

### Q4: 如何修改 Agent 配置？

**答**：编辑配置文件或使用 CLI。

```bash
# 使用 CLI
amazing-cli agent edit <agent-name>

# 或直接编辑
vim .agents/<agent-name>/config.json
```

---

## 示例

完整的示例请参考：
- [大模型管理平台](../../06-examples/model-platform/init.md)
- [算力平台 Agent 配置](../../06-examples/model-platform/agents/compute.md)

---

## 相关文档

- [Agent-Teams 层说明](../README.md)
- [固定 Agent 说明](../fixed-agents/README.md)
- [Sub-Agent 层说明](../../03-sub-agents/README.md)
- [技术选型层说明](../../04-tech-stack/README.md)
