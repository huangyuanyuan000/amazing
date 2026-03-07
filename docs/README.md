# Amazing 文档中心

## 📚 核心理念

Amazing 是基于**组织形态驱动**的 AI 协同开发范式平台。

**核心架构**：组织形态 → 产品形态 → 技术架构

---

## 🎯 快速导航

### 新手入门

1. [架构理念](./00-overview/architecture.md) - 理解 Amazing 的核心思想
2. [快速开始](./01-scaffolding/README.md) - 5 分钟初始化项目
3. [大模型平台示例](./06-examples/model-platform/init.md) - 完整的初始化流程

### 核心概念

- [组织形态层](./02-agent-teams/README.md) - 固定角色和固定部门
- [产品形态层](./02-agent-teams/business-agents/README.md) - 动态业务划分
- [技术架构层](./04-tech-stack/README.md) - 技术选型和实现

### 实践指南

- [产品形态描述](./01-scaffolding/product-description.md) - 如何描述产品
- [业务划分方法](./01-scaffolding/business-split.md) - 如何拆分业务模块
- [技术栈选择](./04-tech-stack/default-stacks.md) - 如何选择技术栈

---

## 📖 文档结构

```
docs/
├── 00-overview/              # 总览
│   └── architecture.md       # 架构理念
│
├── 01-scaffolding/           # 脚手架层
│   ├── README.md             # Amazing CLI 使用指南
│   ├── product-description.md # 产品形态描述
│   └── business-split.md     # 业务划分方法
│
├── 02-agent-teams/           # Agent-Teams 层
│   ├── README.md             # 组织形态层总览
│   ├── fixed-agents/         # 固定 Agent
│   │   ├── common.md         # Common Agent
│   │   └── review.md         # Review Agent
│   ├── business-agents/      # 业务 Agent
│   │   ├── README.md         # 业务 Agent 说明
│   │   └── create-guide.md   # 创建指南
│   └── roles/                # 固定角色
│       ├── README.md         # 角色总览
│       └── architect.md      # 架构师角色
│
├── 03-sub-agents/            # Sub-Agent 层
│   ├── README.md             # Sub-Agent 说明
│   └── orchestration.md      # 编排机制
│
├── 04-tech-stack/            # 技术选型层
│   ├── README.md             # 技术栈总览
│   ├── default-stacks.md     # 默认推荐
│   └── custom-stacks.md      # 自定义选择
│
├── 05-workflows/             # 工作流程
│   ├── init-workflow.md      # 初始化流程
│   └── development.md        # 开发流程
│
└── 06-examples/              # 示例
    └── model-platform/       # 大模型管理平台
        └── init.md           # 初始化流程
```

---

## 🚀 快速开始

### 1. 安装 Amazing CLI

```bash
pip install amazing-cli
```

### 2. 初始化项目

```bash
amazing-cli init my-project
```

### 3. 按照提示完成配置

- 描述产品形态
- 选择业务划分方案
- 配置技术栈
- 生成项目结构

---

## 💡 核心概念

### 三层架构

```
┌─────────────────────────────────┐
│   第一层：组织形态层             │
│   固定角色 + 固定部门            │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│   第二层：产品形态层             │
│   动态业务划分 + 业务 Agent      │
└──────────────┬──────────────────┘
               ↓
┌─────────────────────────────────┐
│   第三层：技术架构层             │
│   技术选型 + Sub-Agent 实现      │
└─────────────────────────────────┘
```

### 为什么这样设计？

基于**康威定律**：
> 系统架构会反映组织结构

因此：
1. **组织形态决定协作方式** - 先定义团队结构
2. **产品形态反映组织结构** - 业务模块对应团队
3. **技术架构服务于产品** - 技术选型支撑业务

---

## 📞 获取帮助

- **GitHub Issues**: [提交问题](https://github.com/z58362026/amazing/issues)
- **GitHub Discussions**: [参与讨论](https://github.com/z58362026/amazing/discussions)
- **Email**: 305068308@qq.com

---

<div align="center">

**[⬆ 回到顶部](#amazing-文档中心)**

Made with ❤️ by Amazing Team

</div>
