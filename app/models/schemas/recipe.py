"""配方Pydantic模型"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator

from .common import BaseSchema


class RecipeDifficulty(str, Enum):
    """配方难度枚举"""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class RecipeStatus(str, Enum):
    """配方状态枚举"""

    DRAFT = "draft"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class IngredientItem(BaseModel):
    """原料项模型"""

    name: str = Field(..., description="原料名称")
    amount: float = Field(..., gt=0, description="用量")
    unit: str = Field(..., description="单位")
    purity: Optional[float] = Field(None, ge=0, le=100, description="纯度(%)")
    supplier: Optional[str] = Field(None, description="供应商")
    cas_number: Optional[str] = Field(None, description="CAS号")
    notes: Optional[str] = Field(None, description="备注")


class ProcedureStep(BaseModel):
    """实验步骤模型"""

    step_number: int = Field(..., ge=1, description="步骤号")
    description: str = Field(..., description="步骤描述")
    duration: Optional[int] = Field(None, ge=0, description="耗时(分钟)")
    temperature: Optional[float] = Field(None, description="温度(°C)")
    conditions: Optional[Dict[str, Any]] = Field(None, description="实验条件")
    equipment: Optional[List[str]] = Field(None, description="所需设备")
    safety_notes: Optional[str] = Field(None, description="安全注意事项")


class RecipeBase(BaseSchema):
    """配方基础模型"""

    name: str = Field(
        ..., min_length=1, max_length=200, description="配方名称"
    )
    description: Optional[str] = Field(None, description="配方描述")
    version: str = Field(default="1.0", description="配方版本")
    category: Optional[str] = Field(
        None, max_length=100, description="配方类别"
    )
    tags: Optional[List[str]] = Field(
        default_factory=list, description="配方标签"
    )
    difficulty: RecipeDifficulty = Field(
        default=RecipeDifficulty.MEDIUM, description="难度级别"
    )

    # 配方内容
    ingredients: List[IngredientItem] = Field(
        ..., min_items=1, description="原料列表"
    )
    procedures: List[ProcedureStep] = Field(
        ..., min_items=1, description="实验步骤"
    )
    parameters: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="实验参数"
    )
    equipment: Optional[List[str]] = Field(
        default_factory=list, description="所需设备"
    )

    # 预期结果
    expected_results: Optional[str] = Field(None, description="预期实验结果")
    success_criteria: Optional[Dict[str, Any]] = Field(
        None, description="成功标准"
    )

    # 安全信息
    safety_notes: Optional[str] = Field(None, description="安全注意事项")
    risk_level: int = Field(default=1, ge=1, le=5, description="风险等级(1-5)")

    # 资源信息
    estimated_time: Optional[int] = Field(
        None, ge=0, description="预计耗时(分钟)"
    )
    estimated_cost: Optional[float] = Field(None, ge=0, description="预计成本")

    # 状态
    is_public: bool = Field(default=False, description="是否公开")
    is_template: bool = Field(default=False, description="是否模板")

    # 元数据
    source: Optional[str] = Field(None, max_length=100, description="配方来源")
    reference: Optional[str] = Field(None, description="参考文献")
    notes: Optional[str] = Field(None, description="备注")


class RecipeCreate(RecipeBase):
    """创建配方模型"""

    @validator("procedures")
    def validate_procedures(cls, v):
        """验证实验步骤"""
        if not v:
            raise ValueError("至少需要一个实验步骤")

        step_numbers = [step.step_number for step in v]
        if len(step_numbers) != len(set(step_numbers)):
            raise ValueError("步骤号不能重复")

        if min(step_numbers) != 1 or max(step_numbers) != len(step_numbers):
            raise ValueError("步骤号必须从1开始连续编号")

        return v


class RecipeUpdate(BaseSchema):
    """更新配方模型"""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    difficulty: Optional[RecipeDifficulty] = None
    ingredients: Optional[List[IngredientItem]] = None
    procedures: Optional[List[ProcedureStep]] = None
    parameters: Optional[Dict[str, Any]] = None
    equipment: Optional[List[str]] = None
    expected_results: Optional[str] = None
    success_criteria: Optional[Dict[str, Any]] = None
    safety_notes: Optional[str] = None
    risk_level: Optional[int] = Field(None, ge=1, le=5)
    estimated_time: Optional[int] = Field(None, ge=0)
    estimated_cost: Optional[float] = Field(None, ge=0)
    is_public: Optional[bool] = None
    is_template: Optional[bool] = None
    source: Optional[str] = None
    reference: Optional[str] = None
    notes: Optional[str] = None


class RecipeResponse(RecipeBase):
    """配方响应模型"""

    id: int
    status: RecipeStatus
    view_count: int = 0
    use_count: int = 0
    success_rate: Optional[float] = None
    average_rating: Optional[float] = None
    creator_id: int
    parent_recipe_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    # 关联信息
    creator_name: Optional[str] = Field(None, description="创建者姓名")


class RecipeSearchRequest(BaseModel):
    """配方搜索请求模型"""

    query: Optional[str] = Field(None, description="搜索关键词")
    category: Optional[str] = Field(None, description="类别筛选")
    tags: Optional[List[str]] = Field(None, description="标签筛选")
    difficulty: Optional[RecipeDifficulty] = Field(
        None, description="难度筛选"
    )
    status: Optional[RecipeStatus] = Field(None, description="状态筛选")
    min_rating: Optional[float] = Field(
        None, ge=0, le=5, description="最低评分"
    )
    max_time: Optional[int] = Field(None, ge=0, description="最大耗时(分钟)")
    max_cost: Optional[float] = Field(None, ge=0, description="最大成本")
    is_public: Optional[bool] = Field(None, description="是否公开")
    creator_id: Optional[int] = Field(None, description="创建者ID")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")


class RecipeGenerateRequest(BaseModel):
    """AI生成配方请求模型"""

    description: str = Field(..., min_length=10, description="需求描述")
    target_product: Optional[str] = Field(None, description="目标产物")
    constraints: Optional[Dict[str, Any]] = Field(None, description="约束条件")
    preferred_methods: Optional[List[str]] = Field(
        None, description="偏好方法"
    )
    safety_requirements: Optional[str] = Field(None, description="安全要求")
    time_limit: Optional[int] = Field(None, ge=0, description="时间限制(分钟)")
    cost_limit: Optional[float] = Field(None, ge=0, description="成本限制")


class RecipeOptimizeRequest(BaseModel):
    """配方优化请求模型"""

    recipe_id: int = Field(..., description="配方ID")
    optimization_goals: List[str] = Field(..., description="优化目标")
    constraints: Optional[Dict[str, Any]] = Field(None, description="约束条件")


# 为了兼容性，创建别名
Recipe = RecipeResponse
