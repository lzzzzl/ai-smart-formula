"""通用Pydantic模型"""

from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field

DataType = TypeVar("DataType")


class ResponseModel(BaseModel, Generic[DataType]):
    """通用API响应模型"""

    success: bool = Field(default=True, description="请求是否成功")
    message: str = Field(default="操作成功", description="响应消息")
    data: Optional[DataType] = Field(default=None, description="响应数据")
    error: Optional[str] = Field(default=None, description="错误信息")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="响应时间"
    )


class PaginatedResponse(BaseModel, Generic[DataType]):
    """分页响应模型"""

    items: List[DataType] = Field(description="数据列表")
    total: int = Field(description="总数量")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页大小")
    total_pages: int = Field(description="总页数")
    has_next: bool = Field(description="是否有下一页")
    has_prev: bool = Field(description="是否有上一页")

    @classmethod
    def create(
        cls, items: List[DataType], total: int, page: int, page_size: int
    ):
        """创建分页响应"""
        total_pages = (total + page_size - 1) // page_size
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )


class BaseSchema(BaseModel):
    """基础Schema类"""

    class Config:
        """Pydantic配置"""

        from_attributes = True  # 支持从ORM对象创建
        use_enum_values = True  # 枚举使用值而不是名称
        json_encoders = {datetime: lambda v: v.isoformat() if v else None}


class SearchRequest(BaseModel):
    """通用搜索请求模型"""

    query: Optional[str] = Field(None, description="搜索关键词")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页大小")
    sort_by: Optional[str] = Field(None, description="排序字段")
    sort_order: str = Field(
        default="desc", regex="^(asc|desc)$", description="排序方向"
    )


class StatusResponse(BaseModel):
    """状态响应模型"""

    status: str = Field(description="状态")
    message: str = Field(description="状态消息")
    details: Optional[dict] = Field(None, description="详细信息")
