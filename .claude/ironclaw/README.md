# IronClaw 权限体系

## 概述
IronClaw 是 Amazing 框架的权限管理系统，确保每个角色在授权范围内工作，维护项目的安全性和规范性。

## 核心原则

### 1. 最小权限原则
每个角色只拥有完成其职责所需的最小权限集。

### 2. 架构师主导
只有架构师拥有全局权限和角色管理权限，其他角色必须申请。

### 3. 审批机制
所有关键操作（角色申请、架构变更、生产部署）都需要审批。

### 4. 审计追踪
所有操作都有完整的审计日志，可追溯责任人。

## 权限级别

### Level 1: Viewer（查看者）
- 只读权限
- 可查看文档、代码、日志
- 不能修改任何内容

### Level 2: Developer（开发者）
- 读写权限（限定范围）
- 可修改代码、创建 PR
- 需要代码审查才能合并

### Level 3: Operator（操作者）
- 执行权限
- 可执行部署、运维操作
- 需要审批才能操作生产环境

### Level 4: Manager（管理者）
- 管理权限
- 可审批需求、验收功能
- 可管理团队成员

### Level 5: Admin（管理员）
- 全局权限
- 只有架构师拥有
- 可管理所有角色和权限

## 权限配置

### 架构师（Admin）
```yaml
role: architect
level: admin
permissions:
  read: ["*"]
  write: ["*"]
  create: ["*"]
  delete: ["*"]
  approve: ["*"]
  execute: ["*"]
capabilities:
  - manage_roles
  - manage_permissions
  - approve_architecture
  - approve_deployment
  - modify_workflows
```

### 产品经理（Manager）
```yaml
role: product-manager
level: manager
permissions:
  read: ["*"]
  write:
    - docs/requirements/
    - docs/acceptance/
    - docs/roadmap/
  create:
    - requirements
    - user-stories
    - acceptance-criteria
  approve:
    - requirements
    - features
    - releases
capabilities:
  - define_requirements
  - acceptance_testing
  - prioritize_features
```

### 前端开发（Developer）
```yaml
role: frontend-dev
level: developer
permissions:
  read:
    - docs/
    - src/frontend/
    - src/shared/
    - .agents/*/frontend/
  write:
    - src/frontend/
    - tests/frontend/
    - docs/frontend/
  create:
    - components
    - pages
    - styles
    - frontend-tests
capabilities:
  - implement_ui
  - write_frontend_tests
  - create_pull_requests
restrictions:
  - cannot_modify_backend
  - cannot_modify_infrastructure
  - cannot_deploy_production
```

### 后端开发（Developer）
```yaml
role: backend-dev
level: developer
permissions:
  read:
    - docs/
    - src/backend/
    - src/shared/
    - .agents/*/backend/
  write:
    - src/backend/
    - tests/backend/
    - docs/api/
  create:
    - api-endpoints
    - services
    - models
    - backend-tests
capabilities:
  - implement_api
  - write_backend_tests
  - create_pull_requests
  - modify_database_schema
restrictions:
  - cannot_modify_frontend
  - cannot_modify_infrastructure
  - cannot_deploy_production
```

### 测试工程师（Developer）
```yaml
role: test-engineer
level: developer
permissions:
  read: ["*"]
  write:
    - tests/
    - .github/workflows/test-*.yml
    - docs/testing/
  create:
    - test-cases
    - test-suites
    - test-reports
  approve:
    - bug-fixes
    - test-coverage
capabilities:
  - write_tests
  - run_tests
  - verify_fixes
  - report_bugs
restrictions:
  - cannot_modify_source_code
  - cannot_deploy
```

### 运维工程师（Operator）
```yaml
role: devops-engineer
level: operator
permissions:
  read: ["*"]
  write:
    - deploy/
    - .github/workflows/
    - Makefile
    - docker-compose.yml
    - k8s/
  create:
    - deployment-configs
    - ci-cd-pipelines
    - monitoring-configs
  execute:
    - deploy_dev
    - deploy_staging
    - rollback
    - scale
  approve:
    - deployment_staging
capabilities:
  - manage_infrastructure
  - configure_ci_cd
  - monitor_systems
  - handle_incidents
restrictions:
  - cannot_deploy_production_without_approval
  - cannot_modify_source_code
```

### 运营人员（Viewer）
```yaml
role: operations
level: viewer
permissions:
  read:
    - docs/
    - logs/
    - metrics/
    - dashboards/
  write:
    - config/operations/
    - docs/operations/
  create:
    - reports
    - dashboards
    - alerts
capabilities:
  - view_metrics
  - create_reports
  - configure_alerts
restrictions:
  - cannot_modify_code
  - cannot_deploy
  - cannot_access_production_data
```

## 角色申请流程

### 1. 提交申请
```bash
# 使用 CLI
python3 scripts/ironclaw.py request-role --role=backend-dev --reason="加入后端团队"

# 或通过对话
claude-code
> 申请后端开发角色，我有 3 年 Python 开发经验
```

### 2. 申请内容
```yaml
role_request:
  applicant: user@example.com
  role: backend-dev
  reason: 加入后端团队开发用户模块
  experience:
    - 3 年 Python 开发经验
    - 熟悉 FastAPI 框架
    - 有微服务架构经验
  references:
    - github.com/user/project1
    - github.com/user/project2
```

### 3. 架构师审批
```bash
# 查看待审批申请
python3 scripts/ironclaw.py list-requests

# 审批申请
python3 scripts/ironclaw.py approve-request --id=REQ-001

# 拒绝申请
python3 scripts/ironclaw.py reject-request --id=REQ-001 --reason="需要更多经验"
```

### 4. 自动分配权限
审批通过后，系统自动：
- 创建角色配置
- 分配权限
- 生成 IronClaw 实例
- 发送欢迎邮件

## IronClaw 实例

每个角色拥有独立的 IronClaw 实例：

```
my-project/
├── .claude/
│   └── ironclaw/
│       ├── instances/
│       │   ├── architect-alice.yml
│       │   ├── backend-bob.yml
│       │   ├── frontend-charlie.yml
│       │   └── test-david.yml
│       ├── permissions.yml
│       └── workflows.yml
```

### 实例配置示例
```yaml
# .claude/ironclaw/instances/backend-bob.yml
user: bob@example.com
role: backend-dev
level: developer
granted_at: 2024-01-15T10:00:00Z
granted_by: architect-alice
expires_at: null  # 永久有效，除非撤销

permissions:
  read:
    - docs/
    - src/backend/
    - src/shared/
  write:
    - src/backend/
    - tests/backend/
  create:
    - api-endpoints
    - services
    - models

restrictions:
  - cannot_modify_frontend
  - cannot_modify_infrastructure
  - cannot_deploy_production

audit_log:
  - timestamp: 2024-01-15T10:30:00Z
    action: create_file
    target: src/backend/api/users.py
    result: success

  - timestamp: 2024-01-15T11:00:00Z
    action: create_pull_request
    target: PR-123
    result: success

  - timestamp: 2024-01-15T11:30:00Z
    action: deploy_production
    target: production
    result: denied
    reason: insufficient_permissions
```

## 权限检查

### 自动检查
所有操作都会自动进行权限检查：

```python
# 示例：后端开发尝试修改前端代码
@require_permission("write", "src/frontend/")
def modify_frontend_code(file_path):
    # 如果没有权限，会抛出 PermissionDenied 异常
    pass
```

### 手动检查
```bash
# 检查当前用户权限
python3 scripts/ironclaw.py check-permission --action=write --target=src/backend/

# 检查特定用户权限
python3 scripts/ironclaw.py check-permission --user=bob@example.com --action=deploy --target=production
```

## 审计日志

所有操作都会记录审计日志：

```yaml
# .claude/ironclaw/audit.log
- timestamp: 2024-01-15T10:00:00Z
  user: architect-alice
  action: approve_role_request
  target: REQ-001
  details:
    applicant: bob@example.com
    role: backend-dev
  result: success

- timestamp: 2024-01-15T10:30:00Z
  user: backend-bob
  action: create_file
  target: src/backend/api/users.py
  result: success

- timestamp: 2024-01-15T11:30:00Z
  user: backend-bob
  action: deploy_production
  target: production
  result: denied
  reason: insufficient_permissions
```

## 最佳实践

### 1. 定期审查权限
架构师应定期审查角色权限，确保符合最小权限原则。

### 2. 及时撤销权限
当成员离开项目时，立即撤销其权限。

### 3. 使用临时权限
对于临时任务，可以授予临时权限，自动过期。

### 4. 监控异常操作
定期检查审计日志，发现异常操作。

### 5. 权限分离
避免一个人拥有过多权限，实现职责分离。
