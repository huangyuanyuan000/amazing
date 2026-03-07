#!/usr/bin/env python3
"""
Phase 4: 后端代码生成

生成后端代码，包括数据模型、API、业务逻辑和 AI 交互层
"""

from pathlib import Path
from typing import Dict


def execute(context: Dict) -> Dict:
    """执行后端代码生成"""
    project_path = context["project_path"]
    phase_results = context["phase_results"]

    # 获取业务 Agent 信息
    business_result = phase_results.get("business-agent-gen", {})
    agents = business_result.get("business_agents", [])
    tech_stack = business_result.get("tech_stack", {})

    print(f"🔧 生成后端代码 ({tech_stack.get('backend', 'Python + FastAPI')})...")

    backend_dir = project_path / "src" / "backend"

    # 为每个业务 Agent 生成后端代码
    for agent in agents:
        agent_name = agent["name"]
        print(f"\n  📦 {agent['displayName']} ({agent_name})")

        # 创建模块目录
        module_dir = backend_dir / agent_name
        module_dir.mkdir(parents=True, exist_ok=True)

        # 生成基础文件结构
        (module_dir / "models").mkdir(exist_ok=True)
        (module_dir / "api").mkdir(exist_ok=True)
        (module_dir / "services").mkdir(exist_ok=True)
        (module_dir / "ai").mkdir(exist_ok=True)

        # 生成 __init__.py
        (module_dir / "__init__.py").write_text("")
        (module_dir / "models" / "__init__.py").write_text("")
        (module_dir / "api" / "__init__.py").write_text("")
        (module_dir / "services" / "__init__.py").write_text("")
        (module_dir / "ai" / "__init__.py").write_text("")

        print(f"    ✓ 模块结构")
        print(f"    ✓ models/ - 数据模型")
        print(f"    ✓ api/ - API 接口")
        print(f"    ✓ services/ - 业务逻辑")
        print(f"    ✓ ai/ - AI 交互层")

    # 生成主应用文件
    print(f"\n  🚀 生成主应用...")
    generate_main_app(backend_dir, agents, tech_stack)

    # 生成配置文件
    print(f"  ⚙️  生成配置...")
    generate_config(backend_dir)

    # 生成 requirements.txt
    print(f"  📋 生成依赖...")
    generate_requirements(backend_dir, tech_stack)

    return {
        "backend_code": "generated",
        "modules": [a["name"] for a in agents],
        "api_specs": "pending"
    }


def generate_main_app(backend_dir: Path, agents: list, tech_stack: dict):
    """生成主应用文件"""
    if "FastAPI" in tech_stack.get("backend", ""):
        content = '''"""
主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Amazing API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Amazing API"}

@app.get("/health")
def health():
    return {"status": "ok"}
'''
        (backend_dir / "main.py").write_text(content)
        print("    ✓ main.py")


def generate_config(backend_dir: Path):
    """生成配置文件"""
    content = '''"""
配置管理
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Amazing"
    database_url: str = "postgresql://user:pass@localhost/db"
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"

settings = Settings()
'''
    (backend_dir / "config.py").write_text(content)
    print("    ✓ config.py")


def generate_requirements(backend_dir: Path, tech_stack: dict):
    """生成依赖文件"""
    if "FastAPI" in tech_stack.get("backend", ""):
        content = '''fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
redis==5.0.1
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
'''
        (backend_dir / "requirements.txt").write_text(content)
        print("    ✓ requirements.txt")
