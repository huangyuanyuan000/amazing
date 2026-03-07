# Skill: RBAC Setup
# Version: 1.0.0
# Agent: common
# Tags: rbac, permission, role

## 描述
搭建基于角色的访问控制（RBAC）权限体系。

## 权限模型
```
用户(User) → 角色(Role) → 权限(Permission) → 资源(Resource)
```

## 数据模型
```python
class Role(Base):
    __tablename__ = "roles"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(64), unique=True, nullable=False)
    description = Column(String(256))
    permissions = relationship("Permission", secondary="role_permissions")

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resource = Column(String(64), nullable=False)  # e.g., "model", "dataset", "gpu"
    action = Column(String(32), nullable=False)     # e.g., "read", "write", "delete", "admin"

class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_id = Column(String(36), ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(String(36), ForeignKey("permissions.id"), primary_key=True)
```

## 默认角色
| 角色 | 权限 |
|------|------|
| super_admin | 全部资源全部操作 |
| admin | 全部资源读写 |
| developer | 模型/数据/训练 读写 |
| viewer | 全部资源只读 |
| operator | 运营配置读写 |

## 中间件
```python
from functools import wraps
from fastapi import HTTPException, status

def require_permission(resource: str, action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user.has_permission(resource, action):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
```

## 进化日志
- v1.0.0: 基础 RBAC 模型
