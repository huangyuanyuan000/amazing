# Docker Deploy Skill - Docker 部署配置

## 功能描述
提供 Docker 部署配置规范、镜像优化策略和 Compose 编排模板。

## 触发方式
- Docker 部署配置
- 镜像优化
- 本地开发环境搭建

## 核心内容

### 1. Dockerfile 最佳实践
- 使用多阶段构建、slim/alpine 基础镜像
- 合并 RUN 指令、使用 .dockerignore
- 非 root 用户运行、添加 HEALTHCHECK

### 2. 多阶段构建模板
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
USER appuser
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### 3. Docker Compose 模板
```yaml
version: "3.8"
services:
  api:
    build: .
    ports: ["8000:8000"]
    depends_on:
      db: { condition: service_healthy }
  db:
    image: postgres:15-alpine
    volumes: ["pgdata:/var/lib/postgresql/data"]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
volumes:
  pgdata:
```

### 4. 镜像优化清单
| 优化项 | 效果 | 方法 |
|--------|------|------|
| 基础镜像 | -60% 体积 | slim/alpine |
| 多阶段构建 | -40% 体积 | 分离编译和运行 |
| 层合并 | -10% 体积 | 合并 RUN |

## 进化能力
- 镜像优化策略持续更新
- 安全基线自动更新
