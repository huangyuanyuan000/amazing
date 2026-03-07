# Amazing - AI 驱动的企业级脚手架框架

> 📖 **[查看完整架构文档](https://z58362026.github.io/amazing/)**

## 框架定位
通用的 Agent-Teams 协同开发框架，支持通过命令或对话快速初始化任何业务的完整架构。

## 核心能力

### 1. 智能初始化
- **命令式初始化**: `python3 scripts/init.py <project> --template=<name>`
- **对话式初始化**: 通过自然语言描述业务需求，自动生成完整架构
- **模板库**: 预置 SaaS、电商、AI 平台、IoT 等业务模板
- **案例库**: 可从成功案例快速复制架构

### 2. 动态架构生成
- 根据业务描述自动生成技术架构
- 自动选择技术栈（Python/Go/Node.js/Java）
- 自动配置数据库（PostgreSQL/MySQL/MongoDB/Redis）
- 自动生成部署配置（本地/Docker/K8s/离线）

### 3. 多环境适配
- **数据库**: 动态检测和适配多种数据库，支持混合使用
- **部署**: 自动适配有/无 K8s、有/无数据库等场景
- **环境**: 开发/测试/生产环境自动切换
- **网络**: 在线/离线/私有化部署

### 4. 一键部署
- `make dev`: 本地开发环境（热重载）
- `make docker`: Docker Compose 一键部署
- `make k8s`: Kubernetes 集群部署
- `make offline`: 离线/私有化部署包

### 5. Handoffs 任务拆分
- **自动拆分**: 复杂任务自动拆分成小任务，防止上下文溢出
- **粒度控制**: 单个文件 < 200 行，多文件按模块拆分
- **状态管理**: 每个子任务独立执行，支持暂停和恢复
- **角色专属**: 每个角色有专属的 Handoff Agents

### 6. 进化能力
- **影响分析**: 变更自动分析影响范围
- **智能通知**: 自动通知相关角色和 Agent
- **自动更新**: Agent/Sub-Agent/Skill 自动进化
- **依赖追踪**: 全链路依赖关系管理

## 框架结构

```
amazing/                          # 框架核心
├── .claude/                      # 框架级配置
│   ├── roles/                    # 通用角色（产品/前端/后端/测试/运维/运营）
│   ├── skills/                   # 通用技能
│   └── commands/                 # 框架命令
│
├── .agents/                      # 框架级通用 Agent
│   ├── common/                   # 通用模块（用户/权限/日志）
│   ├── database/                 # 数据库适配器
│   ├── deployment/               # 部署能力
│   ├── monitoring/               # 监控告警
│   ├── evolution/                # 进化能力
│   └── init-handoffs/            # 初始化 Handoff Agents（模板）
│       ├── page-generator/       # 页面生成器
│       ├── service-generator/    # API 服务生成器
│       ├── store-generator/      # 状态管理生成器
│       ├── model-generator/      # 数据模型生成器
│       ├── api-generator/        # API 端点生成器
│       └── test-generator/       # 测试生成器
│   ├── monitoring/               # 监控告警
│   └── evolution/                # 进化能力
│
├── templates/                    # 业务模板库
│   ├── saas-platform/            # SaaS 平台
│   ├── e-commerce/               # 电商平台
│   ├── ai-platform/              # AI 平台
│   └── iot-platform/             # IoT 平台
│
├── examples/                     # 案例库
│   ├── model-platform/           # 大模型管理平台
│   ├── e-commerce/               # 电商平台
│   └── saas-platform/            # SaaS 平台
│
├── standards/                    # 开发规范
│   ├── code/                     # 代码规范
│   ├── git/                      # Git 规范
│   ├── api/                      # API 规范
│   └── testing/                  # 测试规范
│
└── scripts/                      # 框架脚本
    ├── init.py                   # 初始化项目
    ├── orchestrator.py           # 初始化编排器
    ├── handoff_manager.py        # Handoff 管理器
    ├── evolve.py                 # 进化分析
    └── deploy.py                 # 部署脚本
```

## Handoffs 任务拆分系统

### 核心原则
所有角色在执行复杂任务时，都会自动使用 Handoffs 模式进行任务拆分，避免一次性生成过多内容导致上下文溢出。

### 拆分粒度
- **单个文件 < 200 行**: 可以一次性生成
- **单个文件 200-500 行**: 先生成骨架，再分段填充
- **单个文件 > 500 行**: 拆分成多个文件
- **多文件任务**: 按模块/功能拆分，逐个完成

### 自动触发条件
- 预估生成代码 > 200 行
- 涉及 3 个以上文件
- 需要多个步骤才能完成
- 依赖其他任务的输出

### Handoff Agents

#### 前端开发
- **page-generator**: 生成单个页面组件（< 200 行）
- **component-generator**: 生成可复用组件（< 150 行）
- **service-generator**: 生成 API 服务层（< 150 行）
- **store-generator**: 生成状态管理（< 150 行）

#### 后端开发
- **model-generator**: 生成数据模型（< 150 行）
- **api-generator**: 生成 API 端点（< 200 行）
- **service-generator-backend**: 生成业务逻辑（< 200 行）
- **test-generator**: 生成测试代码（< 200 行）

### 使用方式

```bash
# 创建任务（自动拆分）
python scripts/handoff_manager.py create frontend-dev "开发用户管理模块"

# 执行任务
python scripts/handoff_manager.py execute <task-id>

# 查看状态
python scripts/handoff_manager.py status <task-id>

# 列出任务
python scripts/handoff_manager.py list frontend-dev
```

### 任务拆分示例

**前端任务**: 开发用户管理模块
```
├─ 子任务1: 生成 user API 服务
├─ 子任务2: 生成 userStore 状态管理
├─ 子任务3: 生成 UserList 页面
└─ 子任务4: 生成 UserDetail 页面
```

**后端任务**: 开发用户管理 API
```
├─ 子任务1: 生成 User 数据模型
├─ 子任务2: 生成 user API 端点
├─ 子任务3: 生成 UserService 业务逻辑
└─ 子任务4: 生成 user 测试
```

## IronClaw 权限体系

### 核心机制
框架初始化时自动继承 IronClaw 功能，每个角色通过独立的 IronClaw 实例与项目沟通。

### 权限模型

#### 1. 架构师（Architect）- 最高权限
- **唯一拥有整体角色设定权限**
- 可以创建/修改/删除角色
- 可以审批角色申请
- 可以调整权限边界
- 可以修改工作流规则

#### 2. 其他角色 - 受限权限
- **只能申请角色，不能自行设定**
- 必须通过架构师审批
- 权限范围由角色定义限制
- 只能在授权范围内操作

### 角色定义

| 角色 | 职责 | 权限范围 | IronClaw 配置 |
|------|------|----------|---------------|
| 架构师 | 技术决策、架构设计、权限管理 | 全局 | .claude/roles/architect/ |
| 产品经理 | 需求定义、验收 | 需求文档、验收标准 | .claude/roles/product-manager/ |
| 前端开发 | UI/UX 实现 | 前端代码、前端配置 | .claude/roles/frontend-dev/ |
| 后端开发 | API/服务开发 | 后端代码、API 定义 | .claude/roles/backend-dev/ |
| 测试工程师 | 测试用例、自动化测试 | 测试代码、测试配置 | .claude/roles/test-engineer/ |
| 运维工程师 | 部署、监控、环境管理 | 部署配置、基础设施 | .claude/roles/devops-engineer/ |
| 运营人员 | 数据分析、运营配置 | 运营数据、配置管理 | .claude/roles/operations/ |

### 权限矩阵

```yaml
# .claude/ironclaw/permissions.yml
roles:
  architect:
    level: admin
    permissions:
      - all  # 全局权限

  product-manager:
    level: manager
    permissions:
      - read: all
      - write: [docs/requirements/, docs/acceptance/]
      - approve: [requirements, features]

  frontend-dev:
    level: developer
    permissions:
      - read: [docs/, src/frontend/, .agents/*/frontend/]
      - write: [src/frontend/, tests/frontend/]
      - create: [frontend-components, frontend-pages]

  backend-dev:
    level: developer
    permissions:
      - read: [docs/, src/backend/, .agents/*/backend/]
      - write: [src/backend/, tests/backend/]
      - create: [api-endpoints, services, models]

  test-engineer:
    level: developer
    permissions:
      - read: all
      - write: [tests/, .github/workflows/test-*.yml]
      - create: [test-cases, test-suites]

  devops-engineer:
    level: operator
    permissions:
      - read: all
      - write: [deploy/, .github/workflows/, Makefile, docker-compose.yml]
      - create: [deployment-configs, ci-cd-pipelines]
      - execute: [deploy, rollback, scale]

  operations:
    level: viewer
    permissions:
      - read: [docs/, logs/, metrics/]
      - write: [config/operations/]
      - create: [reports, dashboards]
```

## 标准工作流（内置）

### 1. 角色申请流程

```yaml
# .claude/workflows/role-request.yml
workflow: role-request
trigger: user_request_role

steps:
  - name: 提交申请
    actor: applicant
    action: submit_role_request
    data:
      - role: 申请的角色
      - reason: 申请理由
      - experience: 相关经验

  - name: 架构师审批
    actor: architect
    action: review_role_request
    options:
      - approve: 批准申请
      - reject: 拒绝申请
      - request_more_info: 要求补充信息

  - name: 分配权限
    actor: system
    action: assign_permissions
    condition: approved
    data:
      - role: 批准的角色
      - permissions: 角色权限
      - ironclaw_config: IronClaw 配置

  - name: 通知结果
    actor: system
    action: notify
    targets: [applicant, architect]
```

### 2. 需求开发流程

```yaml
# .claude/workflows/feature-development.yml
workflow: feature-development
trigger: new_requirement

steps:
  - name: 需求定义
    actor: product-manager
    action: create_requirement
    output: docs/requirements/{feature}.md

  - name: 架构设计
    actor: architect
    action: design_architecture
    input: requirement
    output: docs/architecture/{feature}.md
    approval_required: true

  - name: 任务分解
    actor: architect
    action: break_down_tasks
    output: tasks/{feature}/

  - name: 前端开发
    actor: frontend-dev
    action: implement_frontend
    input: tasks/{feature}/frontend/
    output: src/frontend/
    parallel: true

  - name: 后端开发
    actor: backend-dev
    action: implement_backend
    input: tasks/{feature}/backend/
    output: src/backend/
    parallel: true

  - name: 集成测试
    actor: test-engineer
    action: integration_test
    input: [frontend, backend]
    output: tests/integration/{feature}/

  - name: 部署
    actor: devops-engineer
    action: deploy
    condition: tests_passed
    environments: [dev, staging, production]

  - name: 验收
    actor: product-manager
    action: acceptance_test
    approval_required: true
```

### 3. Bug 修复流程

```yaml
# .claude/workflows/bug-fix.yml
workflow: bug-fix
trigger: bug_reported

steps:
  - name: Bug 报告
    actor: [test-engineer, operations, any]
    action: create_bug_report
    output: issues/{bug-id}.md

  - name: 优先级评估
    actor: product-manager
    action: prioritize_bug
    options: [critical, high, medium, low]

  - name: 分配开发者
    actor: architect
    action: assign_developer
    condition: priority >= medium

  - name: 修复实现
    actor: [frontend-dev, backend-dev]
    action: fix_bug
    output: src/

  - name: 测试验证
    actor: test-engineer
    action: verify_fix
    approval_required: true

  - name: 紧急部署
    actor: devops-engineer
    action: hotfix_deploy
    condition: priority == critical
```

### 4. 代码审查流程

```yaml
# .claude/workflows/code-review.yml
workflow: code-review
trigger: pull_request

steps:
  - name: 提交 PR
    actor: [frontend-dev, backend-dev]
    action: create_pull_request
    checks:
      - lint_passed
      - tests_passed
      - coverage >= 80%

  - name: 自动检查
    actor: system
    action: run_ci_checks
    checks:
      - code_style
      - security_scan
      - dependency_check

  - name: 同行评审
    actor: [frontend-dev, backend-dev]
    action: peer_review
    required_approvals: 1

  - name: 架构师审批
    actor: architect
    action: architect_review
    condition: changes_architecture
    approval_required: true

  - name: 合并代码
    actor: system
    action: merge_pr
    condition: all_approved
```

### 5. 部署流程

```yaml
# .claude/workflows/deployment.yml
workflow: deployment
trigger: deployment_request

steps:
  - name: 部署申请
    actor: [backend-dev, frontend-dev]
    action: request_deployment
    data:
      - environment: [dev, staging, production]
      - version: 版本号
      - changes: 变更说明

  - name: 架构师审批
    actor: architect
    action: approve_deployment
    condition: environment == production
    approval_required: true

  - name: 运维审批
    actor: devops-engineer
    action: approve_deployment
    approval_required: true

  - name: 执行部署
    actor: devops-engineer
    action: deploy
    steps:
      - backup_current
      - deploy_new_version
      - health_check
      - rollback_if_failed

  - name: 验证部署
    actor: test-engineer
    action: smoke_test
    approval_required: true

  - name: 通知相关方
    actor: system
    action: notify
    targets: [architect, product-manager, operations]
```

| Agent | 能力 | 说明 |
|-------|------|------|
| common | 用户/权限/日志 | 所有业务通用的基础能力 |
| database | 数据库适配 | 动态适配 PG/MySQL/Mongo/Redis |
| deployment | 部署能力 | 支持本地/Docker/K8s/离线 |
| monitoring | 监控告警 | 日志/指标/链路追踪 |
| evolution | 进化分析 | 影响分析/通知/自动更新 |

## 开发规范

- **Git**: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `chore:`)
- **API**: RESTful + OpenAPI 3.0，统一响应格式
- **代码风格**: Python (black + ruff), Go (gofmt + golangci-lint), TS (eslint + prettier)
- **测试**: 单测覆盖率 > 80%, 集成测试必须通过
- **CI/CD**: GitHub Actions / GitLab CI, 自动化部署
- **文档**: 每个模块必须有 README，API 必须有 Swagger

## 使用方式

### 命令行初始化
```bash
# 从模板初始化
python3 scripts/init.py my-business --template=ai-platform

# 从案例初始化
python3 scripts/init.py my-business --from-example=model-platform

# 交互式初始化
python3 scripts/init.py my-business --interactive
```

### 对话式初始化
```bash
claude-code
> 初始化一个电商平台项目，需要：
> - 用户系统、商品管理、订单系统、支付系统
> - 支持 MySQL 数据库
> - 支持 Docker 和 K8s 部署
> - 需要前后端分离架构
```

## 初始化后的项目结构

```
my-business/                      # 业务实例
├── CLAUDE.md                     # 业务配置（自动生成）
├── .claude/roles/                # 业务角色
├── .agents/                      # 业务 Agent
│   ├── common/                   # 继承框架通用能力
│   ├── module-1/                 # 业务模块 1
│   └── module-2/                 # 业务模块 2
├── src/                          # 源代码
├── deploy/                       # 部署配置
├── docs/                         # 业务文档
├── tests/                        # 测试
└── Makefile                      # 业务命令
```

## AI 工具链

- **Claude Code CLI**: 主力开发工具
- **Codex CLI**: 本地降级方案
- **Codex Desktop**: 可视化操作
