# 架构师角色快速上手指南

## 1. 角色定位

你是 Amazing 平台的架构师，负责：
- 技术方案决策
- 产品形态定义
- 代码质量把关
- 团队协作协调

## 2. 核心能力

### 你能做什么？
- ✅ 从 AI 提供的多种方案中选择最优方案
- ✅ 定制产品的 UI/UX 设计
- ✅ 审查代码、架构、安全、性能
- ✅ 拆分任务并分配给团队
- ✅ 批准或拒绝上线

### 你不能做什么？
- ❌ 直接编写代码（由前后端完成）
- ❌ 直接部署（由运维完成）

## 3. 典型工作流

### 场景 1: 新功能开发

```bash
# 1. 查看 PM 提交的 PRD
amazing task view <task-id>

# 2. AI 会提供 3-5 种技术方案，你选择一种
amazing arch solution login-feature \
  --choice "JWT + Redis" \
  --reason "高性能，适合移动端" \
  --tech-stack "Node.js, Redis, JWT" \
  --database "MySQL"

# 3. AI 会提供多种 UI 设计，你定制产品形态
amazing arch ui-spec login-feature \
  --layout "center-card" \
  --style "modern-minimal" \
  --colors "#007AFF,#34C759,#FF3B30" \
  --components "Ant Design"

# 4. 创建架构文档
amazing arch create login-feature \
  --solution "JWT + Redis" \
  --ui-style "modern-minimal"

# 5. 查看待审查任务
amazing review pending

# 6. 审查前端代码
amazing review start frontend-login-page

# 7. 批准或拒绝
amazing review approve frontend-login-page --comment "UI 还原度高"
# 或
amazing review reject frontend-login-page --reason "圆角不符合规范"
```

### 场景 2: 技术决策

```bash
# 1. 查看待决策事项
amazing decision pending

# 2. 做出决策
amazing decision make cache-solution \
  --choice "Redis" \
  --reason "性能好，支持分布式"

# 3. 查看决策历史
amazing decision history
```

### 场景 3: 代码审查

```bash
# 1. 查看待审查任务
amazing review pending

# 2. 开始审查
amazing review start backend-api-implementation

# 3. 查看代码
cd /path/to/code
git diff main...feature-branch

# 4. 批准或拒绝
amazing review approve backend-api-implementation \
  --comment "代码质量高，测试覆盖率达标"
```

## 4. 决策原则

### 技术方案选择
- 优先考虑长期价值
- 平衡技术先进性和团队能力
- 考虑成本效益和时间要求
- 保持架构一致性

### 产品形态定义
- 关注用户体验
- 保持品牌一致性
- 考虑实现难度
- 平衡美观和性能

### 代码审查
- 关注关键问题，不纠结细节
- 提供建设性意见
- 及时反馈，避免阻塞
- 记录决策理由

## 5. 常用命令速查

```bash
# 架构管理
amazing arch create <feature>           # 创建架构文档
amazing arch solution <feature>         # 定义技术方案
amazing arch ui-spec <feature>          # 定义 UI 规范

# 决策管理
amazing decision pending                # 查看待决策
amazing decision make <id>              # 做出决策
amazing decision history                # 决策历史

# 审查管理
amazing review pending                  # 查看待审查
amazing review start <task-id>          # 开始审查
amazing review approve <task-id>        # 批准任务
amazing review reject <task-id>         # 拒绝任务
amazing review history                  # 审查历史
```

## 6. 与 AI 的协作

### AI 的职责
- 提供多种方案供你选择
- 在你定义的边界内执行
- 自动化重复性工作
- 提供技术建议

### 你的职责
- 做出关键决策
- 定义质量标准
- 把关产品形态
- 协调团队协作

### 协作原则
- AI 提供选项，你做决策
- AI 执行实现，你做审查
- AI 自动化流程，你把控方向

## 7. 示例：完整流程

```bash
# 1. 接收需求
amazing task view prd-user-login

# 2. 定义技术方案
amazing arch solution user-login \
  --choice "JWT + Redis" \
  --reason "高性能，适合移动端" \
  --tech-stack "Node.js, Express, Redis, JWT" \
  --database "MySQL" \
  --cache "Redis"

# 3. 定义 UI 规范
amazing arch ui-spec user-login \
  --layout "center-card" \
  --style "modern-minimal" \
  --colors "#007AFF,#34C759,#FF3B30" \
  --components "Ant Design"

# 4. 创建架构文档
amazing arch create user-login \
  --solution "JWT + Redis" \
  --ui-style "modern-minimal"

# 5. 等待开发完成，查看待审查任务
amazing review pending

# 6. 审查前端
amazing review start frontend-login-page
# 查看代码...
amazing review approve frontend-login-page

# 7. 审查后端
amazing review start backend-login-api
# 查看代码...
amazing review approve backend-login-api

# 8. 批准上线
amazing deploy approve user-login
```

## 8. 注意事项

1. **决策要有理由**: 每次决策都要说明理由，便于团队理解和追溯
2. **审查要及时**: 避免阻塞开发进度
3. **标准要明确**: 提前定义质量标准，避免后期争议
4. **沟通要清晰**: 拒绝任务时要说明具体问题和改进方向
5. **记录要完整**: 所有决策和审查都会自动记录，便于追溯

## 9. 获取帮助

```bash
# 查看帮助
amazing arch --help
amazing decision --help
amazing review --help

# 查看角色权限
amazing role info architect

# 查看完整文档
cat docs/architecture/architect-role.md
```

---
祝你工作愉快！
