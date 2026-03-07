"""
PRD (产品需求文档) 生成模块

产品经理通过自然语言描述需求，系统自动生成结构化的PRD文档
包括：功能描述、验收标准、技术方案、工作量评估等
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.core.database import get_db
from app.core.logging import get_logger
from app.services.agent_service import AgentService

logger = get_logger(__name__)
router = APIRouter()


class PRDRequest(BaseModel):
    """PRD 生成请求"""
    title: str = Field(..., description="需求标题")
    description: str = Field(..., description="需求描述（自然语言）")
    priority: str = Field(default="medium", description="优先级: low/medium/high/urgent")
    requester: str = Field(..., description="需求提出人")
    target_version: Optional[str] = Field(default=None, description="目标版本")


class PRDResponse(BaseModel):
    """PRD 生成响应"""
    id: str
    title: str
    description: str
    priority: str
    status: str

    # AI 生成的结构化内容
    background: str = Field(..., description="需求背景")
    objectives: List[str] = Field(..., description="需求目标")
    user_stories: List[str] = Field(..., description="用户故事")
    functional_requirements: List[dict] = Field(..., description="功能需求")
    non_functional_requirements: List[dict] = Field(..., description="非功能需求")
    acceptance_criteria: List[str] = Field(..., description="验收标准")
    technical_solution: dict = Field(..., description="技术方案")
    estimated_workload: dict = Field(..., description="工作量评估")
    risks: List[str] = Field(..., description="风险点")
    dependencies: List[str] = Field(..., description="依赖项")

    created_at: datetime
    updated_at: datetime


@router.post("/generate", response_model=PRDResponse)
async def generate_prd(
    request: PRDRequest,
    db: Session = Depends(get_db)
):
    """
    生成 PRD 文档

    产品经理输入需求描述，AI 自动生成完整的 PRD 文档
    """
    try:
        logger.info(f"Generating PRD for: {request.title}")

        # 调用 Agent 服务生成 PRD
        agent_service = AgentService()
        prd_data = await agent_service.generate_prd(
            title=request.title,
            description=request.description,
            priority=request.priority,
            requester=request.requester,
        )

        # 保存到数据库
        # TODO: 实现数据库保存逻辑

        logger.info(f"PRD generated successfully: {prd_data['id']}")
        return prd_data

    except Exception as e:
        logger.error(f"Failed to generate PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{prd_id}", response_model=PRDResponse)
async def get_prd(
    prd_id: str,
    db: Session = Depends(get_db)
):
    """获取 PRD 详情"""
    try:
        # TODO: 从数据库查询
        logger.info(f"Fetching PRD: {prd_id}")
        raise HTTPException(status_code=404, detail="PRD not found")
    except Exception as e:
        logger.error(f"Failed to fetch PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[PRDResponse])
async def list_prds(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取 PRD 列表"""
    try:
        logger.info(f"Listing PRDs: skip={skip}, limit={limit}")
        # TODO: 从数据库查询
        return []
    except Exception as e:
        logger.error(f"Failed to list PRDs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{prd_id}/approve")
async def approve_prd(
    prd_id: str,
    db: Session = Depends(get_db)
):
    """审批 PRD，开始开发"""
    try:
        logger.info(f"Approving PRD: {prd_id}")

        # 调用 Agent 服务开始开发
        agent_service = AgentService()
        result = await agent_service.start_development(prd_id)

        return {"message": "PRD approved, development started", "result": result}
    except Exception as e:
        logger.error(f"Failed to approve PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{prd_id}/reject")
async def reject_prd(
    prd_id: str,
    reason: str,
    db: Session = Depends(get_db)
):
    """拒绝 PRD"""
    try:
        logger.info(f"Rejecting PRD: {prd_id}, reason: {reason}")
        # TODO: 更新数据库状态
        return {"message": "PRD rejected"}
    except Exception as e:
        logger.error(f"Failed to reject PRD: {e}")
        raise HTTPException(status_code=500, detail=str(e))
