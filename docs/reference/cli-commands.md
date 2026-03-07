# Amazing 角色命令快速参考

## 查看所有角色

```bash
python3 scripts/amazing-cli.py role list
```

输出:
```
产品经理 (pm):
  权限: prd:create, prd:edit, requirement:review...
  技能: prd-generator, requirement-analyzer, prototype-design...

前端开发 (frontend):
  权限: ui:develop, component:create, style:edit...
  技能: react-component, ui-design, state-management...

后端开发 (backend):
  权限: api:develop, database:design, service:create...
  技能: api-design, database-design, auth-implement...

测试工程师 (qa):
  权限: test:design, test:execute, bug:report...
  技能: test-design, automation, bug-tracking...

运维工程师 (ops):
  权限: deploy:execute, monitor:configure, troubleshoot:debug...
  技能: deployment, monitoring, troubleshooting...

运营人员 (operation):
  权限: data:analyze, config:manage, user:operate...
  技能: data-analysis, user-operation, config-management...
```

## 设置角色 (非交互式)

### 产品经理
```bash
python3 scripts/amazing-cli.py role set pm
```

### 前端开发
```bash
python3 scripts/amazing-cli.py role set frontend
```

### 后端开发
```bash
python3 scripts/amazing-cli.py role set backend
```

### 测试工程师
```bash
python3 scripts/amazing-cli.py role set qa
```

### 运维工程师
```bash
python3 scripts/amazing-cli.py role set ops
```

### 运营人员
```bash
python3 scripts/amazing-cli.py role set operation
```

## 选择角色 (交互式)

```bash
python3 scripts/amazing-cli.py role select
```

会提示你选择:
```
可用角色:
1. 产品经理 (pm)
2. 前端开发 (frontend)
3. 后端开发 (backend)
4. 测试工程师 (qa)
5. 运维工程师 (ops)
6. 运营人员 (operation)
请选择角色: 
```

## 查看当前角色

```bash
python3 scripts/amazing-cli.py status
```

## 角色权限说明

### 产品经理 (pm)
- **权限**: 创建/编辑 PRD、需求评审、功能批准、验收测试
- **技能**: PRD 生成、需求分析、原型设计
- **工具**: Claude Code, Codex

### 前端开发 (frontend)
- **权限**: UI 开发、组件创建、样式编辑、前端部署
- **技能**: React 组件、UI 设计、状态管理、性能优化
- **技术栈**: React, TypeScript, Vite, TailwindCSS

### 后端开发 (backend)
- **权限**: API 开发、数据库设计、服务创建、后端部署
- **技能**: API 设计、数据库设计、认证实现、微服务
- **技术栈**: Python (FastAPI), Go (Gin), PostgreSQL, Redis

### 测试工程师 (qa)
- **权限**: 测试设计、测试执行、Bug 报告、质量审查
- **技能**: 测试设计、自动化测试、Bug 追踪、性能测试
- **技术栈**: Pytest, Jest, Playwright, JMeter

### 运维工程师 (ops)
- **权限**: 部署执行、监控配置、故障排查、基础设施管理
- **技能**: 部署、监控、故障排查、K8s 管理
- **技术栈**: Docker, Kubernetes, Prometheus, Grafana

### 运营人员 (operation)
- **权限**: 数据分析、配置管理、用户运营
- **技能**: 数据分析、用户运营、配置管理
- **技术栈**: SQL, Python, Jupyter

## 使用示例

### 场景 1: 产品经理创建需求

```bash
# 1. 设置角色
python3 scripts/amazing-cli.py role set pm

# 2. 创建 PRD
python3 scripts/amazing-cli.py prd create "用户权限管理模块"

# 3. 使用 Claude Code 生成详细 PRD
claude "生成 PRD: 用户权限管理模块，包含功能设计、技术方案、验收标准"
```

### 场景 2: 前端开发实现功能

```bash
# 1. 设置角色
python3 scripts/amazing-cli.py role set frontend

# 2. 启动开发服务器
cd frontend
npm run dev

# 3. 使用 Claude Code 开发
claude "创建用户列表组件，支持分页、搜索、排序" --role frontend
```

### 场景 3: 后端开发实现 API

```bash
# 1. 设置角色
python3 scripts/amazing-cli.py role set backend

# 2. 启动开发服务器
cd backend/python
python3 main.py

# 3. 使用 Claude Code 开发
claude "实现用户管理 API，包含 CRUD 操作" --role backend
```

### 场景 4: 测试工程师编写测试

```bash
# 1. 设置角色
python3 scripts/amazing-cli.py role set qa

# 2. 使用 Claude Code 生成测试
claude "为用户登录功能编写测试用例" --role qa

# 3. 运行测试
pytest
```

### 场景 5: 运维工程师部署应用

```bash
# 1. 设置角色
python3 scripts/amazing-cli.py role set ops

# 2. 部署到 K8s
make k8s-deploy

# 3. 查看状态
kubectl get pods -n amazing
```

## 快捷命令别名

可以在 `~/.zshrc` 或 `~/.bashrc` 中添加别名:

```bash
# Amazing CLI 别名
alias amazing="python3 ~/minger/amazing/scripts/amazing-cli.py"
alias amazing-pm="python3 ~/minger/amazing/scripts/amazing-cli.py role set pm"
alias amazing-fe="python3 ~/minger/amazing/scripts/amazing-cli.py role set frontend"
alias amazing-be="python3 ~/minger/amazing/scripts/amazing-cli.py role set backend"
alias amazing-qa="python3 ~/minger/amazing/scripts/amazing-cli.py role set qa"
alias amazing-ops="python3 ~/minger/amazing/scripts/amazing-cli.py role set ops"
```

然后可以直接使用:
```bash
amazing-pm      # 设置为产品经理
amazing-fe      # 设置为前端开发
amazing-be      # 设置为后端开发
amazing-qa      # 设置为测试工程师
amazing-ops     # 设置为运维工程师
```

## 更多信息

- 完整文档: [docs/ROLE_ONBOARDING.md](./docs/ROLE_ONBOARDING.md)
- Claude Code 使用: [docs/CLAUDE_CODE_GUIDE.md](./docs/CLAUDE_CODE_GUIDE.md)
- 文档索引: [docs/INDEX.md](./docs/INDEX.md)
