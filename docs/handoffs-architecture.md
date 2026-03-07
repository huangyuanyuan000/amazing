# Handoffs 初始化流程架构

## 设计目标

1. **避免上下文溢出**: 将大型初始化任务拆分为多个独立阶段
2. **支持断点续传**: 每个阶段完成后保存状态，支持中断恢复
3. **清晰的职责划分**: 每个 handoff agent 专注于特定任务
4. **可观测性**: 实时显示进度和状态
5. **可扩展性**: 易于添加新的初始化阶段

## 流程架构

```
用户输入
   ↓
Orchestrator (编排器)
   ↓
┌─────────────────────────────────────────────────────┐
│ Phase 1: 基础结构初始化 (structure-init)              │
│ - 创建项目目录                                        │
│ - 复制模板文件                                        │
│ - 初始化 Git 仓库                                     │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ Phase 2: 角色配置 (role-config)                       │
│ - 生成角色定义                                        │
│ - 配置 IronClaw 权限                                  │
│ - 生成工作流配置                                      │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ Phase 3: 业务 Agent 生成 (business-agent-gen)         │
│ - 分析产品形态                                        │
│ - 推荐业务模块划分                                    │
│ - 生成 Agent 配置                                     │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ Phase 4: 后端代码生成 (backend-gen)                   │
│ - 生成数据模型                                        │
│ - 生成 API 接口                                       │
│ - 生成业务逻辑                                        │
│ - 生成 AI 交互层                                      │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ Phase 5: 前端代码生成 (frontend-gen)                  │
│ - 生成页面组件                                        │
│ - 生成 AI 对话界面                                    │
│ - 生成传统表单界面                                    │
│ - 生成路由配置                                        │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ Phase 6: 部署配置生成 (deploy-gen)                    │
│ - 生成 Docker 配置                                    │
│ - 生成 K8s 配置                                       │
│ - 生成私有化部署脚本                                  │
└─────────────────────────────────────────────────────┘
   ↓
┌─────────────────────────────────────────────────────┐
│ Phase 7: 文档生成 (docs-gen)                          │
│ - 生成 README                                         │
│ - 生成架构文档                                        │
│ - 生成 API 文档                                       │
│ - 生成部署文档                                        │
└─────────────────────────────────────────────────────┘
   ↓
完成
```

## Orchestrator 设计

### 核心职责

1. **流程编排**: 按顺序执行各个 handoff 阶段
2. **状态管理**: 保存和恢复初始化状态
3. **上下文传递**: 在各阶段间传递必要的上下文信息
4. **错误处理**: 捕获错误并支持重试
5. **进度报告**: 实时显示初始化进度

### 状态文件结构

```json
{
  "project_name": "my-project",
  "project_path": "/path/to/my-project",
  "product_description": "...",
  "current_phase": "backend-gen",
  "completed_phases": ["structure-init", "role-config", "business-agent-gen"],
  "phase_results": {
    "business-agent-gen": {
      "agents": [
        {"name": "model-management", "displayName": "模型管理"},
        {"name": "compute-management", "displayName": "算力管理"}
      ]
    }
  },
  "timestamp": "2026-03-08T10:30:00Z"
}
```

### 接口设计

```python
class Orchestrator:
    def start(self, project_name: str, product_description: str) -> None
    def resume(self, project_name: str) -> None
    def get_status(self) -> Dict
    def execute_phase(self, phase_name: str) -> Dict
```

## Handoff Agent 设计

### Agent 目录结构

```
.agents/init-handoffs/
├── structure-init/
│   ├── agent.json          # Agent 配置
│   ├── prompt.md           # Agent 提示词
│   └── templates/          # 模板文件
├── role-config/
│   ├── agent.json
│   ├── prompt.md
│   └── templates/
├── business-agent-gen/
│   ├── agent.json
│   ├── prompt.md
│   └── templates/
├── backend-gen/
│   ├── agent.json
│   ├── prompt.md
│   └── templates/
├── frontend-gen/
│   ├── agent.json
│   ├── prompt.md
│   └── templates/
├── deploy-gen/
│   ├── agent.json
│   ├── prompt.md
│   └── templates/
└── docs-gen/
    ├── agent.json
    ├── prompt.md
    └── templates/
```

### Agent 配置示例

```json
{
  "name": "backend-gen",
  "displayName": "后端代码生成器",
  "description": "生成完整的后端代码，包括数据模型、API、业务逻辑和 AI 交互层",
  "inputs": [
    "business_agents",
    "tech_stack",
    "database_config"
  ],
  "outputs": [
    "backend_code",
    "api_specs",
    "database_schema"
  ],
  "max_context": 50000
}
```

## 上下文传递机制

### 输入上下文

每个 handoff agent 接收：
- 项目基本信息（名称、路径）
- 产品描述
- 前序阶段的输出结果
- 用户自定义配置

### 输出上下文

每个 handoff agent 输出：
- 生成的文件列表
- 关键配置信息
- 下一阶段需要的数据
- 执行日志

## 断点续传机制

1. 每个阶段完成后保存状态到 `.amazing/init-state.json`
2. 用户可以通过 `--resume` 参数恢复中断的初始化
3. Orchestrator 检查已完成的阶段，从下一阶段继续执行
4. 支持重新执行某个阶段（`--retry-phase=<phase-name>`）

## 进度显示

```
🚀 初始化项目: my-ai-platform

[✓] Phase 1/7: 基础结构初始化 (完成)
[✓] Phase 2/7: 角色配置 (完成)
[✓] Phase 3/7: 业务 Agent 生成 (完成)
[→] Phase 4/7: 后端代码生成 (进行中...)
    ├─ 生成数据模型 (完成)
    ├─ 生成 API 接口 (进行中...)
    └─ 生成业务逻辑 (等待)
[ ] Phase 5/7: 前端代码生成
[ ] Phase 6/7: 部署配置生成
[ ] Phase 7/7: 文档生成

预计剩余时间: 5 分钟
```

## 错误处理

1. **阶段失败**: 保存当前状态，提示用户错误信息
2. **部分失败**: 记录失败的子任务，允许单独重试
3. **依赖缺失**: 检查前序阶段输出，提示缺失的依赖
4. **超时处理**: 单个阶段超时后自动保存状态并退出

## 扩展性设计

### 添加新阶段

1. 在 `.agents/init-handoffs/` 下创建新目录
2. 编写 `agent.json` 配置
3. 编写 `prompt.md` 提示词
4. 在 Orchestrator 中注册新阶段

### 自定义阶段顺序

```json
{
  "phases": [
    "structure-init",
    "role-config",
    "business-agent-gen",
    "custom-phase",  // 自定义阶段
    "backend-gen",
    "frontend-gen",
    "deploy-gen",
    "docs-gen"
  ]
}
```
