"""
数据库适配层 - 统一接口

提供统一的数据库访问接口，支持多种数据库无缝切换
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from contextlib import contextmanager


class DatabaseAdapter(ABC):
    """数据库适配器抽象基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._connection = None

    @abstractmethod
    def connect(self):
        """建立数据库连接"""
        pass

    @abstractmethod
    def disconnect(self):
        """断开数据库连接"""
        pass

    @abstractmethod
    def execute(self, query: str, params: Optional[Dict] = None) -> Any:
        """执行 SQL 查询"""
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """查询单条记录"""
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        """查询多条记录"""
        pass

    @abstractmethod
    def insert(self, table: str, data: Dict) -> Any:
        """插入记录"""
        pass

    @abstractmethod
    def update(self, table: str, data: Dict, where: Dict) -> int:
        """更新记录"""
        pass

    @abstractmethod
    def delete(self, table: str, where: Dict) -> int:
        """删除记录"""
        pass

    @abstractmethod
    @contextmanager
    def transaction(self):
        """事务管理"""
        pass

    @abstractmethod
    def create_table(self, table: str, schema: Dict):
        """创建表"""
        pass

    @abstractmethod
    def drop_table(self, table: str):
        """删除表"""
        pass

    @abstractmethod
    def table_exists(self, table: str) -> bool:
        """检查表是否存在"""
        pass


class DatabaseFactory:
    """数据库工厂"""

    _adapters = {}

    @classmethod
    def register(cls, db_type: str, adapter_class):
        """注册适配器"""
        cls._adapters[db_type] = adapter_class

    @classmethod
    def create(cls, db_type: str, config: Dict) -> DatabaseAdapter:
        """创建数据库适配器"""
        if db_type not in cls._adapters:
            raise ValueError(f"不支持的数据库类型: {db_type}")

        adapter_class = cls._adapters[db_type]
        return adapter_class(config)

    @classmethod
    def get_supported_types(cls) -> List[str]:
        """获取支持的数据库类型"""
        return list(cls._adapters.keys())
