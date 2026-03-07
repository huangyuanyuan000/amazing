"""
MySQL 适配器
"""

from typing import Any, Dict, List, Optional
from contextlib import contextmanager
from .database import DatabaseAdapter, DatabaseFactory


class MySQLAdapter(DatabaseAdapter):
    """MySQL 数据库适配器"""

    def connect(self):
        """建立连接"""
        try:
            import pymysql
            from pymysql.cursors import DictCursor

            self._connection = pymysql.connect(
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 3306),
                database=self.config.get('name'),
                user=self.config.get('user'),
                password=self.config.get('password'),
                charset='utf8mb4',
                cursorclass=DictCursor
            )
            print(f"✓ 连接 MySQL: {self.config.get('name')}")
        except ImportError:
            raise ImportError("请安装 pymysql: pip install pymysql")

    def disconnect(self):
        """断开连接"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute(self, query: str, params: Optional[Dict] = None) -> Any:
        """执行查询"""
        with self._connection.cursor() as cursor:
            cursor.execute(query, params or {})
            self._connection.commit()
            return cursor.rowcount

    def fetch_one(self, query: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """查询单条"""
        with self._connection.cursor() as cursor:
            cursor.execute(query, params or {})
            return cursor.fetchone()

    def fetch_all(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """查询多条"""
        with self._connection.cursor() as cursor:
            cursor.execute(query, params or {})
            return cursor.fetchall()

    def insert(self, table: str, data: Dict) -> Any:
        """插入记录"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        with self._connection.cursor() as cursor:
            cursor.execute(query, list(data.values()))
            self._connection.commit()
            return cursor.lastrowid

    def update(self, table: str, data: Dict, where: Dict) -> int:
        """更新记录"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])

        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = list(data.values()) + list(where.values())

        return self.execute(query, params)

    def delete(self, table: str, where: Dict) -> int:
        """删除记录"""
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        return self.execute(query, list(where.values()))

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
        query = "SHOW TABLES LIKE %s"
        result = self.fetch_one(query, [table])
        return result is not None


# 注册适配器
DatabaseFactory.register('mysql', MySQLAdapter)
