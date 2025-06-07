"""反馈数据模型"""

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


class FeedbackType(PyEnum):
    """反馈类型枚举"""

    RECIPE = "recipe"  # 配方反馈
    EXPERIMENT = "experiment"  # 实验反馈
    SYSTEM = "system"  # 系统反馈
    SUGGESTION = "suggestion"  # 建议反馈
    BUG = "bug"  # 问题反馈


class FeedbackStatus(PyEnum):
    """反馈状态枚举"""

    PENDING = "pending"  # 待处理
    REVIEWED = "reviewed"  # 已审核
    RESOLVED = "resolved"  # 已解决
    CLOSED = "closed"  # 已关闭
    REJECTED = "rejected"  # 已拒绝


class FeedbackPriority(PyEnum):
    """反馈优先级枚举"""

    LOW = "low"  # 低
    MEDIUM = "medium"  # 中
    HIGH = "high"  # 高
    URGENT = "urgent"  # 紧急


class Feedback(Base):
    """反馈模型"""

    __tablename__ = "feedbacks"

    # 基础字段
    id = Column(Integer, primary_key=True, index=True, comment="反馈ID")
    title = Column(String(200), nullable=False, comment="反馈标题")
    content = Column(Text, nullable=False, comment="反馈内容")

    # 分类信息
    type = Column(Enum(FeedbackType), nullable=False, comment="反馈类型")
    category = Column(String(100), comment="反馈类别")
    priority = Column(
        Enum(FeedbackPriority),
        default=FeedbackPriority.MEDIUM,
        comment="优先级",
    )

    # 关联字段
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, comment="反馈用户ID"
    )
    recipe_id = Column(Integer, ForeignKey("recipes.id"), comment="关联配方ID")
    experiment_id = Column(
        Integer, ForeignKey("experiments.id"), comment="关联实验ID"
    )

    # 评分信息
    rating = Column(Integer, comment="评分(1-5)")
    usefulness_score = Column(Float, comment="有用性评分(0-10)")
    accuracy_score = Column(Float, comment="准确性评分(0-10)")
    clarity_score = Column(Float, comment="清晰度评分(0-10)")

    # 详细评价
    what_worked = Column(Text, comment="有效的方面")
    what_failed = Column(Text, comment="失败的方面")
    suggestions = Column(Text, comment="改进建议")
    additional_notes = Column(Text, comment="额外备注")

    # 技术细节
    technical_details = Column(JSON, comment="技术细节(JSON格式)")
    error_logs = Column(Text, comment="错误日志")
    screenshots = Column(JSON, comment="截图路径(JSON数组)")
    attachments = Column(JSON, comment="附件路径(JSON数组)")

    # 上下文信息
    browser_info = Column(String(200), comment="浏览器信息")
    system_info = Column(String(200), comment="系统信息")
    version_info = Column(String(100), comment="版本信息")

    # 状态管理
    status = Column(
        Enum(FeedbackStatus),
        default=FeedbackStatus.PENDING,
        comment="处理状态",
    )
    is_public = Column(Boolean, default=False, comment="是否公开")
    is_verified = Column(Boolean, default=False, comment="是否已验证")

    # 处理信息
    assigned_to = Column(
        Integer, ForeignKey("users.id"), comment="分配给用户ID"
    )
    resolved_by = Column(Integer, ForeignKey("users.id"), comment="解决者ID")
    resolution = Column(Text, comment="解决方案")
    resolved_at = Column(DateTime(timezone=True), comment="解决时间")

    # 统计信息
    helpfulness_votes = Column(Integer, default=0, comment="有用投票数")
    view_count = Column(Integer, default=0, comment="查看次数")

    # 标签和元数据
    tags = Column(JSON, comment="标签(JSON数组)")
    metadata = Column(JSON, comment="元数据(JSON格式)")

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
    user = relationship(
        "User", back_populates="feedbacks", foreign_keys=[user_id]
    )
    recipe = relationship("Recipe", back_populates="feedbacks")
    experiment = relationship("Experiment", back_populates="feedbacks")
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    resolver = relationship("User", foreign_keys=[resolved_by])

    def __repr__(self):
        return (
            f"<Feedback(id={self.id}, title='{self.title}', "
            f"type='{self.type.value}')>"
        )

    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "type": self.type.value if self.type else None,
            "category": self.category,
            "priority": self.priority.value if self.priority else None,
            "user_id": self.user_id,
            "recipe_id": self.recipe_id,
            "experiment_id": self.experiment_id,
            "rating": self.rating,
            "usefulness_score": self.usefulness_score,
            "accuracy_score": self.accuracy_score,
            "clarity_score": self.clarity_score,
            "what_worked": self.what_worked,
            "what_failed": self.what_failed,
            "suggestions": self.suggestions,
            "additional_notes": self.additional_notes,
            "technical_details": self.technical_details,
            "error_logs": self.error_logs,
            "screenshots": self.screenshots,
            "attachments": self.attachments,
            "browser_info": self.browser_info,
            "system_info": self.system_info,
            "version_info": self.version_info,
            "status": self.status.value if self.status else None,
            "is_public": self.is_public,
            "is_verified": self.is_verified,
            "assigned_to": self.assigned_to,
            "resolved_by": self.resolved_by,
            "resolution": self.resolution,
            "resolved_at": self.resolved_at,
            "helpfulness_votes": self.helpfulness_votes,
            "view_count": self.view_count,
            "tags": self.tags,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
