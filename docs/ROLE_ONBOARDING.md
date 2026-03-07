# 各工种接入指南

## 概述

Amazing 平台支持 6 种工种角色，每个角色都有专属的工作流程和工具。本文档详细说明各工种如何接入和使用平台。

---

## 1. 产品经理 (PM) 接入指南

### 1.1 角色设置

```bash
# 进入项目目录
cd ~/minger/amazing

# 选择 PM 角色
python3 scripts/amazing-cli.py role select
# 选择: 1. 产品经理 (pm)
```

### 1.2 工作流程

#### 步骤 1: 需求分析

```bash
# 使用 Claude Code 分析需求
claude-code "分析需求: 用户权限管理模块，需要支持角色管理、权限分配、审计日志"

# 或使用 Codex
codex "分析需求: 用户权限管理模块"
```

#### 步骤 2: 生成 PRD

```bash
# 创建 PRD
python3 scripts/amazing-cli.py prd create "用户权限管理模块"

# 使用 Claude Code 生成详细 PRD
claude-code "根据需求生成 PRD: 用户权限管理模块，包含功能设计、技术方案、验收标准"
```

PRD 会自动保存到 `docs/prd/` 目录。

#### 步骤 3: 分配任务

```bash
# 分配给 Common Agent
python3 scripts/amazing-cli.py agent assign common --task prd-001

# 查看任务状态
python3 scripts/amazing-cli.py status
```

#### 步骤 4: 跟踪进度

```bash
# 查看开发进度
python3 scripts/amazing-cli.py status --task prd-001

# 查看 Agent 工作日志
cat .agents/common/logs/prd-001.log
```

#### 步骤 5: 功能验收

```bash
# 运行验收测试
python3 scripts/amazing-cli.py test acceptance --task prd-001

# 批准上线
python3 scripts/amazing-cli.py approve --task prd-001
```

### 1.3 可用工具

- **Claude Code**: 主力开发工具
- **Codex CLI**: 备选工具
- **Codex Desktop**: 可视化操作

### 1.4 权限

- ✅ 创建/编辑 PRD
- ✅ 需求评审
- ✅ 功能批准
- ✅ 验收测试
- ❌ 代码开发
- ❌ 部署操作

---

## 2. 前端开发 (Frontend) 接入指南

### 2.1 角色设置

```bash
python3 scripts/amazing-cli.py role select
# 选择: 2. 前端开发 (frontend)
```

### 2.2 开发环境

```bash
# 启动前端开发服务器
cd frontend
npm run dev

# 访问: http://localhost:3000
```

### 2.3 工作流程

#### 步骤 1: 认领任务

```bash
# 查看可用任务
python3 scripts/amazing-cli.py tasks --role frontend

# 认领任务
python3 scripts/amazing-cli.py task claim <task-id>
```

#### 步骤 2: 开发组件

```bash
# 使用 Claude Code 生成组件
claude-code "创建 UserList 组件，显示用户列表，支持分页和搜索"

# 或使用 Skill
python3 scripts/amazing-cli.py skill run react-component --name UserList
```

#### 步骤 3: 状态管理

```bash
# 使用 Claude Code 创建 Store
claude-code "创建 userStore，使用 Zustand 管理用户状态"
```

#### 步骤 4: API 集成

```bash
# 使用 Claude Code 创建 API 调用
claude-code "创建 userApi，调用后端 /api/v1/users 接口"
```

#### 步骤 5: 测试

```bash
# 运行测试
npm run test

# 运行 Lint
npm run lint
```

#### 步骤 6: 提交代码

```bash
# 提交代码
git add .
git commit -m "feat(user): 添加用户列表组件"
git push
```

### 2.4 技术栈

- React 18
- TypeScript
- Vite
- TailwindCSS
- Zustand
- Axios

### 2.5 权限

- ✅ UI 开发
- ✅ 组件创建
- ✅ 样式编辑
- ✅ 前端部署
- ❌ 后端开发
- ❌ 数据库操作

---

## 3. 后端开发 (Backend) 接入指南

### 3.1 角色设置

```bash
python3 scripts/amazing-cli.py role select
# 选择: 3. 后端开发 (backend)
```

### 3.2 开发环境

```bash
# 启动 Python API
cd backend/python
python3 main.py

# 或启动 Go API
cd backend/go
go run main.go
```

### 3.3 工作流程

#### 步骤 1: 认领任务

```bash
python3 scripts/amazing-cli.py tasks --role backend
python3 scripts/amazing-cli.py task claim <task-id>
```

#### 步骤 2: 设计 API

```bash
# 使用 Claude Code 设计 API
claude-code "设计用户管理 API，包含 CRUD 操作，使用 FastAPI"
```

#### 步骤 3: 数据库设计

```bash
# 使用 Claude Code 设计数据库
claude-code "设计 User 表，包含 id, name, email, role, created_at 字段"
```

#### 步骤 4: 实现业务逻辑

```bash
# 使用 Claude Code 实现
claude-code "实现用户创建接口，包含参数验证、密码加密、数据库保存"
```

#### 步骤 5: 编写测试

```bash
# 使用 Claude Code 生成测试
claude-code "为用户创建接口编写单元测试和集成测试"

# 运行测试
pytest
```

#### 步骤 6: API 文档

访问 http://localhost:8000/docs 查看自动生成的 API 文档。

### 3.4 技术栈

**Python**:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- JWT

**Go**:
- Gin
- GORM
- PostgreSQL
- Redis
- gRPC

### 3.5 权限

- ✅ API 开发
- ✅ 数据库设计
- ✅ 服务创建
- ✅ 后端部署
- ❌ 前端开发
- ❌ 生产部署

---

## 4. 测试工程师 (QA) 接入指南

### 4.1 角色设置

```bash
python3 scripts/amazing-cli.py role select
# 选择: 4. 测试工程师 (qa)
```

### 4.2 工作流程

#### 步骤 1: 查看待测试任务

```bash
python3 scripts/amazing-cli.py tasks --role qa --status ready-for-test
```

#### 步骤 2: 设计测试用例

```bash
# 使用 Claude Code 生成测试用例
claude-code "为用户登录功能设计测试用例，包含正常流程、异常流程、边界条件"
```

#### 步骤 3: 编写自动化测试

```bash
# Python 后端测试
cd backend/python
claude-code "编写用户登录接口的自动化测试"

# 前端测试
cd frontend
claude-code "编写用户登录组件的自动化测试"
```

#### 步骤 4: 执行测试

```bash
# 后端测试
cd backend/python
pytest

# 前端测试
cd frontend
npm run test

# E2E 测试
npm run test:e2e
```

#### 步骤 5: Bug 报告

```bash
# 创建 Bug 报告
python3 scripts/amazing-cli.py bug create \
  --title "用户登录失败" \
  --description "输入错误密码时未显示错误提示" \
  --severity high
```

### 4.3 技术栈

- Pytest (Python)
- Jest (JavaScript)
- Playwright (E2E)
- JMeter (性能测试)

### 4.4 权限

- ✅ 测试设计
- ✅ 测试执行
- ✅ Bug 报告
- ✅ 质量审查
- ❌ 代码开发
- ❌ 部署操作

---

## 5. 运维工程师 (Ops) 接入指南

### 5.1 角色设置

```bash
python3 scripts/amazing-cli.py role select
# 选择: 5. 运维工程师 (ops)
```

### 5.2 工作流程

#### 步骤 1: 环境准备

```bash
# 启动数据库
docker-compose -f docker-compose.dev.yml up -d

# 检查服务状态
docker-compose -f docker-compose.dev.yml ps
```

#### 步骤 2: 部署应用

**本地部署**:
```bash
make dev
```

**Docker 部署**:
```bash
make docker-up
```

**K8s 部署**:
```bash
make k8s-deploy
kubectl get pods -n amazing
```

#### 步骤 3: 监控

```bash
# 查看日志
docker-compose logs -f

# 查看资源使用
docker stats

# K8s 监控
kubectl top pods -n amazing
```

#### 步骤 4: 故障排查

```bash
# 使用 Claude Code 诊断问题
claude-code "分析日志，定位服务启动失败的原因"

# 查看详细日志
docker logs amazing-python-api
kubectl logs deployment/python-api -n amazing
```

#### 步骤 5: 回滚

```bash
# Docker 回滚
docker-compose down
docker-compose up -d

# K8s 回滚
kubectl rollout undo deployment/python-api -n amazing
```

### 5.3 技术栈

- Docker
- Kubernetes
- Prometheus
- Grafana
- ELK Stack

### 5.4 权限

- ✅ 部署执行
- ✅ 监控配置
- ✅ 故障排查
- ✅ 基础设施管理
- ❌ 代码开发
- ❌ 需求变更

---

## 6. 运营人员 (Operation) 接入指南

### 6.1 角色设置

```bash
python3 scripts/amazing-cli.py role select
# 选择: 6. 运营人员 (operation)
```

### 6.2 工作流程

#### 步骤 1: 数据分析

```bash
# 使用 Claude Code 分析数据
claude-code "分析用户活跃度数据，生成周报"
```

#### 步骤 2: 配置管理

```bash
# 查看配置
python3 scripts/amazing-cli.py config list

# 更新配置
python3 scripts/amazing-cli.py config set feature.new_ui true
```

#### 步骤 3: 用户运营

```bash
# 查看用户统计
python3 scripts/amazing-cli.py stats users

# 导出用户数据
python3 scripts/amazing-cli.py export users --format csv
```

### 6.3 技术栈

- SQL
- Python
- Jupyter Notebook
- Excel/CSV

### 6.4 权限

- ✅ 数据分析
- ✅ 配置管理
- ✅ 用户运营
- ❌ 代码开发
- ❌ 部署操作
- ❌ 数据库修改

---

## 通用操作

### 查看帮助

```bash
# CLI 帮助
python3 scripts/amazing-cli.py --help

# Make 帮助
make help
```

### 切换角色

```bash
python3 scripts/amazing-cli.py role select
```

### 查看权限

```bash
python3 scripts/amazing-cli.py role permissions
```

### 协作开发

```bash
# 查看团队任务
python3 scripts/amazing-cli.py tasks --team

# 查看某个任务的协作者
python3 scripts/amazing-cli.py task show <task-id>
```

---

## 常见问题

### Q: 如何切换工种？
A: 使用 `python3 scripts/amazing-cli.py role select` 命令。

### Q: 如何查看我的权限？
A: 使用 `python3 scripts/amazing-cli.py role permissions` 命令。

### Q: 如何与其他工种协作？
A: 通过任务系统，使用 `python3 scripts/amazing-cli.py tasks` 查看和认领任务。

### Q: 如何使用 AI 工具？
A: 优先使用 Claude Code，降级使用 Codex CLI 或 Codex Desktop。

### Q: 遇到问题怎么办？
A: 查看文档 `docs/` 目录，或使用 Claude Code 诊断问题。
