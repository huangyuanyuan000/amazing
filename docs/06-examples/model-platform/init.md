# 大模型管理平台初始化操作流程

## 概述

本文档演示如何使用 Amazing 脚手架初始化一个大模型管理平台项目。

## 前置条件

- 已安装 Amazing CLI
- 已选择架构师角色
- 了解大模型管理平台的基本需求

## 完整流程

### 步骤 1：安装 Amazing CLI

```bash
# 使用 pip 安装
pip install amazing-cli

# 或使用 npm 安装
npm install -g amazing-cli

# 验证安装
amazing-cli --version
```

**预期输出**:
```
Amazing CLI v1.0.0
```

---

### 步骤 2：初始化项目

```bash
# 创建新项目
amazing-cli init ai-model-platform

# 或使用交互式模式
amazing-cli init
```

**交互过程**:
```
? 项目名称: ai-model-platform
? 项目描述: 企业级大模型管理平台
? 作者: Your Name
? 许可证: MIT

✅ 项目基本信息已设置
```

---

### 步骤 3：描述产品形态

```
📋 请描述你的产品形态

? 产品类型:
  ○ 电商平台
  ○ SaaS 应用
  ● AI/ML 平台
  ○ 企业管理系统
  ○ 其他

? 请详细描述产品功能（支持多行输入，输入 'done' 结束）:
```

**输入内容**:
```
我要构建一个企业级大模型管理平台，核心功能包括：

1. 算力资源管理
   - GPU/CPU 资源池管理
   - 资源调度和分配
   - 资源监控和告警
   - 成本统计和优化

2. 数据管理
   - 数据集上传和管理
   - 数据标注工具
   - 数据版本控制
   - 数据质量检查

3. 模型训练
   - 训练任务创建和管理
   - 分布式训练支持
   - 超参数调优
   - 实验跟踪和对比

4. 模型服务
   - 模型版本管理
   - 模型部署和推理
   - API 服务管理
   - 性能监控

5. 用户和权限
   - 多租户支持
   - 角色权限管理
   - 审计日志
   - 配额管理

done
```

**AI 分析**:
```
✨ AI 正在分析你的产品形态...

📊 产品分析结果：
- 产品类型: AI/ML 平台
- 核心模块: 5 个
- 复杂度: 高
- 推荐团队规模: 10-15 人
- 预计开发周期: 6-9 个月
```

---

### 步骤 4：选择业务划分方案

```
🎯 基于你的产品描述，AI 推荐以下业务划分方案：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
方案 A：按资源类型划分（推荐）⭐
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

优势：
✓ 职责清晰，每个 Agent 管理一类资源
✓ 易于扩展，新增资源类型只需添加 Agent
✓ 便于优化，可针对不同资源类型优化

业务 Agent：
1. 💻 Compute Agent - 算力资源管理
   - GPU/CPU 资源池
   - 资源调度
   - 监控告警

2. 📊 Data Agent - 数据资源管理
   - 数据集管理
   - 数据标注
   - 版本控制

3. 🎓 Training Agent - 训练任务管理
   - 训练任务
   - 实验跟踪
   - 超参数调优

4. 🚀 Model-Service Agent - 模型服务管理
   - 模型部署
   - API 服务
   - 性能监控

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
方案 B：按功能流程划分
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

优势：
✓ 符合用户使用流程
✓ 便于理解和使用

业务 Agent：
1. 📦 Resource Agent - 资源管理
   - 算力资源
   - 数据资源

2. 🔄 Workflow Agent - 工作流管理
   - 训练流程
   - 推理流程

3. 🛠️ Service Agent - 服务管理
   - API 服务
   - 监控告警

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
方案 C：按用户角色划分
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

优势：
✓ 权限管理简单
✓ 符合组织结构

业务 Agent：
1. 👨‍💼 Admin Agent - 管理员功能
2. 👨‍💻 Developer Agent - 开发者功能
3. 👤 User Agent - 用户功能

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? 请选择方案：
  ● 方案 A - 按资源类型划分（推荐）
  ○ 方案 B - 按功能流程划分
  ○ 方案 C - 按用户角色划分
  ○ 自定义方案
```

**选择**: 方案 A

---

### 步骤 5：架构师确认和调整

```
👑 架构师模式已启用

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
当前业务 Agent 配置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 💻 Compute Agent
   名称: 算力资源管理
   职责: GPU/CPU 资源池、调度、监控

2. 📊 Data Agent
   名称: 数据资源管理
   职责: 数据集、标注、版本控制

3. 🎓 Training Agent
   名称: 训练任务管理
   职责: 训练任务、实验跟踪、调优

4. 🚀 Model-Service Agent
   名称: 模型服务管理
   职责: 模型部署、API、监控

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? 是否需要调整？
  ○ 确认，继续下一步
  ● 调整 Agent 配置
  ○ 添加新 Agent
  ○ 删除 Agent
  ○ 重新选择方案
```

**调整示例**:
```
? 选择要调整的 Agent:
  ● 1. Compute Agent
  ○ 2. Data Agent
  ○ 3. Training Agent
  ○ 4. Model-Service Agent

? 新的 Agent 名称（留空保持不变）:
  算力平台

? 新的 Agent 描述（留空保持不变）:
  负责 GPU/CPU 资源的统一管理、调度和监控，支持多集群管理

✅ 已更新 Compute Agent → 算力平台 Agent

? 继续调整其他 Agent？
  ○ 是
  ● 否，确认配置
```

---

### 步骤 6：配置技术栈

```
🔧 配置技术栈

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
算力平台 Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? 后端语言:
  ● Python（推荐 - 适合 AI/ML 场景）
  ○ Go（高性能）
  ○ Java（企业级）
  ○ Node.js（全栈 JS）
  ○ 自定义

? 后端框架:
  ● FastAPI（推荐 - 现代、高性能）
  ○ Flask（轻量级）
  ○ Django（全功能）
  ○ 自定义

? 数据库:
  ● PostgreSQL（推荐 - 功能强大）
  ○ MySQL（流行）
  ○ MongoDB（文档型）
  ○ 自定义

? 缓存:
  ● Redis（推荐）
  ○ Memcached
  ○ 不使用缓存

? 消息队列:
  ● RabbitMQ（推荐）
  ○ Kafka（高吞吐）
  ○ Redis（轻量级）
  ○ 不使用队列

✅ 算力平台 Agent 技术栈配置完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
数据 Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? 使用相同的技术栈？
  ● 是（推荐 - 保持一致性）
  ○ 否（自定义）

✅ 数据 Agent 技术栈配置完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
训练 Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? 使用相同的技术栈？
  ● 是
  ○ 否

✅ 训练 Agent 技术栈配置完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
模型服务 Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? 后端语言:
  ○ Python
  ● Go（推荐 - 高性能推理服务）
  ○ Java
  ○ 自定义

? 后端框架:
  ● Gin（推荐 - 高性能）
  ○ Echo
  ○ Fiber
  ○ 自定义

✅ 模型服务 Agent 技术栈配置完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
前端配置
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

? 前端框架:
  ● React（推荐）
  ○ Vue
  ○ Angular
  ○ Svelte

? UI 组件库:
  ● Ant Design（推荐 - 企业级）
  ○ Material-UI
  ○ Chakra UI
  ○ 自定义

? 状态管理:
  ● Zustand（推荐 - 轻量级）
  ○ Redux
  ○ MobX
  ○ Context API

✅ 前端技术栈配置完成
```

---

### 步骤 7：配置部署方式

```
🚀 配置部署方式

? 部署环境:
  ☑ 本地开发（Docker Compose）
  ☑ 测试环境（Docker Compose）
  ☑ 生产环境（Kubernetes）

? 容器化:
  ● 是（推荐）
  ○ 否

? CI/CD:
  ● GitHub Actions（推荐）
  ○ GitLab CI
  ○ Jenkins
  ○ 不使用

? 监控方案:
  ● Prometheus + Grafana（推荐）
  ○ ELK Stack
  ○ 自定义
  ○ 不使用

✅ 部署配置完成
```

---

### 步骤 8：生成项目结构

```
🎉 正在生成项目结构...

[1/6] 创建目录结构...        ████████████████████ 100%
[2/6] 生成配置文件...        ████████████████████ 100%
[3/6] 初始化 Agent...        ████████████████████ 100%
[4/6] 生成文档...            ████████████████████ 100%
[5/6] 配置 Git...            ████████████████████ 100%
[6/6] 安装依赖...            ████████████████████ 100%

✅ 项目初始化完成！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
项目结构
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ai-model-platform/
├── .agents/                    # Agent 配置
│   ├── common/                # 通用 Agent（固定）
│   ├── review/                # 审核 Agent（固定）
│   ├── compute/               # 算力平台 Agent
│   ├── data/                  # 数据 Agent
│   ├── training/              # 训练 Agent
│   └── model-service/         # 模型服务 Agent
│
├── backend/                   # 后端代码
│   ├── compute/              # 算力平台服务
│   ├── data/                 # 数据服务
│   ├── training/             # 训练服务
│   └── model-service/        # 模型服务（Go）
│
├── frontend/                  # 前端代码
│   ├── src/
│   │   ├── pages/
│   │   │   ├── compute/     # 算力管理页面
│   │   │   ├── data/        # 数据管理页面
│   │   │   ├── training/    # 训练管理页面
│   │   │   └── model/       # 模型管理页面
│   │   └── components/
│   └── package.json
│
├── docs/                      # 文档
│   ├── architecture.md       # 架构文档
│   ├── agents.md             # Agent 说明
│   ├── api.md                # API 文档
│   └── deployment.md         # 部署文档
│
├── deploy/                    # 部署配置
│   ├── docker-compose.yml    # 本地/测试环境
│   ├── k8s/                  # Kubernetes 配置
│   └── ci/                   # CI/CD 配置
│
├── scripts/                   # 脚本工具
│   ├── amazing-cli.py        # CLI 工具
│   └── init.sh               # 初始化脚本
│
├── .gitignore
├── README.md
└── amazing.config.json       # Amazing 配置文件

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### 步骤 9：查看生成的配置

```bash
# 查看 Amazing 配置
cat amazing.config.json
```

**配置内容**:
```json
{
  "project": {
    "name": "ai-model-platform",
    "description": "企业级大模型管理平台",
    "version": "1.0.0",
    "author": "Your Name"
  },
  "architecture": {
    "pattern": "agent-teams",
    "mode": "semi-auto"
  },
  "agents": {
    "fixed": [
      {
        "name": "common",
        "type": "fixed",
        "description": "通用功能管理"
      },
      {
        "name": "review",
        "type": "fixed",
        "description": "代码和质量审核"
      }
    ],
    "business": [
      {
        "name": "compute",
        "displayName": "算力平台",
        "description": "GPU/CPU 资源管理、调度和监控",
        "techStack": {
          "backend": "Python + FastAPI",
          "database": "PostgreSQL",
          "cache": "Redis",
          "queue": "RabbitMQ"
        }
      },
      {
        "name": "data",
        "displayName": "数据管理",
        "description": "数据集管理、标注和版本控制",
        "techStack": {
          "backend": "Python + FastAPI",
          "database": "PostgreSQL",
          "cache": "Redis"
        }
      },
      {
        "name": "training",
        "displayName": "训练管理",
        "description": "训练任务、实验跟踪和调优",
        "techStack": {
          "backend": "Python + FastAPI",
          "database": "PostgreSQL",
          "cache": "Redis"
        }
      },
      {
        "name": "model-service",
        "displayName": "模型服务",
        "description": "模型部署、API 和监控",
        "techStack": {
          "backend": "Go + Gin",
          "database": "PostgreSQL",
          "cache": "Redis"
        }
      }
    ]
  },
  "roles": [
    "architect",
    "pm",
    "frontend",
    "backend",
    "qa",
    "ops"
  ],
  "frontend": {
    "framework": "React",
    "ui": "Ant Design",
    "stateManagement": "Zustand"
  },
  "deployment": {
    "local": "docker-compose",
    "production": "kubernetes",
    "ci": "github-actions",
    "monitoring": "prometheus-grafana"
  }
}
```

---

### 步骤 10：启动开发

```bash
# 进入项目目录
cd ai-model-platform

# 查看可用命令
amazing-cli --help

# 查看 Agent 列表
amazing-cli agent list

# 选择角色
amazing-cli role select

# 启动开发环境
amazing-cli dev
```

**预期输出**:
```
🚀 启动开发环境...

[1/4] 启动数据库...          ████████████████████ 100%
[2/4] 启动后端服务...        ████████████████████ 100%
[3/4] 启动前端服务...        ████████████████████ 100%
[4/4] 启动监控服务...        ████████████████████ 100%

✅ 开发环境已启动！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
服务地址
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

前端:     http://localhost:3000
后端 API: http://localhost:8000
API 文档: http://localhost:8000/docs
监控:     http://localhost:9090

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 下一步：
1. 访问 http://localhost:3000 查看前端
2. 访问 http://localhost:8000/docs 查看 API 文档
3. 使用 amazing-cli role select 选择角色开始开发
```

---

## 初始化后的项目结构详解

### Agent 配置目录

```
.agents/
├── common/                    # 通用 Agent（固定）
│   ├── config.json           # Agent 配置
│   ├── prompt.md             # Agent Prompt
│   └── sub-agents/           # Sub-Agent
│       ├── pm.json
│       ├── frontend.json
│       ├── backend.json
│       ├── qa.json
│       └── ops.json
│
├── compute/                   # 算力平台 Agent（业务）
│   ├── config.json
│   ├── prompt.md
│   ├── api-spec.yaml         # API 规范
│   ├── database-schema.sql   # 数据库设计
│   └── sub-agents/
│       ├── pm.json           # PM Sub-Agent
│       ├── frontend.json     # Frontend Sub-Agent
│       ├── backend.json      # Backend Sub-Agent
│       ├── qa.json           # QA Sub-Agent
│       └── ops.json          # Ops Sub-Agent
│
└── ...
```

### 后端代码目录

```
backend/
├── compute/                   # 算力平台服务
│   ├── app/
│   │   ├── api/              # API 路由
│   │   ├── models/           # 数据模型
│   │   ├── services/         # 业务逻辑
│   │   └── utils/            # 工具函数
│   ├── tests/                # 测试
│   ├── requirements.txt      # 依赖
│   └── main.py               # 入口文件
│
├── data/                      # 数据服务
├── training/                  # 训练服务
└── model-service/             # 模型服务（Go）
    ├── cmd/
    ├── internal/
    ├── pkg/
    └── go.mod
```

### 前端代码目录

```
frontend/
├── src/
│   ├── pages/
│   │   ├── compute/          # 算力管理页面
│   │   │   ├── ResourceList.tsx
│   │   │   ├── ResourceDetail.tsx
│   │   │   └── Monitoring.tsx
│   │   ├── data/             # 数据管理页面
│   │   ├── training/         # 训练管理页面
│   │   └── model/            # 模型管理页面
│   ├── components/           # 公共组件
│   ├── stores/               # 状态管理
│   ├── services/             # API 服务
│   └── App.tsx
└── package.json
```

---

## 常见问题

### Q1: 如何修改 Agent 配置？

```bash
# 编辑 Agent 配置
amazing-cli agent edit compute

# 或直接编辑配置文件
vim .agents/compute/config.json
```

### Q2: 如何添加新的业务 Agent？

```bash
# 添加新 Agent
amazing-cli agent create monitoring --description "监控告警管理"

# 配置技术栈
amazing-cli agent config monitoring
```

### Q3: 如何切换 AI 模式？

```bash
# 切换到全自动模式
amazing-cli mode set full-auto -r REQ-001

# 切换到半自动模式
amazing-cli mode set semi-auto -r REQ-002
```

### Q4: 如何查看架构文档？

```bash
# 生成架构文档
amazing-cli docs generate

# 查看架构图
amazing-cli docs view architecture
```

---

## 总结

通过以上流程，你已经成功初始化了一个大模型管理平台项目，包括：

✅ 4 个业务 Agent（算力、数据、训练、模型服务）
✅ 2 个固定 Agent（通用、审核）
✅ 完整的技术栈配置
✅ 前后端代码结构
✅ 部署配置
✅ 文档和 API 规范

下一步可以：
1. 选择角色开始开发
2. 使用 AI 辅助生成代码
3. 配置 CI/CD 流程
4. 部署到测试环境

---

**相关文档**:
- [架构设计文档](../02-agent-teams/README.md)
- [Agent 创建指南](../02-agent-teams/business-agents/create-guide.md)
- [技术栈配置](../04-tech-stack/README.md)
- [开发工作流](../05-workflows/development.md)
