"""
Amazing 大模型管理平台 - 主应用入口

这是 FastAPI 应用的主入口文件，负责：
1. 初始化 FastAPI 应用
2. 配置中间件
3. 注册路由
4. 配置 CORS
5. 启动应用
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.core.config import settings
from app.api.v1.router import api_router
from app.core.logging import setup_logging

# 设置日志
setup_logging()

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Amazing 大模型管理平台 API",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """根路径 - 健康检查"""
    return JSONResponse(
        content={
            "message": "Amazing 大模型管理平台",
            "version": settings.VERSION,
            "status": "running",
        }
    )


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return JSONResponse(
        content={
            "status": "healthy",
            "version": settings.VERSION,
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
