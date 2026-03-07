#!/usr/bin/env python3
"""
Phase 3: 业务 Agent 生成

分析产品形态，推荐业务模块划分，生成业务 Agent 配置
"""

import json
from pathlib import Path
from typing import Dict, List


def execute(context: Dict) -> Dict:
    """执行业务 Agent 生成"""
    project_path = context["project_path"]
    product_description = context["product_description"]

    print("✨ 分析产品形态...")

    # 检测产品类型
    product_type = detect_product_type(product_description)
    print(f"  产品类型: {product_type}")

    # 推荐业务 Agent
    agents = recommend_agents(product_type, product_description)

    print(f"\n📊 推荐 {len(agents)} 个业务模块:\n")
    for agent in agents:
        print(f"  • {agent['displayName']} - {agent['description']}")

    # 创建业务 Agent
    print("\n🔨 创建业务 Agent...")

    agents_dir = project_path / ".agents"
    for agent in agents:
        agent_dir = agents_dir / agent["name"]
        agent_dir.mkdir(parents=True, exist_ok=True)

        # 保存 Agent 配置
        config_file = agent_dir / "config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(agent, f, indent=2, ensure_ascii=False)

        print(f"  ✓ {agent['displayName']}")

    return {
        "business_agents": agents,
        "tech_stack": detect_tech_stack(product_description),
        "database_config": detect_database(product_description)
    }


def detect_product_type(description: str) -> str:
    """检测产品类型"""
    desc_lower = description.lower()

    if any(word in desc_lower for word in ['ai', 'ml', '模型', '训练', 'gpu', '大模型']):
        return 'ai-platform'
    elif any(word in desc_lower for word in ['电商', '商品', '订单', '支付', 'e-commerce']):
        return 'e-commerce'
    elif any(word in desc_lower for word in ['saas', '租户', '多租户', '订阅']):
        return 'saas'
    elif any(word in desc_lower for word in ['iot', '物联网', '设备', '传感器']):
        return 'iot'
    else:
        return 'custom'


def recommend_agents(product_type: str, description: str) -> List[Dict]:
    """推荐业务 Agent"""
    templates = {
        'ai-platform': [
            {
                'name': 'model-management',
                'displayName': '模型管理',
                'description': '模型注册、版本管理、元数据管理',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            },
            {
                'name': 'compute-management',
                'displayName': '算力管理',
                'description': 'GPU/CPU 资源调度和管理',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            },
            {
                'name': 'training-management',
                'displayName': '训练管理',
                'description': '训练任务编排和监控',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            },
            {
                'name': 'inference-service',
                'displayName': '推理服务',
                'description': '模型部署和推理',
                'techStack': {'backend': 'Go + Gin', 'database': 'Redis'}
            }
        ],
        'e-commerce': [
            {
                'name': 'product-management',
                'displayName': '商品管理',
                'description': '商品发布、分类、库存管理',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            },
            {
                'name': 'order-management',
                'displayName': '订单管理',
                'description': '订单创建、支付、物流',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            },
            {
                'name': 'user-management',
                'displayName': '用户管理',
                'description': '用户注册、登录、权限',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            }
        ],
        'saas': [
            {
                'name': 'tenant-management',
                'displayName': '租户管理',
                'description': '租户注册、配置、隔离',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            },
            {
                'name': 'project-management',
                'displayName': '项目管理',
                'description': '项目创建、任务管理',
                'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
            }
        ]
    }

    return templates.get(product_type, [
        {
            'name': 'core-service',
            'displayName': '核心服务',
            'description': '核心业务逻辑',
            'techStack': {'backend': 'Python + FastAPI', 'database': 'PostgreSQL'}
        }
    ])


def detect_tech_stack(description: str) -> Dict:
    """检测技术栈"""
    desc_lower = description.lower()

    backend = 'Python + FastAPI'
    if 'go' in desc_lower or 'golang' in desc_lower:
        backend = 'Go + Gin'
    elif 'java' in desc_lower:
        backend = 'Java + Spring Boot'
    elif 'node' in desc_lower or 'nodejs' in desc_lower:
        backend = 'Node.js + NestJS'

    frontend = 'React + TypeScript'
    if 'vue' in desc_lower:
        frontend = 'Vue + TypeScript'
    elif 'angular' in desc_lower:
        frontend = 'Angular + TypeScript'

    return {
        'backend': backend,
        'frontend': frontend
    }


def detect_database(description: str) -> Dict:
    """检测数据库"""
    desc_lower = description.lower()

    primary = 'PostgreSQL'
    if 'mysql' in desc_lower:
        primary = 'MySQL'
    elif 'mongodb' in desc_lower or 'mongo' in desc_lower:
        primary = 'MongoDB'

    cache = 'Redis'

    return {
        'primary': primary,
        'cache': cache
    }
