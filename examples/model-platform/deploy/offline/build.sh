#!/bin/bash
set -e

# 离线安装包构建脚本
# 用于构建完整的离线部署包

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PACKAGE_DIR="$SCRIPT_DIR/package"
VERSION="${VERSION:-1.0.0}"

echo "🚀 开始构建离线安装包 v${VERSION}..."

# 清理旧的构建
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"/{images,dependencies,config,scripts,docs}

# 1. 构建 Docker 镜像
echo ""
echo "📦 构建 Docker 镜像..."
cd "$PROJECT_ROOT"

# 构建后端镜像
docker build -t model-platform/backend:${VERSION} -f deploy/docker/backend.Dockerfile .
echo "  ✓ backend:${VERSION}"

# 构建前端镜像
docker build -t model-platform/frontend:${VERSION} -f deploy/docker/frontend.Dockerfile .
echo "  ✓ frontend:${VERSION}"

# 构建训练 Worker 镜像
docker build -t model-platform/training-worker:${VERSION} -f deploy/docker/training-worker.Dockerfile .
echo "  ✓ training-worker:${VERSION}"

# 2. 导出 Docker 镜像
echo ""
echo "💾 导出 Docker 镜像..."
cd "$PACKAGE_DIR/images"

docker save model-platform/backend:${VERSION} -o backend.tar
echo "  ✓ backend.tar ($(du -h backend.tar | cut -f1))"

docker save model-platform/frontend:${VERSION} -o frontend.tar
echo "  ✓ frontend.tar ($(du -h frontend.tar | cut -f1))"

docker save model-platform/training-worker:${VERSION} -o training-worker.tar
echo "  ✓ training-worker.tar ($(du -h training-worker.tar | cut -f1))"

# 导出基础镜像
docker pull postgres:15
docker save postgres:15 -o postgres.tar
echo "  ✓ postgres.tar ($(du -h postgres.tar | cut -f1))"

docker pull redis:7-alpine
docker save redis:7-alpine -o redis.tar
echo "  ✓ redis.tar ($(du -h redis.tar | cut -f1))"

docker pull minio/minio:latest
docker save minio/minio:latest -o minio.tar
echo "  ✓ minio.tar ($(du -h minio.tar | cut -f1))"

docker pull nginx:alpine
docker save nginx:alpine -o nginx.tar
echo "  ✓ nginx.tar ($(du -h nginx.tar | cut -f1))"

# 3. 下载 Python 依赖
echo ""
echo "📚 下载 Python 依赖..."
cd "$PACKAGE_DIR/dependencies"

mkdir -p python
pip download -r "$PROJECT_ROOT/src/backend/requirements.txt" -d python/
echo "  ✓ Python 依赖已下载到 dependencies/python/"

# 4. 下载 Node.js 依赖
echo ""
echo "📚 下载 Node.js 依赖..."
mkdir -p nodejs
cd "$PROJECT_ROOT/src/frontend"
npm pack --pack-destination "$PACKAGE_DIR/dependencies/nodejs/"
cd "$PACKAGE_DIR/dependencies/nodejs"
echo "  ✓ Node.js 依赖已打包到 dependencies/nodejs/"

# 5. 复制配置文件
echo ""
echo "⚙️  复制配置文件..."
cd "$PACKAGE_DIR/config"

cp -r "$PROJECT_ROOT/deploy/docker" docker/
cp -r "$PROJECT_ROOT/deploy/k8s" k8s/
cp "$PROJECT_ROOT/.env.example" .env.example

echo "  ✓ Docker 配置"
echo "  ✓ K8s 配置"
echo "  ✓ 环境变量模板"

# 6. 复制安装脚本
echo ""
echo "📝 复制安装脚本..."
cd "$PACKAGE_DIR/scripts"

cp "$SCRIPT_DIR/install.sh" .
cp "$SCRIPT_DIR/upgrade.sh" .
cp "$SCRIPT_DIR/uninstall.sh" .
chmod +x *.sh

echo "  ✓ install.sh"
echo "  ✓ upgrade.sh"
echo "  ✓ uninstall.sh"

# 7. 复制文档
echo ""
echo "📖 复制文档..."
cd "$PACKAGE_DIR/docs"

cp "$PROJECT_ROOT/README.md" .
cp "$PROJECT_ROOT/deploy/k8s/README.md" k8s-deployment.md
cp "$PROJECT_ROOT/deploy/k8s/gpu-operator.md" gpu-setup.md

echo "  ✓ README.md"
echo "  ✓ k8s-deployment.md"
echo "  ✓ gpu-setup.md"

# 8. 生成版本信息
echo ""
echo "📋 生成版本信息..."
cd "$PACKAGE_DIR"

cat > VERSION << EOF
Model Platform Offline Package
Version: ${VERSION}
Build Date: $(date '+%Y-%m-%d %H:%M:%S')
Build Host: $(hostname)
Git Commit: $(cd "$PROJECT_ROOT" && git rev-parse --short HEAD 2>/dev/null || echo "N/A")

Components:
- Backend: ${VERSION}
- Frontend: ${VERSION}
- Training Worker: ${VERSION}
- PostgreSQL: 15
- Redis: 7
- MinIO: latest

Package Contents:
- Docker Images: $(ls images/*.tar | wc -l) files
- Python Dependencies: $(ls dependencies/python/*.whl dependencies/python/*.tar.gz 2>/dev/null | wc -l) packages
- Configuration Files: Yes
- Installation Scripts: Yes
- Documentation: Yes
EOF

echo "  ✓ VERSION"

# 9. 生成安装说明
cat > INSTALL.md << 'EOF'
# 离线安装指南

## 系统要求

- 操作系统: Linux (CentOS 7+, Ubuntu 18.04+)
- CPU: 4 核心+
- 内存: 8GB+
- 磁盘: 100GB+
- Docker: 20.10+
- Docker Compose: 2.0+

## 安装步骤

### 1. 解压安装包

```bash
tar -xzf model-platform-offline-v1.0.0.tar.gz
cd model-platform-offline-v1.0.0
```

### 2. 查看版本信息

```bash
cat VERSION
```

### 3. 运行安装脚本

```bash
sudo bash scripts/install.sh
```

安装脚本会自动：
- 检查系统环境
- 加载 Docker 镜像
- 配置环境变量
- 启动所有服务

### 4. 验证安装

```bash
# 查看服务状态
docker-compose ps

# 访问应用
# 前端: http://localhost
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

## 配置

### 环境变量

编辑 `.env` 文件修改配置：

```bash
# 数据库配置
DB_PASSWORD=your_secure_password

# Redis 配置
REDIS_PASSWORD=your_redis_password

# JWT 密钥
SECRET_KEY=your_secret_key

# 对象存储配置
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
```

### GPU 支持

如需 GPU 支持，请参考 `docs/gpu-setup.md`

## 升级

```bash
# 备份数据
sudo bash scripts/backup.sh

# 运行升级脚本
sudo bash scripts/upgrade.sh
```

## 卸载

```bash
sudo bash scripts/uninstall.sh
```

## 故障排查

### 服务无法启动

```bash
# 查看日志
docker-compose logs -f

# 检查端口占用
netstat -tlnp | grep -E '80|8000|5432|6379'
```

### 数据库连接失败

```bash
# 检查数据库状态
docker-compose ps postgres

# 查看数据库日志
docker-compose logs postgres
```

## 技术支持

- 文档: docs/
- 问题反馈: https://github.com/your-org/model-platform/issues
EOF

echo "  ✓ INSTALL.md"

# 10. 打包
echo ""
echo "📦 打包离线安装包..."
cd "$SCRIPT_DIR"

PACKAGE_NAME="model-platform-offline-v${VERSION}.tar.gz"
tar -czf "$PACKAGE_NAME" -C "$PACKAGE_DIR" .

PACKAGE_SIZE=$(du -h "$PACKAGE_NAME" | cut -f1)

echo ""
echo "✅ 离线安装包构建完成！"
echo ""
echo "📦 安装包信息:"
echo "  文件名: $PACKAGE_NAME"
echo "  大小: $PACKAGE_SIZE"
echo "  路径: $SCRIPT_DIR/$PACKAGE_NAME"
echo ""
echo "📋 包含内容:"
echo "  - Docker 镜像: $(ls "$PACKAGE_DIR/images"/*.tar | wc -l) 个"
echo "  - Python 依赖: $(ls "$PACKAGE_DIR/dependencies/python" | wc -l) 个"
echo "  - 配置文件: 是"
echo "  - 安装脚本: 是"
echo "  - 文档: 是"
echo ""
echo "🚀 使用方法:"
echo "  1. 将 $PACKAGE_NAME 传输到目标服务器"
echo "  2. tar -xzf $PACKAGE_NAME"
echo "  3. cd model-platform-offline-v${VERSION}"
echo "  4. sudo bash scripts/install.sh"
