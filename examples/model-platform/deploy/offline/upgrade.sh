#!/bin/bash
set -e

# 升级脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALL_DIR="/opt/model-platform"

echo "🔄 Model Platform 升级"
echo ""

# 检查权限
if [ "$EUID" -ne 0 ]; then
  echo "❌ 请使用 root 权限运行此脚本"
  exit 1
fi

# 检查是否已安装
if [ ! -d "$INSTALL_DIR" ]; then
  echo "❌ 未检测到已安装的 Model Platform"
  echo "   请先运行 install.sh 进行安装"
  exit 1
fi

# 1. 备份
echo "💾 备份当前版本..."
BACKUP_DIR="/opt/model-platform-backup-$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 备份配置
cp -r "$INSTALL_DIR/.env" "$BACKUP_DIR/"
cp -r "$INSTALL_DIR/config" "$BACKUP_DIR/"

# 备份数据库
cd "$INSTALL_DIR"
docker-compose exec -T postgres pg_dump -U admin model_platform > "$BACKUP_DIR/database.sql"

echo "  ✓ 备份完成: $BACKUP_DIR"

# 2. 停止服务
echo ""
echo "⏸️  停止服务..."
cd "$INSTALL_DIR"
docker-compose stop

# 3. 加载新镜像
echo ""
echo "📦 加载新镜像..."
cd "$PACKAGE_DIR/images"

for image in *.tar; do
  echo "  加载 $image..."
  docker load -i "$image"
done

# 4. 更新配置
echo ""
echo "⚙️  更新配置..."

# 备份旧配置
cp "$INSTALL_DIR/docker-compose.yml" "$INSTALL_DIR/docker-compose.yml.bak"

# 复制新配置
cp "$PACKAGE_DIR/config/docker/docker-compose.yml" "$INSTALL_DIR/"

# 合并环境变量（保留用户自定义的值）
if [ -f "$PACKAGE_DIR/config/.env.example" ]; then
  # 这里可以添加更智能的配置合并逻辑
  echo "  ⚠️  请手动检查 .env 文件是否需要更新"
fi

# 5. 数据库迁移
echo ""
echo "🗄️  数据库迁移..."
cd "$INSTALL_DIR"
docker-compose up -d postgres redis
sleep 5

docker-compose run --rm backend alembic upgrade head

# 6. 启动服务
echo ""
echo "🚀 启动服务..."
docker-compose up -d

# 7. 健康检查
echo ""
echo "🏥 健康检查..."
sleep 10

if curl -s http://localhost:8000/health &> /dev/null; then
  echo "  ✓ 服务运行正常"
else
  echo "  ❌ 服务启动失败"
  echo "  正在回滚..."

  # 回滚
  docker-compose down
  cp "$INSTALL_DIR/docker-compose.yml.bak" "$INSTALL_DIR/docker-compose.yml"
  docker-compose up -d

  echo "  ✓ 已回滚到之前的版本"
  exit 1
fi

# 8. 清理
echo ""
echo "🧹 清理旧镜像..."
docker image prune -f

echo ""
echo "✅ 升级完成！"
echo ""
echo "📋 备份信息:"
echo "  备份目录: $BACKUP_DIR"
echo "  数据库备份: $BACKUP_DIR/database.sql"
echo ""
echo "🌐 访问地址:"
echo "  前端: http://$(hostname -I | awk '{print $1}')"
echo "  后端 API: http://$(hostname -I | awk '{print $1}'):8000"
echo ""
