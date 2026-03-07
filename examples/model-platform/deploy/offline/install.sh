#!/bin/bash
set -e

# 离线安装脚本
# 用于在目标服务器上安装 Model Platform

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Model Platform 离线安装"
echo ""

# 检查权限
if [ "$EUID" -ne 0 ]; then
  echo "❌ 请使用 root 权限运行此脚本"
  echo "   sudo bash $0"
  exit 1
fi

# 1. 检查系统环境
echo "🔍 检查系统环境..."

# 检查操作系统
if [ -f /etc/os-release ]; then
  . /etc/os-release
  echo "  ✓ 操作系统: $NAME $VERSION"
else
  echo "  ⚠️  无法识别操作系统"
fi

# 检查 Docker
if ! command -v docker &> /dev/null; then
  echo "  ❌ Docker 未安装"
  echo "     请先安装 Docker: https://docs.docker.com/engine/install/"
  exit 1
fi
DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
echo "  ✓ Docker: $DOCKER_VERSION"

# 检查 Docker Compose
if ! command -v docker-compose &> /dev/null; then
  echo "  ❌ Docker Compose 未安装"
  echo "     请先安装 Docker Compose: https://docs.docker.com/compose/install/"
  exit 1
fi
COMPOSE_VERSION=$(docker-compose --version | awk '{print $4}' | sed 's/,//')
echo "  ✓ Docker Compose: $COMPOSE_VERSION"

# 检查磁盘空间
AVAILABLE_SPACE=$(df -BG "$PACKAGE_DIR" | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -lt 50 ]; then
  echo "  ⚠️  磁盘空间不足 (可用: ${AVAILABLE_SPACE}GB, 建议: 50GB+)"
  read -p "是否继续安装? (y/N): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
else
  echo "  ✓ 磁盘空间: ${AVAILABLE_SPACE}GB"
fi

# 2. 加载 Docker 镜像
echo ""
echo "📦 加载 Docker 镜像..."
cd "$PACKAGE_DIR/images"

for image in *.tar; do
  echo "  加载 $image..."
  docker load -i "$image"
done

echo "  ✓ 所有镜像已加载"

# 3. 创建安装目录
echo ""
echo "📁 创建安装目录..."
INSTALL_DIR="/opt/model-platform"
mkdir -p "$INSTALL_DIR"/{data,logs,config}

echo "  ✓ 安装目录: $INSTALL_DIR"

# 4. 复制配置文件
echo ""
echo "⚙️  配置应用..."
cd "$PACKAGE_DIR"

# 复制 docker-compose 配置
cp config/docker/docker-compose.yml "$INSTALL_DIR/"
cp config/docker/nginx.conf "$INSTALL_DIR/config/"

# 生成环境变量文件
if [ ! -f "$INSTALL_DIR/.env" ]; then
  cp config/.env.example "$INSTALL_DIR/.env"

  # 生成随机密码
  DB_PASSWORD=$(openssl rand -base64 32)
  REDIS_PASSWORD=$(openssl rand -base64 32)
  SECRET_KEY=$(openssl rand -base64 64)
  S3_ACCESS_KEY=$(openssl rand -base64 16)
  S3_SECRET_KEY=$(openssl rand -base64 32)

  # 替换密码
  sed -i "s/CHANGE_ME_IN_PRODUCTION/$DB_PASSWORD/g" "$INSTALL_DIR/.env"
  sed -i "s/your_redis_password/$REDIS_PASSWORD/g" "$INSTALL_DIR/.env"
  sed -i "s/your_secret_key/$SECRET_KEY/g" "$INSTALL_DIR/.env"
  sed -i "s/your_access_key/$S3_ACCESS_KEY/g" "$INSTALL_DIR/.env"
  sed -i "s/your_secret_key/$S3_SECRET_KEY/g" "$INSTALL_DIR/.env"

  echo "  ✓ 已生成随机密码"
  echo "  ⚠️  请保存 $INSTALL_DIR/.env 文件中的密码"
else
  echo "  ✓ 使用现有配置文件"
fi

# 5. 启动服务
echo ""
echo "🚀 启动服务..."
cd "$INSTALL_DIR"

docker-compose up -d

echo "  ✓ 服务已启动"

# 6. 等待服务就绪
echo ""
echo "⏳ 等待服务就绪..."

# 等待数据库
echo "  等待数据库..."
for i in {1..30}; do
  if docker-compose exec -T postgres pg_isready -U admin &> /dev/null; then
    echo "  ✓ 数据库已就绪"
    break
  fi
  sleep 2
done

# 等待后端
echo "  等待后端 API..."
for i in {1..30}; do
  if curl -s http://localhost:8000/health &> /dev/null; then
    echo "  ✓ 后端 API 已就绪"
    break
  fi
  sleep 2
done

# 7. 初始化数据库
echo ""
echo "🗄️  初始化数据库..."
docker-compose exec -T backend alembic upgrade head
echo "  ✓ 数据库迁移完成"

# 8. 创建管理脚本
echo ""
echo "📝 创建管理脚本..."

cat > /usr/local/bin/model-platform << 'EOF'
#!/bin/bash
cd /opt/model-platform
case "$1" in
  start)
    docker-compose start
    ;;
  stop)
    docker-compose stop
    ;;
  restart)
    docker-compose restart
    ;;
  status)
    docker-compose ps
    ;;
  logs)
    docker-compose logs -f "${@:2}"
    ;;
  *)
    echo "Usage: model-platform {start|stop|restart|status|logs}"
    exit 1
    ;;
esac
EOF

chmod +x /usr/local/bin/model-platform
echo "  ✓ 管理命令: model-platform"

# 9. 创建 systemd 服务
echo ""
echo "🔧 配置系统服务..."

cat > /etc/systemd/system/model-platform.service << EOF
[Unit]
Description=Model Platform
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/model-platform
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable model-platform.service
echo "  ✓ 系统服务已配置"

# 10. 显示安装信息
echo ""
echo "✅ 安装完成！"
echo ""
echo "📋 服务信息:"
echo "  安装目录: $INSTALL_DIR"
echo "  配置文件: $INSTALL_DIR/.env"
echo "  日志目录: $INSTALL_DIR/logs"
echo ""
echo "🌐 访问地址:"
echo "  前端: http://$(hostname -I | awk '{print $1}')"
echo "  后端 API: http://$(hostname -I | awk '{print $1}'):8000"
echo "  API 文档: http://$(hostname -I | awk '{print $1}'):8000/docs"
echo "  MinIO Console: http://$(hostname -I | awk '{print $1}'):9001"
echo ""
echo "🔑 默认账号:"
echo "  用户名: admin"
echo "  密码: 请查看 $INSTALL_DIR/.env 文件"
echo ""
echo "📝 管理命令:"
echo "  启动服务: model-platform start"
echo "  停止服务: model-platform stop"
echo "  重启服务: model-platform restart"
echo "  查看状态: model-platform status"
echo "  查看日志: model-platform logs [service]"
echo ""
echo "📖 文档:"
echo "  安装文档: $PACKAGE_DIR/INSTALL.md"
echo "  K8s 部署: $PACKAGE_DIR/docs/k8s-deployment.md"
echo "  GPU 配置: $PACKAGE_DIR/docs/gpu-setup.md"
echo ""
