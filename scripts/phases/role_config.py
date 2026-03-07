#!/usr/bin/env python3
"""
Phase 2: 角色配置

生成角色定义、IronClaw 权限配置和工作流配置
"""

import json
import shutil
from pathlib import Path
from typing import Dict


def execute(context: Dict) -> Dict:
    """执行角色配置"""
    project_path = context["project_path"]
    framework_path = context["framework_path"]

    print("👥 配置角色...")

    # 定义角色
    roles = [
        {
            "name": "architect",
            "displayName": "架构师",
            "icon": "👑",
            "level": "admin",
            "permissions": ["all"],
            "skills": ["architecture-design", "code-review", "tech-decision"]
        },
        {
            "name": "product-manager",
            "displayName": "产品经理",
            "icon": "📋",
            "level": "manager",
            "permissions": ["read:all", "write:docs/requirements/", "approve:requirements"],
            "skills": ["requirement-analysis", "acceptance-test", "prioritization"]
        },
        {
            "name": "frontend-dev",
            "displayName": "前端开发",
            "icon": "🎨",
            "level": "developer",
            "permissions": ["read:docs/,src/frontend/", "write:src/frontend/,tests/frontend/"],
            "skills": ["react-dev", "ui-implementation", "frontend-test"]
        },
        {
            "name": "backend-dev",
            "displayName": "后端开发",
            "icon": "⚙️",
            "level": "developer",
            "permissions": ["read:docs/,src/backend/", "write:src/backend/,tests/backend/"],
            "skills": ["api-dev", "database-design", "backend-test"]
        },
        {
            "name": "test-engineer",
            "displayName": "测试工程师",
            "icon": "🧪",
            "level": "developer",
            "permissions": ["read:all", "write:tests/"],
            "skills": ["test-design", "automation-test", "bug-report"]
        },
        {
            "name": "devops-engineer",
            "displayName": "运维工程师",
            "icon": "🚀",
            "level": "operator",
            "permissions": ["read:all", "write:deploy/", "execute:deploy,rollback"],
            "skills": ["deployment", "monitoring", "troubleshooting"]
        }
    ]

    # 创建角色目录和配置
    roles_dir = project_path / ".claude" / "roles"
    for role in roles:
        role_dir = roles_dir / role["name"]
        role_dir.mkdir(parents=True, exist_ok=True)

        # 保存角色配置
        config_file = role_dir / "config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(role, f, indent=2, ensure_ascii=False)

        print(f"  {role['icon']} {role['displayName']}")

    # 生成权限配置
    print("\n🔐 配置权限...")

    permissions_config = {
        "roles": {r["name"]: {"level": r["level"], "permissions": r["permissions"]} for r in roles}
    }

    permissions_file = project_path / ".claude" / "ironclaw" / "permissions.json"
    with open(permissions_file, "w", encoding="utf-8") as f:
        json.dump(permissions_config, f, indent=2, ensure_ascii=False)
    print("  ✓ 权限配置已生成")

    # 生成工作流配置
    print("\n🔄 配置工作流...")

    workflows = [
        {
            "name": "feature-development",
            "displayName": "需求开发流程",
            "trigger": "new_requirement",
            "steps": [
                {"name": "需求定义", "actor": "product-manager"},
                {"name": "架构设计", "actor": "architect", "approval_required": True},
                {"name": "前端开发", "actor": "frontend-dev", "parallel": True},
                {"name": "后端开发", "actor": "backend-dev", "parallel": True},
                {"name": "集成测试", "actor": "test-engineer"},
                {"name": "部署", "actor": "devops-engineer"},
                {"name": "验收", "actor": "product-manager", "approval_required": True}
            ]
        },
        {
            "name": "bug-fix",
            "displayName": "Bug 修复流程",
            "trigger": "bug_reported",
            "steps": [
                {"name": "Bug 报告", "actor": "any"},
                {"name": "优先级评估", "actor": "product-manager"},
                {"name": "分配开发者", "actor": "architect"},
                {"name": "修复实现", "actor": ["frontend-dev", "backend-dev"]},
                {"name": "测试验证", "actor": "test-engineer", "approval_required": True},
                {"name": "紧急部署", "actor": "devops-engineer"}
            ]
        }
    ]

    workflows_dir = project_path / ".claude" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    for workflow in workflows:
        workflow_file = workflows_dir / f"{workflow['name']}.json"
        with open(workflow_file, "w", encoding="utf-8") as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        print(f"  ✓ {workflow['displayName']}")

    return {
        "roles": [r["name"] for r in roles],
        "permissions": "configured",
        "workflows": [w["name"] for w in workflows]
    }
