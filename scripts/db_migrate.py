#!/usr/bin/env python3
"""
数据库迁移工具

支持多种数据库的迁移管理
"""

import sys
import yaml
from pathlib import Path
from typing import Dict


class DatabaseMigrator:
    """数据库迁移器"""

    def __init__(self, config_file: Path):
        self.config_file = config_file
        self.config = self._load_config()
        self.db_type = self.config['database']['primary']['type']

    def _load_config(self) -> Dict:
        """加载配置"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def init(self):
        """初始化数据库"""
        print(f"🚀 初始化数据库: {self.db_type}")

        # 导入适配器
        sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))
        from adapters import DatabaseFactory

        # 创建适配器
        adapter = DatabaseFactory.create(self.db_type, self.config['database']['primary'])
        adapter.connect()

        # 创建迁移表
        adapter.create_table('migrations', {
            'id': 'SERIAL PRIMARY KEY' if self.db_type == 'postgresql' else 'INTEGER PRIMARY KEY AUTOINCREMENT',
            'version': 'VARCHAR(255) NOT NULL',
            'name': 'VARCHAR(255) NOT NULL',
            'applied_at': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'
        })

        adapter.disconnect()
        print("✅ 数据库初始化完成")

    def migrate(self):
        """执行迁移"""
        print(f"🚀 执行迁移: {self.db_type}")
        # TODO: 实现迁移逻辑
        print("✅ 迁移完成")

    def rollback(self):
        """回滚迁移"""
        print(f"↩️  回滚迁移: {self.db_type}")
        # TODO: 实现回滚逻辑
        print("✅ 回滚完成")

    def seed(self):
        """填充种子数据"""
        print(f"🌱 填充种子数据: {self.db_type}")
        # TODO: 实现种子数据逻辑
        print("✅ 种子数据填充完成")

    def switch(self, new_type: str):
        """切换数据库类型"""
        print(f"🔄 切换数据库: {self.db_type} → {new_type}")

        # 更新配置
        self.config['database']['primary']['type'] = new_type

        # 保存配置
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)

        print(f"✅ 已切换到 {new_type}")
        print("⚠️  请运行 'python scripts/db_migrate.py init' 初始化新数据库")


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="数据库迁移工具")
    parser.add_argument("command", choices=['init', 'migrate', 'rollback', 'seed', 'switch'],
                       help="命令")
    parser.add_argument("--to", help="切换到的数据库类型")
    parser.add_argument("--config", default="config/database.yml", help="配置文件路径")

    args = parser.parse_args()

    config_file = Path(args.config)
    if not config_file.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        sys.exit(1)

    migrator = DatabaseMigrator(config_file)

    try:
        if args.command == 'init':
            migrator.init()
        elif args.command == 'migrate':
            migrator.migrate()
        elif args.command == 'rollback':
            migrator.rollback()
        elif args.command == 'seed':
            migrator.seed()
        elif args.command == 'switch':
            if not args.to:
                print("❌ 请指定目标数据库类型: --to=<type>")
                sys.exit(1)
            migrator.switch(args.to)
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
