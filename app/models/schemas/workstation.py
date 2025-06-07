"""工站Pydantic模型"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from .common import BaseSchema


class WorkstationStatus(str, Enum):
    """工站状态枚举"""

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class TaskStatus(str, Enum):
    """任务状态枚举"""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskPriority(str, Enum):
    """任务优先级枚举"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class EquipmentInfo(BaseModel):
    """设备信息模型"""

    name: str = Field(..., description="设备名称")
    type: str = Field(..., description="设备类型")
    model: Optional[str] = Field(None, description="设备型号")
    capabilities: List[str] = Field(
        default_factory=list, description="设备能力"
    )
    status: str = Field(default="available", description="设备状态")
    location: Optional[str] = Field(None, description="设备位置")


class WorkstationBase(BaseSchema):
    """工站基础模型"""

    name: str = Field(
        ..., min_length=1, max_length=100, description="工站名称"
    )
    description: Optional[str] = Field(None, description="工站描述")
    location: Optional[str] = Field(None, description="工站位置")
    capabilities: List[str] = Field(
        default_factory=list, description="工站能力"
    )
    equipment: List[EquipmentInfo] = Field(
        default_factory=list, description="设备列表"
    )
    max_concurrent_tasks: int = Field(
        default=1, ge=1, description="最大并发任务数"
    )


class WorkstationCreate(WorkstationBase):
    """创建工站模型"""

    api_endpoint: str = Field(..., description="API端点")
    api_key: Optional[str] = Field(None, description="API密钥")
    connection_timeout: int = Field(
        default=30, ge=1, description="连接超时(秒)"
    )


class WorkstationUpdate(BaseSchema):
    """更新工站模型"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = None
    capabilities: Optional[List[str]] = None
    equipment: Optional[List[EquipmentInfo]] = None
    max_concurrent_tasks: Optional[int] = Field(None, ge=1)
    api_endpoint: Optional[str] = None
    connection_timeout: Optional[int] = Field(None, ge=1)
    is_active: Optional[bool] = None


class WorkstationResponse(WorkstationBase):
    """工站响应模型"""

    id: int
    status: WorkstationStatus
    api_endpoint: str
    connection_timeout: int
    is_active: bool
    current_tasks: int = 0
    total_completed_tasks: int = 0
    success_rate: Optional[float] = None
    average_task_duration: Optional[float] = None
    last_heartbeat: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class TaskCommand(BaseModel):
    """任务命令模型"""

    action: str = Field(..., description="动作名称")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="动作参数"
    )
    timeout: Optional[int] = Field(None, ge=0, description="超时时间(秒)")
    retry_count: int = Field(default=0, ge=0, description="重试次数")


class TaskBase(BaseSchema):
    """任务基础模型"""

    name: str = Field(
        ..., min_length=1, max_length=200, description="任务名称"
    )
    description: Optional[str] = Field(None, description="任务描述")
    priority: TaskPriority = Field(
        default=TaskPriority.NORMAL, description="任务优先级"
    )
    commands: List[TaskCommand] = Field(
        ..., min_items=1, description="任务命令列表"
    )
    estimated_duration: Optional[int] = Field(
        None, ge=0, description="预计耗时(分钟)"
    )
    max_retries: int = Field(default=3, ge=0, description="最大重试次数")


class TaskCreate(TaskBase):
    """创建任务模型"""

    workstation_id: int = Field(..., description="工站ID")
    recipe_id: Optional[int] = Field(None, description="关联配方ID")
    experiment_id: Optional[int] = Field(None, description="关联实验ID")
    scheduled_time: Optional[datetime] = Field(
        None, description="计划执行时间"
    )


class TaskUpdate(BaseSchema):
    """更新任务模型"""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    scheduled_time: Optional[datetime] = None
    max_retries: Optional[int] = Field(None, ge=0)


class TaskResponse(TaskBase):
    """任务响应模型"""

    id: int
    workstation_id: int
    recipe_id: Optional[int] = None
    experiment_id: Optional[int] = None
    user_id: int
    status: TaskStatus
    progress: float = Field(
        default=0.0, ge=0.0, le=100.0, description="进度百分比"
    )

    # 时间信息
    scheduled_time: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actual_duration: Optional[int] = None

    # 执行结果
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    retry_count: int = 0

    # 日志和输出
    logs: List[str] = Field(default_factory=list, description="执行日志")
    outputs: Optional[Dict[str, Any]] = Field(None, description="输出数据")

    created_at: datetime
    updated_at: datetime

    # 关联信息
    workstation_name: Optional[str] = Field(None, description="工站名称")
    recipe_name: Optional[str] = Field(None, description="配方名称")


class TaskSearchRequest(BaseModel):
    """任务搜索请求模型"""

    query: Optional[str] = Field(None, description="搜索关键词")
    workstation_id: Optional[int] = Field(None, description="工站ID")
    user_id: Optional[int] = Field(None, description="用户ID")
    recipe_id: Optional[int] = Field(None, description="配方ID")
    status: Optional[TaskStatus] = Field(None, description="状态筛选")
    priority: Optional[TaskPriority] = Field(None, description="优先级筛选")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")


class WorkstationHealthCheck(BaseModel):
    """工站健康检查模型"""

    status: WorkstationStatus = Field(description="工站状态")
    cpu_usage: Optional[float] = Field(
        None, ge=0, le=100, description="CPU使用率(%)"
    )
    memory_usage: Optional[float] = Field(
        None, ge=0, le=100, description="内存使用率(%)"
    )
    disk_usage: Optional[float] = Field(
        None, ge=0, le=100, description="磁盘使用率(%)"
    )
    temperature: Optional[float] = Field(None, description="温度(°C)")
    equipment_status: List[Dict[str, Any]] = Field(
        default_factory=list, description="设备状态"
    )
    error_messages: List[str] = Field(
        default_factory=list, description="错误消息"
    )
    last_maintenance: Optional[datetime] = Field(
        None, description="最后维护时间"
    )


class TaskControlRequest(BaseModel):
    """任务控制请求模型"""

    action: str = Field(
        ...,
        regex="^(start|pause|resume|cancel|retry)$",
        description="控制动作",
    )
    reason: Optional[str] = Field(None, description="操作原因")


# 为了兼容性，创建别名
Workstation = WorkstationResponse
Task = TaskResponse
