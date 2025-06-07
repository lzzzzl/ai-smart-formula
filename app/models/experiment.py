"""实验记录数据模型"""

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


class ExperimentStatus(PyEnum):
    """实验状态枚举"""

    PENDING = "pending"  # 待执行
    RUNNING = "running"  # 执行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"  # 失败
    CANCELLED = "cancelled"  # 已取消
    PAUSED = "paused"  # 已暂停


class ExperimentResult(PyEnum):
    """实验结果枚举"""

    SUCCESS = "success"  # 成功
    PARTIAL = "partial"  # 部分成功
    FAILURE = "failure"  # 失败
    UNKNOWN = "unknown"  # 未知


class Experiment(Base):
    """实验记录模型"""

    __tablename__ = "experiments"

    # 基础字段
    id = Column(Integer, primary_key=True, index=True, comment="实验ID")
    name = Column(String(200), nullable=False, comment="实验名称")
    description = Column(Text, comment="实验描述")
    batch_number = Column(String(50), index=True, comment="批次号")

    # 关联字段
    recipe_id = Column(
        Integer, ForeignKey("recipes.id"), nullable=False, comment="配方ID"
    )
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, comment="执行用户ID"
    )

    # 实验参数
    actual_ingredients = Column(JSON, comment="实际使用原料(JSON格式)")
    actual_parameters = Column(JSON, comment="实际实验参数(JSON格式)")
    actual_procedures = Column(JSON, comment="实际执行步骤(JSON格式)")

    # 环境条件
    temperature = Column(Float, comment="环境温度(°C)")
    humidity = Column(Float, comment="环境湿度(%)")
    pressure = Column(Float, comment="环境压力(kPa)")
    environment_notes = Column(Text, comment="环境备注")

    # 状态管理
    status = Column(
        Enum(ExperimentStatus),
        default=ExperimentStatus.PENDING,
        comment="实验状态",
    )
    result = Column(Enum(ExperimentResult), comment="实验结果")

    # 时间信息
    planned_start_time = Column(
        DateTime(timezone=True), comment="计划开始时间"
    )
    actual_start_time = Column(DateTime(timezone=True), comment="实际开始时间")
    planned_end_time = Column(DateTime(timezone=True), comment="计划结束时间")
    actual_end_time = Column(DateTime(timezone=True), comment="实际结束时间")
    duration_minutes = Column(Integer, comment="实际耗时(分钟)")

    # 结果数据
    observations = Column(Text, comment="实验观察记录")
    measurements = Column(JSON, comment="测量数据(JSON格式)")
    photos = Column(JSON, comment="实验照片路径(JSON数组)")
    files = Column(JSON, comment="相关文件路径(JSON数组)")

    # 成本信息
    actual_cost = Column(Float, comment="实际成本")
    material_usage = Column(JSON, comment="材料使用量(JSON格式)")

    # 质量评估
    quality_score = Column(Float, comment="质量评分(0-10)")
    success_rating = Column(Integer, comment="成功评级(1-5)")
    meets_criteria = Column(Boolean, comment="是否满足成功标准")

    # 问题记录
    issues_encountered = Column(Text, comment="遇到的问题")
    deviations = Column(JSON, comment="偏差记录(JSON格式)")
    corrective_actions = Column(Text, comment="纠正措施")

    # 改进建议
    improvements = Column(Text, comment="改进建议")
    lessons_learned = Column(Text, comment="经验教训")

    # 审核信息
    reviewed_by = Column(Integer, ForeignKey("users.id"), comment="审核人ID")
    reviewed_at = Column(DateTime(timezone=True), comment="审核时间")
    review_notes = Column(Text, comment="审核备注")

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
    recipe = relationship("Recipe", back_populates="experiments")
    user = relationship(
        "User", back_populates="experiments", foreign_keys=[user_id]
    )
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    feedbacks = relationship(
        "Feedback", back_populates="experiment", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Experiment(id={self.id}, name='{self.name}', "
            f"status='{self.status.value}')>"
        )

    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "batch_number": self.batch_number,
            "recipe_id": self.recipe_id,
            "user_id": self.user_id,
            "actual_ingredients": self.actual_ingredients,
            "actual_parameters": self.actual_parameters,
            "actual_procedures": self.actual_procedures,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "environment_notes": self.environment_notes,
            "status": self.status.value if self.status else None,
            "result": self.result.value if self.result else None,
            "planned_start_time": self.planned_start_time,
            "actual_start_time": self.actual_start_time,
            "planned_end_time": self.planned_end_time,
            "actual_end_time": self.actual_end_time,
            "duration_minutes": self.duration_minutes,
            "observations": self.observations,
            "measurements": self.measurements,
            "photos": self.photos,
            "files": self.files,
            "actual_cost": self.actual_cost,
            "material_usage": self.material_usage,
            "quality_score": self.quality_score,
            "success_rating": self.success_rating,
            "meets_criteria": self.meets_criteria,
            "issues_encountered": self.issues_encountered,
            "deviations": self.deviations,
            "corrective_actions": self.corrective_actions,
            "improvements": self.improvements,
            "lessons_learned": self.lessons_learned,
            "reviewed_by": self.reviewed_by,
            "reviewed_at": self.reviewed_at,
            "review_notes": self.review_notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
