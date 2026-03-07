#!/usr/bin/env python3
"""
Phase 1: 基础结构初始化

创建项目目录结构，复制模板文件，初始化 Git 仓库
"""

import shutil
from pathlib import Path
from typing import Dict


def execute(context: Dict) -> Dict:
    """执行基础结构初始化"""
    project_path = context["project_path"]
    framework_path = context["framework_path"]

    print("📁 创建项目目录...")

    # 创建基础目录结构
    directories = [
        ".agents/common",
        ".claude/roles",
        ".claude/skills",
        ".claude/ironclaw",
        "src/backend",
        "src/frontend",
        "deploy/docker",
        "deploy/k8s",
        "deploy/offline",
        "docs",
        "tests",
        "scripts"
    ]

    created_dirs = []
    for dir_path in directories:
        full_path = project_path / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(dir_path))
        print(f"  ✓ {dir_path}")

    print("\n📋 复制模板文件...")

    # 复制通用 Agent
    common_agent = framework_path / ".agents" / "common"
    if common_agent.exists():
        shutil.copytree(common_agent, project_path / ".agents" / "common", dirs_exist_ok=True)
        print("  ✓ 通用 Agent (用户/权限/日志)")

    # 复制 IronClaw 配置
    ironclaw_config = framework_path / ".claude" / "ironclaw"
    if ironclaw_config.exists():
        shutil.copytree(ironclaw_config, project_path / ".claude" / "ironclaw", dirs_exist_ok=True)
        print("  ✓ IronClaw 权限体系")

    # 创建基础配置文件
    print("\n⚙️  创建配置文件...")

    # .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Amazing
.amazing/
*.log
"""

    with open(project_path / ".gitignore", "w") as f:
        f.write(gitignore_content)
    print("  ✓ .gitignore")

    # Makefile
    makefile_content = """# Amazing Project Makefile

.PHONY: dev docker k8s offline status clean

dev:
\t@echo "🚀 启动开发环境..."
\tdocker-compose -f deploy/docker/docker-compose.dev.yml up

docker:
\t@echo "🐳 Docker 部署..."
\tdocker-compose -f deploy/docker/docker-compose.yml up -d

k8s:
\t@echo "☸️  Kubernetes 部署..."
\tkubectl apply -f deploy/k8s/

offline:
\t@echo "📦 构建离线部署包..."
\tbash deploy/offline/build.sh

status:
\t@echo "📊 服务状态..."
\tdocker-compose ps

clean:
\t@echo "🧹 清理环境..."
\tdocker-compose down -v
"""

    with open(project_path / "Makefile", "w") as f:
        f.write(makefile_content)
    print("  ✓ Makefile")

    # 初始化 Git
    print("\n🔧 初始化 Git 仓库...")
    import subprocess
    try:
        subprocess.run(["git", "init"], cwd=project_path, check=True, capture_output=True)
        print("  ✓ Git 仓库已初始化")
    except Exception as e:
        print(f"  ⚠️  Git 初始化失败: {e}")

    return {
        "created_directories": created_dirs,
        "copied_files": ["common agent", "ironclaw config"],
        "config_files": [".gitignore", "Makefile"]
    }
