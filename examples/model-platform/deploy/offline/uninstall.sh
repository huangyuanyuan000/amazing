#!/bin/bash
set -e

# 卸载脚本

INSTALL_DIR="/opt/model-platform"

echo "🗑️  Model Platform 卸载"
echo ""

# 检查权限
if [ "$EUID" -ne 0 ]; then
  echo "❌ 请使用 root 权限运行此脚本"
  exit 1
fi

# 确认卸载
echo "⚠️  警告: 此操作将删除所有数据，包括:"
echo "  - 所有容器和镜像"
echo "  - 数据库数据"
echo "  - 上传的文件"
echo "  - 配置文件"
echo ""
read -p "确认卸载? (yes/NO): " -r
if [[ ! $REPLY =~ ^yes$ ]]; then
  echo "已取消卸载"
  exit 0
fi

# 1. 备份数据（可选）
read -p "是否备份数据? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  BACKUP_DIR="/opt/model-platform-backup-$(date +%Y%m%d%H%M%S)"
  mkdir -p "$BACKUP_DIR"

  echo "💾 备份数据..."
  cd "$INSTALL_DIR"

  # 备份配置
  cp -r .env config "$BACKUP_DIR/"

  # 备份数据库
  if docker-compose ps | grep -q postgres; then
    docker-compose exec -T postgres pg_dump -U admin model_platform > "$BACKUP_DIR/database.sql"
  fi

  # 备份上传文件
  if [ -d "$INSTALL_DIR/data" ]; then
    tar -czf "$BACKUP_DIR/data.tar.gz" -C "$INSTALL_DIR" data/
  fi

  echo "  ✓ 备份完成: $BACKUP_DIR"
fi

# 2. 停止服务
echo ""
echo "⏸️  停止服务..."
cd "$INSTALL_DIR"
docker-compose down -v

# 3. 删除镜像
echo ""
echo "🗑️  删除镜像..."
docker rmi model-platform/backend:latest 2>/dev/null || true
docker rmi model-platform/frontend:latest 2>/dev/null || true
docker rmi model-platform/training-worker:latest 2>/dev/null || true

# 4. 删除安装目录
echo ""
echo "📁 删除安装目录..."
rm -rf "$INSTALL_DIR"

# 5. 删除管理命令
echo ""
echo "🔧 删除管理命令..."
rm -f /usr/local/bin/model-platform

# 6. 删除系统服务
echo ""
echo "🔧 删除系统服务..."
systemctl stop model-platform.service 2>/dev/null || true
systemctl disable model-platform.service 2>/dev/null || true
rm -f /etc/systemd/system/model-platform.service
systemctl daemon-reload

echo ""
echo "✅ 卸载完成！"
echo ""
if [ -n "$BACKUP_DIR" ]; then
  echo "📋 备份信息:"
  echo "  备份目录: $BACKUP_DIR"
  echo "  数据库备份: $BACKUP_DIR/database.sql"
  echo "  文件备份: $BACKUP_DIR/data.tar.gz"
  echo ""
fi
