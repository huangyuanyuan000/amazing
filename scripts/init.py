#!/usr/bin/env python3
"""
Amazing 初始化脚本

使用 orchestrator 进行分步初始化，支持恢复中断的初始化流程。
"""

import sys
import argparse
from pathlib import Path
from orchestrator import Orchestrator


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Amazing 项目初始化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 新建项目
  python3 scripts/init.py my-project

  # 交互式初始化
  python3 scripts/init.py my-project --interactive

  # 恢复中断的初始化
  python3 scripts/init.py my-project --resume

  # 从模板初始化
  python3 scripts/init.py my-project --template=ai-platform

  # 从案例初始化
  python3 scripts/init.py my-project --from-example=model-platform

  # 选择业务 Agent
  python3 scripts/init.py my-project --business-agents=compute,data
        """
    )

    parser.add_argument(
        'project_name',
        help='项目名称'
    )

    parser.add_argument(
        '--path',
        dest='project_path',
        help='项目路径（默认为当前目录下的项目名）'
    )

    parser.add_argument(
        '--resume',
        action='store_true',
        help='恢复中断的初始化'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='交互式初始化（引导用户输入）'
    )

    parser.add_argument(
        '--template',
        help='使用模板初始化（ai-platform/e-commerce/saas/iot）'
    )

    parser.add_argument(
        '--from-example',
        dest='from_example',
        help='从案例初始化（model-platform/e-commerce/saas）'
    )

    parser.add_argument(
        '--business-agents',
        dest='business_agents',
        help='选择业务 Agent 模板（compute,data,training,model-service）'
    )

    parser.add_argument(
        '--desc',
        dest='product_description',
        help='产品描述（非交互模式）'
    )

    parser.add_argument(
        '--status',
        action='store_true',
        help='查看初始化状态'
    )

    args = parser.parse_args()

    # 创建 orchestrator
    project_path = Path(args.project_path) if args.project_path else None
    orchestrator = Orchestrator(args.project_name, project_path)

    # 查看状态
    if args.status:
        status = orchestrator.get_status()
        print(f"项目: {status['project_name']}")
        print(f"路径: {status['project_path']}")
        print(f"当前阶段: {status.get('current_phase', 'None')}")
        print(f"已完成阶段: {', '.join(status['completed_phases'])}")
        return

    # 恢复初始化
    if args.resume:
        orchestrator.resume()
        return

    # 获取产品描述
    product_description = None

    if args.from_example:
        # 从案例初始化
        product_description = load_example_description(args.from_example)
        if not product_description:
            print(f"❌ 未找到案例: {args.from_example}")
            print("可用案例: model-platform, e-commerce, saas")
            sys.exit(1)

    elif args.template:
        # 从模板初始化
        product_description = load_template_description(args.template)
        if not product_description:
            print(f"❌ 未找到模板: {args.template}")
            print("可用模板: ai-platform, e-commerce, saas, iot")
            sys.exit(1)

    elif args.interactive:
        # 交互式输入
        product_description = interactive_input()

    elif args.product_description:
        # 命令行参数
        product_description = args.product_description

    else:
        # 默认交互式
        product_description = interactive_input()

    # 解析业务 Agent
    business_agents = []
    if args.business_agents:
        business_agents = [agent.strip() for agent in args.business_agents.split(',')]
        # 验证业务 Agent
        valid_agents = ['compute', 'data', 'training', 'model-service']
        invalid = [a for a in business_agents if a not in valid_agents]
        if invalid:
            print(f"❌ 无效的业务 Agent: {', '.join(invalid)}")
            print(f"可用的业务 Agent: {', '.join(valid_agents)}")
            sys.exit(1)

    # 开始初始化
    orchestrator.start(product_description, business_agents=business_agents)


def interactive_input() -> str:
    """交互式输入产品描述"""
    print()
    print("=" * 60)
    print("Amazing 项目初始化")
    print("=" * 60)
    print()
    print("请描述你的产品形态（详细描述核心功能、目标用户、技术要求等）")
    print("输入 'done' 结束输入")
    print()

    lines = []
    while True:
        try:
            line = input("> ")
            if line.strip().lower() == 'done':
                break
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            print("\n\n❌ 初始化已取消")
            sys.exit(0)

    description = "\n".join(lines)

    if not description.strip():
        print("\n❌ 产品描述不能为空")
        sys.exit(1)

    return description


def load_example_description(example_name: str) -> str:
    """从案例加载产品描述"""
    examples_path = Path(__file__).parent.parent / "examples"
    example_path = examples_path / example_name / "product.txt"

    if not example_path.exists():
        return None

    with open(example_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_template_description(template_name: str) -> str:
    """从模板加载产品描述"""
    templates_path = Path(__file__).parent.parent / "templates"
    template_path = templates_path / template_name / "product.txt"

    if not template_path.exists():
        return None

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    main()
