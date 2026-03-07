#!/usr/bin/env python3
"""
Handoff 管理器 v3.0

支持 3 种任务执行模式：
- Auto（全自动）：链路自动流转到终点
- Semi-Auto（半自动）：每节点暂停确认
- Chain Slice（链路切片）：指定起止环节

支持 9 条 Handoff Chain：
- product-analysis（产品分析链）
- tech-architecture（技术架构链）
- code-generation（代码开发链）
- testing（测试链）
- bug-fix（Bug 修复链）
- deployment（部署运维链）
- operations（运营链）
- code-review（代码审查链）
- evolution（进化迭代链）
"""

import json
import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum


class ExecutionMode(Enum):
    """执行模式"""
    AUTO = "auto"              # 全自动
    SEMI_AUTO = "semi_auto"    # 半自动
    CHAIN_SLICE = "chain_slice"  # 链路切片


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class HandoffConfig:
    """Handoff 配置"""
    id: str
    name: str
    agent: str
    output: Optional[str] = None
    html_output: Optional[str] = None
    max_lines: int = 200
    per_module: bool = False
    ironclaw_role: Optional[str] = None
    condition: Optional[str] = None


@dataclass
class ChainConfig:
    """Chain 配置"""
    chain: str
    name: str
    description: str
    handoffs: List[HandoffConfig]


@dataclass
class SubTask:
    """子任务"""
    id: str
    name: str
    agent: str
    status: str
    input: Dict
    output: Optional[Dict] = None
    error: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class Task:
    """任务"""
    task_id: str
    task_name: str
    chain: Optional[str] = None  # 所属链路
    mode: str = "auto"  # 执行模式
    from_handoff: Optional[str] = None  # 起始 Handoff（Chain Slice）
    to_handoff: Optional[str] = None  # 终止 Handoff（Chain Slice）
    role: Optional[str] = None
    status: str = "pending"
    subtasks: List[SubTask] = None
    context: Dict = None
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
        if self.subtasks is None:
            self.subtasks = []
        if self.context is None:
            self.context = {}


class HandoffManager:
    """Handoff 管理器 v3.0"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.chains_dir = project_path / ".agents" / "handoffs" / "chains"
        self.state_dir = project_path / ".agents" / "handoffs" / "state"
        self.ironclaw_dir = project_path / ".claude" / "ironclaw" / "instances"

        # 确保目录存在
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # 加载配置
        self.chains = self._load_chains()
        self.ironclaw_instances = self._load_ironclaw_instances()

    def _load_chains(self) -> Dict[str, ChainConfig]:
        """加载所有 Chain 配置"""
        chains = {}

        if not self.chains_dir.exists():
            print(f"⚠️  Chains 目录不存在: {self.chains_dir}")
            return chains

        for chain_file in self.chains_dir.glob("*.yml"):
            try:
                with open(chain_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                handoffs = []
                for h in data.get('handoffs', []):
                    handoffs.append(HandoffConfig(
                        id=h['id'],
                        name=h['name'],
                        agent=h['agent'],
                        output=h.get('output'),
                        html_output=h.get('html_output'),
                        max_lines=h.get('max_lines', 200),
                        per_module=h.get('per_module', False),
                        ironclaw_role=h.get('ironclaw_role'),
                        condition=h.get('condition')
                    ))

                chain_config = ChainConfig(
                    chain=data['chain'],
                    name=data['name'],
                    description=data['description'],
                    handoffs=handoffs
                )

                chains[data['chain']] = chain_config

            except Exception as e:
                print(f"⚠️  加载 Chain 配置失败 {chain_file}: {e}")

        return chains

    def _load_ironclaw_instances(self) -> Dict[str, Dict]:
        """加载所有 IronClaw 实例"""
        instances = {}

        if not self.ironclaw_dir.exists():
            print(f"⚠️  IronClaw 目录不存在: {self.ironclaw_dir}")
            return instances

        for instance_file in self.ironclaw_dir.glob("*.yml"):
            try:
                with open(instance_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                role = data['ironclaw_instance']['role']
                instances[role] = data['ironclaw_instance']

            except Exception as e:
                print(f"⚠️  加载 IronClaw 实例失败 {instance_file}: {e}")

        return instances

    def run(self, task_name: str, chain: Optional[str] = None,
            mode: str = "auto", from_handoff: Optional[str] = None,
            to_handoff: Optional[str] = None, context: Optional[Dict] = None) -> Task:
        """
        运行任务

        Args:
            task_name: 任务名称
            chain: 链路名称（可选）
            mode: 执行模式（auto/semi_auto）
            from_handoff: 起始 Handoff ID（Chain Slice 模式）
            to_handoff: 终止 Handoff ID（Chain Slice 模式）
            context: 上下文
        """
        print(f"\n🚀 运行任务: {task_name}")
        print(f"执行模式: {mode}")

        if chain:
            print(f"链路: {chain}")
        if from_handoff and to_handoff:
            print(f"链路切片: {from_handoff} → {to_handoff}")

        # 创建任务
        task = self._create_task(task_name, chain, mode, from_handoff, to_handoff, context or {})

        # 执行任务
        if mode == "auto":
            return self._execute_auto(task)
        elif mode == "semi_auto":
            return self._execute_semi_auto(task)
        else:
            raise ValueError(f"不支持的执行模式: {mode}")

    def _create_task(self, task_name: str, chain: Optional[str], mode: str,
                     from_handoff: Optional[str], to_handoff: Optional[str],
                     context: Dict) -> Task:
        """创建任务"""
        task_id = f"task-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 生成子任务
        subtasks = self._generate_subtasks(task_name, chain, from_handoff, to_handoff, context)

        task = Task(
            task_id=task_id,
            task_name=task_name,
            chain=chain,
            mode=mode,
            from_handoff=from_handoff,
            to_handoff=to_handoff,
            status="pending",
            subtasks=subtasks,
            context=context
        )

        self._save_task(task)

        print(f"\n✅ 任务已创建: {task_id}")
        print(f"子任务数量: {len(subtasks)}")
        for i, st in enumerate(subtasks, 1):
            print(f"  {i}. {st.name} ({st.agent})")

        return task

    def _generate_subtasks(self, task_name: str, chain: Optional[str],
                          from_handoff: Optional[str], to_handoff: Optional[str],
                          context: Dict) -> List[SubTask]:
        """生成子任务"""
        subtasks = []

        if chain and chain in self.chains:
            # 从 Chain 配置生成
            chain_config = self.chains[chain]
            handoffs = chain_config.handoffs

            # Chain Slice 模式：过滤 Handoffs
            if from_handoff and to_handoff:
                start_idx = next((i for i, h in enumerate(handoffs) if h.id == from_handoff), 0)
                end_idx = next((i for i, h in enumerate(handoffs) if h.id == to_handoff), len(handoffs) - 1)
                handoffs = handoffs[start_idx:end_idx + 1]

            for handoff in handoffs:
                subtasks.append(SubTask(
                    id=handoff.id,
                    name=handoff.name,
                    agent=handoff.agent,
                    status="pending",
                    input={
                        "task_name": task_name,
                        "context": context,
                        "output": handoff.output,
                        "html_output": handoff.html_output,
                        "max_lines": handoff.max_lines
                    }
                ))
        else:
            # 默认：单个子任务
            subtasks.append(SubTask(
                id="1",
                name=task_name,
                agent="default",
                status="pending",
                input={"task_name": task_name, "context": context}
            ))

        return subtasks

    def _execute_auto(self, task: Task) -> Task:
        """全自动执行"""
        print(f"\n🤖 全自动模式：链路自动流转到终点")

        task.status = "in_progress"
        self._save_task(task)

        for i, subtask in enumerate(task.subtasks, 1):
            print(f"\n[{i}/{len(task.subtasks)}] {subtask.name}")

            try:
                # 执行子任务
                result = self._execute_subtask(subtask, task.context)

                subtask.status = "completed"
                subtask.output = result
                subtask.completed_at = datetime.now().isoformat()

                print(f"✓ 完成")

            except Exception as e:
                subtask.status = "failed"
                subtask.error = str(e)
                task.status = "failed"
                self._save_task(task)

                print(f"✗ 失败: {e}")
                raise

            self._save_task(task)

        task.status = "completed"
        self._save_task(task)

        print(f"\n✅ 任务完成: {task.task_name}")
        return task

    def _execute_semi_auto(self, task: Task) -> Task:
        """半自动执行"""
        print(f"\n👤 半自动模式：每节点暂停等待确认")

        task.status = "in_progress"
        self._save_task(task)

        for i, subtask in enumerate(task.subtasks, 1):
            print(f"\n[{i}/{len(task.subtasks)}] {subtask.name}")
            print(f"Agent: {subtask.agent}")

            # 等待用户确认
            choice = input("\n选择操作 [c]继续 [s]跳过 [a]中止: ").strip().lower()

            if choice == 'a':
                task.status = "paused"
                self._save_task(task)
                print("⏸️  任务已暂停")
                return task

            if choice == 's':
                subtask.status = "skipped"
                print("⏭️  已跳过")
                self._save_task(task)
                continue

            try:
                # 执行子任务
                result = self._execute_subtask(subtask, task.context)

                subtask.status = "completed"
                subtask.output = result
                subtask.completed_at = datetime.now().isoformat()

                print(f"✓ 完成")

            except Exception as e:
                subtask.status = "failed"
                subtask.error = str(e)
                print(f"✗ 失败: {e}")

                retry = input("是否重试? [y/N]: ").strip().lower()
                if retry == 'y':
                    # 重试逻辑
                    pass
                else:
                    task.status = "failed"
                    self._save_task(task)
                    raise

            self._save_task(task)

        task.status = "completed"
        self._save_task(task)

        print(f"\n✅ 任务完成: {task.task_name}")
        return task

    def _execute_subtask(self, subtask: SubTask, context: Dict) -> Dict:
        """执行子任务"""
        # TODO: 实际调用 agent
        # 目前返回模拟结果
        return {
            "status": "success",
            "message": f"子任务 {subtask.name} 执行成功",
            "agent": subtask.agent
        }

    def pause(self, task_id: str):
        """暂停任务"""
        task = self._load_task(task_id)
        task.status = "paused"
        self._save_task(task)
        print(f"⏸️  任务已暂停: {task_id}")

    def resume(self, task_id: str):
        """恢复任务"""
        task = self._load_task(task_id)

        if task.mode == "auto":
            return self._execute_auto(task)
        else:
            return self._execute_semi_auto(task)

    def rollback(self, task_id: str, to_handoff: str):
        """回滚任务到指定 Handoff"""
        task = self._load_task(task_id)

        # 找到目标 Handoff
        target_idx = next((i for i, st in enumerate(task.subtasks) if st.id == to_handoff), None)

        if target_idx is None:
            raise ValueError(f"Handoff 不存在: {to_handoff}")

        # 重置后续任务状态
        for i in range(target_idx, len(task.subtasks)):
            task.subtasks[i].status = "pending"
            task.subtasks[i].output = None
            task.subtasks[i].error = None
            task.subtasks[i].completed_at = None

        task.status = "in_progress"
        self._save_task(task)

        print(f"↩️  任务已回滚到: {to_handoff}")

    def status(self, task_id: str) -> Dict:
        """获取任务状态"""
        task = self._load_task(task_id)

        completed = sum(1 for st in task.subtasks if st.status == "completed")
        total = len(task.subtasks)

        return {
            "task_id": task.task_id,
            "task_name": task.task_name,
            "chain": task.chain,
            "mode": task.mode,
            "status": task.status,
            "progress": f"{completed}/{total}",
            "subtasks": [
                {
                    "id": st.id,
                    "name": st.name,
                    "status": st.status,
                    "agent": st.agent
                }
                for st in task.subtasks
            ]
        }

    def list_tasks(self) -> List[Dict]:
        """列出所有任务"""
        tasks = []
        for file in self.state_dir.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    tasks.append({
                        "task_id": data["task_id"],
                        "task_name": data["task_name"],
                        "chain": data.get("chain"),
                        "mode": data.get("mode", "auto"),
                        "status": data["status"],
                        "created_at": data["created_at"]
                    })
            except Exception as e:
                print(f"⚠️  加载任务失败 {file}: {e}")

        return sorted(tasks, key=lambda x: x["created_at"], reverse=True)

    def _save_task(self, task: Task):
        """保存任务"""
        file_path = self.state_dir / f"{task.task_id}.json"

        data = {
            "task_id": task.task_id,
            "task_name": task.task_name,
            "chain": task.chain,
            "mode": task.mode,
            "from_handoff": task.from_handoff,
            "to_handoff": task.to_handoff,
            "role": task.role,
            "status": task.status,
            "subtasks": [asdict(st) for st in task.subtasks],
            "context": task.context,
            "created_at": task.created_at,
            "updated_at": datetime.now().isoformat()
        }

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _load_task(self, task_id: str) -> Task:
        """加载任务"""
        file_path = self.state_dir / f"{task_id}.json"

        if not file_path.exists():
            raise ValueError(f"任务不存在: {task_id}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        subtasks = [SubTask(**st) for st in data["subtasks"]]

        return Task(
            task_id=data["task_id"],
            task_name=data["task_name"],
            chain=data.get("chain"),
            mode=data.get("mode", "auto"),
            from_handoff=data.get("from_handoff"),
            to_handoff=data.get("to_handoff"),
            role=data.get("role"),
            status=data["status"],
            subtasks=subtasks,
            context=data["context"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Handoff 管理器 v3.0")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行任务")
    run_parser.add_argument("--task", required=True, help="任务名称")
    run_parser.add_argument("--chain", help="链路名称")
    run_parser.add_argument("--mode", default="auto", choices=["auto", "semi_auto"], help="执行模式")
    run_parser.add_argument("--from", dest="from_handoff", help="起始 Handoff ID")
    run_parser.add_argument("--to", dest="to_handoff", help="终止 Handoff ID")

    # status 命令
    status_parser = subparsers.add_parser("status", help="查看任务状态")
    status_parser.add_argument("task_id", help="任务 ID")

    # pause 命令
    pause_parser = subparsers.add_parser("pause", help="暂停任务")
    pause_parser.add_argument("task_id", help="任务 ID")

    # resume 命令
    resume_parser = subparsers.add_parser("resume", help="恢复任务")
    resume_parser.add_argument("task_id", help="任务 ID")

    # rollback 命令
    rollback_parser = subparsers.add_parser("rollback", help="回滚任务")
    rollback_parser.add_argument("task_id", help="任务 ID")
    rollback_parser.add_argument("--to", required=True, help="回滚到的 Handoff ID")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出所有任务")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    project_path = Path.cwd()
    manager = HandoffManager(project_path)

    try:
        if args.command == "run":
            manager.run(
                task_name=args.task,
                chain=args.chain,
                mode=args.mode,
                from_handoff=args.from_handoff,
                to_handoff=args.to_handoff
            )

        elif args.command == "status":
            status = manager.status(args.task_id)
            print(json.dumps(status, indent=2, ensure_ascii=False))

        elif args.command == "pause":
            manager.pause(args.task_id)

        elif args.command == "resume":
            manager.resume(args.task_id)

        elif args.command == "rollback":
            manager.rollback(args.task_id, args.to)

        elif args.command == "list":
            tasks = manager.list_tasks()
            print(json.dumps(tasks, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
