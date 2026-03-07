# Bug 修复工作流

## 概述

Bug 修复流程强调快速响应和风险控制，支持快速修复和回滚机制。

## 参与角色

- 👑 架构师 (Architect)
- 🧪 测试工程师 (QA)
- ⚙️ 后端开发 (Backend)
- 🚀 运维工程师 (Ops)

## 完整流程

### 步骤 1：Bug 报告 (QA/User)

**负责人**: 测试工程师或用户

**工作内容**:
- 发现问题
- 记录现象
- 提供复现步骤
- 评估影响范围

**CLI 命令**:
```bash
# 创建 Bug 报告
python3 scripts/amazing-cli.py bug create \
  --title "用户登录失败" \
  --description "输入错误密码时未显示错误提示" \
  --severity high
```

### 步骤 2：Bug 复现 (QA)

**负责人**: 测试工程师

**工作内容**:
- 复现 Bug
- 确认问题
- 分析日志
- 定位模块

**CLI 命令**:
```bash
# 使用 Claude Code 复现
claude-code "复现用户登录失败问题"
```

### 步骤 3：架构师评估 (Architect)

**负责人**: 架构师

**工作内容**:
- 评估影响范围
- 判断严重程度
- 决定修复策略
- 选择 AI 模式

**决策**:
- **Critical**: 立即回滚 + 紧急修复
- **High**: 快速修复 + 灰度发布
- **Medium**: 正常修复流程
- **Low**: 计划修复

**CLI 命令**:
```bash
# 评估 Bug
python3 scripts/architect_cli.py bug evaluate BUG-001

# 决定修复策略
python3 scripts/mode_cli.py mode set semi-auto \
  -r BUG-001 \
  --reason "高风险 Bug，需要人工把关"
```

### 步骤 4：问题定位 (Backend)

**负责人**: 后端开发

**工作内容**:
- 分析日志
- 定位代码
- 找出根因
- 设计修复方案

**CLI 命令**:
```bash
# 使用 Claude Code 定位问题
claude-code "分析登录失败日志，定位问题原因"
```

### 步骤 5：架构师审查方案 (Architect)

**负责人**: 架构师

**工作内容**:
- 审查修复方案
- 评估风险
- 批准或调整
- 确定修复策略

**CLI 命令**:
```bash
# 审查修复方案
python3 scripts/architect_cli.py review start BUG-001-fix

# 批准方案
python3 scripts/architect_cli.py review approve BUG-001-fix
```

### 步骤 6：代码修复 (Backend)

**负责人**: 后端开发

**工作内容**:
- 修改代码
- 本地测试
- 提交代码
- 等待审查

**CLI 命令**:
```bash
# 使用 Claude Code 修复
claude-code "修复登录失败问题"

# 提交代码
git add .
git commit -m "fix: 修复登录失败问题"
git push
```

### 步骤 7：回归测试 (QA)

**负责人**: 测试工程师

**工作内容**:
- 验证修复
- 回归测试
- 确认关闭
- 更新状态

**CLI 命令**:
```bash
# 运行回归测试
pytest tests/test_login.py

# 验证修复
python3 scripts/amazing-cli.py bug verify BUG-001
```

### 步骤 8：热修复部署 (Ops)

**负责人**: 运维工程师

**工作内容**:
- 灰度发布
- 监控指标
- 观察日志
- 全量发布或回滚

**CLI 命令**:
```bash
# 灰度发布
make deploy-canary

# 监控
kubectl logs -f deployment/python-api -n amazing

# 全量发布
make deploy-production

# 如果有问题，立即回滚
kubectl rollout undo deployment/python-api -n amazing
```

## 回滚机制

### 何时回滚？

- **Critical Bug**: 系统崩溃、数据丢失
- **High Bug**: 核心功能不可用
- **修复失败**: 修复后问题依然存在
- **新问题**: 修复引入新的问题

### 回滚流程

```
1. 发现问题
   ↓
2. 立即决策回滚
   ├── 架构师批准
   └── 通知相关人员
   ↓
3. 执行回滚
   ├── K8s: kubectl rollout undo
   ├── Docker: docker-compose down && up
   └── 本地: git revert
   ↓
4. 验证回滚
   ├── 检查服务状态
   ├── 验证功能正常
   └── 确认问题解决
   ↓
5. 分析原因
   ├── 找出回滚原因
   ├── 制定新方案
   └── 重新修复
```

**CLI 命令**:
```bash
# K8s 回滚
kubectl rollout undo deployment/python-api -n amazing

# Docker 回滚
docker-compose down
docker-compose up -d

# Git 回滚
git revert HEAD
git push
```

## AI 模式选择

### 全自动模式

适用于简单 Bug、影响范围小：

```bash
python3 scripts/mode_cli.py mode set full-auto \
  -r BUG-001 \
  --reason "简单 Bug，影响范围小"
```

### 半自动模式

适用于复杂 Bug、影响范围大：

```bash
python3 scripts/mode_cli.py mode set semi-auto \
  -r BUG-002 \
  --reason "核心功能 Bug，需要人工把关"
```

## 时间估算

| Bug 严重程度 | 全自动模式 | 半自动模式 |
|-------------|-----------|-----------|
| Critical | 1小时 | 2小时 |
| High | 2小时 | 4小时 |
| Medium | 4小时 | 8小时 |
| Low | 1天 | 2天 |

## 最佳实践

1. **快速响应**：Critical/High Bug 立即处理
2. **充分测试**：修复后必须回归测试
3. **灰度发布**：先小流量验证
4. **准备回滚**：随时准备回滚
5. **根因分析**：找出根本原因，避免再次发生
6. **文档记录**：记录 Bug 和修复过程

## 相关文档

- [功能开发流程](feature-development.md)
- [架构师工作流](https://z58362026.github.io/amazing/workflows/architect-workflow.html)
- [模式切换流程](https://z58362026.github.io/amazing/workflows/mode-switch.html)
