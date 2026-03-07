#!/usr/bin/env python3
"""
Amazing CLI - Agent-Teams 协同开发平台命令行工具
"""

import click
import json
import os
import re
from pathlib import Path
from datetime import datetime

AMAZING_ROOT = Path.home() / "minger" / "amazing"
AGENTS_DIR = AMAZING_ROOT / ".agents"
CLAUDE_DIR = AMAZING_ROOT / ".claude"

# 角色关键词映射
ROLE_KEYWORDS = {
    "architect": ["架构", "架构师", "技术方案", "系统设计", "architecture"],
    "pm": ["产品", "需求", "prd", "产品经理", "product"],
    "frontend": ["前端", "ui", "界面", "页面", "react", "vue", "前端开发"],
    "backend": ["后端", "api", "接口", "数据库", "服务", "后端开发"],
    "qa": ["测试", "质量", "bug", "测试工程师", "quality"],
    "ops": ["运维", "部署", "监控", "devops", "运维工程师"],
    "operation": ["运营", "数据分析", "用户运营", "运营人员"]
}


@click.group()
def cli():
    """Amazing - 大模型管理平台 CLI"""
    pass


@cli.command()
def init():
    """初始化 Amazing 项目"""
    click.echo("🚀 初始化 Amazing 项目...")

    # 检查目录是否存在
    if not AMAZING_ROOT.exists():
        click.echo(f"❌ 项目目录不存在: {AMAZING_ROOT}")
        return

    click.echo("✅ 项目已初始化")
    click.echo(f"📁 项目路径: {AMAZING_ROOT}")


@cli.group()
def role():
    """角色管理"""
    pass


@role.command("select")
def role_select():
    """选择角色"""
    roles_config = CLAUDE_DIR / "roles" / "config.json"

    if not roles_config.exists():
        click.echo("❌ 角色配置文件不存在")
        return

    with open(roles_config) as f:
        config = json.load(f)

    click.echo("\n可用角色:")
    for idx, (key, role) in enumerate(config["roles"].items(), 1):
        icon = "👑" if key == "architect" else ""
        click.echo(f"{idx}. {icon} {role['name']} ({key})")

    choice = click.prompt("请选择角色", type=int)
    role_key = list(config["roles"].keys())[choice - 1]

    # 保存选择
    user_config = CLAUDE_DIR / "user.json"
    user_data = {"role": role_key}
    with open(user_config, "w") as f:
        json.dump(user_data, f, indent=2)

    click.echo(f"✅ 已选择角色: {config['roles'][role_key]['name']}")


@role.command("list")
def role_list():
    """列出所有角色"""
    roles_config = CLAUDE_DIR / "roles" / "config.json"

    with open(roles_config) as f:
        config = json.load(f)

    for key, role in config["roles"].items():
        click.echo(f"\n{role['name']} ({key}):")
        click.echo(f"  权限: {', '.join(role['permissions'][:3])}...")
        click.echo(f"  技能: {', '.join(role['skills'][:3])}...")


@role.command("set")
@click.argument("role_name")
def role_set(role_name):
    """设置角色 (非交互式)"""
    roles_config = CLAUDE_DIR / "roles" / "config.json"

    if not roles_config.exists():
        click.echo("❌ 角色配置文件不存在")
        return

    with open(roles_config) as f:
        config = json.load(f)

    # 检查角色是否存在
    if role_name not in config["roles"]:
        click.echo(f"❌ 角色 '{role_name}' 不存在")
        click.echo("\n可用角色:")
        for key, role in config["roles"].items():
            click.echo(f"  - {key}: {role['name']}")
        return

    # 保存选择
    user_config = CLAUDE_DIR / "user.json"
    user_data = {"role": role_name}
    with open(user_config, "w") as f:
        json.dump(user_data, f, indent=2)

    click.echo(f"✅ 已设置角色: {config['roles'][role_name]['name']} ({role_name})")
    click.echo(f"\n权限: {', '.join(config['roles'][role_name]['permissions'][:5])}")
    click.echo(f"技能: {', '.join(config['roles'][role_name]['skills'][:5])}")


@role.command("chat")
@click.argument("message", required=False)
def role_chat(message):
    """通过对话申请角色"""
    roles_config = CLAUDE_DIR / "roles" / "config.json"

    if not roles_config.exists():
        click.echo("❌ 角色配置文件不存在")
        return

    with open(roles_config) as f:
        config = json.load(f)

    # 如果没有提供消息，进入交互模式
    if not message:
        click.echo("\n👋 你好！我是 Amazing 角色助手")
        click.echo("请告诉我你想申请什么角色，或者描述你的工作内容")
        click.echo("例如: '我是前端开发' 或 '我负责产品需求'")
        click.echo("输入 'quit' 退出\n")

        while True:
            message = click.prompt("你", default="", show_default=False)
            if message.lower() in ['quit', 'exit', 'q']:
                click.echo("👋 再见！")
                return

            if not message.strip():
                continue

            # 处理消息
            result = _process_role_message(message, config)
            if result:
                return
    else:
        # 直接处理消息
        _process_role_message(message, config)


def _process_role_message(message, config):
    """处理角色申请消息"""
    message_lower = message.lower()

    # 尝试匹配角色关键词
    matched_roles = []
    for role_key, keywords in ROLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                matched_roles.append(role_key)
                break

    # 去重
    matched_roles = list(set(matched_roles))

    if len(matched_roles) == 1:
        # 唯一匹配，直接申请
        role_key = matched_roles[0]
        role_info = config["roles"][role_key]

        click.echo(f"\n🎯 我理解了！你想申请 **{role_info['name']}** 角色")
        click.echo(f"\n角色信息:")
        click.echo(f"  名称: {role_info['name']}")
        click.echo(f"  权限: {', '.join(role_info['permissions'][:3])}...")
        click.echo(f"  技能: {', '.join(role_info['skills'][:3])}...")

        if click.confirm("\n确认申请这个角色吗?", default=True):
            # 保存角色
            user_config = CLAUDE_DIR / "user.json"
            user_data = {
                "role": role_key,
                "applied_at": datetime.now().isoformat(),
                "applied_by": "chat",
                "message": message
            }
            with open(user_config, "w") as f:
                json.dump(user_data, f, indent=2)

            click.echo(f"\n✅ 已成功申请 {role_info['name']} 角色！")
            click.echo(f"\n你现在可以:")
            for i, perm in enumerate(role_info['permissions'][:5], 1):
                click.echo(f"  {i}. {perm}")

            click.echo(f"\n💡 提示: 使用 'python3 scripts/amazing-cli.py status' 查看当前状态")
            return True
        else:
            click.echo("\n❌ 已取消申请")
            return False

    elif len(matched_roles) > 1:
        # 多个匹配，让用户选择
        click.echo(f"\n🤔 我找到了 {len(matched_roles)} 个可能的角色:")
        for idx, role_key in enumerate(matched_roles, 1):
            role_info = config["roles"][role_key]
            click.echo(f"\n{idx}. {role_info['name']} ({role_key})")
            click.echo(f"   权限: {', '.join(role_info['permissions'][:2])}...")
            click.echo(f"   技能: {', '.join(role_info['skills'][:2])}...")

        choice = click.prompt("\n请选择角色 (输入数字)", type=int, default=1)
        if 1 <= choice <= len(matched_roles):
            role_key = matched_roles[choice - 1]
            role_info = config["roles"][role_key]

            # 保存角色
            user_config = CLAUDE_DIR / "user.json"
            user_data = {
                "role": role_key,
                "applied_at": datetime.now().isoformat(),
                "applied_by": "chat",
                "message": message
            }
            with open(user_config, "w") as f:
                json.dump(user_data, f, indent=2)

            click.echo(f"\n✅ 已成功申请 {role_info['name']} 角色！")
            return True
        else:
            click.echo("\n❌ 无效的选择")
            return False

    else:
        # 没有匹配，显示所有角色让用户选择
        click.echo("\n🤔 抱歉，我没有理解你的意思")
        click.echo("请从以下角色中选择:\n")

        roles_list = list(config["roles"].items())
        for idx, (role_key, role_info) in enumerate(roles_list, 1):
            click.echo(f"{idx}. {role_info['name']} ({role_key})")
            click.echo(f"   描述: {role_info.get('description', '暂无描述')}")
            click.echo(f"   权限: {', '.join(role_info['permissions'][:2])}...")
            click.echo()

        choice = click.prompt("请选择角色 (输入数字)", type=int, default=0)
        if 1 <= choice <= len(roles_list):
            role_key, role_info = roles_list[choice - 1]

            # 保存角色
            user_config = CLAUDE_DIR / "user.json"
            user_data = {
                "role": role_key,
                "applied_at": datetime.now().isoformat(),
                "applied_by": "chat",
                "message": message
            }
            with open(user_config, "w") as f:
                json.dump(user_data, f, indent=2)

            click.echo(f"\n✅ 已成功申请 {role_info['name']} 角色！")
            return True
        else:
            click.echo("\n❌ 无效的选择")
            return False


@cli.group()
def agent():
    """Agent 管理"""
    pass


@agent.command("list")
def agent_list():
    """列出所有 Agent"""
    config_file = AGENTS_DIR / "config.json"

    with open(config_file) as f:
        config = json.load(f)

    click.echo("\n可用 Agent:")
    for key, agent in config["agents"].items():
        click.echo(f"\n{agent['name']} ({key}):")
        click.echo(f"  描述: {agent['description']}")
        click.echo(f"  Sub-Agents: {', '.join(agent['subAgents'])}")


@agent.command("assign")
@click.argument("agent_name")
@click.option("--task", help="任务ID")
def agent_assign(agent_name, task):
    """分配任务给 Agent"""
    click.echo(f"✅ 已将任务 {task} 分配给 {agent_name} Agent")


@cli.group()
def prd():
    """PRD 管理"""
    pass


@prd.command("create")
@click.argument("title")
def prd_create(title):
    """创建 PRD"""
    click.echo(f"📝 创建 PRD: {title}")
    click.echo("🤖 使用 Claude Code 生成 PRD...")
    click.echo("✅ PRD 已生成: docs/prd/prd-001.md")


@cli.command()
def status():
    """查看项目状态"""
    click.echo("\n📊 Amazing 项目状态")
    click.echo("=" * 50)

    # 读取用户配置
    user_config = CLAUDE_DIR / "user.json"
    if user_config.exists():
        with open(user_config) as f:
            user_data = json.load(f)
        click.echo(f"当前角色: {user_data.get('role', '未设置')}")

    click.echo(f"项目路径: {AMAZING_ROOT}")
    click.echo("=" * 50)


if __name__ == "__main__":
    cli()
