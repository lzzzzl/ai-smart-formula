from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    """用户模型"""

    __tablename__ = "users"

    # 基础字段
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(
        String(50), unique=True, index=True, nullable=False, comment="用户名"
    )
    email = Column(
        String(100), unique=True, index=True, nullable=False, comment="邮箱"
    )
    hashed_password = Column(String(255), nullable=False, comment="密码哈希")

    # 用户信息
    full_name = Column(String(100), comment="全名")
    role = Column(
        String(20), default="user", comment="用户角色: admin, expert, user"
    )
    department = Column(String(100), comment="部门")
    position = Column(String(100), comment="职位")

    # 状态字段
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_verified = Column(Boolean, default=False, comment="是否验证邮箱")
    is_expert = Column(Boolean, default=False, comment="是否专家用户")

    # 偏好设置
    preferences = Column(Text, comment="用户偏好设置(JSON格式)")

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
    last_login_at = Column(DateTime(timezone=True), comment="最后登录时间")

    # 关系
    recipes = relationship(
        "Recipe", back_populates="creator", cascade="all, delete-orphan"
    )
    experiments = relationship(
        "Experiment", back_populates="user", cascade="all, delete-orphan"
    )
    feedbacks = relationship(
        "Feedback", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, username='{self.username}', "
            f"email='{self.email}')>"
        )

    def to_dict(self):
        """转换为字典格式"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "department": self.department,
            "position": self.position,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_expert": self.is_expert,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login_at": self.last_login_at,
        }
