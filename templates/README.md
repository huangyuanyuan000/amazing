# 模板库

## 说明

Amazing 脚手架采用**动态生成**模式，不依赖静态模板文件。

所有项目内容都是在初始化时根据用户需求动态生成的，包括：
- 目录结构
- 配置文件
- 代码骨架
- 部署配置
- 文档

## 为什么不使用静态模板？

### 传统模板的问题
- ❌ 模板过时难以维护
- ❌ 无法适应不同业务需求
- ❌ 修改模板需要手动同步
- ❌ 模板冗余，占用空间

### 动态生成的优势
- ✅ 根据需求定制生成
- ✅ 始终使用最新逻辑
- ✅ 灵活适应各种场景
- ✅ 代码即文档，易于维护

## 生成流程

初始化时通过 8 个阶段动态生成：

1. **structure-init**: 创建目录结构
2. **handoffs-setup**: 部署 Handoffs 能力
3. **role-config**: 生成角色配置
4. **business-agent-gen**: 分析业务生成 Agent
5. **backend-gen**: 生成后端代码
6. **frontend-gen**: 生成前端代码
7. **deploy-gen**: 生成部署配置
8. **docs-gen**: 生成文档

每个阶段的逻辑在 `scripts/phases/` 目录中。

## 案例库

虽然不使用静态模板，但我们提供了完整的案例供参考：

- `examples/model-platform/`: 大模型管理平台
- `examples/e-commerce/`: 电商平台（规划中）
- `examples/saas-platform/`: SaaS 平台（规划中）

案例可以作为初始化的参考，但不会被直接复制。

## 扩展

如需添加新的生成逻辑：

1. 在 `scripts/phases/` 中添加新阶段
2. 在 `scripts/orchestrator.py` 中注册
3. 在 `.agents/init-handoffs/` 中添加对应的 Handoff Agent

所有生成逻辑都是代码化的，易于版本控制和协作开发。
