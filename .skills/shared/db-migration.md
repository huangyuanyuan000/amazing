# Skill: DB Migration
# Version: 1.0.0
# Agent: shared
# Tags: database, migration, alembic

## 描述
数据库迁移脚本生成，支持多种数据库。

## 支持的数据库
| 数据库 | 连接串格式 | 用途 |
|--------|-----------|------|
| PostgreSQL | `postgresql+asyncpg://user:pass@host:5432/db` | 主库（推荐） |
| MySQL | `mysql+aiomysql://user:pass@host:3306/db` | 兼容方案 |
| MongoDB | `mongodb://user:pass@host:27017/db` | 非结构化数据 |
| SQLite | `sqlite+aiosqlite:///./data.db` | 本地开发 |

## Alembic 配置模板
```ini
# alembic.ini
[alembic]
script_location = alembic
sqlalchemy.url = ${DATABASE_URL}

[loggers]
keys = root,sqlalchemy,alembic
```

## 迁移命令
```bash
# 创建迁移
alembic revision --autogenerate -m "description"

# 执行迁移
alembic upgrade head

# 回滚一个版本
alembic downgrade -1

# 回滚到指定版本
alembic downgrade <revision>

# 查看历史
alembic history
```

## 自动接入逻辑
```python
# app/db/session.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

## 数据库接入检测
```python
async def detect_and_connect():
    """自动检测数据库环境并连接"""
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return create_engine_from_url(db_url)
    # 按优先级尝试连接
    for url in [
        "postgresql+asyncpg://localhost:5432/amazing",
        "mysql+aiomysql://localhost:3306/amazing",
        "sqlite+aiosqlite:///./dev.db",
    ]:
        try:
            engine = create_async_engine(url)
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return engine
        except Exception:
            continue
    raise RuntimeError("No database available")
```
