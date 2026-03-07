#!/usr/bin/env python3
"""
批量生成 Handoff Agents

快速生成剩余的 32 个 Agents 配置文件
"""

import json
from pathlib import Path

# Agent 定义
AGENTS = {
    # 产品分析链（5 个）
    "domain-analyzer": {
        "type": "product-analysis",
        "description": "业务领域分析器",
        "output": "docs/product/domain-analysis.md",
        "prompt": "分析业务领域，识别核心业务概念、业务流程和业务规则"
    },
    "persona-modeler": {
        "type": "product-analysis",
        "description": "用户角色建模器",
        "output": "docs/product/user-personas.md",
        "prompt": "建立用户画像，分析用户需求、行为和痛点"
    },
    "module-decomposer": {
        "type": "product-analysis",
        "description": "功能模块拆分器",
        "output": "docs/product/module-breakdown.md",
        "prompt": "拆分功能模块，定义模块边界和依赖关系"
    },
    "story-generator": {
        "type": "product-analysis",
        "description": "用户故事生成器",
        "output": "docs/product/user-stories/",
        "prompt": "生成用户故事，包含角色、目标、价值和验收标准"
    },
    "spec-writer": {
        "type": "product-analysis",
        "description": "产品规格书生成器",
        "output": "docs/product/PRD.md",
        "prompt": "编写产品规格书（PRD），包含需求、功能、流程和验收标准"
    },

    # 测试链（6 个）
    "test-strategist": {
        "type": "testing",
        "description": "测试策略制定器",
        "output": "docs/testing/test-strategy.md",
        "prompt": "制定测试策略，包含测试范围、测试方法、测试工具和质量标准"
    },
    "unit-test-generator": {
        "type": "testing",
        "description": "单元测试生成器",
        "output": "tests/unit/",
        "prompt": "生成单元测试，覆盖率 ≥ 80%"
    },
    "integration-test-generator": {
        "type": "testing",
        "description": "集成测试生成器",
        "output": "tests/integration/",
        "prompt": "生成集成测试，测试模块间交互"
    },
    "e2e-test-generator": {
        "type": "testing",
        "description": "E2E 测试生成器",
        "output": "tests/e2e/",
        "prompt": "生成端到端测试，测试完整业务流程"
    },
    "performance-test-generator": {
        "type": "testing",
        "description": "性能测试生成器",
        "output": "tests/performance/",
        "prompt": "生成性能测试，测试响应时间和并发能力"
    },
    "test-report-generator": {
        "type": "testing",
        "description": "测试报告生成器",
        "output": "docs/testing/test-report.md",
        "prompt": "生成测试报告，包含测试结果、覆盖率和问题列表"
    },

    # Bug 修复链（6 个）
    "bug-reporter": {
        "type": "bug-fix",
        "description": "Bug 报告器",
        "output": "issues/{bug-id}.md",
        "prompt": "标准化 Bug 报告，包含复现步骤、环境信息、截图和严重程度"
    },
    "priority-assessor": {
        "type": "bug-fix",
        "description": "优先级评估器",
        "output": "priority assessment",
        "prompt": "评估 Bug 优先级（critical/high/medium/low）和影响范围"
    },
    "root-cause-analyzer": {
        "type": "bug-fix",
        "description": "根因分析器",
        "output": "root cause analysis",
        "prompt": "定位 Bug 根本原因，分析影响范围，提出修复方案"
    },
    "bug-fixer": {
        "type": "bug-fix",
        "description": "Bug 修复器",
        "output": "code fix",
        "prompt": "修复 Bug，确保不引入新问题"
    },
    "regression-tester": {
        "type": "bug-fix",
        "description": "回归测试器",
        "output": "regression test results",
        "prompt": "执行回归测试，确保修复有效且无副作用"
    },
    "hotfix-deployer": {
        "type": "bug-fix",
        "description": "热修复部署器",
        "output": "deployment result",
        "prompt": "快速部署热修复，仅用于 critical 级别 Bug"
    },

    # 部署运维链（4 个）
    "deployment-requester": {
        "type": "deployment",
        "description": "部署申请器",
        "output": "deployment request",
        "prompt": "创建部署申请，包含环境、版本、变更说明和回滚方案"
    },
    "deployment-executor": {
        "type": "deployment",
        "description": "部署执行器",
        "output": "deployment result",
        "prompt": "执行部署，包含备份、部署、健康检查和自动回滚"
    },
    "deployment-verifier": {
        "type": "deployment",
        "description": "部署验证器",
        "output": "verification result",
        "prompt": "验证部署，执行冒烟测试和核心链路验证"
    },
    "deployment-notifier": {
        "type": "deployment",
        "description": "部署通知器",
        "output": "notification sent",
        "prompt": "通知相关人员部署结果，更新变更日志"
    },

    # 运营链（4 个）
    "data-analyst": {
        "type": "operations",
        "description": "数据分析器",
        "output": "data analysis",
        "prompt": "分析用户行为、核心指标和漏斗转化"
    },
    "report-generator": {
        "type": "operations",
        "description": "报告生成器",
        "output": "docs/operations/report-{date}.md",
        "prompt": "生成运营报告，包含数据分析、趋势和建议"
    },
    "strategy-advisor": {
        "type": "operations",
        "description": "策略建议器",
        "output": "strategy recommendations",
        "prompt": "提供运营策略建议，包含增长、留存和转化优化"
    },
    "config-manager": {
        "type": "operations",
        "description": "配置管理器",
        "output": "config changes",
        "prompt": "管理运营配置，包含功能开关、A/B 测试和推送策略"
    },

    # 代码审查链（3 个）
    "auto-checker": {
        "type": "code-review",
        "description": "自动检查器",
        "output": "check results",
        "prompt": "自动检查代码风格、安全漏洞、依赖问题和测试覆盖率"
    },
    "peer-reviewer": {
        "type": "code-review",
        "description": "同行评审器",
        "output": "review comments",
        "prompt": "同行评审代码质量，提供改进建议"
    },
    "architect-reviewer": {
        "type": "code-review",
        "description": "架构师审批器",
        "output": "approval result",
        "prompt": "架构师审批架构变更、API 变更和数据库变更"
    },

    # 进化链（4 个）
    "pattern-detector": {
        "type": "evolution",
        "description": "模式检测器",
        "output": "detected patterns",
        "prompt": "检测重复模式，识别优化机会"
    },
    "impact-analyzer": {
        "type": "evolution",
        "description": "影响分析器",
        "output": "impact analysis",
        "prompt": "分析变更影响，识别下游 Agent 和关联工作流"
    },
    "evolution-executor": {
        "type": "evolution",
        "description": "进化执行器",
        "output": "evolution result",
        "prompt": "执行进化，优化 Prompt、添加 Skill、更新约束"
    },
    "evolution-logger": {
        "type": "evolution",
        "description": "进化记录器",
        "output": "docs/html/status/evolution-timeline.html",
        "prompt": "记录进化历史，生成进化时间线"
    }
}


def generate_agent(name: str, config: dict):
    """生成单个 Agent"""
    base_dir = Path(".agents/init-handoffs") / name
    base_dir.mkdir(parents=True, exist_ok=True)

    # 生成 agent.json
    agent_json = {
        "name": name,
        "type": config["type"],
        "description": config["description"],
        "max_lines": 200,
        "output": config["output"]
    }

    if "html" in config.get("output", ""):
        agent_json["html_output"] = config["output"]

    with open(base_dir / "agent.json", "w", encoding="utf-8") as f:
        json.dump(agent_json, f, indent=2, ensure_ascii=False)

    # 生成 prompt.md
    prompt_md = f"""# {config['description']}

## 角色
你是一个 {config['description']}。

## 任务
{config['prompt']}

## 输入
- 任务上下文
- 相关文档
- 前置步骤输出

## 输出
{config['output']}

## 约束
- 单文件 ≤ 200 行
- 输出清晰可执行
- 遵循项目规范
"""

    with open(base_dir / "prompt.md", "w", encoding="utf-8") as f:
        f.write(prompt_md)

    print(f"✓ {name}")


def main():
    """批量生成"""
    print("🚀 批量生成 Handoff Agents\n")

    for name, config in AGENTS.items():
        generate_agent(name, config)

    print(f"\n✅ 完成！共生成 {len(AGENTS)} 个 Agents")


if __name__ == "__main__":
    main()
