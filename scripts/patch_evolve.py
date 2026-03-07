#!/usr/bin/env python3
"""
完善进化系统 - 添加进化报告生成功能

在 evolve.py 中添加以下功能：
1. 生成详细的进化报告
2. 添加审批意见记录
3. 添加拒绝功能
"""

import re
from pathlib import Path

# 读取原文件
evolve_file = Path("scripts/evolve.py")
content = evolve_file.read_text(encoding='utf-8')

# 1. 在 EvolutionRecord 中添加新字段
if 'approval_comment' not in content:
    content = content.replace(
        'approved_by: Optional[str] = None',
        '''approved_by: Optional[str] = None
    approval_comment: Optional[str] = None
    rejection_reason: Optional[str] = None'''
    )
    print("✓ 添加审批意见字段")

# 2. 添加生成进化报告的方法
report_method = '''
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

{json.dumps(record.impact, indent=2, ensure_ascii=False)}

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
'''

if '_generate_evolution_report' not in content:
    # 在 analyze_impact 方法后添加
    content = content.replace(
        '        print(f"✓ 影响分析完成")\n        return impact',
        '        print(f"✓ 影响分析完成")\n        return impact\n' + report_method
    )
    print("✓ 添加生成进化报告方法")

# 3. 添加 reject 方法
reject_method = '''
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
'''

if 'def reject_evolution' not in content:
    # 在 approve_evolution 方法后添加
    content = content.replace(
        '        self._save_record(record)\n        print(f"✓ 进化已批准")',
        '''        self._save_record(record)
        print(f"✓ 进化已批准")
        if comment:
            print(f"✓ 审批意见: {comment}")
''' + reject_method
    )
    print("✓ 添加拒绝进化方法")

# 4. 更新 approve_evolution 方法签名
content = content.replace(
    'def approve_evolution(self, evolution_id: str, approver: str):',
    'def approve_evolution(self, evolution_id: str, approver: str, comment: str = ""):'
)

content = content.replace(
    '        record.approved_by = approver\n\n        self._save_record(record)',
    '''        record.approved_by = approver
        record.approval_comment = comment

        self._save_record(record)'''
)

# 5. 更新 CLI 参数
content = content.replace(
    '    approve_parser.add_argument("--approver", required=True, help="审批人")',
    '''    approve_parser.add_argument("--approver", required=True, help="审批人")
    approve_parser.add_argument("--comment", default="", help="审批意见")'''
)

# 添加 reject 命令
if 'reject_parser' not in content:
    content = content.replace(
        '    # apply 命令',
        '''    # reject 命令
    reject_parser = subparsers.add_parser("reject", help="拒绝进化")
    reject_parser.add_argument("evolution_id", help="进化 ID")
    reject_parser.add_argument("--approver", required=True, help="审批人")
    reject_parser.add_argument("--reason", required=True, help="拒绝理由")

    # apply 命令'''
    )
    print("✓ 添加 reject 命令")

# 添加 reject 命令处理
if 'elif args.command == "reject":' not in content:
    content = content.replace(
        '        elif args.command == "approve":',
        '''        elif args.command == "approve":
            manager.approve_evolution(args.evolution_id, args.approver, args.comment)

        elif args.command == "reject":
            manager.reject_evolution(args.evolution_id, args.approver, args.reason)

        elif args.command == "approve_old":'''
    )
    # 修正重复
    content = content.replace('elif args.command == "approve_old":', 'elif False:')

# 写回文件
evolve_file.write_text(content, encoding='utf-8')
print("\n✅ 进化系统完善完成！")
