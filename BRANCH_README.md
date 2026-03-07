# 模型管理平台分支说明

## 分支信息

- **分支名称**: `feature/model-management-platform`
- **创建时间**: 2025-03-15
- **基于版本**: main@a1468a0

## 分支目的

本分支保存了 Amazing 作为**大模型管理平台**的完整实现，包括：

### 核心功能

1. **6 大 Agent 体系**
   - Common Agent (通用模块)
   - Compute Agent (算力平台)
   - Data Agent (数据平台)
   - Training Agent (训推平台)
   - Model-Service Agent (模型服务)
   - Review Agent (审核)

2. **7 种角色支持**
   - 👑 架构师 (Architect)
   - 📋 产品经理 (PM)
   - 🎨 前端开发 (Frontend)
   - ⚙️ 后端开发 (Backend)
   - 🧪 测试工程师 (QA)
   - 🚀 运维工程师 (Ops)
   - 📊 运营人员 (Operation)

3. **AI 双模式**
   - 全自动模式 (Full-Auto)
   - 半自动模式 (Semi-Auto)
   - 架构师权限控制

4. **完整文档**
   - 架构设计文档
   - 角色指南
   - 工作流程
   - API 文档

## 主要特性

### 模型管理相关

- GPU/CPU 资源调度
- 数据集管理和标注
- 模型训练和推理
- 模型版本管理
- API 服务部署

### Agent-Teams 协同

- 多角色协同开发
- 场景适配 (开发/修复/分析)
- 进化机制 (Agent/Sub-Agent/Skill)
- 工具链降级 (Claude Code → Codex → IronClaw)

## 文件结构

```
amazing/
├── .agents/                    # Agent 配置
│   ├── common/                # 通用模块
│   ├── compute/               # 算力平台
│   ├── data/                  # 数据平台
│   ├── training/              # 训推平台
│   ├── model-service/         # 模型服务
│   ├── review/                # 审核
│   └── architect/             # 架构师
├── .claude/                   # Claude 配置
├── docs/                      # 文档
│   ├── architecture/          # 架构设计
│   ├── roles/                 # 角色指南
│   ├── workflows/             # 工作流程
│   └── guides/                # 使用指南
├── frontend/                  # 前端代码
├── backend/                   # 后端代码
└── scripts/                   # CLI 工具
```

## 技术栈

### 后端
- Python 3.11+ (FastAPI)
- Go 1.22+ (高性能服务)
- PostgreSQL (主数据库)
- Redis (缓存)
- MinIO (对象存储)

### 前端
- React 18+
- TypeScript 5+
- Vite
- Ant Design

### 基础设施
- Docker
- Kubernetes
- Prometheus + Grafana

## 使用场景

本分支适用于以下场景：

1. **企业级大模型管理平台开发**
   - 需要管理 GPU/CPU 资源
   - 需要数据集管理和标注
   - 需要模型训练和推理
   - 需要模型版本管理

2. **多角色协同的 AI 项目**
   - 产品、开发、测试、运维协同
   - 需要 AI 辅助但要人工把关
   - 需要按需求切换自动化程度

3. **Agent-Teams 范式研究**
   - 研究 AI 协同开发模式
   - 探索多 Agent 协作机制
   - 实践进化机制

## 后续计划

### 短期 (Q2 2025)
- 完善 6 大 Agent 实现
- 增强 IronClaw 功能
- 落地进化机制

### 长期
- 开放生态建设
- 跨平台集成
- 企业级特性

## 相关链接

- **GitHub 仓库**: https://github.com/z58362026/amazing
- **在线架构图**: https://z58362026.github.io/amazing/
- **文档中心**: https://github.com/z58362026/amazing/blob/feature/model-management-platform/docs/README.md

## 切换到此分支

```bash
# 克隆仓库
git clone https://github.com/z58362026/amazing.git
cd amazing

# 切换到模型管理平台分支
git checkout feature/model-management-platform

# 安装依赖
make install

# 启动服务
make dev
```

## 注意事项

1. 本分支保持稳定，不会频繁更新
2. 主分支 (main) 会继续优化架构
3. 如需模型管理平台功能，请使用本分支
4. 如需最新架构优化，请使用主分支

---

**维护者**: Amazing Team
**最后更新**: 2025-03-15
