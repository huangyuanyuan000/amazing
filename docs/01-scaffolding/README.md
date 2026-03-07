# 脚手架层：Amazing CLI

## 概述

Amazing CLI 是 Amazing 平台的脚手架工具，类似于 vue-cli、create-react-app，用于快速初始化项目。

## 核心功能

### 1. 项目初始化

```bash
amazing-cli init <project-name>
```

**功能**：
- 创建项目目录结构
- 初始化配置文件
- 安装依赖
- 初始化 Git 仓库

### 2. 产品形态分析

**交互式问答**：
- 产品类型（电商/SaaS/AI平台/其他）
- 核心功能描述
- 用户规模
- 技术要求

**AI 分析**：
- 提取关键信息
- 识别业务模块
- 评估复杂度
- 推荐团队规模

### 3. 业务划分推荐

**AI 推荐 3-5 种方案**：
- 方案 A：按资源类型划分
- 方案 B：按功能流程划分
- 方案 C：按用户角色划分
- 方案 D：自定义

**每个方案包含**：
- 业务 Agent 列表
- 每个 Agent 的职责
- 优缺点分析
- 适用场景

### 4. 架构师确认

**架构师可以**：
- 选择推荐方案
- 调整 Agent 名称和职责
- 添加新 Agent
- 删除 Agent
- 完全自定义

### 5. 技术栈配置

**为每个业务 Agent 配置**：
- 后端语言和框架
- 数据库
- 缓存
- 消息队列
- 其他中间件

**提供**：
- 默认推荐（基于最佳实践）
- 自定义选择（基于团队能力）

### 6. 项目生成

**生成内容**：
- 目录结构
- 配置文件
- Agent 配置
- 文档模板
- 部署配置
- CI/CD 配置

---

## 使用流程

### 完整流程图

```
用户执行命令
    ↓
amazing-cli init my-project
    ↓
┌─────────────────────────────────────┐
│  步骤 1：项目基本信息                │
│  - 项目名称                          │
│  - 项目描述                          │
│  - 作者                              │
│  - 许可证                            │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  步骤 2：描述产品形态                │
│  - 产品类型                          │
│  - 核心功能（多行输入）              │
│  - 用户规模                          │
│  - 技术要求                          │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  步骤 3：AI 分析产品                 │
│  - 提取关键信息                      │
│  - 识别业务模块                      │
│  - 评估复杂度                        │
│  - 推荐团队规模                      │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  步骤 4：AI 推荐业务划分             │
│  - 方案 A（推荐）                    │
│  - 方案 B                            │
│  - 方案 C                            │
│  - 自定义                            │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  步骤 5：架构师确认和调整            │
│  - 选择方案                          │
│  - 调整 Agent 配置                   │
│  - 添加/删除 Agent                   │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  步骤 6：配置技术栈                  │
│  - 为每个 Agent 选择技术栈           │
│  - 默认推荐 or 自定义                │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  步骤 7：配置部署方式                │
│  - 本地开发（Docker Compose）        │
│  - 生产环境（Kubernetes）            │
│  - CI/CD（GitHub Actions）           │
│  - 监控（Prometheus + Grafana）      │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  步骤 8：生成项目结构                │
│  - 创建目录                          │
│  - 生成配置文件                      │
│  - 初始化 Agent                      │
│  - 生成文档                          │
│  - 配置 Git                          │
│  - 安装依赖                          │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│  完成！                              │
│  - 显示项目结构                      │
│  - 显示下一步操作                    │
└─────────────────────────────────────┘
```

---

## 命令参考

### 初始化命令

```bash
# 交互式初始化
amazing-cli init

# 指定项目名称
amazing-cli init my-project

# 使用模板
amazing-cli init my-project --template model-platform

# 跳过交互（使用默认配置）
amazing-cli init my-project --yes
```

### Agent 管理

```bash
# 列出所有 Agent
amazing-cli agent list

# 查看 Agent 详情
amazing-cli agent show compute

# 创建新 Agent
amazing-cli agent create monitoring --description "监控告警"

# 编辑 Agent 配置
amazing-cli agent edit compute

# 删除 Agent
amazing-cli agent delete monitoring
```

### 角色管理

```bash
# 选择角色
amazing-cli role select

# 查看当前角色
amazing-cli role show

# 切换角色
amazing-cli role set architect
```

### 开发命令

```bash
# 启动开发环境
amazing-cli dev

# 启动特定 Agent
amazing-cli dev compute

# 构建项目
amazing-cli build

# 运行测试
amazing-cli test
```

### 部署命令

```bash
# 部署到本地
amazing-cli deploy local

# 部署到 Kubernetes
amazing-cli deploy k8s

# 查看部署状态
amazing-cli deploy status
```

### 文档命令

```bash
# 生成文档
amazing-cli docs generate

# 查看架构图
amazing-cli docs view architecture

# 查看 API 文档
amazing-cli docs view api
```

---

## 配置文件

### amazing.config.json

项目的主配置文件：

```json
{
  "project": {
    "name": "my-project",
    "description": "项目描述",
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
        "description": "通用功能"
      },
      {
        "name": "review",
        "type": "fixed",
        "description": "质量审核"
      }
    ],
    "business": [
      {
        "name": "compute",
        "displayName": "算力平台",
        "description": "GPU/CPU 资源管理",
        "techStack": {
          "backend": "Python + FastAPI",
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

## 模板

### 内置模板

Amazing CLI 提供以下内置模板：

1. **model-platform** - 大模型管理平台
   - 算力管理
   - 数据管理
   - 训练管理
   - 模型服务

2. **e-commerce** - 电商平台
   - 商品管理
   - 订单管理
   - 支付管理
   - 物流管理

3. **saas** - SaaS 应用
   - 租户管理
   - 计费管理
   - 工作流
   - 报表

4. **blank** - 空白模板
   - 只包含固定 Agent
   - 完全自定义业务 Agent

### 使用模板

```bash
# 使用模板初始化
amazing-cli init my-project --template model-platform

# 列出所有模板
amazing-cli template list

# 查看模板详情
amazing-cli template show model-platform
```

---

## 最佳实践

### 1. 充分描述产品形态

**好的描述**：
```
我要构建一个企业级大模型管理平台，核心功能包括：

1. 算力资源管理
   - GPU/CPU 资源池管理
   - 资源调度和分配
   - 资源监控和告警

2. 数据管理
   - 数据集上传和管理
   - 数据标注工具
   - 数据版本控制

3. 模型训练
   - 训练任务创建
   - 分布式训练
   - 实验跟踪

4. 模型服务
   - 模型部署
   - API 服务
   - 性能监控
```

**不好的描述**：
```
做一个 AI 平台
```

### 2. 仔细评估 AI 推荐方案

**评估维度**：
- 职责是否清晰
- 是否易于扩展
- 是否符合团队结构
- 是否便于维护

### 3. 根据团队能力选择技术栈

**考虑因素**：
- 团队熟悉什么技术
- 学习成本
- 招聘难度
- 社区支持

### 4. 保持配置一致性

**建议**：
- 相似的 Agent 使用相同技术栈
- 统一的代码规范
- 统一的部署方式

---

## 常见问题

### Q1: 如何修改已生成的项目？

```bash
# 添加新 Agent
amazing-cli agent create monitoring

# 修改 Agent 配置
amazing-cli agent edit compute

# 重新生成文档
amazing-cli docs generate
```

### Q2: 如何使用自定义模板？

```bash
# 创建模板
amazing-cli template create my-template

# 使用自定义模板
amazing-cli init my-project --template my-template
```

### Q3: 如何升级 Amazing CLI？

```bash
# 使用 pip
pip install --upgrade amazing-cli

# 使用 npm
npm update -g amazing-cli
```

---

## 下一步

- [产品形态描述指南](./product-description.md)
- [业务划分最佳实践](./business-split.md)
- [大模型平台示例](../06-examples/model-platform/init.md)
