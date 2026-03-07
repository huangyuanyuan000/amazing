#!/usr/bin/env python3
"""
Amazing CLI - AI 模式管理
支持全自动和半自动模式切换
只有架构师有权限切换模式
"""

import click
import json
from pathlib import Path
from datetime import datetime

AMAZING_ROOT = Path.home() / "minger" / "amazing"
AGENTS_CONFIG = AMAZING_ROOT / ".agents" / "config.json"
USER_CONFIG = AMAZING_ROOT / ".claude" / "user.json"


def check_architect_permission():
    """检查是否有架构师权限"""
    if not USER_CONFIG.exists():
        return False, "未找到用户配置文件"

    try:
        with open(USER_CONFIG) as f:
            user_data = json.load(f)

        current_role = user_data.get("role", "")
        if current_role != "architect":
            return False, f"权限不足：只有架构师可以切换模式（当前角色: {current_role}）"

        return True, "权限验证通过"
    except Exception as e:
        return False, f"权限验证失败: {str(e)}"


def log_mode_change(old_mode, new_mode, requirement_id=None):
    """记录模式切换日志"""
    log_dir = AMAZING_ROOT / ".agents" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / "mode_changes.log"

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "old_mode": old_mode,
        "new_mode": new_mode,
        "requirement_id": requirement_id,
        "operator": "architect"
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")


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
@click.option('--requirement-id', '-r', help='需求ID')
@click.option('--reason', help='切换原因')
def set(mode_name, requirement_id, reason):
    """切换 AI 模式（仅架构师）"""
    # 权限检查
    has_permission, message = check_architect_permission()
    if not has_permission:
        click.echo(f"❌ {message}")
        click.echo("\n💡 提示: 请先切换到架构师角色")
        click.echo("   python3 scripts/amazing-cli.py role set architect")
        return

    if not AGENTS_CONFIG.exists():
        click.echo("❌ 配置文件不存在")
        return

    with open(AGENTS_CONFIG) as f:
        config = json.load(f)

    old_mode = config.get("mode", {}).get("current", "unknown")

    # 如果模式相同，不需要切换
    if old_mode == mode_name:
        click.echo(f"ℹ️  当前已经是 {mode_name} 模式")
        return

    # 记录切换信息
    config["mode"]["current"] = mode_name
    config["orchestrator"]["mode"] = mode_name

    # 添加切换记录
    if "modeHistory" not in config:
        config["modeHistory"] = []

    config["modeHistory"].append({
        "timestamp": datetime.now().isoformat(),
        "from": old_mode,
        "to": mode_name,
        "requirement_id": requirement_id,
        "reason": reason,
        "operator": "architect"
    })

    with open(AGENTS_CONFIG, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    # 记录日志
    log_mode_change(old_mode, mode_name, requirement_id)

    click.echo(f"✅ 模式已切换: {old_mode} → {mode_name}")

    if requirement_id:
        click.echo(f"   需求ID: {requirement_id}")
    if reason:
        click.echo(f"   切换原因: {reason}")

    mode_info = config.get("mode", {}).get("options", {}).get(mode_name, {})
    click.echo(f"\n{mode_info.get('description', '')}")


@mode.command()
def history():
    """查看模式切换历史"""
    if not AGENTS_CONFIG.exists():
        click.echo("❌ 配置文件不存在")
        return

    with open(AGENTS_CONFIG) as f:
        config = json.load(f)

    history = config.get("modeHistory", [])

    if not history:
        click.echo("暂无模式切换历史")
        return

    click.echo("\n模式切换历史:")
    click.echo("-" * 80)

    for record in reversed(history[-10:]):  # 显示最近10条
        click.echo(f"\n时间: {record.get('timestamp', 'N/A')}")
        click.echo(f"切换: {record.get('from', 'N/A')} → {record.get('to', 'N/A')}")
        if record.get('requirement_id'):
            click.echo(f"需求ID: {record['requirement_id']}")
        if record.get('reason'):
            click.echo(f"原因: {record['reason']}")
        click.echo(f"操作者: {record.get('operator', 'N/A')}")


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
@click.option('--requirement-id', '-r', help='需求ID')
def mode(agent_name, mode_name, requirement_id):
    """设置特定 Agent 的模式（仅架构师）"""
    # 权限检查
    has_permission, message = check_architect_permission()
    if not has_permission:
        click.echo(f"❌ {message}")
        return

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
    agent_config["autonomy"]["requirement_id"] = requirement_id
    agent_config["autonomy"]["updated_at"] = datetime.now().isoformat()

    with open(AGENTS_CONFIG, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    click.echo(f"✅ {agent_name} Agent 模式已设置为: {mode_name}")
    if requirement_id:
        click.echo(f"   需求ID: {requirement_id}")


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

    if autonomy.get("requirement_id"):
        click.echo(f"需求ID: {autonomy['requirement_id']}")
    if autonomy.get("updated_at"):
        click.echo(f"更新时间: {autonomy['updated_at']}")

    click.echo(f"\n全自动模式配置:")
    click.echo(json.dumps(autonomy.get("full-auto", {}), indent=2, ensure_ascii=False))
    click.echo(f"\n半自动模式配置:")
    click.echo(json.dumps(autonomy.get("semi-auto", {}), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    cli = click.Group()
    cli.add_command(mode)
    cli.add_command(agent)
    cli()



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
