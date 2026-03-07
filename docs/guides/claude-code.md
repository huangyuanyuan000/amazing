# Claude Code (龙虾) 接入指南

## 概述

Claude Code (龙虾) 是 Amazing 平台的主力 AI 开发工具。本文档详细说明如何配置和使用 Claude Code 进行协同开发。

---

## 1. 安装 Claude Code

### 1.1 前置要求

- macOS / Linux / Windows
- 终端访问权限
- Anthropic API Key

### 1.2 安装步骤

**macOS / Linux**:
```bash
# 使用 npm 安装
npm install -g @anthropic-ai/claude-code

# 或使用 curl 安装
curl -fsSL https://claude.ai/install.sh | sh

# 验证安装
claude --version
```

**Windows**:
```powershell
# 使用 npm 安装
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

---

## 2. 配置 Claude Code

### 2.1 设置 API Key

```bash
# 设置 API Key
claude auth login

# 或使用环境变量
export ANTHROPIC_API_KEY="your-api-key-here"

# 验证配置
claude auth status
```

### 2.2 项目配置

Amazing 项目已包含 Claude Code 配置文件 `.claude/config.json`：

```json
{
  "toolchain": {
    "priority": ["claude-code", "codex-cli", "codex-desktop"],
    "claude-code": {
      "enabled": true,
      "model": "claude-sonnet-4-6",
      "config": {
        "temperature": 0.7,
        "max_tokens": 4096
      }
    }
  }
}
```

### 2.3 角色配置

Claude Code 会根据你选择的角色自动加载对应的配置：

```bash
# 选择角色
python3 scripts/amazing-cli.py role select

# Claude Code 会自动读取角色配置
# 配置文件: .claude/roles/config.json
```

---

## 3. 使用 Claude Code

### 3.1 基础用法

**交互式模式**:
```bash
# 启动 Claude Code
claude

# 进入交互式对话
> 帮我创建一个用户列表组件
```

**命令行模式**:
```bash
# 直接执行任务
claude "创建用户列表组件，使用 React + TypeScript"

# 指定文件
claude "优化这个文件的性能" --file src/components/UserList.tsx

# 指定角色
claude "作为前端开发，实现用户列表组件" --role frontend
```

### 3.2 场景化使用

#### 场景 1: 功能开发 (PM)

```bash
# 1. 需求分析
claude "分析需求: 用户权限管理模块，需要支持角色管理、权限分配、审计日志"

# 2. 生成 PRD
claude "根据需求生成 PRD，包含功能设计、技术方案、验收标准" \
  --output docs/prd/user-permission.md

# 3. 技术评审
claude "评审 PRD，给出技术实现建议" \
  --file docs/prd/user-permission.md
```

#### 场景 2: 前端开发

```bash
# 1. 创建组件
claude "创建 UserList 组件，显示用户列表，支持分页和搜索" \
  --role frontend \
  --output frontend/src/components/UserList.tsx

# 2. 创建 Store
claude "创建 userStore，使用 Zustand 管理用户状态" \
  --role frontend \
  --output frontend/src/stores/userStore.ts

# 3. 创建 API 调用
claude "创建 userApi，调用后端 /api/v1/users 接口" \
  --role frontend \
  --output frontend/src/api/user.ts

# 4. 编写测试
claude "为 UserList 组件编写单元测试" \
  --role frontend \
  --output frontend/src/components/UserList.test.tsx
```

#### 场景 3: 后端开发

```bash
# 1. 设计 API
claude "设计用户管理 API，包含 CRUD 操作，使用 FastAPI" \
  --role backend

# 2. 实现接口
claude "实现用户创建接口，包含参数验证、密码加密、数据库保存" \
  --role backend \
  --output backend/python/app/api/users.py

# 3. 数据库模型
claude "创建 User 模型，包含 id, name, email, role, created_at 字段" \
  --role backend \
  --output backend/python/app/models/user.py

# 4. 编写测试
claude "为用户创建接口编写单元测试和集成测试" \
  --role backend \
  --output backend/python/tests/test_users.py
```

#### 场景 4: Bug 修复

```bash
# 1. 分析 Bug
claude "分析这个 Bug，定位问题原因" \
  --file backend/python/app/api/users.py \
  --context "用户登录失败，返回 500 错误"

# 2. 修复代码
claude "修复用户登录接口的 Bug" \
  --file backend/python/app/api/users.py

# 3. 编写测试
claude "为 Bug 修复编写回归测试" \
  --output backend/python/tests/test_login_fix.py
```

#### 场景 5: 代码审查 (Review Agent)

```bash
# 1. 代码审查
claude "审查这段代码，检查代码质量、安全性、性能" \
  --file backend/python/app/api/users.py \
  --role review

# 2. 生成审查报告
claude "生成代码审查报告" \
  --output docs/reviews/users-api-review.md
```

### 3.3 高级用法

#### 多文件操作

```bash
# 同时处理多个文件
claude "重构用户模块，优化代码结构" \
  --files "backend/python/app/api/users.py,backend/python/app/models/user.py"
```

#### 上下文管理

```bash
# 使用项目上下文
claude "基于现有代码风格，实现用户删除功能" \
  --context-files "backend/python/app/api/*.py"
```

#### 批量操作

```bash
# 批量生成测试
claude "为所有 API 接口生成单元测试" \
  --glob "backend/python/app/api/*.py"
```

---

## 4. 与 Agent 系统集成

### 4.1 Agent 调用

Claude Code 会自动与 Agent 系统集成：

```bash
# 通过 Agent 调用 Claude Code
python3 scripts/amazing-cli.py agent run common \
  --task "实现用户管理功能" \
  --tool claude-code
```

### 4.2 Sub-Agent 协作

```bash
# PM Sub-Agent
python3 scripts/amazing-cli.py agent run common.pm \
  --task "生成 PRD"

# Frontend Sub-Agent
python3 scripts/amazing-cli.py agent run common.frontend \
  --task "实现 UI"

# Backend Sub-Agent
python3 scripts/amazing-cli.py agent run common.backend \
  --task "实现 API"
```

### 4.3 Skill 调用

```bash
# 使用 Skill
python3 scripts/amazing-cli.py skill run prd-generator \
  --input "用户权限管理模块"

# Claude Code 会自动执行 Skill
```

---

## 5. 工作流集成

### 5.1 功能开发流程

```bash
# 1. PM: 需求分析
claude "分析需求: 用户权限管理" --role pm

# 2. PM: 生成 PRD
claude "生成 PRD" --role pm --output docs/prd/user-permission.md

# 3. Frontend: 实现 UI
claude "实现用户权限管理 UI" --role frontend

# 4. Backend: 实现 API
claude "实现用户权限管理 API" --role backend

# 5. QA: 编写测试
claude "编写测试用例" --role qa

# 6. Review: 代码审查
claude "审查代码" --role review

# 7. Ops: 部署
claude "生成部署脚本" --role ops
```

### 5.2 Bug 修复流程

```bash
# 1. QA: Bug 复现
claude "复现 Bug: 用户登录失败" --role qa

# 2. Backend: 定位问题
claude "定位问题原因" --role backend --file backend/python/app/api/auth.py

# 3. Backend: 修复代码
claude "修复 Bug" --role backend

# 4. QA: 回归测试
claude "编写回归测试" --role qa

# 5. Ops: 热修复部署
claude "生成热修复部署脚本" --role ops
```

---

## 6. 配置优化

### 6.1 性能优化

```json
{
  "claude-code": {
    "config": {
      "temperature": 0.7,
      "max_tokens": 4096,
      "cache_enabled": true,
      "parallel_requests": 3
    }
  }
}
```

### 6.2 角色定制

编辑 `.claude/roles/config.json` 定制角色行为：

```json
{
  "roles": {
    "frontend": {
      "name": "前端开发",
      "skills": ["react-component", "ui-design"],
      "tools": ["claude-code"],
      "techStack": ["React", "TypeScript", "Vite"]
    }
  }
}
```

### 6.3 Skill 定制

编辑 `.claude/skills/config.json` 定制 Skill：

```json
{
  "skills": {
    "prd-generator": {
      "name": "PRD 生成器",
      "template": "prd-template.md",
      "tools": ["claude-code"]
    }
  }
}
```

---

## 7. 降级机制

当 Claude Code 不可用时，自动降级到 Codex：

```bash
# 配置降级
# .claude/config.json
{
  "toolchain": {
    "priority": ["claude-code", "codex-cli", "codex-desktop"],
    "fallback": true
  }
}
```

使用时会自动切换：
```bash
# 优先使用 Claude Code
python3 scripts/amazing-cli.py agent run common --task "实现功能"

# 如果 Claude Code 不可用，自动切换到 Codex CLI
# 如果 Codex CLI 不可用，自动切换到 Codex Desktop
```

---

## 8. 最佳实践

### 8.1 清晰的任务描述

```bash
# ❌ 不好的描述
claude "做个用户列表"

# ✅ 好的描述
claude "创建用户列表组件，使用 React + TypeScript，支持分页、搜索、排序功能，使用 Ant Design 组件库"
```

### 8.2 提供上下文

```bash
# 提供相关文件作为上下文
claude "基于现有代码风格，实现用户删除功能" \
  --context-files "backend/python/app/api/users.py"
```

### 8.3 分步执行

```bash
# 复杂任务分步执行
claude "第一步: 设计用户管理 API 接口"
claude "第二步: 实现用户创建接口"
claude "第三步: 实现用户查询接口"
```

### 8.4 验证结果

```bash
# 生成代码后立即测试
claude "实现用户创建接口"
pytest backend/python/tests/test_users.py
```

---

## 9. 常见问题

### Q: Claude Code 连接失败？
A: 检查 API Key 配置和网络连接。

### Q: 如何切换模型？
A: 编辑 `.claude/config.json`，修改 `model` 字段。

### Q: 如何查看 Claude Code 日志？
A: 日志保存在 `.claude/logs/` 目录。

### Q: 如何自定义 Skill？
A: 编辑 `.claude/skills/config.json`，添加自定义 Skill。

### Q: 如何与团队共享配置？
A: 将 `.claude/` 目录提交到 Git 仓库。

---

## 10. 进阶功能

### 10.1 自定义 Prompt

创建自定义 Prompt 模板：

```bash
# .claude/prompts/custom-api.md
你是一个后端开发专家，请帮我实现以下 API:

功能: {功能描述}
技术栈: FastAPI + PostgreSQL
要求:
- 使用 RESTful 规范
- 包含参数验证
- 包含错误处理
- 包含单元测试
```

使用自定义 Prompt:
```bash
claude --prompt custom-api --vars "功能描述=用户创建接口"
```

### 10.2 批量处理

```bash
# 批量生成测试
for file in backend/python/app/api/*.py; do
  claude "为这个文件生成单元测试" --file "$file"
done
```

### 10.3 CI/CD 集成

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Claude Code Review
        run: |
          claude "审查 PR 代码，给出改进建议" \
            --files "$(git diff --name-only origin/main)"
```

---

## 11. 资源链接

- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Amazing 项目文档](./README.md)
- [角色指南](./ROLE_ONBOARDING.md)
- [技术规范](./docs/specs/README.md)

---

## 12. 获取帮助

```bash
# Claude Code 帮助
claude --help

# Amazing CLI 帮助
python3 scripts/amazing-cli.py --help

# 查看示例
claude examples
```
