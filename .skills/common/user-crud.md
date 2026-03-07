# Skill: User CRUD
# Version: 1.0.0
# Agent: common
# Tags: user, crud, fastapi

## 描述
生成用户管理的完整 CRUD 接口，包括模型、API、服务层、测试。

## 输入
- 数据库类型: postgresql | mysql | mongodb
- 认证方式: jwt | oauth2 | apikey
- 是否多租户: true | false

## 输出模板

### Model (models/user.py)
```python
from sqlalchemy import Column, String, Boolean, DateTime
from app.db.base import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(32), default="user")
    tenant_id = Column(String(36), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### API (api/v1/users.py)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.core.deps import get_current_user, get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db=Depends(get_db)):
    return await UserService(db).create(user_in)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    return await UserService(db).get_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_in: UserUpdate, db=Depends(get_db), current_user=Depends(get_current_user)):
    return await UserService(db).update(user_id, user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    return await UserService(db).delete(user_id)

@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 20, db=Depends(get_db), current_user=Depends(get_current_user)):
    return await UserService(db).list(skip=skip, limit=limit)
```

## 进化日志
- v1.0.0: 基础 CRUD 模板
