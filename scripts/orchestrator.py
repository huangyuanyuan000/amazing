#!/usr/bin/env python3
"""
Amazing 初始化编排器

负责协调各个 handoff 阶段的执行，管理状态和上下文传递。
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


class InitState:
    """初始化状态管理"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.state_dir = project_path / ".amazing"
        self.state_file = self.state_dir / "init-state.json"
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """加载状态"""
        if self.state_file.exists():
            with open(self.state_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._default_state()

    def _default_state(self) -> Dict:
        """默认状态"""
        return {
            "project_name": "",
            "project_path": str(self.project_path),
            "product_description": "",
            "current_phase": None,
            "completed_phases": [],
            "phase_results": {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    def save(self):
        """保存状态"""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state["updated_at"] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def update(self, **kwargs):
        """更新状态"""
        self.state.update(kwargs)
        self.save()


class PhaseExecutor:
    """阶段执行器"""

    def __init__(self, phase_name: str, phase_config: Dict):
        self.phase_name = phase_name
        self.phase_config = phase_config

    def execute(self, context: Dict) -> Dict:
        """执行阶段"""
        print(f"\n{'='*60}")
        print(f"Phase: {self.phase_config['displayName']}")
        print(f"{'='*60}\n")

        # 调用对应的执行函数
        executor_func = getattr(self, f"_execute_{self.phase_name.replace('-', '_')}", None)
        if not executor_func:
            raise ValueError(f"Unknown phase: {self.phase_name}")

        result = executor_func(context)
        return result

    def _execute_structure_init(self, context: Dict) -> Dict:
        """执行基础结构初始化"""
        from .phases.structure_init import execute
        return execute(context)

    def _execute_handoffs_setup(self, context: Dict) -> Dict:
        """执行 Handoffs 能力部署"""
        from .phases.handoffs_setup import execute
        return execute(context)

    def _execute_role_config(self, context: Dict) -> Dict:
        """执行角色配置"""
        from .phases.role_config import execute
        return execute(context)

    def _execute_business_agent_gen(self, context: Dict) -> Dict:
        """执行业务 Agent 生成"""
        from .phases.business_agent_gen import execute
        return execute(context)

    def _execute_backend_gen(self, context: Dict) -> Dict:
        """执行后端代码生成"""
        from .phases.backend_gen import execute
        return execute(context)

    def _execute_frontend_gen(self, context: Dict) -> Dict:
        """执行前端代码生成"""
        from .phases.frontend_gen import execute
        return execute(context)

    def _execute_deploy_gen(self, context: Dict) -> Dict:
        """执行部署配置生成"""
        from .phases.deploy_gen import execute
        return execute(context)

    def _execute_docs_gen(self, context: Dict) -> Dict:
        """执行文档生成"""
        from .phases.docs_gen import execute
        return execute(context)


class Orchestrator:
    """初始化编排器"""

    PHASES = [
        {
            "name": "structure-init",
            "displayName": "基础结构初始化",
            "description": "创建项目目录和基础文件"
        },
        {
            "name": "handoffs-setup",
            "displayName": "Handoffs 能力部署",
            "description": "部署任务拆分和管理能力"
        },
        {
            "name": "role-config",
            "displayName": "角色配置",
            "description": "生成角色定义和权限配置"
        },
        {
            "name": "business-agent-gen",
            "displayName": "业务 Agent 生成",
            "description": "分析产品形态并生成业务模块"
        },
        {
            "name": "backend-gen",
            "displayName": "后端代码生成",
            "description": "生成后端代码和 API"
        },
        {
            "name": "frontend-gen",
            "displayName": "前端代码生成",
            "description": "生成前端界面和组件"
        },
        {
            "name": "deploy-gen",
            "displayName": "部署配置生成",
            "description": "生成 Docker、K8s 和私有化部署配置"
        },
        {
            "name": "docs-gen",
            "displayName": "文档生成",
            "description": "生成项目文档"
        }
    ]

    def __init__(self, project_name: str, project_path: Optional[Path] = None):
        self.project_name = project_name
        self.project_path = project_path or Path.cwd() / project_name
        self.state = InitState(self.project_path)

    def start(self, product_description: str):
        """开始初始化"""
        print(f"🚀 初始化项目: {self.project_name}\n")

        # 初始化状态
        self.state.update(
            project_name=self.project_name,
            product_description=product_description
        )

        # 执行各个阶段
        self._execute_phases()

        print("\n✅ 项目初始化完成！")
        print(f"\n📁 项目目录: {self.project_path}")
        print("\n下一步：")
        print(f"  cd {self.project_name}")
        print("  make dev")

    def resume(self):
        """恢复初始化"""
        print(f"🔄 恢复项目初始化: {self.project_name}\n")

        if not self.state.state_file.exists():
            print("❌ 未找到初始化状态，请使用 start 开始新的初始化")
            return

        print(f"已完成阶段: {', '.join(self.state.state['completed_phases'])}")
        print(f"当前阶段: {self.state.state.get('current_phase', 'None')}\n")

        # 继续执行剩余阶段
        self._execute_phases()

        print("\n✅ 项目初始化完成！")

    def _execute_phases(self):
        """执行所有阶段"""
        completed = set(self.state.state["completed_phases"])
        total = len(self.PHASES)

        for i, phase_config in enumerate(self.PHASES, 1):
            phase_name = phase_config["name"]

            # 跳过已完成的阶段
            if phase_name in completed:
                print(f"[✓] Phase {i}/{total}: {phase_config['displayName']} (已完成)")
                continue

            # 显示进度
            print(f"[→] Phase {i}/{total}: {phase_config['displayName']}")

            # 更新当前阶段
            self.state.update(current_phase=phase_name)

            # 执行阶段
            try:
                executor = PhaseExecutor(phase_name, phase_config)
                context = self._build_context()
                result = executor.execute(context)

                # 保存结果
                phase_results = self.state.state["phase_results"]
                phase_results[phase_name] = result
                completed_phases = self.state.state["completed_phases"]
                completed_phases.append(phase_name)

                self.state.update(
                    phase_results=phase_results,
                    completed_phases=completed_phases
                )

                print(f"[✓] Phase {i}/{total}: {phase_config['displayName']} (完成)\n")

            except Exception as e:
                print(f"\n❌ 阶段执行失败: {e}")
                print(f"\n可以使用以下命令恢复:")
                print(f"  python3 scripts/init.py {self.project_name} --resume")
                raise

    def _build_context(self) -> Dict:
        """构建执行上下文"""
        return {
            "project_name": self.state.state["project_name"],
            "project_path": self.project_path,
            "product_description": self.state.state["product_description"],
            "phase_results": self.state.state["phase_results"],
            "framework_path": Path(__file__).parent.parent
        }

    def get_status(self) -> Dict:
        """获取状态"""
        return self.state.state

