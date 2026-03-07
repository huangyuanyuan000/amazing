"""
数据库适配层

统一的数据库访问接口，支持多种数据库
"""

from .database import DatabaseAdapter, DatabaseFactory
from .postgresql import PostgreSQLAdapter
from .mysql import MySQLAdapter
from .sqlite import SQLiteAdapter

__all__ = [
    'DatabaseAdapter',
    'DatabaseFactory',
    'PostgreSQLAdapter',
    'MySQLAdapter',
    'SQLiteAdapter',
]
