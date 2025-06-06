# AI 智能配方

## 系统设计

智能推荐配方 AI 系统设计思路

### 总体架构

智能推荐配方系统将利用大语言模型(LLM)的强大能力，结合工站特定领域知识，构建一个端到端的实验配方生成系统。整

体架构分为四层：

1. 交互层 - 用户输入需求并查看推荐配方
2. 认知层 - 基于 LLM 的意图理解和配方生成核心
3. 转换层 - 将生成的配方转换为工站可执行的任务
4. 知识层 - 提供专业知识支持和约束条件

### 关键功能模块

1. 自然语言理解模块
   通过大语言模型处理用户的自然语言输入，提取核心实验要素：

- 目标产物和预期结果
- 所需材料和试剂
- 特殊实验条件
- 实验参数范围
  这一步将用户非结构化的需求转换为系统可处理的结构化信息。

2. 配方设计引擎
   基于大语言模型实现配方生成：

- 使用 RAG(检索增强生成)方法，将大模型与专业实验知识库结合
- 构建专门的提示词工程，引导模型生成符合工站能力的配方
- 支持实验步骤的因果推理和逻辑验证
- 考虑工站的物理约束和资源限制

3. 配方优化层
   对初步生成的配方进行多维度优化：

- 实验效率优化：减少不必要的步骤和等待时间
- 资源利用优化：最小化试剂和材料的消耗
- 安全性分析：检测潜在的危险操作组合
- 预测成功率并提供备选方案

4. 配方-任务转换器
   将抽象配方转换为工站实际可执行的任务：

- 映射配方步骤到工站特定的操作模块
- 生成符合工站 API 的任务描述格式
- 添加设备特定的参数和控制指令
- 确保任务执行的时序正确性和资源协调

### 大模型应用策略

1. 提示词工程
   设计专业化提示模板，包含：

- 关键实验参数和限制条件
- 工站设备能力说明
- 示例配方格式
- 安全操作规范和最佳实践

2. 检索增强生成(RAG)
   结合大模型与专业知识库：

- 化学反应和实验方法数据库
- 历史成功配方记录
- 工站设备操作手册
- 材料安全数据表

3. 专家反馈机制
   构建迭代改进系统：

- 收集专家对生成配方的评价
- 记录实验成功/失败案例
- 利用反馈数据微调模型
- 建立配方质量评分体系

4. 多模态融合
   整合不同模态信息：

- 配方文本描述
- 实验流程可视化
- 预期实验结果图谱
- 设备操作序列动画

### 系统工作流程

1. 用户通过自然语言描述实验需求
2. 系统解析用户意图并提取关键信息
3. 大模型生成初步配方建议
4. 系统检查配方可行性并进行优化
5. 转换配方为工站可执行任务
6. 展示配方及可视化流程给用户确认
7. 用户确认后提交至工站执行
8. 记录实验结果用于未来优化

### 持续学习机制

1. 记录每次实验的完整过程和结果
2. 分析成功与失败案例的差异
3. 定期使用新数据更新知识库
4. 根据实验结果反馈优化模型

这一设计充分利用大语言模型的推理和生成能力，同时通过专业知识库和约束条件确保生成的配方是实用且可执行的，为智能工站提供可靠的配方推荐服务。

## 系统实现

智能推荐配方 AI 系统实现步骤

### 后端基础层实现

1. 数据模型 (backend/app/models/)

- 定义配方、任务、用户等基础数据结构
- 实现数据库模型和 Pydantic 验证模型

2. 工具函数 (backend/app/utils/)

- 实现日志配置、环境变量加载
- 通用工具函数和验证器

3. 配置文件 (backend/config/)

- 创建配置文件载入机制
- 定义不同环境的配置参数

### 知识层实现

1. 知识管理 (backend/app/knowledge/)

- 实现向量存储和检索功能
- 开发嵌入模型和本体模型
- 构建知识库管理工具

2. 核心功能模块
3. 自然语言处理模块 (backend/app/core/nlp/)

- 实现意图解析器
- 开发实体提取功能
- 构建文本处理工具

4. 配方设计引擎 (backend/app/core/recipe_engine/)

- 实现配方生成器
- 开发配方验证机制
- 构建提示词管理系统

5. 配方优化模块 (backend/app/core/optimizer/)

- 实现效率优化算法
- 开发资源优化功能
- 构建风险分析工具

6. 配方转换器 (backend/app/core/converter/)

- 实现任务映射功能
- 开发工作流生成器
- 构建 API 格式转换工具

### 服务模块实现

1. LLM 服务 (backend/app/services/llm_service.py)

- 封装对大语言模型的调用
- 实现提示词模板管理

2. RAG 服务 (backend/app/services/rag_service.py)

- 实现检索增强生成功能
- 开发知识检索和排序

3. 反馈服务 (backend/app/services/feedback_service.py)

- 实现反馈收集和分析
- 开发持续学习机制

4. 工站交互服务 (backend/app/services/workstation_service.py)

- 实现与工站的 API 交互
- 开发任务执行监控

### API 层实现

1. API 路由 (backend/app/api/routes/)

- 实现配方、工站、反馈相关接口
- 开发错误处理机制

5. API 中间件 (backend/app/api/middleware/)

- 实现认证和权限控制
- 开发请求日志和监控

### 前端基础层实现

1. 类型定义 (frontend/src/types/)

- 定义所有 API 数据类型
- 实现共享接口

2. API 客户端 (frontend/src/lib/api.ts)

- 实现与后端的通信
- 开发请求和响应处理

### Docker 配置实现

1. 后端 Dockerfile (docker/backend.Dockerfile)

- 配置 Python 环境和依赖

2. 前端 Dockerfile (docker/frontend.Dockerfile)

- 配置 Node 环境和构建流程

3. Docker Compose (docker/docker-compose.yml)

- 配置服务集成和网络

### 测试和文档

1. 后端测试 (backend/tests/)

- 实现单元测试和集成测试
- 开发测试自动化

2. 项目文档 (docs/)

- 编写 API 文档和使用指南
- 开发部署和配置说明
  这个实现顺序确保了依赖关系的合理性，从底层数据模型开始，逐步构建核心功能，最后完成用户界面和部署配置。

## 技术方案

### 后端技术栈

- **Web 框架**: FastAPI - 高性能异步 Web 框架，支持自动 API 文档生成
- **数据库**: PostgreSQL + SQLAlchemy ORM - 关系型数据库存储配方和用户数据
- **向量数据库**: Chroma/Qdrant - 存储知识库向量嵌入，支持语义检索
- **大语言模型**:
  - OpenAI GPT-4/Claude - 主要配方生成模型
  - 本地模型支持 - Ollama 集成，支持私有化部署
- **嵌入模型**: sentence-transformers - 文本向量化和语义相似度计算
- **缓存**: Redis - 缓存频繁查询的配方和知识库检索结果
- **任务队列**: Celery + Redis - 异步处理配方生成和优化任务
- **依赖管理**: Poetry - Python 包管理和虚拟环境
- **数据验证**: Pydantic - 数据模型验证和序列化
- **配置管理**: python-dotenv + Pydantic Settings - 环境变量和配置管理

### 数据存储方案

- **关系型数据**: PostgreSQL 存储用户、配方、实验记录等结构化数据
- **向量数据**: Chroma 存储知识库文档向量，支持语义检索
- **缓存数据**: Redis 缓存热点数据和会话信息
- **文件存储**: 本地文件系统/对象存储，存储配方附件和实验图片

### AI 模型集成方案

- **主模型**: OpenAI GPT-4 API，用于配方生成和自然语言理解
- **备用模型**: Claude API，提供多样化的配方建议
- **本地模型**: Ollama 集成，支持离线和私有化部署
- **嵌入模型**: all-MiniLM-L6-v2，用于文本向量化和相似度计算
- **模型切换**: 支持动态模型选择和负载均衡

### 部署架构

- **容器化**: Docker + Docker Compose，统一开发和生产环境
- **反向代理**: Nginx，处理静态文件和 API 路由
- **数据库**: PostgreSQL 容器，持久化数据存储
- **缓存**: Redis 容器，提供缓存和消息队列服务
- **监控**: 日志聚合和性能监控（可选集成 Prometheus + Grafana）

### 安全方案

- **API 认证**: JWT Token 认证机制
- **数据加密**: 敏感数据加密存储
- **输入验证**: 严格的输入验证和 SQL 注入防护
- **CORS 配置**: 跨域请求安全控制
- **环境隔离**: 开发、测试、生产环境分离

### 性能优化

- **异步处理**: FastAPI 异步特性，提高并发处理能力
- **缓存策略**: 多层缓存，减少数据库查询和 AI 模型调用
- **连接池**: 数据库连接池，优化数据库访问性能
- **CDN**: 静态资源 CDN 加速（生产环境）
- **代码分割**: 前端代码分割和懒加载，优化首屏加载速度

## 项目结构

```bash
ai-smart-recipe/
├── backend/                          # Python后端服务
│   ├── app/                          # 应用主目录
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI应用入口
│   │   ├── api/                      # FastAPI接口层
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # 依赖注入
│   │   │   ├── middleware/           # API中间件
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py           # 认证中间件
│   │   │   │   ├── cors.py           # CORS中间件
│   │   │   │   └── logging.py        # 日志中间件
│   │   │   └── routes/               # API路由
│   │   │       ├── __init__.py
│   │   │       ├── recipes.py        # 配方相关接口
│   │   │       ├── workstation.py    # 工站相关接口
│   │   │       ├── knowledge.py      # 知识库接口
│   │   │       ├── feedback.py       # 反馈接口
│   │   │       └── health.py         # 健康检查接口
│   │   ├── core/                     # 核心功能模块
│   │   │   ├── __init__.py
│   │   │   ├── nlp/                  # 自然语言处理
│   │   │   │   ├── __init__.py
│   │   │   │   ├── intent_parser.py  # 意图解析器
│   │   │   │   ├── entity_extractor.py # 实体提取
│   │   │   │   └── text_processor.py # 文本处理工具
│   │   │   ├── recipe_engine/        # 配方设计引擎
│   │   │   │   ├── __init__.py
│   │   │   │   ├── generator.py      # 配方生成器
│   │   │   │   ├── validator.py      # 配方验证器
│   │   │   │   └── prompt_manager.py # 提示词管理
│   │   │   ├── optimizer/            # 配方优化
│   │   │   │   ├── __init__.py
│   │   │   │   ├── efficiency.py     # 效率优化
│   │   │   │   ├── resource.py       # 资源优化
│   │   │   │   └── risk_analyzer.py  # 风险分析
│   │   │   └── converter/            # 配方转换器
│   │   │       ├── __init__.py
│   │   │       ├── task_mapper.py    # 任务映射
│   │   │       ├── workflow_generator.py # 工作流生成
│   │   │       └── api_formatter.py  # API格式转换
│   │   ├── knowledge/                # 知识管理
│   │   │   ├── __init__.py
│   │   │   ├── vector_store.py       # 向量存储
│   │   │   ├── embeddings.py         # 嵌入模型
│   │   │   ├── retriever.py          # 检索器
│   │   │   └── knowledge_base.py     # 知识库管理
│   │   ├── services/                 # 服务模块
│   │   │   ├── __init__.py
│   │   │   ├── llm_service.py        # LLM服务
│   │   │   ├── rag_service.py        # RAG服务
│   │   │   ├── feedback_service.py   # 反馈服务
│   │   │   ├── workstation_service.py # 工站交互服务
│   │   │   └── cache_service.py      # 缓存服务
│   │   ├── models/                   # 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── database.py           # 数据库模型
│   │   │   │   ├── recipe.py         # 配方模型
│   │   │   │   ├── user.py           # 用户模型
│   │   │   │   ├── experiment.py     # 实验记录模型
│   │   │   │   └── feedback.py       # 反馈模型
│   │   │   └── schemas.py            # Pydantic模型
│   │   │       ├── recipe.py         # 配方Schema
│   │   │       ├── user.py           # 用户Schema
│   │   │       ├── workstation.py    # 工站Schema
│   │   │       └── common.py         # 通用Schema
│   │   ├── utils/                    # 通用工具函数
│   │   │   ├── __init__.py
│   │   │   ├── logger.py             # 日志配置
│   │   │   ├── config.py             # 配置加载
│   │   │   ├── validators.py         # 验证器
│   │   │   └── helpers.py            # 辅助函数
│   │   └── db/                       # 数据库相关
│   │       ├── __init__.py
│   │       ├── database.py           # 数据库连接
│   │       ├── migrations/           # 数据库迁移
│   │       └── seeds/                # 初始数据
│   ├── tests/                        # 测试用例
│   │   ├── __init__.py
│   │   ├── conftest.py               # 测试配置
│   │   ├── unit/                     # 单元测试
│   │   │   ├── test_nlp.py
│   │   │   ├── test_recipe_engine.py
│   │   │   └── test_services.py
│   │   ├── integration/              # 集成测试
│   │   │   ├── test_api.py
│   │   │   └── test_workflows.py
│   │   └── fixtures/                 # 测试数据
│   ├── data/                         # 数据文件
│   │   ├── knowledge_base/           # 知识库文档
│   │   ├── prompts/                  # 提示词模板
│   │   └── examples/                 # 示例配方
│   ├── scripts/                      # 辅助脚本
│   │   ├── init_db.py                # 数据库初始化
│   │   ├── load_knowledge.py         # 知识库加载
│   │   └── migrate.py                # 数据迁移
│   ├── config/                       # 配置文件
│   │   ├── __init__.py
│   │   ├── settings.py               # 应用配置
│   │   ├── database.py               # 数据库配置
│   │   └── llm.py                    # LLM配置
│   ├── pyproject.toml                # Poetry配置和依赖管理
│   ├── poetry.lock                   # Poetry锁文件(自动生成)
│   ├── .env.example                  # 环境变量示例
│   ├── alembic.ini                   # Alembic配置
│   └── requirements.txt              # 备用依赖文件
├── docker/                           # Docker配置
│   ├── backend.Dockerfile            # 后端Dockerfile
│   ├── docker-compose.yml            # Docker Compose配置
│   ├── docker-compose.dev.yml        # 开发环境配置
│   └── nginx.conf                    # Nginx配置
├── docs/                             # 项目文档
│   ├── api/                          # API文档
│   ├── deployment/                   # 部署文档
│   ├── development/                  # 开发文档
│   └── architecture/                 # 架构文档
├── .gitignore                        # Git忽略文件
├── .env.example                      # 全局环境变量示例
└── README.md                         # 项目说明
```

## 实现阶段

### 第一阶段：基础设施搭建 (1-2 周)

#### 项目初始化和环境配置

```bash
# 优先级：最高
backend/
├── pyproject.toml              # Poetry依赖管理
├── .env.example               # 环境变量模板
├── config/settings.py         # 基础配置
└── app/main.py               # FastAPI应用入口
```

**原因**: 没有基础环境就无法进行后续开发

#### 数据库基础设施

```bash
# 优先级：最高
backend/app/
├── db/database.py            # 数据库连接
├── models/database/          # 核心数据模型
│   ├── user.py
│   ├── recipe.py
│   └── experiment.py
└── alembic.ini              # 数据库迁移配置
```

**原因**: 数据模型是整个系统的基础，其他功能都依赖于此

#### 基础 API 框架

```bash
# 优先级：高
backend/app/api/
├── routes/health.py          # 健康检查接口
├── routes/recipes.py         # 配方基础CRUD接口
└── middleware/              # 基础中间件
```

**原因**: 提供基础的 API 服务，便于测试和后续功能集成

### 第二阶段：核心 AI 功能 (2-3 周)

#### LLM 服务集成

```bash
# 优先级：高
backend/app/services/
├── llm_service.py           # LLM基础调用服务
└── core/recipe_engine/
    ├── generator.py         # 基础配方生成
    └── prompt_manager.py    # 提示词管理
```

**原因**: 这是系统的核心价值，需要尽早验证可行性

#### 自然语言处理

```bash
# 优先级：中高
backend/app/core/nlp/
├── intent_parser.py         # 意图解析
├── entity_extractor.py      # 实体提取
└── text_processor.py        # 文本预处理
```

**原因**: 用户输入处理是用户体验的关键

### 第三阶段：知识库和 RAG (2-3 周)

#### 向量存储和检索

```bash
# 优先级：中高
backend/app/knowledge/
├── vector_store.py          # 向量数据库
├── embeddings.py           # 文本嵌入
├── retriever.py            # 检索器
└── app/services/rag_service.py  # RAG服务
```

**原因**: RAG 能显著提升配方生成质量，是核心竞争力

#### 知识库管理

```bash
# 优先级：中
backend/
├── data/knowledge_base/     # 知识库文档
├── scripts/load_knowledge.py  # 知识库加载脚本
└── app/api/routes/knowledge.py # 知识库管理接口
```

### 第四阶段：优化和转换 (1-2 周)

#### 配方优化模块

```bash
# 优先级：中
backend/app/core/optimizer/
├── efficiency.py           # 效率优化
├── resource.py            # 资源优化
└── risk_analyzer.py       # 风险分析
```

#### 工站集成

```bash
# 优先级：中
backend/app/
├── core/converter/         # 配方转换器
├── services/workstation_service.py  # 工站服务
└── api/routes/workstation.py       # 工站接口
```

### 第五阶段：完善和优化 (1-2 周)

#### 缓存和性能优化

```bash
# 优先级：低
backend/app/services/cache_service.py  # 缓存服务
```

#### 反馈和学习机制

```bash
# 优先级：低
backend/app/
├── services/feedback_service.py    # 反馈服务
└── api/routes/feedback.py         # 反馈接口
```

#### 测试和部署

```bash
# 优先级：中
backend/
├── tests/                  # 测试用例
├── docker/                # Docker配置
└── docs/                  # 文档
```

#### 开发建议

1. **MVP 优先**: 先实现最小可用版本，包括基础配方生成功能
2. **迭代开发**: 每个阶段都要有可演示的功能
3. **测试驱动**: 核心功能模块要有对应的测试用例
4. **文档同步**: 重要接口和功能要及时编写文档

这样的开发顺序确保了：

- 早期就能验证核心 AI 功能的可行性
- 每个阶段都有可交付的成果
- 风险控制在可接受范围内
- 为后续功能扩展打好基础
