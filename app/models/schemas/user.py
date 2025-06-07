from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from .common import BaseSchema


class UserBase(BaseSchema):
    """用户基础模型"""

    username: str = Field(
        ..., min_length=3, max_length=50, description="用户名"
    )
    email: EmailStr = Field(..., description="邮箱地址")
    full_name: Optional[str] = Field(None, max_length=100, description="全名")
    role: str = Field(
        default="user", description="用户角色: admin, expert, user"
    )
    department: Optional[str] = Field(None, max_length=100, description="部门")
    position: Optional[str] = Field(None, max_length=100, description="职位")
    is_active: bool = Field(default=True, description="是否激活")
    is_expert: bool = Field(default=False, description="是否专家用户")


class UserCreate(UserBase):
    """用户创建模型"""

    password: str = Field(
        ..., min_length=8, max_length=128, description="密码"
    )
    confirm_password: str = Field(..., description="确认密码")

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("密码不匹配")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        """密码强度验证"""
        if len(v) < 8:
            raise ValueError("密码长度至少8位")
        if not any(c.isdigit() for c in v):
            raise ValueError("密码必须包含数字")
        if not any(c.isalpha() for c in v):
            raise ValueError("密码必须包含字母")
        return v


class UserUpdate(BaseSchema):
    """更新用户模型"""

    full_name: Optional[str] = Field(None, max_length=100)
    department: Optional[str] = Field(None, max_length=100)
    position: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    is_expert: Optional[bool] = None
    preferences: Optional[Dict[str, Any]] = None


class UserResponse(UserBase):
    """用户响应模型"""

    id: int
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime] = None

    # 统计信息
    recipe_count: Optional[int] = Field(None, description="配方数量")
    experiment_count: Optional[int] = Field(None, description="实验数量")


class UserLogin(BaseModel):
    """用户登录模型"""

    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")
    remember_me: bool = Field(default=False, description="记住我")


class UserLoginResponse(BaseModel):
    """登录响应模型"""

    access_token: str = Field(description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(description="过期时间(秒)")
    user: UserResponse = Field(description="用户信息")


class UserPasswordReset(BaseModel):
    """密码重置模型"""

    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=8, description="新密码")
    confirm_password: str = Field(..., description="确认新密码")

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("新密码不匹配")
        return v


class UserPasswordForgot(BaseModel):
    """忘记密码模型"""

    email: EmailStr = Field(..., description="邮箱地址")


class UserVerification(BaseModel):
    """用户验证模型"""

    verification_code: str = Field(..., description="验证码")


# 为了兼容性，创建别名
User = UserResponse
