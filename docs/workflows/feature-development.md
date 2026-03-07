# 功能开发工作流

## 概述

功能开发是最常见的开发场景，涉及从需求分析到上线部署的完整流程。

## 参与角色

- 👑 架构师 (Architect)
- 📋 产品经理 (PM)
- 🎨 前端开发 (Frontend)
- ⚙️ 后端开发 (Backend)
- 🧪 测试工程师 (QA)
- 🚀 运维工程师 (Ops)

## 完整流程

### 步骤 1：需求分析 (PM)

**负责人**: 产品经理

**工作内容**:
- 收集用户需求
- 分析业务价值
- 评估技术可行性
- 确定优先级

**输出物**:
- 需求文档
- 用户故事
- 验收标准

### 步骤 2：PRD 生成 (PM)

**负责人**: 产品经理

**工作内容**:
- 编写产品需求文档
- 定义功能范围
- 设计交互流程
- 制定验收标准

**CLI 命令**:
```bash
# 创建 PRD
python3 scripts/amazing-cli.py prd create "用户权限管理"

# 使用 Claude Code 生成 PRD
claude-code "生成用户权限管理 PRD"
```

**输出物**:
- PRD 文档 (docs/prd/xxx.md)

### 步骤 3：架构师决策 (Architect)

**负责人**: 架构师

**工作内容**:
- 评估技术方案
- 选择技术栈
- 设计系统架构
- 定义接口规范
- 决定 AI 模式

**CLI 命令**:
```bash
# 切换到架构师角色
python3 scripts/amazing-cli.py role set architect

# 创建架构文档
python3 scripts/architect_cli.py arch create "用户权限管理"

# 定义技术方案
python3 scripts/architect_cli.py arch solution "用户权限管理" \
  --choice "RBAC" \
  --reason "实现简单，满足需求"

# 设置 AI 模式
python3 scripts/mode_cli.py mode set full-auto \
  -r REQ-001 \
  --reason "成熟功能，风险可控"
```

**输出物**:
- 架构设计文档
- 技术方案文档
- API 接口设计
- 数据库设计

### 步骤 4：并行开发

#### 4.1 前端开发 (Frontend)

**负责人**: 前端开发

**工作内容**:
- UI 组件开发
- 状态管理
- API 集成
- 单元测试

**CLI 命令**:
```bash
# 切换到前端角色
python3 scripts/amazing-cli.py role set frontend

# 使用 Claude Code 开发
claude-code "创建用户列表组件"
```

#### 4.2 后端开发 (Backend)

**负责人**: 后端开发

**工作内容**:
- API 接口开发
- 业务逻辑实现
- 数据库操作
- 单元测试

**CLI 命令**:
```bash
# 切换到后端角色
python3 scripts/amazing-cli.py role set backend

# 使用 Claude Code 开发
claude-code "实现用户 CRUD API"
```

### 步骤 5：架构师审查 (Architect)

**负责人**: 架构师

**工作内容**:
- 代码审查
- 架构一致性检查
- 安全审查
- 性能评估

**CLI 命令**:
```bash
# 查看待审查任务
python3 scripts/architect_cli.py review pending

# 审查代码
python3 scripts/architect_cli.py review start task-001

# 批准或拒绝
python3 scripts/architect_cli.py review approve task-001
```

### 步骤 6：集成测试 (QA)

**负责人**: 测试工程师

**工作内容**:
- 功能测试
- 集成测试
- E2E 测试
- Bug 报告

**CLI 命令**:
```bash
# 切换到 QA 角色
python3 scripts/amazing-cli.py role set qa

# 运行测试
pytest
npm run test:e2e
```

### 步骤 7：架构师验收 (Architect)

**负责人**: 架构师

**工作内容**:
- 功能验收
- 性能测试
- 安全测试
- 批准上线

**CLI 命令**:
```bash
# 运行验收测试
python3 scripts/amazing-cli.py test acceptance --task prd-001

# 批准上线
python3 scripts/amazing-cli.py approve prd-001
```

### 步骤 8：部署上线 (Ops)

**负责人**: 运维工程师

**工作内容**:
- 部署到生产环境
- 配置监控告警
- 观察运行状态
- 处理异常

**CLI 命令**:
```bash
# 切换到 Ops 角色
python3 scripts/amazing-cli.py role set ops

# 部署到生产
make deploy-k8s

# 查看状态
kubectl get pods -n amazing
```

## AI 模式选择

### 全自动模式

适用于成熟功能、低风险任务：

```bash
python3 scripts/mode_cli.py mode set full-auto \
  -r REQ-001 \
  --reason "成熟功能，团队熟悉"
```

**特点**:
- AI 自主完成开发
- 关键节点架构师审查
- 异常时人工介入

### 半自动模式

适用于新项目、高风险任务：

```bash
python3 scripts/mode_cli.py mode set semi-auto \
  -r REQ-002 \
  --reason "新项目，需要把关"
```

**特点**:
- AI 生成方案供选择
- 架构师决策和审查
- 关键步骤人工批准

## 时间估算

| 阶段 | 全自动模式 | 半自动模式 |
|------|-----------|-----------|
| 需求分析 | 0.5天 | 0.5天 |
| PRD 生成 | 0.5天 | 0.5天 |
| 架构设计 | 0.5天 | 1天 |
| 并行开发 | 1天 | 2天 |
| 代码审查 | 0.5天 | 1天 |
| 测试 | 0.5天 | 1天 |
| 部署 | 0.5天 | 0.5天 |
| **总计** | **4天** | **6.5天** |

## 最佳实践

1. **需求明确**：开始开发前确保需求清晰
2. **架构先行**：先设计架构再开发
3. **并行开发**：前后端并行提高效率
4. **及时沟通**：遇到问题及时沟通
5. **代码审查**：确保代码质量
6. **充分测试**：上线前充分测试
7. **灰度发布**：先小流量验证

## 相关文档

- [架构师工作流](https://z58362026.github.io/amazing/workflows/architect-workflow.html)
- [模式切换流程](https://z58362026.github.io/amazing/workflows/mode-switch.html)
- [Bug 修复流程](bug-fix.md)
