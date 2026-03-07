"""
API 路由模块

统一管理所有 API 路由
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    users,
    prd,
    agents,
    compute,
    data,
    training,
    model_service,
)

api_router = APIRouter()

# 注册各模块路由
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户管理"])
api_router.include_router(prd.router, prefix="/prd", tags=["PRD生成"])
api_router.include_router(agents.router, prefix="/agents", tags=["Agent管理"])
api_router.include_router(compute.router, prefix="/compute", tags=["算力平台"])
api_router.include_router(data.router, prefix="/data", tags=["数据平台"])
api_router.include_router(training.router, prefix="/training", tags=["训推平台"])
api_router.include_router(model_service.router, prefix="/model-service", tags=["模型服务"])
