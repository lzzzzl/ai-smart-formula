from typing import Optional, List
from pydantic import validator
from pydantic_settings import BaseSettings as PydanticBaseSettings
from pathlib import Path


class Settings(PydanticBaseSettings):
    """应用配置类"""

    # 应用基础配置
    app_name: str = "AI智能配方系统"
    app_version: str = "0.1.0"
    debug: bool = False
    secret_key: str

    # 服务器配置
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = False

    # 数据库配置
    database_url: str
    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str
    database_password: str
    database_name: str

    # Redis配置
    redis_url: str = "redis://localhost:6379/0"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # LLM配置
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    default_llm_provider: str = "openai"
    default_model: str = "gpt-4"

    # 向量数据库配置
    chroma_persist_directory: str = "./data/chroma"
    embedding_model: str = "all-MiniLM-L6-v2"

    # JWT配置
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"

    # Celery配置
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # CORS配置
    allowed_hosts: List[str] = ["*"]
    allowed_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        """构建数据库连接URL"""
        if isinstance(v, str):
            return v
        return (
            f"postgresql://{values.get('database_user')}:"
            f"{values.get('database_password')}@"
            f"{values.get('database_host')}:"
            f"{values.get('database_port')}/"
            f"{values.get('database_name')}"
        )

    @validator("chroma_persist_directory", pre=True)
    def create_chroma_directory(cls, v: str) -> str:
        """确保Chroma持久化目录存在"""
        path = Path(v)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)

    @validator("log_file", pre=True)
    def create_log_directory(cls, v: str) -> str:
        """确保日志目录存在"""
        path = Path(v)
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)


# 创建全局配置实例
settings = Settings()
