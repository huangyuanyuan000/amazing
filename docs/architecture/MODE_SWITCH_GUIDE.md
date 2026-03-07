# Amazing AI 模式切换机制详解

> 本文是《Amazing：基于 Agent-Teams 的 AI 协同开发平台》的补充章节，详细介绍 AI 模式切换机制

## 一、为什么需要模式切换？

在实际的软件开发中，不同的需求有不同的特点：

- **成熟功能**：技术栈熟悉、风险可控 → 适合全自动
- **新项目**：技术不确定、风险较高 → 适合半自动
- **Bug 修复**：影响范围小、快速修复 → 适合全自动
- **架构设计**：影响深远、需要慎重 → 适合半自动

Amazing 平台提供了**按需求维度的模式切换机制**，让架构师可以根据具体情况灵活选择。

---

## 二、两种 AI 模式

### 2.1 全自动模式 (Full-Auto)

**核心理念**：AI 是执行者，人类是监督者

```
需求输入 → AI 分析 → AI 设计 → AI 开发 → AI 测试 → AI 部署
                ↑                ↑                ↑
            关键节点检查      异常时暂停      人工可介入
```

**特点**：
- ✅ AI 自主决策和执行
- ✅ 自动推进工作流
- ✅ 关键节点设置检查点
- ✅ 异常时暂停等待人工
- ✅ 人工可随时接管

**适用场景**：
- 成熟的业务流程
- 低风险的功能开发
- Bug 修复
- 代码重构
- 性能优化

### 2.2 半自动模式 (Semi-Auto)

**核心理念**：AI 是辅助者，人类是决策者

```
需求输入 → AI 生成方案 → 人工选择 → AI 生成代码 → 人工审查 → 人工批准 → AI 执行
            (3-5种)        (决策)      (草稿)        (审查)      (批准)    (执行)
```

**特点**：
- ✅ AI 生成方案和建议
- ✅ 人工审核和决策
- ✅ 人工可提供建议和想法
- ✅ AI 根据反馈优化方案
- ✅ 关键决策点必须人工确认

**适用场景**：
- 新项目启动
- 架构设计
- 技术选型
- 安全相关变更
- 生产环境部署

---

## 三、权限控制：只有架构师可以切换

### 3.1 为什么只有架构师？

1. **技术决策权**：架构师负责整体技术方案，有权决定自动化程度
2. **风险评估能力**：架构师能够评估不同模式的风险和收益
3. **全局视角**：架构师了解项目整体情况，能做出最优决策
4. **责任明确**：模式切换影响重大，需要明确责任人

### 3.2 权限验证流程

```python
def check_architect_permission():
    """检查是否有架构师权限"""
    # 读取用户配置
    user_data = json.load(open(".claude/user.json"))
    current_role = user_data.get("role", "")

    # 验证角色
    if current_role != "architect":
        return False, f"权限不足：只有架构师可以切换模式（当前角色: {current_role}）"

    return True, "权限验证通过"
```

### 3.3 权限拒绝示例

```bash
$ python3 scripts/mode_cli.py mode set full-auto

❌ 权限不足：只有架构师可以切换模式（当前角色: frontend）

💡 提示: 请先切换到架构师角色
   python3 scripts/amazing-cli.py role set architect
```

---

## 四、完整切换流程

### 步骤 1：切换到架构师角色

```bash
$ python3 scripts/amazing-cli.py role set architect

✅ 已选择角色: 架构师
```

### 步骤 2：评估需求

架构师评估需求的以下维度：

| 评估维度 | 选项 | 说明 |
|---------|------|------|
| 技术复杂度 | 高/中/低 | 技术实现的难度 |
| 业务风险 | 高/中/低 | 对业务的影响程度 |
| 团队熟悉度 | 熟悉/一般/不熟悉 | 团队对技术栈的掌握程度 |
| 时间要求 | 紧急/正常/宽松 | 交付时间的紧迫性 |

**决策矩阵**：

```
技术复杂度: 低 + 业务风险: 低 + 团队熟悉度: 熟悉 → 全自动模式
技术复杂度: 高 + 业务风险: 高 + 团队熟悉度: 不熟悉 → 半自动模式
```

### 步骤 3：执行模式切换

```bash
# 切换到全自动模式
$ python3 scripts/mode_cli.py mode set full-auto \
  -r REQ-001 \
  --reason "成熟功能，团队熟悉，风险可控"

✅ 模式已切换: semi-auto → full-auto
   需求ID: REQ-001
   切换原因: 成熟功能，团队熟悉，风险可控

全自动AI模式：AI独立完成任务，遇到问题时人工可介入
```

### 步骤 4：系统记录切换

系统自动记录切换信息：

```json
{
  "timestamp": "2025-03-15T10:30:00",
  "operator": "architect",
  "from": "semi-auto",
  "to": "full-auto",
  "requirement_id": "REQ-001",
  "reason": "成熟功能，团队熟悉，风险可控"
}
```

记录位置：
- `.agents/config.json` - 配置文件中的 modeHistory
- `.agents/logs/mode_changes.log` - 审计日志文件

### 步骤 5：AI 按新模式执行

AI 根据新的模式设置执行任务：

**全自动模式**：
```
1. AI 自动分析需求
2. AI 自动设计架构
3. AI 自动生成代码
4. AI 自动运行测试
5. [检查点] 架构师审查
6. AI 自动部署
```

**半自动模式**：
```
1. AI 生成 3-5 种方案
2. 架构师选择方案
3. AI 生成代码草稿
4. 架构师审查代码
5. 架构师批准
6. AI 执行部署
```

---

## 五、按需求维度切换

### 5.1 什么是按需求维度切换？

- 每个需求可以独立设置模式
- 不同需求可以使用不同模式
- 模式与需求ID绑定

### 5.2 实际案例

假设有 3 个并行的需求：

```bash
# 需求 REQ-001: 用户登录功能（成熟功能，低风险）
$ python3 scripts/mode_cli.py mode set full-auto -r REQ-001

# 需求 REQ-002: 支付系统（高风险，需要把关）
$ python3 scripts/mode_cli.py mode set semi-auto -r REQ-002

# 需求 REQ-003: 数据报表（低风险，快速开发）
$ python3 scripts/mode_cli.py mode set full-auto -r REQ-003
```

**结果**：
- REQ-001 和 REQ-003 使用全自动模式，AI 快速完成
- REQ-002 使用半自动模式，架构师全程把关
- 三个需求互不影响，并行推进

### 5.3 按 Agent 维度切换

除了按需求切换，还可以针对不同的 Agent 设置不同模式：

```bash
# Common Agent 使用全自动模式（成熟模块）
$ python3 scripts/mode_cli.py agent mode common full-auto -r REQ-001

# Training Agent 使用半自动模式（复杂逻辑）
$ python3 scripts/mode_cli.py agent mode training semi-auto -r REQ-001
```

---

## 六、审计和追溯

### 6.1 查看切换历史

```bash
$ python3 scripts/mode_cli.py mode history

模式切换历史:
--------------------------------------------------------------------------------

时间: 2025-03-15T10:30:00
切换: semi-auto → full-auto
需求ID: REQ-001
原因: 成熟功能，团队熟悉，风险可控
操作者: architect

时间: 2025-03-14T15:20:00
切换: full-auto → semi-auto
需求ID: REQ-002
原因: 新项目，需要人工把关
操作者: architect
```

### 6.2 审计日志

所有模式切换都会记录到审计日志：

```bash
$ cat .agents/logs/mode_changes.log

{"timestamp":"2025-03-15T10:30:00","old_mode":"semi-auto","new_mode":"full-auto","requirement_id":"REQ-001","operator":"architect"}
{"timestamp":"2025-03-14T15:20:00","old_mode":"full-auto","new_mode":"semi-auto","requirement_id":"REQ-002","operator":"architect"}
```

---

## 七、最佳实践

### 7.1 何时使用全自动模式？

✅ **推荐场景**：
- 成熟的 CRUD 功能
- 常见的 Bug 修复
- 代码重构和优化
- 单元测试编写
- 文档生成

❌ **不推荐场景**：
- 新技术栈的引入
- 核心业务逻辑变更
- 安全相关功能
- 生产环境首次部署

### 7.2 何时使用半自动模式？

✅ **推荐场景**：
- 新项目启动
- 架构设计和技术选型
- 核心业务逻辑开发
- 安全功能实现
- 生产环境部署

❌ **不推荐场景**：
- 简单的 Bug 修复
- 重复性的开发任务
- 低风险的功能迭代

### 7.3 模式切换的时机

**项目初期**：
```
新项目启动 → 半自动模式
  ↓
架构稳定后 → 逐步切换到全自动模式
  ↓
成熟阶段 → 大部分使用全自动模式
```

**紧急情况**：
```
生产环境故障 → 临时切换到半自动模式
  ↓
问题修复 → 恢复全自动模式
```

---

## 八、技术实现

### 8.1 配置文件结构

```json
{
  "mode": {
    "current": "semi-auto",
    "options": {
      "full-auto": {
        "description": "全自动AI模式",
        "checkpoints": ["架构设计", "安全审查", "生产部署"],
        "humanIntervention": "on-error"
      },
      "semi-auto": {
        "description": "半自动AI模式",
        "requireApproval": ["架构设计", "技术选型", "代码合并", "部署发布"],
        "humanIntervention": "on-decision"
      }
    }
  },
  "modeHistory": [
    {
      "timestamp": "2025-03-15T10:30:00",
      "from": "semi-auto",
      "to": "full-auto",
      "requirement_id": "REQ-001",
      "reason": "成熟功能，风险可控",
      "operator": "architect"
    }
  ]
}
```

### 8.2 权限检查实现

```python
def check_architect_permission():
    """检查是否有架构师权限"""
    if not USER_CONFIG.exists():
        return False, "未找到用户配置文件"

    try:
        with open(USER_CONFIG) as f:
            user_data = json.load(f)

        current_role = user_data.get("role", "")
        if current_role != "architect":
            return False, f"权限不足：只有架构师可以切换模式（当前角色: {current_role}）"

        return True, "权限验证通过"
    except Exception as e:
        return False, f"权限验证失败: {str(e)}"
```

### 8.3 切换日志记录

```python
def log_mode_change(old_mode, new_mode, requirement_id=None):
    """记录模式切换日志"""
    log_dir = AMAZING_ROOT / ".agents" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "mode_changes.log"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "old_mode": old_mode,
        "new_mode": new_mode,
        "requirement_id": requirement_id,
        "operator": "architect"
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
```

---

## 九、总结

Amazing 的 AI 模式切换机制具有以下特点：

1. **灵活性**：按需求维度切换，不同需求可以使用不同模式
2. **安全性**：只有架构师有权限切换，确保决策质量
3. **可追溯**：所有切换操作都有记录，便于审计
4. **可控性**：人工可以随时介入，确保风险可控

通过合理使用两种模式，可以在**效率**和**可控性**之间取得最佳平衡：

- **全自动模式**：提高效率，适合成熟流程
- **半自动模式**：保证质量，适合高风险任务

---

## 相关链接

- [完整架构文档](https://z58362026.github.io/amazing/)
- [模式切换流程](https://z58362026.github.io/amazing/workflows/mode-switch.html)
- [架构师工作流](https://z58362026.github.io/amazing/workflows/architect-workflow.html)
- [GitHub 仓库](https://github.com/z58362026/amazing)

---

**关键词**: AI模式切换、权限控制、按需求切换、全自动模式、半自动模式、架构师决策

**标签**: #AI开发 #模式切换 #权限控制 #架构师 #Amazing
