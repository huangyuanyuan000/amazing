# Amazing 环境安装指南

## 1. 安装 Go

### macOS

**方式 1: 使用 Homebrew (推荐)**
```bash
# 安装 Homebrew (如果未安装)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Go
brew install go

# 验证安装
go version
```

**方式 2: 手动安装**
```bash
# 下载 Go (ARM64 版本)
curl -LO https://go.dev/dl/go1.22.0.darwin-arm64.tar.gz

# 解压到 /usr/local
sudo tar -C /usr/local -xzf go1.22.0.darwin-arm64.tar.gz

# 配置环境变量
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.zshrc
source ~/.zshrc

# 验证安装
go version
```

### Linux

```bash
# 下载 Go
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz

# 解压
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz

# 配置环境变量
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# 验证安装
go version
```

### Windows

1. 下载安装包: https://go.dev/dl/go1.22.0.windows-amd64.msi
2. 运行安装程序
3. 验证: 打开 CMD，运行 `go version`

## 2. 启动数据库和 Redis (Docker)

### 前置要求

确保已安装 Docker:
```bash
# 检查 Docker
docker --version

# 如果未安装，访问: https://www.docker.com/products/docker-desktop
```

### 启动数据库服务

**方式 1: 使用 docker-compose (推荐)**

```bash
# 进入项目目录
cd ~/minger/amazing

# 创建 docker-compose 配置
cat > docker-compose.dev.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:16
    container_name: amazing-postgres
    environment:
      POSTGRES_DB: amazing
      POSTGRES_USER: amazing
      POSTGRES_PASSWORD: amazing123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U amazing"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: amazing-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  mongodb:
    image: mongo:7
    container_name: amazing-mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: amazing
      MONGO_INITDB_ROOT_PASSWORD: amazing123

volumes:
  postgres_data:
  redis_data:
  mongodb_data:
EOF

# 启动服务
docker-compose -f docker-compose.dev.yml up -d

# 查看状态
docker-compose -f docker-compose.dev.yml ps

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f
```

**方式 2: 单独启动**

```bash
# 启动 PostgreSQL
docker run -d \
  --name amazing-postgres \
  -e POSTGRES_DB=amazing \
  -e POSTGRES_USER=amazing \
  -e POSTGRES_PASSWORD=amazing123 \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:16

# 启动 Redis
docker run -d \
  --name amazing-redis \
  -p 6379:6379 \
  -v redis_data:/data \
  redis:7-alpine

# 启动 MongoDB (可选)
docker run -d \
  --name amazing-mongodb \
  -e MONGO_INITDB_ROOT_USERNAME=amazing \
  -e MONGO_INITDB_ROOT_PASSWORD=amazing123 \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:7
```

### 验证数据库连接

**PostgreSQL**:
```bash
# 使用 psql 连接
docker exec -it amazing-postgres psql -U amazing -d amazing

# 或使用 Python 测试
python3 << EOF
import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="amazing",
    user="amazing",
    password="amazing123"
)
print("PostgreSQL 连接成功!")
conn.close()
EOF
```

**Redis**:
```bash
# 使用 redis-cli 连接
docker exec -it amazing-redis redis-cli ping

# 或使用 Python 测试
python3 << EOF
import redis
r = redis.Redis(host='localhost', port=6379)
print(f"Redis 连接成功! PING: {r.ping()}")
EOF
```

### 停止数据库服务

```bash
# 使用 docker-compose
docker-compose -f docker-compose.dev.yml down

# 或单独停止
docker stop amazing-postgres amazing-redis amazing-mongodb
docker rm amazing-postgres amazing-redis amazing-mongodb
```

## 3. 完成项目初始化

```bash
# 进入项目目录
cd ~/minger/amazing

# 重新初始化 (包含 Go 依赖)
make init

# 安装数据库依赖
cd backend/python
python3 -m pip install -r requirements-optional.txt
```

## 4. 配置环境变量

```bash
# 创建 Python 后端环境变量
cat > backend/python/.env << 'EOF'
# 数据库配置
DATABASE_URL=postgresql://amazing:amazing123@localhost:5432/amazing
REDIS_URL=redis://localhost:6379
MONGODB_URL=mongodb://amazing:amazing123@localhost:27017/amazing

# JWT 配置
SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# 应用配置
APP_NAME=Amazing
APP_VERSION=1.0.0
DEBUG=true
EOF

# 创建 Go 后端环境变量
cat > backend/go/.env << 'EOF'
# 数据库配置
DATABASE_URL=postgresql://amazing:amazing123@localhost:5432/amazing
REDIS_URL=redis://localhost:6379

# JWT 配置
JWT_SECRET=your-secret-key-change-in-production

# 应用配置
APP_NAME=Amazing
APP_VERSION=1.0.0
PORT=8080
EOF

# 创建前端环境变量
cat > frontend/.env << 'EOF'
VITE_API_URL=http://localhost:8000
VITE_GO_API_URL=http://localhost:8080
EOF
```

## 5. 启动开发环境

```bash
# 终端 1: 启动 Python API
cd backend/python
python3 main.py

# 终端 2: 启动 Go API
cd backend/go
go run main.go

# 终端 3: 启动前端
cd frontend
npm run dev
```

## 6. 验证安装

访问以下地址验证:
- 前端: http://localhost:3000
- Python API 文档: http://localhost:8000/docs
- Go API: http://localhost:8080/health

## 常见问题

### Go 安装失败

```bash
# 检查系统架构
uname -m

# ARM64 (M1/M2 Mac): 下载 darwin-arm64 版本
# AMD64 (Intel Mac): 下载 darwin-amd64 版本
```

### Docker 启动失败

```bash
# 检查 Docker 是否运行
docker ps

# 检查端口占用
lsof -i :5432
lsof -i :6379

# 清理旧容器
docker rm -f amazing-postgres amazing-redis
```

### 数据库连接失败

```bash
# 检查容器状态
docker ps | grep amazing

# 查看容器日志
docker logs amazing-postgres
docker logs amazing-redis

# 重启容器
docker restart amazing-postgres amazing-redis
```
