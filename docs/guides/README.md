# 角色指南

## 概述

Amazing 平台支持多角色协同开发，每个角色都有专属的工具、权限和工作流程。

## 角色列表

### 1. [产品经理 (PM)](./pm.md)

**职责**:
- 需求分析
- PRD 编写
- 原型设计
- 功能验收

**工具**: Claude Code, Codex

**Skills**: prd-generator, requirement-analyzer

---

### 2. [前端开发 (Frontend)](./frontend.md)

**职责**:
- UI/UX 实现
- 组件开发
- 状态管理
- 性能优化

**技术栈**: React, TypeScript, Vite, TailwindCSS

**Skills**: react-component, ui-design, state-management

---

### 3. [后端开发 (Backend)](./backend.md)

**职责**:
- API 开发
- 数据库设计
- 业务逻辑
- 性能优化

**技术栈**: Python (FastAPI), Go (Gin)

**Skills**: api-design, database-design, auth-implement

---

### 4. [测试工程师 (QA)](./qa.md)

**职责**:
- 测试用例设计
- 自动化测试
- Bug 追踪
- 质量报告

**技术栈**: Pytest, Jest, Playwright

**Skills**: test-design, automation, bug-tracking

---

### 5. [运维工程师 (Ops)](./ops.md)

**职责**:
- 部署
- 监控
- 故障排查
- 性能调优

**技术栈**: Docker, Kubernetes, Prometheus, Grafana

**Skills**: deployment, monitoring, troubleshooting

---

### 6. [运营人员 (Operation)](./operation.md)

**职责**:
- 数据分析
- 用户运营
- 配置管理

**技术栈**: SQL, Python, Jupyter

**Skills**: data-analysis, user-operation

---

## 快速开始

### 1. 选择角色

```bash
# 使用 CLI
amazing role select

# 或直接指定
amazing role set pm
```

### 2. 查看权限

```bash
amazing role permissions
```

### 3. 开始工作

```bash
# 查看任务
amazing tasks

# 认领任务
amazing task claim <task-id>

# 完成任务
amazing task complete <task-id>
```

## 协作流程

### 功能开发流程

```
PM (需求分析)
  → PM (PRD 生成)
  → Frontend + Backend (并行开发)
  → QA (测试)
  → Review Agent (审查)
  → Ops (部署)
```

### Bug 修复流程

```
QA (Bug 复现)
  → Backend (问题定位)
  → Backend (代码修复)
  → QA (回归测试)
  → Ops (热修复部署)
```

## 工具链

### Claude Code (主力)

```bash
# 使用 Claude Code
claude-code "你的任务描述"
```

### Codex CLI (备选)

```bash
# 使用 Codex CLI
codex "你的任务描述"
```

### Codex Desktop (可视化)

打开 Codex Desktop，选择角色，进行可视化操作。

## 权限矩阵

| 角色 | PRD | 开发 | 测试 | 部署 | 监控 |
|------|-----|------|------|------|------|
| PM | ✅ | ❌ | ❌ | ❌ | ❌ |
| Frontend | ❌ | ✅ | ✅ | ✅ | ❌ |
| Backend | ❌ | ✅ | ✅ | ✅ | ❌ |
| QA | ❌ | ❌ | ✅ | ❌ | ❌ |
| Ops | ❌ | ❌ | ❌ | ✅ | ✅ |
| Operation | ❌ | ❌ | ❌ | ❌ | ✅ |

## 常见问题

**Q: 如何切换角色?**
A: 使用 `amazing role select` 命令。

**Q: 如何查看我的权限?**
A: 使用 `amazing role permissions` 命令。

**Q: 如何协作开发?**
A: 使用 `amazing tasks` 查看任务，使用 `amazing task claim` 认领任务。

**Q: 如何使用 AI 工具?**
A: 优先使用 Claude Code，降级使用 Codex CLI 或 Codex Desktop。
