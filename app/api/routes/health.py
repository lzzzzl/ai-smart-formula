import psutil

from fastapi import APIRouter
from datetime import datetime
from config.settings import settings


router = APIRouter(prefix="/api/v1", tags=["健康检查"])


@router.get("/health")
async def health_check():
    """系统健康检查"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production",
    }


@router.get("/health/detailed")
async def detailed_health_check():
    """详细健康检查"""
    # 获取系统信息
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production",
        "system": {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
            },
            "disk": {
                "total": disk.total,
                "free": disk.free,
                "percent": (disk.used / disk.total) * 100,
            },
        },
        "config": {
            "database_host": settings.database_host,
            "redis_host": settings.redis_host,
            "log_level": settings.log_level,
        },
    }
