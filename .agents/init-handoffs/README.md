# 初始化 Handoff Agents

这个目录包含了项目初始化流程中的所有 handoff agents，每个 agent 负责初始化的一个特定阶段。

## Agent 列表

| Agent | 职责 | 输入 | 输出 |
|-------|------|------|------|
| structure-init | 创建项目目录结构 | project_name, project_path | 目录结构 |
| role-config | 生成角色和权限配置 | project_path | 角色配置、工作流 |
| business-agent-gen | 分析业务并生成 Agent | product_description | 业务模块、技术栈 |
| backend-gen | 生成后端代码骨架 | business_agents, tech_stack | 后端代码 |
| frontend-gen | 生成前端代码骨架 | business_agents, api_endpoints | 前端代码 |
| deploy-gen | 生成部署配置 | tech_stack, deployment_targets | 部署配置 |
| docs-gen | 生成项目文档 | 所有上下文 | 文档 |

## 执行流程

```
1. structure-init
   ↓
2. role-config
   ↓
3. business-agent-gen
   ↓
4. backend-gen + frontend-gen (并行)
   ↓
5. deploy-gen
   ↓
6. docs-gen
```

## 使用方式

通过 orchestrator 自动编排执行：

```bash
python3 scripts/orchestrator.py \
  --project-name my-business \
  --product-desc "电商平台" \
  --phases all
```

或单独执行某个阶段：

```bash
python3 scripts/orchestrator.py \
  --project-name my-business \
  --phases structure-init,role-config
```

## Agent 配置

每个 agent 包含：
- `agent.json`: Agent 元数据配置
- `prompt.md`: Agent 的详细提示词
- `README.md`: Agent 使用说明（可选）

## 扩展

添加新的初始化阶段：
1. 在此目录下创建新的 agent 目录
2. 添加 `agent.json` 和 `prompt.md`
3. 在 `orchestrator.py` 中注册新阶段
