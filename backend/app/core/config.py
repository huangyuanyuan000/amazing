"""
配置管理模块

负责管理应用的所有配置项，包括：
- 数据库配置
- Redis 配置
- JWT 配置
- CORS 配置
- 日志配置
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """应用配置"""

    # 基础配置
    PROJECT_NAME: str = "Amazing"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = True

    # 数据库配置 - 支持多种数据库
    DATABASE_TYPE: str = Field(default="postgresql", description="数据库类型: postgresql/mysql/mongodb/sqlite")
    DATABASE_URL: Optional[str] = Field(default=None, description="数据库连接URL")
    DATABASE_HOST: str = Field(default="localhost")
    DATABASE_PORT: int = Field(default=5432)
    DATABASE_USER: str = Field(default="amazing")
    DATABASE_PASSWORD: str = Field(default="amazing123")
    DATABASE_NAME: str = Field(default="amazing")

    # Redis 配置
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: Optional[str] = Field(default=None)
    REDIS_DB: int = Field(default=0)

    # JWT 配置
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # CORS 配置
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )

    # 日志配置
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="logs/amazing.log")

    # Agent 配置
    CLAUDE_API_KEY: Optional[str] = Field(default=None)
    CODEX_API_KEY: Optional[str] = Field(default=None)
    AGENT_MODEL: str = Field(default="claude-sonnet-4-6")

    # 文件存储配置
    UPLOAD_DIR: str = Field(default="uploads")
    MAX_UPLOAD_SIZE: int = Field(default=100 * 1024 * 1024)  # 100MB

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        """获取数据库连接URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL

        if self.DATABASE_TYPE == "postgresql":
            return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        elif self.DATABASE_TYPE == "mysql":
            return f"mysql+pymysql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        elif self.DATABASE_TYPE == "sqlite":
            return f"sqlite:///./{self.DATABASE_NAME}.db"
        else:
            raise ValueError(f"Unsupported database type: {self.DATABASE_TYPE}")


settings = Settings()
