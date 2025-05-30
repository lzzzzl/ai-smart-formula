from config.settings import settings
from utils.logger import setup_logger
from api.routes import health_router

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# 设置日志
logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info(f"启动 {settings.app_name} v{settings.app_version}")
    logger.info(f"调试模式: {settings.debug}")
    logger.info(f"数据库: {settings.database_url}")

    yield

    # 关闭时执行
    logger.info("应用关闭")


# 创建FastAPI应用实例
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="基于大语言模型的智能配方推荐系统",
    debug=settings.debug,
    lifespan=lifespan,
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    logger.error(f"全局异常: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "内部服务器错误",
            "message": str(exc) if settings.debug else "服务暂时不可用",
            "path": str(request.url),
        },
    )


# 注册路由
app.include_router(health_router, prefix="/api/v1", tags=["健康检查"])


# 根路径
@app.get("/")
async def root():
    """根路径欢迎信息"""
    return {
        "message": f"欢迎使用{settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )
