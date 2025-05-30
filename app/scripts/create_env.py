#!/usr/bin/env python3
"""
一键创建 .env 文件脚本
自动生成 AI智能配方系统 所需的环境变量配置文件
"""

import secrets
from pathlib import Path


def generate_secret_key(length: int = 32) -> str:
    """生成安全的密钥"""
    return secrets.token_urlsafe(length)


def create_env_file():
    """创建 .env 文件"""

    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    env_file_path = project_root / ".env"

    # 检查是否已存在 .env 文件
    if env_file_path.exists():
        response = input("⚠️  .env 文件已存在，是否覆盖？(y/N): ")
        if response.lower() != "y":
            print("❌ 操作已取消")
            return

    print("🚀 开始创建 .env 文件...")

    # 生成密钥
    secret_key = generate_secret_key()
    jwt_secret_key = generate_secret_key()

    # 环境变量模板
    env_template = f"""# AI智能配方系统 环境配置文件
# 请根据实际情况修改以下配置

# ==================== 应用基础配置 ====================
APP_NAME=AI智能配方系统
APP_VERSION=0.1.0
DEBUG=false
SECRET_KEY={secret_key}

# ==================== 服务器配置 ====================
HOST=0.0.0.0
PORT=8000
RELOAD=false

# ==================== 数据库配置 ====================
# 完整数据库URL（优先使用）
DATABASE_URL=postgresql://username:password@localhost:5432/ai_recipe_db

# 或者分别配置（如果没有DATABASE_URL）
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=ai_recipe_db

# ==================== Redis配置 ====================
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# ==================== LLM配置 ====================
# OpenAI API密钥
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API密钥
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# 默认LLM提供商 (openai/anthropic)
DEFAULT_LLM_PROVIDER=openai

# 默认模型
DEFAULT_MODEL=gpt-4

# ==================== 向量数据库配置 ====================
CHROMA_PERSIST_DIRECTORY=./data/chroma
EMBEDDING_MODEL=all-MiniLM-L6-v2

# ==================== JWT配置 ====================
JWT_SECRET_KEY={jwt_secret_key}
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ==================== 日志配置 ====================
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# ==================== Celery配置 ====================
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ==================== CORS配置 ====================
ALLOWED_HOSTS=["*"]
ALLOWED_ORIGINS=["*"]
"""

    try:
        # 写入 .env 文件
        with open(env_file_path, "w", encoding="utf-8") as f:
            f.write(env_template)

        print(f"✅ .env 文件创建成功: {env_file_path}")
        print("\n📝 请注意以下配置需要手动修改:")
        print("   1. DATABASE_URL 或相关数据库配置")
        print("   2. OPENAI_API_KEY (如果使用OpenAI)")
        print("   3. ANTHROPIC_API_KEY (如果使用Anthropic)")
        print("   4. 其他根据实际环境需要调整的配置")
        print("\n🔒 安全提醒:")
        print("   - 请勿将 .env 文件提交到版本控制系统")
        print("   - 确保 .gitignore 中包含 .env")

    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")


def create_env_example():
    """创建 .env.example 示例文件"""

    project_root = Path(__file__).parent.parent
    env_example_path = project_root / ".env.example"

    env_example_template = """# AI智能配方系统 环境配置示例文件
# 复制此文件为 .env 并填入实际配置值

# ==================== 应用基础配置 ====================
APP_NAME=AI智能配方系统
APP_VERSION=0.1.0
DEBUG=false
SECRET_KEY=your_secret_key_here

# ==================== 服务器配置 ====================
HOST=0.0.0.0
PORT=8000
RELOAD=false

# ==================== 数据库配置 ====================
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=your_db_name

# ==================== Redis配置 ====================
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# ==================== LLM配置 ====================
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL=gpt-4

# ==================== 向量数据库配置 ====================
CHROMA_PERSIST_DIRECTORY=./data/chroma
EMBEDDING_MODEL=all-MiniLM-L6-v2

# ==================== JWT配置 ====================
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ==================== 日志配置 ====================
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# ==================== Celery配置 ====================
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# ==================== CORS配置 ====================
ALLOWED_HOSTS=["*"]
ALLOWED_ORIGINS=["*"]
"""

    try:
        with open(env_example_path, "w", encoding="utf-8") as f:
            f.write(env_example_template)
        print(f"✅ .env.example 文件创建成功: {env_example_path}")
    except Exception as e:
        print(f"❌ 创建 .env.example 文件失败: {e}")


def main():
    """主函数"""
    print("🔧 AI智能配方系统 - 环境配置文件生成器")
    print("=" * 50)

    # 创建 .env 文件
    create_env_file()

    # 询问是否创建 .env.example
    print("\n" + "=" * 50)
    response = input("📄 是否同时创建 .env.example 示例文件？(Y/n): ")
    if response.lower() != "n":
        create_env_example()

    print("\n🎉 配置文件生成完成！")


if __name__ == "__main__":
    main()
