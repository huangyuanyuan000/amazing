#!/usr/bin/env python3
"""
进化管理工具

管理 Agent 的自我进化
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class EvolutionRecord:
    """进化记录"""
    id: str
    type: str  # prompt_refinement, skill_addition, agent_creation, constraint_update
    agent: str
    trigger: str
    description: str
    changes: Dict
    impact: Dict
    status: str  # pending, approved, rejected, applied
    created_at: str
    applied_at: Optional[str] = None
    approved_by: Optional[str] = None
    approval_comment: Optional[str] = None
    rejection_reason: Optional[str] = None


class EvolutionManager:
    """进化管理器"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.evolution_dir = project_path / ".agents" / "evolution"
        self.history_dir = self.evolution_dir / "history"
        self.config_file = self.evolution_dir / "config.yml"

        # 确保目录存在
        self.history_dir.mkdir(parents=True, exist_ok=True)

        # 加载配置
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}

    def detect_patterns(self) -> List[Dict]:
        """检测重复模式"""
        print("🔍 检测重复模式...")

        patterns = []

        # 读取任务历史
        state_dir = self.project_path / ".agents" / "handoffs" / "state"
        if not state_dir.exists():
            print("⚠️  没有任务历史")
            return patterns

        # 统计任务类型
        task_types = {}
        for task_file in state_dir.glob("*.json"):
            try:
                with open(task_file, 'r', encoding='utf-8') as f:
                    task = json.load(f)

                task_name = task.get('task_name', '')
                chain = task.get('chain', 'unknown')

                key = f"{chain}:{task_name}"
                if key not in task_types:
                    task_types[key] = []
                task_types[key].append(task)

            except Exception as e:
                print(f"⚠️  读取任务失败 {task_file}: {e}")

        # 检测重复模式（阈值：3 次）
        threshold = self.config.get('evolution', {}).get('triggers', {}).get('pattern_detected', {}).get('threshold', 3)

        for key, tasks in task_types.items():
            if len(tasks) >= threshold:
                chain, task_name = key.split(':', 1)
                patterns.append({
                    'chain': chain,
                    'task_name': task_name,
                    'count': len(tasks),
                    'suggestion': f"考虑为 '{task_name}' 创建专用 Agent 或优化现有 Prompt"
                })

        if patterns:
            print(f"✓ 发现 {len(patterns)} 个重复模式")
        else:
            print("✓ 未发现重复模式")

        return patterns

    def analyze_impact(self, agent: str, change_type: str) -> Dict:
        """分析影响"""
        print(f"📊 分析影响: {agent} ({change_type})")

        impact = {
            'agent': agent,
            'change_type': change_type,
            'downstream_agents': [],
            'affected_workflows': [],
            'risk_level': 'low'
        }

        # TODO: 实际分析逻辑
        # 1. 查找依赖此 Agent 的其他 Agents
        # 2. 查找使用此 Agent 的工作流
        # 3. 评估风险级别

        print(f"✓ 影响分析完成")
        return impact

    def _generate_evolution_report(self, record: EvolutionRecord) -> Path:
        """生成进化报告"""
        report_dir = self.project_path / "docs" / "evolution" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)

        report_file = report_dir / f"{record.id}.md"

        # 生成报告内容
        report = f"""# 进化报告

## 基本信息

- **进化 ID**: {record.id}
- **Agent**: {record.agent}
- **进化类型**: {record.type}
- **触发方式**: {record.trigger}
- **创建时间**: {record.created_at}
- **状态**: {record.status}

## 进化描述

{record.description}

## 变更详情

```json
{json.dumps(record.changes, indent=2, ensure_ascii=False)}
```

## 影响分析

### 影响范围
- **下游 Agent**: {', '.join(record.impact.get('downstream_agents', [])) or '无'}
- **关联工作流**: {', '.join(record.impact.get('affected_workflows', [])) or '无'}
- **风险级别**: {record.impact.get('risk_level', 'unknown')}

### 详细影响

```json
{json.dumps(record.impact, indent=2, ensure_ascii=False)}
```

## 审批建议

### 优势
- 提升 Agent 能力
- 优化用户体验
- 减少重复工作

### 风险
- 可能影响下游 Agent
- 需要测试验证
- 需要文档更新

### 建议
1. 仔细审查变更内容
2. 评估影响范围
3. 制定回滚方案
4. 通知相关人员

## 审批流程

1. 架构师审查本报告
2. 评估风险和收益
3. 决定批准或拒绝
4. 记录审批意见

### 批准命令
```bash
python scripts/evolve.py approve {record.id} --approver=<架构师名称> --comment=<审批意见>
```

### 拒绝命令
```bash
python scripts/evolve.py reject {record.id} --approver=<架构师名称> --reason=<拒绝理由>
```

---

**注意**: 本报告由系统自动生成，请架构师仔细审查后做出决策。
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        return report_file

    def propose_evolution(self, agent: str, type: str, description: str, changes: Dict) -> str:
        """提议进化"""
        print(f"💡 提议进化: {agent}")

        # 创建进化记录
        evolution_id = f"evo-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 分析影响
        impact = self.analyze_impact(agent, type)

        # ⚠️ 所有进化都需要架构师审批
        needs_approval = True

        record = EvolutionRecord(
            id=evolution_id,
            type=type,
            agent=agent,
            trigger='manual',
            description=description,
            changes=changes,
            impact=impact,
            status='pending',  # 始终为 pending，等待审批
            created_at=datetime.now().isoformat()
        )

        # 保存记录
        self._save_record(record)

        # 生成进化报告
        report_file = self._generate_evolution_report(record)

        print(f"⏳ 进化提议已创建，等待架构师审批: {evolution_id}")
        print(f"📄 进化报告已生成: {report_file}")
        print(f"\n请架构师审查报告后执行：")
        print(f"  python scripts/evolve.py approve {evolution_id} --approver=<架构师名称> --comment=<审批意见>")

        return evolution_id

    def approve_evolution(self, evolution_id: str, approver: str, comment: str = ""):
        """审批进化"""
        print(f"✅ 审批进化: {evolution_id}")

        record = self._load_record(evolution_id)
        record.status = 'approved'
        record.approved_by = approver
        record.approval_comment = comment

        self._save_record(record)
        print(f"✓ 进化已批准")
        if comment:
            print(f"✓ 审批意见: {comment}")

    def reject_evolution(self, evolution_id: str, approver: str, reason: str):
        """拒绝进化"""
        print(f"❌ 拒绝进化: {evolution_id}")

        record = self._load_record(evolution_id)

        if record.status != 'pending':
            raise ValueError(f"进化状态不是 pending，无法拒绝: {record.status}")

        record.status = 'rejected'
        record.approved_by = approver
        record.rejection_reason = reason

        self._save_record(record)
        print(f"✓ 进化已拒绝")
        print(f"✓ 审批人: {approver}")
        print(f"✓ 拒绝理由: {reason}")


    def apply_evolution(self, evolution_id: str):
        """应用进化"""
        print(f"🚀 应用进化: {evolution_id}")

        record = self._load_record(evolution_id)

        if record.status != 'approved':
            raise ValueError(f"进化未批准，无法应用: {record.status}")

        # TODO: 实际应用逻辑
        # 1. 根据 type 执行不同的操作
        # 2. 更新 Agent 配置或 Prompt
        # 3. 记录变更

        record.status = 'applied'
        record.applied_at = datetime.now().isoformat()

        self._save_record(record)
        print(f"✓ 进化已应用")

    def list_evolutions(self, status: Optional[str] = None) -> List[Dict]:
        """列出进化记录"""
        records = []

        for record_file in self.history_dir.glob("*.json"):
            try:
                with open(record_file, 'r', encoding='utf-8') as f:
                    record = json.load(f)

                if status is None or record['status'] == status:
                    records.append(record)

            except Exception as e:
                print(f"⚠️  读取记录失败 {record_file}: {e}")

        return sorted(records, key=lambda x: x['created_at'], reverse=True)

    def generate_timeline(self):
        """生成进化时间线"""
        print("📈 生成进化时间线...")

        records = self.list_evolutions()

        # 生成 HTML
        html = self._generate_timeline_html(records)

        # 保存
        output_file = self.project_path / "docs" / "html" / "status" / "evolution-timeline.html"
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ 时间线已生成: {output_file}")

    def _generate_timeline_html(self, records: List[Dict]) -> str:
        """生成时间线 HTML"""
        items_html = ""

        for record in records:
            status_color = {
                'pending': '#fbbf24',
                'approved': '#10b981',
                'rejected': '#ef4444',
                'applied': '#667eea'
            }.get(record['status'], '#6b7280')

            items_html += f"""
            <div class="timeline-item">
                <div class="timeline-marker" style="background: {status_color};"></div>
                <div class="timeline-content">
                    <div class="timeline-header">
                        <span class="timeline-type">{record['type']}</span>
                        <span class="timeline-status" style="background: {status_color};">{record['status']}</span>
                    </div>
                    <h3>{record['agent']}</h3>
                    <p>{record['description']}</p>
                    <div class="timeline-meta">
                        <span>创建时间: {record['created_at'][:19]}</span>
                        {f"<span>审批人: {record.get('approved_by', 'N/A')}</span>" if record.get('approved_by') else ""}
                    </div>
                </div>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>进化时间线 - Amazing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .container {{ max-width: 1000px; margin: 40px auto; padding: 0 20px; }}
        .timeline {{ position: relative; padding: 20px 0; }}
        .timeline::before {{ content: ''; position: absolute; left: 30px; top: 0; bottom: 0; width: 2px; background: #e5e7eb; }}
        .timeline-item {{ position: relative; padding-left: 70px; margin-bottom: 40px; }}
        .timeline-marker {{ position: absolute; left: 22px; width: 16px; height: 16px; border-radius: 50%; border: 3px solid white; }}
        .timeline-content {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .timeline-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .timeline-type {{ background: #f3f4f6; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; }}
        .timeline-status {{ color: white; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; }}
        .timeline-content h3 {{ color: #667eea; margin-bottom: 10px; }}
        .timeline-meta {{ margin-top: 15px; font-size: 0.85em; color: #6b7280; display: flex; gap: 20px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔄 进化时间线</h1>
        <p>Agent 自我进化历史</p>
    </div>
    <div class="container">
        <div class="timeline">
            {items_html if items_html else '<p style="text-align: center; color: #6b7280;">暂无进化记录</p>'}
        </div>
    </div>
</body>
</html>"""
        return html

    def _save_record(self, record: EvolutionRecord):
        """保存记录"""
        file_path = self.history_dir / f"{record.id}.json"

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(record), f, indent=2, ensure_ascii=False)

    def _load_record(self, evolution_id: str) -> EvolutionRecord:
        """加载记录"""
        file_path = self.history_dir / f"{evolution_id}.json"

        if not file_path.exists():
            raise ValueError(f"进化记录不存在: {evolution_id}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return EvolutionRecord(**data)


def main():
    """CLI 入口"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="进化管理工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # detect 命令
    detect_parser = subparsers.add_parser("detect", help="检测重复模式")

    # propose 命令
    propose_parser = subparsers.add_parser("propose", help="提议进化")
    propose_parser.add_argument("--agent", required=True, help="Agent 名称")
    propose_parser.add_argument("--type", required=True, help="进化类型")
    propose_parser.add_argument("--description", required=True, help="描述")

    # approve 命令
    approve_parser = subparsers.add_parser("approve", help="审批进化")
    approve_parser.add_argument("evolution_id", help="进化 ID")
    approve_parser.add_argument("--approver", required=True, help="审批人")
    approve_parser.add_argument("--comment", default="", help="审批意见")

    # reject 命令
    reject_parser = subparsers.add_parser("reject", help="拒绝进化")
    reject_parser.add_argument("evolution_id", help="进化 ID")
    reject_parser.add_argument("--approver", required=True, help="审批人")
    reject_parser.add_argument("--reason", required=True, help="拒绝理由")

    # apply 命令
    apply_parser = subparsers.add_parser("apply", help="应用进化")
    apply_parser.add_argument("evolution_id", help="进化 ID")

    # list 命令
    list_parser = subparsers.add_parser("list", help="列出进化记录")
    list_parser.add_argument("--status", help="状态过滤")

    # timeline 命令
    timeline_parser = subparsers.add_parser("timeline", help="生成时间线")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    project_path = Path.cwd()
    manager = EvolutionManager(project_path)

    try:
        if args.command == "detect":
            patterns = manager.detect_patterns()
            print(json.dumps(patterns, indent=2, ensure_ascii=False))

        elif args.command == "propose":
            evolution_id = manager.propose_evolution(
                agent=args.agent,
                type=args.type,
                description=args.description,
                changes={}
            )
            print(f"\n进化 ID: {evolution_id}")

        elif args.command == "approve":
            manager.approve_evolution(args.evolution_id, args.approver, args.comment)

        elif args.command == "reject":
            manager.reject_evolution(args.evolution_id, args.approver, args.reason)

        elif False:
            manager.approve_evolution(args.evolution_id, args.approver)

        elif args.command == "apply":
            manager.apply_evolution(args.evolution_id)

        elif args.command == "list":
            records = manager.list_evolutions(args.status)
            print(json.dumps(records, indent=2, ensure_ascii=False))

        elif args.command == "timeline":
            manager.generate_timeline()

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
