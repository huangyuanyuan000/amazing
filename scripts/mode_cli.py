#!/usr/bin/env python3
"""
Amazing CLI - AI 模式管理
支持全自动和半自动模式切换
"""

import click
import json
from pathlib import Path
from datetime import datetime

AMAZING_ROOT = Path.home() / "minger" / "amazing"
AGENTS_CONFIG = AMAZING_ROOT / ".agents" / "config.json"


@click.group()
def mode():
    """AI 模式管理"""
    pass


@mode.command()
def show():
    """显示当前模式"""
    if not AGENTS_CONFIG.exists():
        click.echo("❌ 配置文件不存在")
        return

    with open(AGENTS_CONFIG) as f:
        config = json.load(f)

    current_mode = config.get("mode", {}).get("current", "unknown")
    mode_info = config.get("mode", {}).get("options", {}).get(current_mode, {})

    click.echo(f"\n当前模式: {current_mode}")
    click.echo(f"描述: {mode_info.get('description', 'N/A')}")
    click.echo(f"\n特性:")
    for feature in mode_info.get("features", []):
        click.echo(f"  - {feature}")


@mode.command()
@click.argument('mode_name', type=click.Choice(['full-auto', 'semi-auto']))
def set(mode_name):
    """切换 AI 模式"""
    if not AGENTS_CONFIG.exists():
        click.echo("❌ 配置文件不存在")
        return

    with open(AGENTS_CONFIG) as f:
        config = json.load(f)

    old_mode = config.get("mode", {}).get("current", "unknown")
    config["mode"]["current"] = mode_name
    config["orchestrator"]["mode"] = mode_name

    with open(AGENTS_CONFIG, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    click.echo(f"✅ 模式已切换: {old_mode} → {mode_name}")

    mode_info = config.get("mode", {}).get("options", {}).get(mode_name, {})
    click.echo(f"\n{mode_info.get('description', '')}")


@mode.command()
def config():
    """显示模式配置"""
    if not AGENTS_CONFIG.exists():
        click.echo("❌ 配置文件不存在")
        return

    with open(AGENTS_CONFIG) as f:
        config = json.load(f)

    current_mode = config.get("mode", {}).get("current", "unknown")
    orchestrator = config.get("orchestrator", {})
    human_interaction = orchestrator.get("humanInteraction", {}).get(current_mode, {})

    click.echo(f"\n当前模式: {current_mode}")
    click.echo(f"\n配置详情:")
    click.echo(json.dumps(human_interaction, indent=2, ensure_ascii=False))


@mode.command()
def pause():
    """暂停 AI 执行"""
    status_file = AMAZING_ROOT / ".agents" / "status.json"
    status_file.parent.mkdir(parents=True, exist_ok=True)

    status = {
        "state": "paused",
        "timestamp": datetime.now().isoformat(),
        "reason": "manual-pause"
    }

    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)

    click.echo("⏸️  AI 执行已暂停")


@mode.command()
def resume():
    """恢复 AI 执行"""
    status_file = AMAZING_ROOT / ".agents" / "status.json"

    if not status_file.exists():
        click.echo("❌ 没有暂停的任务")
        return

    status = {
        "state": "running",
        "timestamp": datetime.now().isoformat(),
        "reason": "manual-resume"
    }

    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)

    click.echo("▶️  AI 执行已恢复")


@mode.command()
def manual():
    """切换到手动模式"""
    status_file = AMAZING_ROOT / ".agents" / "status.json"
    status_file.parent.mkdir(parents=True, exist_ok=True)

    status = {
        "state": "manual",
        "timestamp": datetime.now().isoformat(),
        "reason": "manual-override"
    }

    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)

    click.echo("🖐️  已切换到手动模式，AI 将不再自动执行")


@click.group()
def agent():
    """Agent 模式管理"""
    pass


@agent.command()
@click.argument('agent_name')
@click.argument('mode_name', type=click.Choice(['full-auto', 'semi-auto']))
def mode(agent_name, mode_name):
    """设置特定 Agent 的模式"""
    if not AGENTS_CONFIG.exists():
        click.echo("❌ 配置文件不存在")
        return

    with open(AGENTS_CONFIG) as f:
        config = json.load(f)

    if agent_name not in config.get("agents", {}):
        click.echo(f"❌ Agent 不存在: {agent_name}")
        return

    # 设置 Agent 的模式
    agent_config = config["agents"][agent_name]
    if "autonomy" not in agent_config:
        agent_config["autonomy"] = {}

    agent_config["autonomy"]["current"] = mode_name

    with open(AGENTS_CONFIG, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    click.echo(f"✅ {agent_name} Agent 模式已设置为: {mode_name}")


@agent.command()
@click.argument('agent_name')
def show(agent_name):
    """显示特定 Agent 的模式"""
    if not AGENTS_CONFIG.exists():
        click.echo("❌ 配置文件不存在")
        return

    with open(AGENTS_CONFIG) as f:
        config = json.load(f)

    if agent_name not in config.get("agents", {}):
        click.echo(f"❌ Agent 不存在: {agent_name}")
        return

    agent_config = config["agents"][agent_name]
    autonomy = agent_config.get("autonomy", {})
    current_mode = autonomy.get("current", config.get("mode", {}).get("current", "unknown"))

    click.echo(f"\n{agent_name} Agent")
    click.echo(f"当前模式: {current_mode}")
    click.echo(f"\n全自动模式配置:")
    click.echo(json.dumps(autonomy.get("full-auto", {}), indent=2, ensure_ascii=False))
    click.echo(f"\n半自动模式配置:")
    click.echo(json.dumps(autonomy.get("semi-auto", {}), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    cli = click.Group()
    cli.add_command(mode)
    cli.add_command(agent)
    cli()
