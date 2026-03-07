"""
SQLite 适配器
"""

from typing import Any, Dict, List, Optional
from contextlib import contextmanager
from .database import DatabaseAdapter, DatabaseFactory


class SQLiteAdapter(DatabaseAdapter):
    """SQLite 数据库适配器"""

    def connect(self):
        """建立连接"""
        import sqlite3

        db_file = self.config.get('file', './data/amazing.db')
        self._connection = sqlite3.connect(db_file)
        self._connection.row_factory = sqlite3.Row
        print(f"✓ 连接 SQLite: {db_file}")

    def disconnect(self):
        """断开连接"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute(self, query: str, params: Optional[Dict] = None) -> Any:
        """执行查询"""
        cursor = self._connection.cursor()
        cursor.execute(query, params or {})
        self._connection.commit()
        return cursor.rowcount

    def fetch_one(self, query: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """查询单条"""
        cursor = self._connection.cursor()
        cursor.execute(query, params or {})
        row = cursor.fetchone()
        return dict(row) if row else None

    def fetch_all(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """查询多条"""
        cursor = self._connection.cursor()
        cursor.execute(query, params or {})
        return [dict(row) for row in cursor.fetchall()]

    def insert(self, table: str, data: Dict) -> Any:
        """插入记录"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f':{k}' for k in data.keys()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = self._connection.cursor()
        cursor.execute(query, data)
        self._connection.commit()
        return cursor.lastrowid

    def update(self, table: str, data: Dict, where: Dict) -> int:
        """更新记录"""
        set_clause = ', '.join([f"{k} = :{k}" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = :where_{k}" for k in where.keys()])

        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = {**data, **{f'where_{k}': v for k, v in where.items()}}

        return self.execute(query, params)

    def delete(self, table: str, where: Dict) -> int:
        """删除记录"""
        where_clause = ' AND '.join([f"{k} = :{k}" for k in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return self.execute(query, where)

    @contextmanager
    def transaction(self):
        """事务管理"""
        try:
            yield self._connection
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            raise e

    def create_table(self, table: str, schema: Dict):
        """创建表"""
        columns = []
        for name, type_def in schema.items():
            columns.append(f"{name} {type_def}")

        query = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(columns)})"
        self.execute(query)

    def drop_table(self, table: str):
        """删除表"""
        query = f"DROP TABLE IF EXISTS {table}"
        self.execute(query)

    def table_exists(self, table: str) -> bool:
        """检查表是否存在"""
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=:table"
        result = self.fetch_one(query, {'table': table})
        return result is not None


# 注册适配器
DatabaseFactory.register('sqlite', SQLiteAdapter)
