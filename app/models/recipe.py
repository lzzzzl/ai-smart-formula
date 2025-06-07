from enum import Enum as PyEnum

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class RecipeStatus(PyEnum):
    """配方状态枚举"""

    DRAFT = "draft"  # 草稿
    PENDING = "pending"  # 待审核
    APPROVED = "approved"  # 已审核
    REJECTED = "rejected"  # 已拒绝
    ARCHIVED = "archived"  # 已归档


class RecipeDifficulty(PyEnum):
    """配方难度枚举"""

    EASY = "easy"  # 简单
    MEDIUM = "medium"  # 中等
    HARD = "hard"  # 困难
    EXPERT = "expert"  # 专家


class Recipe(Base):
    """配方模型"""

    __tablename__ = "recipes"

    # 基础字段
    id = Column(Integer, primary_key=True, index=True, comment="配方ID")
    name = Column(String(200), nullable=False, index=True, comment="配方名称")
    description = Column(Text, comment="配方描述")
    version = Column(String(20), default="1.0", comment="配方版本")

    # 分类信息
    category = Column(String(100), index=True, comment="配方类别")
    tags = Column(JSON, comment="配方标签(JSON数组)")
    difficulty = Column(
        Enum(RecipeDifficulty),
        default=RecipeDifficulty.MEDIUM,
        comment="难度级别",
    )

    # 配方内容
    ingredients = Column(JSON, nullable=False, comment="原料列表(JSON格式)")
    procedures = Column(JSON, nullable=False, comment="实验步骤(JSON格式)")
    parameters = Column(JSON, comment="实验参数(JSON格式)")
    equipment = Column(JSON, comment="所需设备(JSON格式)")

    # 预期结果
    expected_results = Column(Text, comment="预期实验结果")
    success_criteria = Column(JSON, comment="成功标准(JSON格式)")

    # 安全信息
    safety_notes = Column(Text, comment="安全注意事项")
    risk_level = Column(Integer, default=1, comment="风险等级(1-5)")

    # 资源信息
    estimated_time = Column(Integer, comment="预计耗时(分钟)")
    estimated_cost = Column(Float, comment="预计成本")

    # 状态管理
    status = Column(
        Enum(RecipeStatus), default=RecipeStatus.DRAFT, comment="配方状态"
    )
    is_public = Column(Boolean, default=False, comment="是否公开")
    is_template = Column(Boolean, default=False, comment="是否模板")

    # 统计信息
    view_count = Column(Integer, default=0, comment="查看次数")
    use_count = Column(Integer, default=0, comment="使用次数")
    success_rate = Column(Float, comment="成功率")
    average_rating = Column(Float, comment="平均评分")

    # 元数据
    source = Column(String(100), comment="配方来源")
    reference = Column(Text, comment="参考文献")
    notes = Column(Text, comment="备注")

    # 关联字段
    creator_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, comment="创建者ID"
    )
    parent_recipe_id = Column(
        Integer, ForeignKey("recipes.id"), comment="父配方ID(用于版本管理)"
    )

    # 时间戳
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), comment="创建时间"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )

    # 关系
    creator = relationship("User", back_populates="recipes")
    parent_recipe = relationship(
        "Recipe", remote_side=[id], backref="child_recipes"
    )
    experiments = relationship(
        "Experiment", back_populates="recipe", cascade="all, delete-orphan"
    )
    feedbacks = relationship(
        "Feedback", back_populates="recipe", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Recipe(id={self.id}, name='{self.name}', "
            f"status='{self.status.value}')>"
        )

    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "tags": self.tags,
            "difficulty": self.difficulty.value if self.difficulty else None,
            "ingredients": self.ingredients,
            "procedures": self.procedures,
            "parameters": self.parameters,
            "equipment": self.equipment,
            "expected_results": self.expected_results,
            "success_criteria": self.success_criteria,
            "safety_notes": self.safety_notes,
            "risk_level": self.risk_level,
            "estimated_time": self.estimated_time,
            "estimated_cost": self.estimated_cost,
            "status": self.status.value if self.status else None,
            "is_public": self.is_public,
            "is_template": self.is_template,
            "view_count": self.view_count,
            "use_count": self.use_count,
            "success_rate": self.success_rate,
            "average_rating": self.average_rating,
            "source": self.source,
            "reference": self.reference,
            "notes": self.notes,
            "creator_id": self.creator_id,
            "parent_recipe_id": self.parent_recipe_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
