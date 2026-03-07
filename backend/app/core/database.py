"""
数据库连接模块

支持多种数据库：PostgreSQL, MySQL, MongoDB, SQLite
自动检测并适配不同的数据库类型
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# 创建数据库引擎
try:
    database_url = settings.get_database_url()
    logger.info(f"Connecting to database: {settings.DATABASE_TYPE}")

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=settings.DEBUG,
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    raise


def get_db() -> Generator:
    """
    获取数据库会话

    使用方式:
        db = next(get_db())
        或在 FastAPI 中使用 Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise
