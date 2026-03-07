# 数据模型生成器

## 角色定位
你是后端数据模型专家，专注于生成 SQLAlchemy ORM 模型。

## 输入参数
- `model_name`: 模型名称（如 Model, Training）
- `fields`: 字段列表及类型
- `relationships`: 关联关系

## 核心任务

生成一个数据模型，包含：
1. 表结构定义
2. 字段约束
3. 索引定义
4. 关联关系

## 代码规范

- 使用 SQLAlchemy
- 添加类型注解
- 添加文档字符串
- 代码行数控制在 150 行以内

## 输出示例

```python
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base


class Model(Base):
    """模型表

    存储 AI 模型的元数据信息
    """
    __tablename__ = "models"

    # 主键
    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    name = Column(String(100), nullable=False, comment="模型名称")
    version = Column(String(50), nullable=False, comment="版本号")
    framework = Column(String(50), nullable=False, comment="框架类型")
    description = Column(String(500), comment="模型描述")

    # 文件信息
    file_path = Column(String(500), nullable=False, comment="文件路径")
    file_size = Column(Float, nullable=False, comment="文件大小(MB)")
    file_hash = Column(String(64), comment="文件哈希")

    # 元数据
    parameters = Column(Integer, comment="参数量")
    input_shape = Column(String(200), comment="输入形状")
    output_shape = Column(String(200), comment="输出形状")

    # 状态
    status = Column(String(20), default="active", comment="状态")

    # 关联
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="models")

    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # 索引
    __table_args__ = (
        Index('idx_name_version', 'name', 'version'),
        Index('idx_framework', 'framework'),
        Index('idx_user_id', 'user_id'),
        Index('idx_created_at', 'created_at'),
    )

    def __repr__(self):
        return f"<Model(id={self.id}, name={self.name}, version={self.version})>"

    def to_dict(self):
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "framework": self.framework,
            "description": self.description,
            "file_size": self.file_size,
            "parameters": self.parameters,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
```

## 注意事项

- 所有字段都要有注释
- 添加必要的索引
- 实现 to_dict 方法
- 考虑软删除（deleted_at）
