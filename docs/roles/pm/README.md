# 产品经理指南

## 1. 角色职责

作为产品经理，你负责:
- 需求分析与管理
- PRD 编写
- 原型设计
- 功能验收
- 产品规划

## 2. 工作流程

### 2.1 需求分析

```bash
# 使用 Amazing CLI
amazing prd create "用户权限管理模块"

# 或使用 Claude Code
claude-code "分析需求: 用户权限管理模块"
```

**输出**: 需求分析文档

### 2.2 PRD 编写

使用 `prd-generator` Skill 自动生成 PRD:

```bash
# 生成 PRD
amazing skill run prd-generator \
  --input "需求描述" \
  --output "docs/prd/prd-001.md"
```

**PRD 模板**: `.claude/skills/prd-template.md`

### 2.3 技术评审

```bash
# 分配给技术团队评审
amazing agent assign common --task prd-001 --role frontend,backend
```

### 2.4 功能验收

```bash
# 查看开发进度
amazing status --task prd-001

# 验收测试
amazing test acceptance --task prd-001
```

## 3. 可用工具

### 3.1 Claude Code (主力)

```bash
# 需求分析
claude-code "分析需求: [需求描述]"

# 生成 PRD
claude-code "生成 PRD: [需求描述]"

# 原型设计
claude-code "设计原型: [功能描述]"
```

### 3.2 Codex CLI (备选)

```bash
# 需求分析
codex "分析需求: [需求描述]"
```

### 3.3 Codex Desktop (可视化)

打开 Codex Desktop，选择 PM 角色，进行可视化操作。

## 4. Skills

### 4.1 prd-generator

自动生成 PRD 文档。

**使用**:
```bash
amazing skill run prd-generator --input "需求描述"
```

### 4.2 requirement-analyzer

分析需求，提取关键功能点。

**使用**:
```bash
amazing skill run requirement-analyzer --input "需求描述"
```

### 4.3 prototype-design

生成原型设计。

**使用**:
```bash
amazing skill run prototype-design --input "功能描述"
```

## 5. 最佳实践

### 5.1 需求描述

- 清晰明确
- 包含用户故事
- 定义验收标准
- 考虑边界情况

### 5.2 PRD 编写

- 使用标准模板
- 包含技术方案
- 定义里程碑
- 明确优先级

### 5.3 沟通协作

- 定期同步进度
- 及时响应问题
- 记录决策过程
- 收集反馈

## 6. 示例

### 6.1 创建需求

```bash
# 1. 创建 PRD
amazing prd create "用户权限管理模块"

# 2. 编辑 PRD
vim docs/prd/prd-001.md

# 3. 分配任务
amazing agent assign common --task prd-001

# 4. 跟踪进度
amazing status --task prd-001
```

### 6.2 需求变更

```bash
# 1. 更新 PRD
vim docs/prd/prd-001.md

# 2. 通知团队
amazing notify --task prd-001 --message "需求已更新"

# 3. 重新评审
amazing review --task prd-001
```

## 7. 权限

作为 PM，你拥有以下权限:
- `prd:create` - 创建 PRD
- `prd:edit` - 编辑 PRD
- `requirement:review` - 需求评审
- `feature:approve` - 功能批准
- `acceptance:test` - 验收测试

## 8. 常见问题

**Q: 如何生成 PRD?**
A: 使用 `amazing prd create` 或 `prd-generator` Skill。

**Q: 如何跟踪开发进度?**
A: 使用 `amazing status` 命令。

**Q: 如何进行功能验收?**
A: 使用 `amazing test acceptance` 命令。
