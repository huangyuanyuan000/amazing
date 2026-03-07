# Handoffs 配置 - 大模型管理平台

## 概述

本项目中的所有角色在执行复杂任务时，都应该使用 handoffs 模式进行任务拆分，避免一次性生成过多内容导致上下文溢出。

## Handoffs 原则

### 1. 任务拆分粒度
- **单个文件 < 200 行**: 可以一次性生成
- **单个文件 200-500 行**: 先生成骨架，再分段填充
- **单个文件 > 500 行**: 拆分成多个文件
- **多文件任务**: 按模块/功能拆分，逐个完成

### 2. 拆分策略

#### 前端开发拆分
```
大任务: 开发模型管理模块
├─ 子任务1: 创建页面骨架和路由
├─ 子任务2: 实现列表页面
├─ 子任务3: 实现详情页面
├─ 子任务4: 实现创建/编辑表单
├─ 子任务5: 实现 API 服务层
└─ 子任务6: 实现状态管理
```

#### 后端开发拆分
```
大任务: 开发模型管理 API
├─ 子任务1: 定义数据模型
├─ 子任务2: 实现 CRUD API
├─ 子任务3: 实现业务逻辑
├─ 子任务4: 添加权限控制
├─ 子任务5: 编写单元测试
└─ 子任务6: 编写 API 文档
```

#### 测试开发拆分
```
大任务: 编写集成测试
├─ 子任务1: 设计测试用例
├─ 子任务2: 实现用户模块测试
├─ 子任务3: 实现模型模块测试
├─ 子任务4: 实现训练模块测试
└─ 子任务5: 生成测试报告
```

### 3. Handoff 触发条件

自动触发 handoff（任务拆分）的情况：
- 预估生成代码 > 200 行
- 涉及 3 个以上文件
- 需要多个步骤才能完成
- 依赖其他任务的输出
- 需要等待外部输入

### 4. Handoff 执行流程

```
1. 分析任务复杂度
   ↓
2. 判断是否需要拆分
   ↓
3. 如需拆分，制定子任务列表
   ↓
4. 逐个执行子任务
   ↓
5. 每个子任务完成后保存状态
   ↓
6. 继续下一个子任务
   ↓
7. 所有子任务完成后汇总
```

## 角色专属 Handoffs

### 前端开发 (frontend-dev)

#### 可用的 Handoff Agents

1. **page-generator**: 页面生成器
   - 输入: 页面需求、API 定义
   - 输出: 页面组件代码
   - 限制: 单个页面

2. **component-generator**: 组件生成器
   - 输入: 组件需求、设计稿
   - 输出: 可复用组件
   - 限制: 单个组件

3. **service-generator**: API 服务生成器
   - 输入: API 文档
   - 输出: TypeScript 服务层代码
   - 限制: 单个模块的 API

4. **store-generator**: 状态管理生成器
   - 输入: 数据流设计
   - 输出: Zustand store 代码
   - 限制: 单个 store

#### 使用示例

```yaml
# 前端开发任务拆分示例
task: 开发模型管理模块前端

handoffs:
  - agent: page-generator
    input:
      page_name: ModelList
      features: [列表展示, 分页, 搜索, 删除]
    output: src/pages/Model/List.tsx

  - agent: page-generator
    input:
      page_name: ModelDetail
      features: [详情展示, 版本历史, 下载]
    output: src/pages/Model/Detail.tsx

  - agent: service-generator
    input:
      module: model
      endpoints: [list, get, create, update, delete]
    output: src/services/model.ts

  - agent: store-generator
    input:
      store_name: modelStore
      state: [models, loading, current]
    output: src/stores/modelStore.ts
```

### 后端开发 (backend-dev)

#### 可用的 Handoff Agents

1. **model-generator**: 数据模型生成器
   - 输入: 表结构设计
   - 输出: SQLAlchemy 模型
   - 限制: 单个模型

2. **api-generator**: API 端点生成器
   - 输入: API 规范
   - 输出: FastAPI 路由代码
   - 限制: 单个资源的 CRUD

3. **service-generator**: 业务逻辑生成器
   - 输入: 业务需求
   - 输出: Service 层代码
   - 限制: 单个服务类

4. **test-generator**: 测试生成器
   - 输入: 待测试的代码
   - 输出: pytest 测试代码
   - 限制: 单个模块的测试

#### 使用示例

```yaml
# 后端开发任务拆分示例
task: 开发模型管理 API

handoffs:
  - agent: model-generator
    input:
      model_name: Model
      fields: [name, version, framework, size, created_at]
    output: src/backend/models/model.py

  - agent: api-generator
    input:
      resource: model
      operations: [list, get, create, update, delete]
    output: src/backend/api/v1/model.py

  - agent: service-generator
    input:
      service_name: ModelService
      methods: [create_model, upload_file, validate]
    output: src/backend/services/model_service.py

  - agent: test-generator
    input:
      test_target: api/v1/model.py
      test_cases: [test_list, test_create, test_update]
    output: tests/backend/test_model_api.py
```

### 测试工程师 (test-engineer)

#### 可用的 Handoff Agents

1. **testcase-designer**: 测试用例设计器
   - 输入: 功能需求
   - 输出: 测试用例文档
   - 限制: 单个功能模块

2. **unit-test-generator**: 单元测试生成器
   - 输入: 源代码
   - 输出: 单元测试代码
   - 限制: 单个类/函数

3. **integration-test-generator**: 集成测试生成器
   - 输入: API 文档
   - 输出: 集成测试代码
   - 限制: 单个 API 模块

4. **e2e-test-generator**: E2E 测试生成器
   - 输入: 用户流程
   - 输出: Cypress 测试代码
   - 限制: 单个用户流程

### 运维工程师 (devops-engineer)

#### 可用的 Handoff Agents

1. **dockerfile-generator**: Dockerfile 生成器
   - 输入: 应用类型、依赖
   - 输出: Dockerfile
   - 限制: 单个服务

2. **k8s-manifest-generator**: K8s 配置生成器
   - 输入: 服务配置
   - 输出: K8s YAML 文件
   - 限制: 单个服务

3. **ci-pipeline-generator**: CI 流程生成器
   - 输入: 构建步骤
   - 输出: GitHub Actions YAML
   - 限制: 单个流程

4. **monitoring-config-generator**: 监控配置生成器
   - 输入: 监控指标
   - 输出: Prometheus 配置
   - 限制: 单个服务

## Handoff 状态管理

### 状态文件位置
```
.agents/handoffs/state/
├── frontend-dev/
│   ├── task-001.json
│   └── task-002.json
├── backend-dev/
│   ├── task-001.json
│   └── task-002.json
└── ...
```

### 状态文件格式
```json
{
  "task_id": "frontend-dev-001",
  "task_name": "开发模型管理模块",
  "role": "frontend-dev",
  "status": "in_progress",
  "created_at": "2024-03-08T10:00:00Z",
  "updated_at": "2024-03-08T10:30:00Z",
  "subtasks": [
    {
      "id": "1",
      "name": "创建页面骨架",
      "agent": "page-generator",
      "status": "completed",
      "output": "src/pages/Model/List.tsx"
    },
    {
      "id": "2",
      "name": "实现列表页面",
      "agent": "page-generator",
      "status": "in_progress",
      "output": null
    }
  ],
  "context": {
    "module": "model",
    "api_endpoints": [...],
    "dependencies": [...]
  }
}
```

## 最佳实践

### 1. 任务拆分建议
- 每个子任务专注于单一职责
- 子任务之间尽量解耦
- 明确子任务的输入输出
- 预估每个子任务的工作量

### 2. 上下文管理
- 每个子任务完成后保存关键信息
- 下一个子任务可以读取前面的输出
- 避免重复传递大量上下文
- 使用引用而非复制

### 3. 错误处理
- 子任务失败不影响已完成的部分
- 支持从失败点恢复
- 记录失败原因和上下文
- 提供重试机制

### 4. 进度跟踪
- 实时显示任务进度
- 记录每个子任务的耗时
- 生成任务完成报告
- 支持任务暂停和恢复

## 工具支持

### CLI 命令

```bash
# 查看当前任务
claude-code handoffs status

# 创建新任务（自动拆分）
claude-code handoffs create "开发模型管理模块"

# 继续未完成的任务
claude-code handoffs resume <task-id>

# 查看任务详情
claude-code handoffs show <task-id>

# 取消任务
claude-code handoffs cancel <task-id>
```

### API 接口

```python
from amazing.handoffs import HandoffManager

# 创建 handoff 管理器
manager = HandoffManager(role="frontend-dev")

# 分析任务并自动拆分
subtasks = manager.analyze_and_split(
    task="开发模型管理模块",
    context={...}
)

# 执行子任务
for subtask in subtasks:
    result = manager.execute_subtask(subtask)
    manager.save_result(result)

# 获取任务状态
status = manager.get_status(task_id)
```

## 注意事项

1. **不要过度拆分**: 太小的任务反而增加管理成本
2. **保持上下文连贯**: 子任务之间要有清晰的依赖关系
3. **及时保存状态**: 每个子任务完成后立即保存
4. **合理估算时间**: 避免单个子任务耗时过长
5. **灵活调整**: 根据实际情况动态调整拆分策略
