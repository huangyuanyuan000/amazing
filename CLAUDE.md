# Amazing - 大模型管理平台 AI Coding 规范

## 项目概述
大模型管理平台（Amazing），采用 Agent-Teams 协同开发范式，支持多角色、多场景的 AI 辅助开发。

## 技术栈
- **后端**: Python (FastAPI) + Go (高性能服务)
- **前端**: React + TypeScript + Vite
- **数据库**: PostgreSQL (主库) / MySQL / MongoDB / Redis
- **基础设施**: Kubernetes + Docker + Helm
- **AI 工具链**: Claude Code (主力) > Codex (降级备选)

## Agent 体系
| Agent | 职责 | 路径 |
|-------|------|------|
| common | 通用模块(用户/权限/日志) | .agents/common/ |
| compute | 算力平台 | .agents/compute/ |
| data | 数据平台 | .agents/data/ |
| training | 训推平台 | .agents/training/ |
| model-service | 模型服务平台 | .agents/model-service/ |
| review | 审核 Agent | .agents/review/ |

## 开发规范
- Git: Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `ci:`, `chore:`)
- API: RESTful + OpenAPI 3.0，统一响应格式
- 代码风格: Python (black + ruff), Go (gofmt + golangci-lint), TS (eslint + prettier)
- 测试: 单测覆盖率 > 80%, 集成测试必须通过
- CI/CD: GitHub Actions / GitLab CI, 自动化部署
- 文档: 每个模块必须有 README，API 必须有 Swagger

## 角色权限
- **产品经理**: 需求定义、验收
- **前端开发**: UI/UX 实现
- **后端开发**: API/服务开发
- **测试工程师**: 测试用例、自动化测试
- **运维工程师**: 部署、监控、环境管理
- **运营人员**: 数据分析、运营配置

## 工具链优先级
1. Claude Code CLI (主力开发工具)
2. Codex CLI (本地降级方案)
3. Codex Desktop (可视化操作)

## 部署模式
- `make deploy-local`: 本地开发环境
- `make deploy-docker`: Docker Compose 一键部署
- `make deploy-k8s`: Kubernetes 集群部署
- `make deploy-offline`: 离线/私有化部署
