# 架构师角色设计

## 1. 核心问题

当前架构存在的问题：
1. **缺少整体把控者**：没有人对需求全局、技术方案、产品形态负责
2. **Agent 能力过度自由**：AI 随机生成代码，缺少人类决策和审核
3. **角色能力固化**：每个角色只能做固定的事，无法个性化发挥
4. **产品形态不可控**：最终产品样式、交互由 AI 决定，而非人类

## 2. 架构师角色定位

### 2.1 职责

**架构师 (Architect)** 是整个 Agent-Teams 的核心决策者：

```
┌─────────────────────────────────────────────────┐
│              架构师 (Architect)                  │
├─────────────────────────────────────────────────┤
│  1. 需求全局把控 - 理解业务目标、技术约束       │
│  2. 技术方案决策 - 选型、架构设计、技术栈       │
│  3. 产品形态定义 - UI/UX 风格、交互规范         │
│  4. Agent 编排 - 分配任务、审核产出、协调资源   │
│  5. 质量把关 - 代码审查、性能优化、安全审计     │
└─────────────────────────────────────────────────┘
```

### 2.2 工作模式

**人机协同，人类主导**：

```
人类架构师 (决策)
    ↓
AI 架构师 Agent (辅助)
    ↓
各角色 Sub-Agent (执行)
```

## 3. 新架构设计

### 3.1 完整角色体系

```
┌─────────────────────────────────────────────────┐
│                   用户层                         │
├─────────────────────────────────────────────────┤
│  Architect (架构师) - 核心决策者                 │
│  PM (产品经理) - 需求管理                        │
│  Frontend (前端) - UI 实现                       │
│  Backend (后端) - API 实现                       │
│  QA (测试) - 质量保证                            │
│  Ops (运维) - 部署运维                           │
│  Operation (运营) - 数据运营                     │
└─────────────────────────────────────────────────┘
```

### 3.2 决策流程

```
1. 需求输入 (PM/Architect)
   ↓
2. 架构师决策
   ├── 技术方案 (选型、架构)
   ├── 产品形态 (UI/UX 规范)
   ├── 任务拆分 (分配给各角色)
   └── 质量标准 (验收标准)
   ↓
3. AI Agent 辅助
   ├── 生成技术方案草稿
   ├── 提供多种设计选项
   └── 评估技术风险
   ↓
4. 架构师审核
   ├── 选择最佳方案
   ├── 调整细节
   └── 批准执行
   ↓
5. 各角色执行
   ├── Frontend: 按照 UI 规范实现
   ├── Backend: 按照 API 设计实现
   └── QA: 按照验收标准测试
   ↓
6. 架构师验收
   ├── 代码审查
   ├── 产品形态检查
   └── 批准上线
```

## 4. 架构师工作流

### 4.1 需求阶段

**输入**: PM 提供的业务需求

**架构师工作**:
```bash
# 1. 理解需求
claude-code "分析需求: 用户权限管理，给出 3 种技术方案"

# 2. 决策技术方案
# AI 提供: 方案 A (RBAC), 方案 B (ABAC), 方案 C (混合)
# 架构师选择: 方案 A (RBAC)

# 3. 定义产品形态
# AI 提供: 3 种 UI 设计风格
# 架构师选择: 简洁风格 + 自定义调整

# 4. 创建架构文档
python3 scripts/amazing-cli.py arch create "用户权限管理" \
  --solution "RBAC" \
  --ui-style "简洁风格" \
  --tech-stack "FastAPI + React + PostgreSQL"
```

**输出**:
- 技术方案文档 (`docs/architecture/user-permission.md`)
- UI/UX 规范 (`docs/design/user-permission-ui.md`)
- 任务拆分清单

### 4.2 设计阶段

**架构师工作**:
```bash
# 1. 数据库设计
claude-code "根据 RBAC 方案，设计数据库表结构，给出 ER 图"

# 架构师审核:
# - 检查表结构是否合理
# - 调整字段类型、索引
# - 批准设计

# 2. API 设计
claude-code "设计用户权限管理 API，RESTful 风格"

# 架构师审核:
# - 检查 API 命名规范
# - 调整请求/响应格式
# - 批准设计

# 3. UI 设计
claude-code "根据简洁风格，设计角色管理页面，提供 3 种布局"

# 架构师选择:
# - 选择布局 B
# - 调整颜色、间距
# - 批准设计
```

### 4.3 开发阶段

**架构师工作**:
```bash
# 1. 分配任务
python3 scripts/amazing-cli.py task assign \
  --role frontend \
  --task "实现角色管理页面" \
  --spec "docs/design/user-permission-ui.md"

python3 scripts/amazing-cli.py task assign \
  --role backend \
  --task "实现角色管理 API" \
  --spec "docs/architecture/user-permission.md"

# 2. 监控进度
python3 scripts/amazing-cli.py status

# 3. 代码审查
# Frontend 提交代码后
python3 scripts/amazing-cli.py review \
  --task "角色管理页面" \
  --reviewer architect

# 架构师审查:
# - 检查是否符合 UI 规范
# - 检查代码质量
# - 提出修改意见或批准
```

### 4.4 验收阶段

**架构师工作**:
```bash
# 1. 功能验收
python3 scripts/amazing-cli.py test acceptance \
  --task "用户权限管理"

# 2. 产品形态检查
# - 启动本地环境
# - 检查 UI 是否符合设计
# - 检查交互是否流畅

# 3. 性能测试
python3 scripts/amazing-cli.py test performance \
  --task "用户权限管理"

# 4. 批准上线
python3 scripts/amazing-cli.py approve \
  --task "用户权限管理" \
  --reviewer architect
```

## 5. 人类决策机制

### 5.1 决策点

在以下关键节点，**必须由人类架构师决策**：

1. **技术方案选型**
   - AI 提供 3-5 种方案
   - 架构师选择并调整

2. **产品形态定义**
   - AI 提供多种 UI 设计
   - 架构师选择并定制

3. **代码审查**
   - AI 自动检查代码质量
   - 架构师最终批准

4. **上线决策**
   - AI 提供测试报告
   - 架构师决定是否上线

### 5.2 AI 辅助机制

AI 的角色是**辅助决策，而非替代决策**：

```python
# AI 辅助流程
class ArchitectAssistant:
    def assist_decision(self, context):
        # 1. 分析需求
        analysis = self.analyze_requirement(context)

        # 2. 生成多种方案
        solutions = self.generate_solutions(analysis, count=3)

        # 3. 评估方案
        evaluations = [self.evaluate(s) for s in solutions]

        # 4. 推荐方案 (但不决策)
        recommendation = self.recommend(solutions, evaluations)

        # 5. 等待人类决策
        decision = self.wait_for_human_decision(
            solutions=solutions,
            recommendation=recommendation
        )

        return decision
```

### 5.3 个性化发挥

每个角色可以在**架构师定义的边界内**个性化发挥：

```
架构师定义:
├── 技术栈: React + TypeScript
├── UI 风格: 简洁风格
├── 组件库: Ant Design
└── 代码规范: ESLint + Prettier

Frontend 个性化发挥:
├── 组件拆分方式 (自由)
├── 状态管理方案 (自由)
├── 动画效果 (在风格范围内)
└── 性能优化 (自由)
```

## 6. 架构师 CLI 工具

### 6.1 角色切换

```bash
# 切换到架构师角色
python3 scripts/amazing-cli.py role select
# 选择: 0. 架构师 (architect)
```

### 6.2 架构管理

```bash
# 创建架构文档
python3 scripts/amazing-cli.py arch create <feature-name>

# 定义技术方案
python3 scripts/amazing-cli.py arch solution <feature-name> \
  --tech-stack "FastAPI + React" \
  --database "PostgreSQL" \
  --cache "Redis"

# 定义 UI 规范
python3 scripts/amazing-cli.py arch ui-spec <feature-name> \
  --style "简洁风格" \
  --components "Ant Design" \
  --colors "#1890ff,#52c41a"

# 查看架构文档
python3 scripts/amazing-cli.py arch show <feature-name>
```

### 6.3 决策管理

```bash
# 查看待决策事项
python3 scripts/amazing-cli.py decisions pending

# 做出决策
python3 scripts/amazing-cli.py decision make <decision-id> \
  --choice "方案 A" \
  --reason "性能更好，易于维护"

# 查看决策历史
python3 scripts/amazing-cli.py decisions history
```

### 6.4 审查管理

```bash
# 查看待审查代码
python3 scripts/amazing-cli.py review pending

# 审查代码
python3 scripts/amazing-cli.py review approve <task-id>
python3 scripts/amazing-cli.py review reject <task-id> \
  --reason "不符合 UI 规范"

# 查看审查历史
python3 scripts/amazing-cli.py review history
```

## 7. 架构师权限

```python
ARCHITECT_PERMISSIONS = {
    # 全局权限
    "view_all_tasks": True,
    "view_all_code": True,
    "view_all_logs": True,

    # 决策权限
    "approve_tech_solution": True,
    "approve_ui_design": True,
    "approve_deployment": True,

    # 管理权限
    "assign_tasks": True,
    "reassign_tasks": True,
    "cancel_tasks": True,

    # 审查权限
    "code_review": True,
    "architecture_review": True,
    "security_review": True,

    # 执行权限 (受限)
    "code_development": False,  # 不直接写代码
    "direct_deployment": False,  # 不直接部署
}
```

## 8. 示例：完整流程

### 场景：实现用户权限管理

#### 步骤 1：架构师接收需求

```bash
# PM 创建需求
python3 scripts/amazing-cli.py prd create "用户权限管理"

# 架构师查看需求
python3 scripts/amazing-cli.py prd show prd-001
```

#### 步骤 2：架构师决策技术方案

```bash
# 使用 AI 辅助分析
claude-code "分析用户权限管理需求，提供 3 种技术方案：
1. RBAC (基于角色)
2. ABAC (基于属性)
3. 混合方案
对比优缺点、实现复杂度、性能"

# AI 输出 3 种方案对比

# 架构师决策
python3 scripts/amazing-cli.py arch solution prd-001 \
  --choice "RBAC" \
  --reason "实现简单，满足当前需求" \
  --tech-stack "FastAPI + PostgreSQL + Redis"
```

#### 步骤 3：架构师定义产品形态

```bash
# 使用 AI 辅助设计
claude-code "根据 RBAC 方案，设计角色管理页面，提供 3 种布局：
1. 左侧树形 + 右侧详情
2. 顶部 Tab + 下方列表
3. 卡片式布局
提供 Figma 风格的 ASCII 原型图"

# AI 输出 3 种布局

# 架构师选择并定制
python3 scripts/amazing-cli.py arch ui-spec prd-001 \
  --layout "左侧树形 + 右侧详情" \
  --style "简洁风格" \
  --colors "#1890ff,#52c41a,#faad14" \
  --components "Ant Design"
```

#### 步骤 4：架构师分配任务

```bash
# 分配给 Frontend
python3 scripts/amazing-cli.py task assign \
  --role frontend \
  --task "实现角色管理页面" \
  --spec "docs/architecture/prd-001-ui.md" \
  --deadline "2 days"

# 分配给 Backend
python3 scripts/amazing-cli.py task assign \
  --role backend \
  --task "实现角色管理 API" \
  --spec "docs/architecture/prd-001-api.md" \
  --deadline "2 days"
```

#### 步骤 5：各角色执行

```bash
# Frontend 开发
# (Frontend 角色登录)
python3 scripts/amazing-cli.py role select
# 选择: 2. 前端开发 (frontend)

claude-code "根据 docs/architecture/prd-001-ui.md 实现角色管理页面"

# Backend 开发
# (Backend 角色登录)
python3 scripts/amazing-cli.py role select
# 选择: 3. 后端开发 (backend)

claude-code "根据 docs/architecture/prd-001-api.md 实现角色管理 API"
```

#### 步骤 6：架构师审查

```bash
# 架构师查看待审查任务
python3 scripts/amazing-cli.py review pending

# 审查 Frontend 代码
python3 scripts/amazing-cli.py review start task-001

# 检查点:
# 1. 是否符合 UI 规范？
# 2. 代码质量如何？
# 3. 性能是否达标？

# 批准或拒绝
python3 scripts/amazing-cli.py review approve task-001
# 或
python3 scripts/amazing-cli.py review reject task-001 \
  --reason "颜色不符合规范，请使用 #1890ff"
```

#### 步骤 7：架构师验收

```bash
# 运行验收测试
python3 scripts/amazing-cli.py test acceptance --task prd-001

# 启动本地环境检查
make dev
# 访问 http://localhost:3000
# 手动检查产品形态

# 批准上线
python3 scripts/amazing-cli.py approve prd-001 \
  --reviewer architect \
  --comment "符合设计要求，批准上线"
```

## 9. 总结

### 9.1 核心改进

1. **增加架构师角色**：整体把控需求、技术、产品形态
2. **人类决策机制**：关键决策由人类做出，AI 辅助
3. **个性化发挥空间**：在架构师定义的边界内自由发挥
4. **产品形态可控**：最终样式由架构师决定，而非 AI 随机生成

### 9.2 新架构优势

```
传统架构:
AI Agent → 随机生成代码 → 不可控

新架构:
人类架构师 (决策)
  ↓
AI Agent (辅助)
  ↓
各角色 (执行)
  ↓
人类架构师 (审核)
  ↓
可控的产品形态
```

### 9.3 下一步

1. 实现架构师 CLI 工具
2. 实现决策管理系统
3. 实现审查工作流
4. 完善架构师文档模板
