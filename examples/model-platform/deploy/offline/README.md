# 离线部署指南

## 概述

本目录包含 Model Platform 的离线部署包构建和安装脚本，支持在无网络环境下部署。

## 文件说明

| 文件 | 说明 |
|------|------|
| build.sh | 构建离线安装包 |
| install.sh | 安装脚本 |
| upgrade.sh | 升级脚本 |
| uninstall.sh | 卸载脚本 |

## 构建离线包

### 前置条件

- Docker 20.10+
- Docker Compose 2.0+
- 网络连接（用于下载依赖）
- 50GB+ 可用磁盘空间

### 构建步骤

```bash
# 在有网络的环境中执行
cd deploy/offline

# 构建离线包
bash build.sh

# 指定版本号
VERSION=1.0.0 bash build.sh
```

构建完成后会生成 `model-platform-offline-v1.0.0.tar.gz`

### 离线包内容

```
model-platform-offline-v1.0.0/
├── images/                    # Docker 镜像
│   ├── backend.tar
│   ├── frontend.tar
│   ├── training-worker.tar
│   ├── postgres.tar
│   ├── redis.tar
│   ├── minio.tar
│   └── nginx.tar
├── dependencies/              # 依赖包
│   ├── python/                # Python 依赖
│   └── nodejs/                # Node.js 依赖
├── config/                    # 配置文件
│   ├── docker/
│   ├── k8s/
│   └── .env.example
├── scripts/                   # 安装脚本
│   ├── install.sh
│   ├── upgrade.sh
│   └── uninstall.sh
├── docs/                      # 文档
│   ├── README.md
│   ├── k8s-deployment.md
│   └── gpu-setup.md
├── VERSION                    # 版本信息
└── INSTALL.md                 # 安装说明
```

## 离线安装

### 系统要求

- 操作系统: Linux (CentOS 7+, Ubuntu 18.04+)
- CPU: 4 核心+
- 内存: 8GB+
- 磁盘: 100GB+
- Docker: 20.10+
- Docker Compose: 2.0+

### 安装步骤

1. 传输离线包到目标服务器

```bash
scp model-platform-offline-v1.0.0.tar.gz user@target-server:/tmp/
```

2. 解压安装包

```bash
cd /tmp
tar -xzf model-platform-offline-v1.0.0.tar.gz
cd model-platform-offline-v1.0.0
```

3. 查看版本信息

```bash
cat VERSION
```

4. 运行安装脚本

```bash
sudo bash scripts/install.sh
```

5. 验证安装

```bash
# 查看服务状态
model-platform status

# 访问应用
curl http://localhost:8000/health
```

## 配置

### 环境变量

安装后编辑 `/opt/model-platform/.env` 修改配置：

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

修改后重启服务：

```bash
model-platform restart
```

### GPU 支持

如需 GPU 支持：

1. 安装 NVIDIA 驱动
2. 安装 NVIDIA Container Toolkit
3. 参考 `docs/gpu-setup.md`

## 升级

### 升级步骤

1. 传输新版本离线包到服务器

```bash
scp model-platform-offline-v1.1.0.tar.gz user@target-server:/tmp/
```

2. 解压新版本

```bash
cd /tmp
tar -xzf model-platform-offline-v1.1.0.tar.gz
cd model-platform-offline-v1.1.0
```

3. 运行升级脚本

```bash
sudo bash scripts/upgrade.sh
```

升级脚本会自动：
- 备份当前版本
- 停止服务
- 加载新镜像
- 更新配置
- 数据库迁移
- 启动服务
- 健康检查

### 回滚

如果升级失败，脚本会自动回滚。

手动回滚：

```bash
cd /opt/model-platform
docker-compose down
cp docker-compose.yml.bak docker-compose.yml
docker-compose up -d
```

## 卸载

### 卸载步骤

```bash
cd /tmp/model-platform-offline-v1.0.0
sudo bash scripts/uninstall.sh
```

卸载脚本会：
1. 询问是否备份数据
2. 停止所有服务
3. 删除容器和镜像
4. 删除安装目录
5. 删除管理命令和系统服务

## 管理命令

安装后可使用 `model-platform` 命令管理服务：

```bash
# 启动服务
model-platform start

# 停止服务
model-platform stop

# 重启服务
model-platform restart

# 查看状态
model-platform status

# 查看日志
model-platform logs

# 查看特定服务日志
model-platform logs backend
model-platform logs frontend
```

## 备份和恢复

### 备份

```bash
# 备份数据库
cd /opt/model-platform
docker-compose exec postgres pg_dump -U admin model_platform > backup.sql

# 备份上传文件
tar -czf data-backup.tar.gz data/

# 备份配置
cp .env .env.backup
```

### 恢复

```bash
# 恢复数据库
cd /opt/model-platform
docker-compose exec -T postgres psql -U admin model_platform < backup.sql

# 恢复上传文件
tar -xzf data-backup.tar.gz

# 恢复配置
cp .env.backup .env
model-platform restart
```

## 故障排查

### 服务无法启动

```bash
# 查看日志
model-platform logs

# 检查端口占用
netstat -tlnp | grep -E '80|8000|5432|6379'

# 检查 Docker 状态
systemctl status docker
```

### 数据库连接失败

```bash
# 检查数据库状态
docker-compose ps postgres

# 查看数据库日志
docker-compose logs postgres

# 测试连接
docker-compose exec postgres psql -U admin -d model_platform
```

### 磁盘空间不足

```bash
# 清理 Docker 资源
docker system prune -a

# 清理日志
find /opt/model-platform/logs -name "*.log" -mtime +7 -delete
```

## 监控

### 查看资源使用

```bash
# 查看容器资源使用
docker stats

# 查看磁盘使用
df -h /opt/model-platform
```

### 日志管理

日志位置：`/opt/model-platform/logs/`

```bash
# 查看最近日志
tail -f /opt/model-platform/logs/backend.log

# 清理旧日志
find /opt/model-platform/logs -name "*.log" -mtime +30 -delete
```

## 安全建议

1. **修改默认密码**: 安装后立即修改 `.env` 中的所有密码
2. **防火墙配置**: 只开放必要的端口
3. **定期备份**: 设置定时备份任务
4. **更新**: 定期升级到最新版本
5. **日志审计**: 定期检查日志文件

## 技术支持

- 文档: docs/
- 问题反馈: https://github.com/your-org/model-platform/issues
- 邮件: support@example.com
