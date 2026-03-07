# Amazing：基于 Agent-Teams 的 AI 协同开发范式，让团队效率提升 10 倍

> 一个开源的企业级大模型管理平台，支持 6 大 Agent、6 种角色、3 种场景的全流程 AI 协同开发

## 🎯 写在前面

你是否遇到过这些问题：

- 产品经理写 PRD 要花 2 天，开发理解需求又要 1 天？
- 前后端开发各自为战，接口对接总是出问题？
- 测试用例写到手软，还是漏掉了关键场景？
- 代码审查流于形式，质量问题总是到线上才发现？
- 运维部署像开盲盒，每次上线都提心吊胆？

如果你的答案是"是"，那么这篇文章就是为你准备的。

今天要介绍的 **Amazing** 项目，是一个基于 **Agent-Teams 协同开发范式**的开源平台，通过 AI 赋能，让整个研发流程从需求到上线实现全流程自动化。

**GitHub 仓库**: https://github.com/z58362026/amazing
**在线架构图**: https://z58362026.github.io/amazing/

---

## 💡 核心理念

### 什么是 Agent-Teams？

传统的 AI 辅助开发工具，通常是"单打独斗"：
- Copilot 帮你写代码
- ChatGPT 帮你解答问题
- 各种 AI 工具各管各的

但真实的软件开发是**团队协作**：产品、前端、后端、测试、运维、运营，每个角色都有自己的职责，需要相互配合。

**Agent-Teams 就是让 AI 也学会团队协作**：

```
产品经理 Agent → 生成 PRD
    ↓
前端 Agent + 后端 Agent → 并行开发
    ↓
测试 Agent → 自动化测试
    ↓
审核 Agent → 代码审查
    ↓
运维 Agent → 一键部署
```

每个 Agent 专注自己的领域，通过 **Orchestrator（编排器）** 协调，形成完整的开发流水线。

---

## 🏗️ 架构设计

### 整体架构

Amazing 采用 **8 层架构**，从用户到技能层层递进：

```
👥 用户层
  ↓
🎯 统一入口层 (CLI / IronClaw Dashboard)
  ↓
🤖 AI 工具链层 (Claude Code / Codex)
  ↓
🎭 Agent Orchestrator (编排器)
  ↓
🎪 Agent 层 (6 大 Agent)
  ↓
👨‍💻 Sub-Agent 层 (6 种角色)
  ↓
⚡ Skill 层 (可进化)
```

**在线查看完整架构**: https://z58362026.github.io/amazing/

### 6 大 Agent 体系

| Agent | 职责 | 技术栈 |
|-------|------|--------|
| **Common** | 通用模块 (用户/权限/日志) | FastAPI + PostgreSQL |
| **Compute** | 算力平台 (GPU/CPU 调度) | Go + Kubernetes |
| **Data** | 数据平台 (数据集/标注) | Python + MinIO |
| **Training** | 训推平台 (训练/推理) | PyTorch + Triton |
| **Model-Service** | 模型服务 (API/版本管理) | Go + gRPC |
| **Review** | 审核 Agent (代码审查/质量) | SonarQube + ESLint |

每个 Agent 都有自己的 **Sub-Agents**（PM、Frontend、Backend、QA、Ops、Operation），形成完整的团队结构。

---

## ✨ 核心特性

### 1. 对话式角色申请

不需要复杂的配置，直接用自然语言申请角色：

```bash
$ python3 scripts/amazing-cli.py role chat "我是前端开发"

🎯 我理解了！你想申请 **前端开发** 角色

角色信息:
  名称: 前端开发
  权限: ui:develop, component:create, style:edit...
  技能: react-component, ui-design, state-management...

确认申请这个角色吗? [Y/n]: y

✅ 已成功申请 前端开发 角色！
```

系统会智能识别关键词，自动匹配最合适的角色。

### 2. 智能场景路由

支持 3 种开发场景，自动路由到对应的工作流：

**场景 1: 功能开发**
```
PM (需求分析)
  → PM (PRD 生成)
  → Frontend + Backend (并行开发)
  → QA (测试)
  → Review Agent (审查)
  → Ops (部署)
```

**场景 2: Bug 修复**
```
QA (Bug 复现)
  → Backend (问题定位)
  → Backend (代码修复)
  → QA (回归测试)
  → Ops (热修复部署)
  ↓ (如果失败)
  → 自动回滚
```

**场景 3: 需求分析**
```
PM (需求收集)
  → PM (需求分析)
  → PM (PRD 生成)
  → 技术评审
```

### 3. 三级进化机制

不同于传统的静态 AI 工具，Amazing 的 Agent 可以**自我进化**：

- **Agent 进化**: 基于任务成功率、代码质量、交付时间
- **Sub-Agent 进化**: 基于角色效率、协作分数
- **Skill 进化**: 基于准确率、性能、用户满意度

每次任务完成后，系统会收集指标，自动优化 Agent 的行为。

### 4. 工具链降级

支持多种 AI 工具，自动降级：

```
Claude Code (主力)
  ↓ (不可用时)
Codex CLI (备选)
  ↓ (不可用时)
Codex Desktop (可视化)
  ↓ (不可用时)
IronClaw (Web Dashboard)
```

保证在任何情况下都能正常工作。

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone git@github.com:z58362026/amazing.git
cd amazing
```

### 2. 初始化

```bash
# 安装依赖
make init

# 启动数据库 (PostgreSQL + Redis + MongoDB)
docker-compose -f docker-compose.dev.yml up -d
```

### 3. 启动服务

```bash
# 方式 1: 使用 Make
make dev

# 方式 2: 手动启动
# 终端 1: Python API
cd backend/python && python3 main.py

# 终端 2: 前端
cd frontend && npm run dev
```

### 4. 申请角色

```bash
# 对话式申请 (推荐)
python3 scripts/amazing-cli.py role chat "我是前端开发"

# 或直接设置
python3 scripts/amazing-cli.py role set frontend
```

### 5. 访问应用

- **前端**: http://localhost:3000
- **API 文档**: http://localhost:8000/docs
- **在线架构图**: https://z58362026.github.io/amazing/

---

## 💼 实际应用场景

### 场景 1: 产品经理生成 PRD

**传统方式**:
1. 产品经理手写 PRD (2 天)
2. 开发理解需求 (1 天)
3. 技术评审 (半天)
4. 来回沟通修改 (1 天)

**使用 Amazing**:
```bash
$ python3 scripts/amazing-cli.py prd create "用户权限管理模块"

✅ PRD 已生成: docs/prd/user-permission.md

包含:
- 需求背景
- 功能详细设计
- 技术方案
- 验收标准
- 里程碑

时间: 5 分钟
```

### 场景 2: 前端开发实现 UI

**传统方式**:
1. 看设计稿 (30 分钟)
2. 写组件代码 (2 小时)
3. 调样式 (1 小时)
4. 写测试 (1 小时)

**使用 Amazing**:
```bash
$ claude "创建用户列表组件，支持分页、搜索、排序" --role frontend

✅ 已生成:
- src/components/UserList.tsx (组件)
- src/stores/userStore.ts (状态管理)
- src/api/user.ts (API 调用)
- src/components/UserList.test.tsx (测试)

时间: 2 分钟
```

### 场景 3: Bug 修复

**传统方式**:
1. QA 报 Bug (10 分钟)
2. 开发复现 (30 分钟)
3. 定位问题 (1 小时)
4. 修复代码 (30 分钟)
5. 测试验证 (30 分钟)
6. 部署上线 (20 分钟)

**使用 Amazing**:
```bash
$ python3 scripts/amazing-cli.py bug fix "用户登录失败"

🔍 正在分析日志...
✅ 问题定位: 数据库连接失败
✅ 代码已修复: backend/python/app/core/database.py
✅ 测试已通过
✅ 已部署到测试环境

时间: 5 分钟
```

---

## 🎨 IronClaw: 可视化协同开发

除了 CLI，Amazing 还提供了 **IronClaw** Web Dashboard，支持：

### 任务管理
- 看板视图 (待办/进行中/已完成)
- 拖拽排序
- 进度跟踪

### 代码审查
- 自动代码审查
- 质量评分
- 修复建议

### 智能对话
```
用户: @IronClaw 创建任务: 实现用户登录功能
IronClaw:
✅ 任务已创建
- 任务 ID: TASK-001
- 分配给: Common Agent
- 预计时间: 2 天

需要我帮你生成详细的技术方案吗？
```

### 团队协作
```
用户: @IronClaw @张三 请帮忙实现用户登录的前端页面
IronClaw:
✅ 已通知 @张三 (Frontend)

任务详情:
- 标题: 实现用户登录前端页面
- 关联任务: TASK-001
- 技术要求: React + TypeScript + Ant Design

@张三 会在 30 分钟内响应
```

---

## 📊 技术栈

### 前端
- React 18 + TypeScript
- Vite (构建)
- TailwindCSS (样式)
- Zustand (状态管理)
- Ant Design (UI 库)

### 后端
- **Python**: FastAPI + SQLAlchemy + PostgreSQL
- **Go**: Gin + GORM + gRPC
- **缓存**: Redis
- **对象存储**: MinIO

### 基础设施
- **容器**: Docker + Docker Compose
- **编排**: Kubernetes + Helm
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack
- **CI/CD**: GitHub Actions

### AI 工具链
- **Claude Code** (Anthropic) - 主力
- **Codex CLI** - 备选
- **IronClaw** - 可视化

---

## 🔥 为什么选择 Amazing？

### 1. 开源免费
- MIT 许可证
- 完全开源
- 社区驱动

### 2. 开箱即用
- 一键部署
- 完整文档
- 丰富示例

### 3. 高度可扩展
- 插件化架构
- 自定义 Agent
- 自定义 Skill

### 4. 企业级
- 支持私有化部署
- 支持多数据库 (PostgreSQL/MySQL/MongoDB)
- 支持 K8s 集群部署

### 5. 持续进化
- Agent 自我优化
- Skill 版本管理
- 性能指标监控

---

## 📈 性能对比

| 任务 | 传统方式 | 使用 Amazing | 提升 |
|------|---------|-------------|------|
| PRD 编写 | 2 天 | 5 分钟 | **576x** |
| 前端组件开发 | 4 小时 | 2 分钟 | **120x** |
| API 开发 | 3 小时 | 3 分钟 | **60x** |
| Bug 修复 | 3 小时 | 5 分钟 | **36x** |
| 代码审查 | 1 小时 | 2 分钟 | **30x** |
| 部署上线 | 30 分钟 | 1 分钟 | **30x** |

**平均效率提升**: **10-100 倍**

---

## 🗺️ Roadmap

### v1.0 (已完成) ✅
- [x] 6 大 Agent 体系
- [x] 6 种角色支持
- [x] 对话式角色申请
- [x] CLI 工具
- [x] 完整文档

### v1.1 (进行中) 🚧
- [ ] IronClaw Web Dashboard
- [ ] Agent 进化引擎
- [ ] 更多 Skills
- [ ] 性能优化

### v2.0 (规划中) 📋
- [ ] 多租户支持
- [ ] 企业版功能
- [ ] 更多 AI 引擎集成
- [ ] 移动端支持

---

## 🤝 参与贡献

Amazing 是一个开源项目，欢迎所有人参与贡献！

### 贡献方式

1. **提交 Issue**: 报告 Bug 或提出功能建议
2. **提交 PR**: 贡献代码或文档
3. **分享经验**: 写文章、录视频
4. **推广项目**: Star、Fork、分享

### 贡献指南

查看 [CONTRIBUTING.md](https://github.com/z58362026/amazing/blob/main/CONTRIBUTING.md)

---

## 📚 文档

### 新手必读
- [快速开始](https://github.com/z58362026/amazing/blob/main/QUICKSTART.md)
- [环境安装](https://github.com/z58362026/amazing/blob/main/docs/INSTALLATION.md)
- [角色接入](https://github.com/z58362026/amazing/blob/main/docs/ROLE_ONBOARDING.md)

### 进阶指南
- [架构设计](https://z58362026.github.io/amazing/)
- [技术规范](https://github.com/z58362026/amazing/blob/main/docs/specs/README.md)
- [部署指南](https://github.com/z58362026/amazing/blob/main/docs/deployment/README.md)

### 角色指南
- [产品经理指南](https://github.com/z58362026/amazing/blob/main/docs/guides/pm.md)
- [前端开发指南](https://github.com/z58362026/amazing/blob/main/docs/guides/frontend.md)
- [后端开发指南](https://github.com/z58362026/amazing/blob/main/docs/guides/backend.md)

---

## 💬 社区

### 加入我们

- **GitHub**: https://github.com/z58362026/amazing
- **Issues**: https://github.com/z58362026/amazing/issues
- **Discussions**: https://github.com/z58362026/amazing/discussions
- **Email**: 305068308@qq.com

### Star History

如果你觉得这个项目有用，请给我们一个 Star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=z58362026/amazing&type=Date)](https://star-history.com/#z58362026/amazing&Date)

---

## 🎯 总结

**Amazing** 不仅仅是一个工具，更是一种**全新的开发范式**：

- 🤖 **AI 不再是辅助，而是团队成员**
- 👥 **每个角色都有专属的 AI Agent**
- 🔄 **Agent 可以自我进化，持续优化**
- 🎯 **从需求到上线，全流程自动化**

如果你：
- 是技术 Leader，想提升团队效率
- 是独立开发者，想快速实现想法
- 是创业者，想降低研发成本
- 是 AI 爱好者，想探索 Agent 技术

那么，**Amazing 就是为你准备的**。

---

## 🚀 立即开始

```bash
# 1. 克隆项目
git clone git@github.com:z58362026/amazing.git

# 2. 初始化
cd amazing && make init

# 3. 启动
make dev

# 4. 访问
open http://localhost:3000
```

**GitHub**: https://github.com/z58362026/amazing
**在线架构图**: https://z58362026.github.io/amazing/

---

## 📝 最后

软件开发的未来，不是 AI 替代人类，而是 **AI 与人类协同**。

Amazing 正在探索这条路，我们相信：

> **最好的 AI 工具，不是让你写代码更快，而是让你的团队协作更顺畅。**

如果你认同这个理念，欢迎加入我们，一起打造更好的 AI 协同开发平台！

**给个 Star ⭐ 支持一下吧！**

---

<div align="center">

**Made with ❤️ by Amazing Team**

[GitHub](https://github.com/z58362026/amazing) • [在线架构图](https://z58362026.github.io/amazing/) • [文档](https://github.com/z58362026/amazing/tree/main/docs)

</div>
