# Amazing 项目文档结构规划

## 当前问题
1. 根目录文档过多（13个.md文件）
2. 文档分类不清晰
3. 角色相关文档散落各处
4. 缺少清晰的文档导航

## 新的文档结构

```
amazing/
├── README.md                          # 项目主页（保留）
├── QUICKSTART.md                      # 快速开始（保留）
├── CONTRIBUTING.md                    # 贡献指南（保留）
├── CHANGELOG.md                       # 变更日志（新建）
│
├── docs/                              # 文档根目录
│   ├── README.md                      # 文档导航首页
│   │
│   ├── getting-started/               # 入门指南
│   │   ├── installation.md            # 环境安装
│   │   ├── quickstart.md              # 快速开始
│   │   └── first-project.md           # 第一个项目
│   │
│   ├── architecture/                  # 架构设计
│   │   ├── README.md                  # 架构总览
│   │   ├── system-design.md           # 系统设计
│   │   ├── agent-teams.md             # Agent-Teams范式
│   │   ├── ai-modes.md                # AI模式说明
│   │   └── mode-switch.md             # 模式切换指南
│   │
│   ├── roles/                         # 角色文档
│   │   ├── README.md                  # 角色总览
│   │   ├── architect/                 # 架构师
│   │   │   ├── README.md
│   │   │   ├── quickstart.md
│   │   │   ├── workflow.md
│   │   │   └── permissions.md
│   │   ├── pm/                        # 产品经理
│   │   │   ├── README.md
│   │   │   └── workflow.md
│   │   ├── frontend/                  # 前端开发
│   │   │   ├── README.md
│   │   │   └── workflow.md
│   │   ├── backend/                   # 后端开发
│   │   │   ├── README.md
│   │   │   └── workflow.md
│   │   ├── qa/                        # 测试工程师
│   │   │   ├── README.md
│   │   │   └── workflow.md
│   │   ├── ops/                       # 运维工程师
│   │   │   ├── README.md
│   │   │   └── workflow.md
│   │   └── operation/                 # 运营人员
│   │       ├── README.md
│   │       └── workflow.md
│   │
│   ├── guides/                        # 使用指南
│   │   ├── README.md
│   │   ├── claude-code.md             # Claude Code接入
│   │   ├── ironclaw.md                # IronClaw使用
│   │   ├── role-chat.md               # 对话式角色申请
│   │   └── cli-commands.md            # CLI命令参考
│   │
│   ├── workflows/                     # 工作流程
│   │   ├── README.md
│   │   ├── feature-development.md     # 功能开发
│   │   ├── bug-fix.md                 # Bug修复
│   │   ├── requirement-analysis.md    # 需求分析
│   │   └── code-review.md             # 代码审查
│   │
│   ├── deployment/                    # 部署文档
│   │   ├── README.md
│   │   ├── local.md                   # 本地部署
│   │   ├── docker.md                  # Docker部署
│   │   └── kubernetes.md              # K8s部署
│   │
│   ├── api/                           # API文档
│   │   ├── README.md
│   │   ├── rest-api.md                # REST API
│   │   └── grpc-api.md                # gRPC API
│   │
│   └── reference/                     # 参考文档
│       ├── configuration.md           # 配置参考
│       ├── permissions.md             # 权限矩阵
│       └── troubleshooting.md         # 故障排查
│
├── .agents/                           # Agent配置（代码）
│   ├── README.md                      # Agent说明
│   ├── config.json
│   ├── architect/
│   │   ├── README.md
│   │   ├── config.json
│   │   └── prompt.md
│   ├── common/
│   ├── compute/
│   ├── data/
│   ├── training/
│   ├── model-service/
│   └── review/
│
├── .claude/                           # Claude配置（代码）
│   ├── config.json
│   ├── settings.json
│   └── roles/
│       └── config.json
│
└── scripts/                           # 脚本工具
    ├── README.md
    ├── amazing-cli.py
    ├── architect_cli.py
    └── mode_cli.py
```

## 迁移计划

### 第一步：整理根目录文档
- 保留：README.md, QUICKSTART.md, CONTRIBUTING.md
- 移动到 docs/archive/：
  - FINAL_SUMMARY.md
  - PROJECT_SUMMARY.md
  - UPDATE_SUMMARY.md
  - GITHUB_PAGES.md
  - GITHUB_PUBLISHED.md
- 移动到 docs/guides/：
  - ROLE_CHAT_DEMO.md → role-chat-demo.md
  - ROLE_COMMANDS.md → cli-commands.md
- 移动到 docs/getting-started/：
  - START_HERE.md → README.md
- 移动到 docs/marketing/：
  - JUEJIN_ARTICLE.md

### 第二步：重组 docs/ 目录
- 创建 docs/roles/ 目录，按角色分类
- 创建 docs/getting-started/ 目录
- 创建 docs/workflows/ 目录（已有HTML，补充MD）
- 创建 docs/reference/ 目录

### 第三步：更新导航
- 更新 docs/README.md 作为文档首页
- 更新 docs/index.html 添加新的导航
- 更新根目录 README.md 的文档链接

## 优势
1. 文档分类清晰
2. 易于查找和维护
3. 支持按角色、按功能查找
4. 代码和文档分离
5. 符合开源项目最佳实践
