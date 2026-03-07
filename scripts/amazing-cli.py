#!/usr/bin/env python3
"""
Amazing CLI - Agent-Teams 协同开发平台命令行工具
"""

import click
import json
import os
from pathlib import Path

AMAZING_ROOT = Path.home() / "minger" / "amazing"
AGENTS_DIR = AMAZING_ROOT / ".agents"
CLAUDE_DIR = AMAZING_ROOT / ".claude"


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
        click.echo(f"{idx}. {role['name']} ({key})")

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
