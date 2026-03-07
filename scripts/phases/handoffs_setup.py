#!/usr/bin/env python3
"""
Phase 2: Handoffs 能力部署

将 handoffs 任务拆分和管理能力部署到项目中
"""

import shutil
from pathlib import Path
from typing import Dict


def execute(context: Dict) -> Dict:
    """执行 Handoffs 能力部署"""
    project_path = context["project_path"]
    framework_path = context["framework_path"]

    print("🔧 部署 Handoffs 能力...")

    # 1. 创建 handoffs 目录结构
    handoffs_path = project_path / ".agents" / "handoffs"
    handoffs_path.mkdir(parents=True, exist_ok=True)

    # 2. 复制 handoff agents 模板
    copy_handoff_agents(framework_path, project_path)

    # 3. 复制 handoff 管理器
    copy_handoff_manager(framework_path, project_path)

    # 4. 生成 handoffs 配置文档
    generate_handoffs_readme(project_path)

    # 5. 创建状态目录
    create_state_directories(project_path)

    print("\n✅ Handoffs 能力部署完成")

    return {
        "handoffs_path": str(handoffs_path),
        "agents": ["page-generator", "service-generator", "store-generator",
                   "model-generator", "api-generator"],
        "manager": "scripts/handoff_manager.py"
    }


def copy_handoff_agents(framework_path: Path, project_path: Path):
    """复制 handoff agents 模板"""
    print("\n📦 复制 Handoff Agents...")

    # 前端 agents
    frontend_agents = [
        "page-generator",
        "component-generator",
        "service-generator",
        "store-generator"
    ]

    # 后端 agents
    backend_agents = [
        "model-generator",
        "api-generator",
        "service-generator-backend",
        "test-generator"
    ]

    # 从框架复制到项目
    framework_handoffs = framework_path / ".agents" / "init-handoffs"

    # 复制前端 agents
    for agent in frontend_agents:
        src = framework_handoffs / agent
        if src.exists():
            dst = project_path / ".agents" / "handoffs" / agent
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"  ✓ {agent}")

    # 复制后端 agents
    for agent in backend_agents:
        src = framework_handoffs / agent
        if src.exists():
            dst = project_path / ".agents" / "handoffs" / agent
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"  ✓ {agent}")


def copy_handoff_manager(framework_path: Path, project_path: Path):
    """复制 handoff 管理器"""
    print("\n📋 复制 Handoff 管理器...")

    src = framework_path / "scripts" / "handoff_manager.py"
    dst = project_path / "scripts" / "handoff_manager.py"

    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        dst.chmod(0o755)
        print("  ✓ handoff_manager.py")


def generate_handoffs_readme(project_path: Path):
    """生成 handoffs 配置文档"""
    print("\n📝 生成 Handoffs 配置文档...")

    content = """# Handoffs 任务拆分系统

## 概述

本项目内置了 Handoffs 任务拆分能力，所有角色在执行复杂任务时都会自动拆分成小任务，避免一次性生成过多内容导致上下文溢出。

## 核心原则

### 拆分粒度
- **单个文件 < 200 行**: 可以一次性生成
- **单个文件 200-500 行**: 先生成骨架，再分段填充
- **单个文件 > 500 行**: 拆分成多个文件
- **多文件任务**: 按模块/功能拆分，逐个完成

### 自动触发条件
- 预估生成代码 > 200 行
- 涉及 3 个以上文件
- 需要多个步骤才能完成
- 依赖其他任务的输出

## 可用的 Handoff Agents

### 前端开发 (frontend-dev)

| Agent | 功能 | 输出限制 |
|-------|------|----------|
| page-generator | 生成单个页面组件 | < 200 行 |
| component-generator | 生成可复用组件 | < 150 行 |
| service-generator | 生成 API 服务层 | < 150 行 |
| store-generator | 生成状态管理 | < 150 行 |

### 后端开发 (backend-dev)

| Agent | 功能 | 输出限制 |
|-------|------|----------|
| model-generator | 生成数据模型 | < 150 行 |
| api-generator | 生成 API 端点 | < 200 行 |
| service-generator-backend | 生成业务逻辑 | < 200 行 |
| test-generator | 生成测试代码 | < 200 行 |

### 测试工程师 (test-engineer)

| Agent | 功能 | 输出限制 |
|-------|------|----------|
| testcase-designer | 设计测试用例 | 文档 |
| unit-test-generator | 生成单元测试 | < 150 行 |
| integration-test-generator | 生成集成测试 | < 200 行 |
| e2e-test-generator | 生成 E2E 测试 | < 200 行 |

## 使用方式

### CLI 命令

```bash
# 创建任务（自动拆分）
python scripts/handoff_manager.py create frontend-dev "开发用户管理模块"

# 执行任务
python scripts/handoff_manager.py execute <task-id>

# 查看状态
python scripts/handoff_manager.py status <task-id>

# 列出任务
python scripts/handoff_manager.py list frontend-dev
```

### Python API

```python
from scripts.handoff_manager import HandoffManager

# 创建管理器
manager = HandoffManager(project_path, role="frontend-dev")

# 分析并拆分任务
task = manager.analyze_and_split(
    task_name="开发用户管理模块",
    context={"module": "user"}
)

# 执行任务
manager.execute_task(task.task_id)

# 查看状态
status = manager.get_status(task.task_id)
```

## 任务拆分示例

### 前端任务拆分

**任务**: 开发用户管理模块

自动拆分为：
1. 生成 user API 服务 (service-generator)
2. 生成 userStore 状态管理 (store-generator)
3. 生成 UserList 页面 (page-generator)
4. 生成 UserDetail 页面 (page-generator)
5. 生成 UserForm 组件 (component-generator)

### 后端任务拆分

**任务**: 开发用户管理 API

自动拆分为：
1. 生成 User 数据模型 (model-generator)
2. 生成 user API 端点 (api-generator)
3. 生成 UserService 业务逻辑 (service-generator-backend)
4. 生成 user 测试 (test-generator)

## 状态管理

任务状态保存在 `.agents/handoffs/state/<role>/` 目录下：

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

每个任务文件包含：
- 任务信息（ID、名称、状态）
- 子任务列表（每个子任务的状态和输出）
- 上下文信息
- 时间戳

## 最佳实践

1. **合理拆分**: 不要过度拆分，保持子任务的独立性
2. **保存状态**: 每个子任务完成后立即保存状态
3. **错误处理**: 子任务失败不影响已完成的部分，支持恢复
4. **进度跟踪**: 实时显示任务进度，记录耗时

## 扩展

如需添加新的 Handoff Agent：

1. 在 `.agents/handoffs/` 下创建新目录
2. 添加 `agent.json` 配置文件
3. 添加 `prompt.md` 提示词文件
4. 在 `handoff_manager.py` 中注册新 agent

## 注意事项

- Handoffs 是自动的，无需手动触发
- 每个子任务都有明确的输入输出
- 子任务之间通过状态文件传递信息
- 支持任务暂停和恢复
"""

    readme_path = project_path / ".agents" / "handoffs" / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("  ✓ README.md")


def create_state_directories(project_path: Path):
    """创建状态目录"""
    print("\n📁 创建状态目录...")

    roles = [
        "architect",
        "product-manager",
        "frontend-dev",
        "backend-dev",
        "test-engineer",
        "devops-engineer",
        "operations"
    ]

    state_base = project_path / ".agents" / "handoffs" / "state"

    for role in roles:
        role_dir = state_base / role
        role_dir.mkdir(parents=True, exist_ok=True)

        # 创建 .gitkeep 保持目录
        gitkeep = role_dir / ".gitkeep"
        gitkeep.touch()

    print(f"  ✓ 已创建 {len(roles)} 个角色的状态目录")
