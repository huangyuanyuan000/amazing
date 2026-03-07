# 部署指南

## 1. 本地开发环境

### 1.1 前置要求

- Python 3.11+
- Go 1.22+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+

### 1.2 初始化项目

```bash
# 克隆项目
cd ~/minger/amazing

# 初始化
make init

# 启动开发环境
make dev
```

### 1.3 访问服务

- 前端: http://localhost:3000
- Python API: http://localhost:8000
- Go API: http://localhost:8080
- API 文档: http://localhost:8000/docs

## 2. Docker 部署

### 2.1 前置要求

- Docker 20+
- Docker Compose 2+

### 2.2 部署步骤

```bash
# 启动所有服务
make docker-up

# 查看日志
cd infra/docker
docker-compose logs -f

# 停止服务
make docker-down
```

### 2.3 服务端口

- Frontend: http://localhost:3000
- Python API: http://localhost:8000
- Go API: http://localhost:8080
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## 3. Kubernetes 部署

### 3.1 前置要求

- Kubernetes 1.28+
- kubectl
- Helm 3+ (可选)

### 3.2 部署步骤

```bash
# 部署到 K8s
make k8s-deploy

# 查看状态
kubectl get pods -n amazing
kubectl get svc -n amazing

# 查看日志
kubectl logs -f deployment/python-api -n amazing

# 清理资源
make k8s-clean
```

### 3.3 访问服务

```bash
# 获取 Frontend 外部 IP
kubectl get svc frontend -n amazing

# 端口转发 (本地测试)
kubectl port-forward svc/frontend 3000:80 -n amazing
kubectl port-forward svc/python-api 8000:8000 -n amazing
```

## 4. 私有化部署

### 4.1 离线部署包准备

```bash
# 导出 Docker 镜像
docker save amazing/python-api:latest > python-api.tar
docker save amazing/go-api:latest > go-api.tar
docker save amazing/frontend:latest > frontend.tar
docker save postgres:16 > postgres.tar
docker save redis:7-alpine > redis.tar

# 打包部署文件
tar -czf amazing-deploy.tar.gz \
  *.tar \
  infra/ \
  scripts/ \
  Makefile \
  README.md
```

### 4.2 离线安装

```bash
# 解压部署包
tar -xzf amazing-deploy.tar.gz

# 加载镜像
docker load < python-api.tar
docker load < go-api.tar
docker load < frontend.tar
docker load < postgres.tar
docker load < redis.tar

# 启动服务
make docker-up
```

## 5. 数据库配置

### 5.1 PostgreSQL

**有数据库环境**:

```bash
# 修改配置
export DATABASE_URL="postgresql://user:pass@host:5432/amazing"

# 运行迁移
cd backend/python
alembic upgrade head
```

**无数据库环境**:

```bash
# 使用 Docker 启动 PostgreSQL
docker run -d \
  --name postgres \
  -e POSTGRES_DB=amazing \
  -e POSTGRES_USER=amazing \
  -e POSTGRES_PASSWORD=amazing123 \
  -p 5432:5432 \
  postgres:16
```

### 5.2 MySQL (可选)

```bash
# 修改配置
export DATABASE_URL="mysql://user:pass@host:3306/amazing"

# 安装驱动
pip install pymysql

# 运行迁移
alembic upgrade head
```

### 5.3 MongoDB (可选)

```bash
# 启动 MongoDB
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  mongo:7

# 配置连接
export MONGODB_URL="mongodb://localhost:27017/amazing"
```

## 6. 环境变量配置

### 6.1 Python API

```bash
# .env
DATABASE_URL=postgresql://amazing:amazing123@localhost:5432/amazing
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
```

### 6.2 Go API

```bash
# .env
DATABASE_URL=postgresql://amazing:amazing123@localhost:5432/amazing
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
```

### 6.3 Frontend

```bash
# .env
VITE_API_URL=http://localhost:8000
VITE_GO_API_URL=http://localhost:8080
```

## 7. 生产环境配置

### 7.1 性能优化

**Python API**:
```bash
# 使用 gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

**Go API**:
```bash
# 编译优化
go build -ldflags="-s -w" -o main
```

**Frontend**:
```bash
# 生产构建
npm run build

# 使用 nginx 部署
nginx -c nginx.conf
```

### 7.2 数据库优化

```sql
-- 创建索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- 配置连接池
-- PostgreSQL: max_connections = 100
-- Redis: maxclients = 10000
```

### 7.3 监控配置

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'python-api'
    static_configs:
      - targets: ['python-api:8000']
  - job_name: 'go-api'
    static_configs:
      - targets: ['go-api:8080']
```

## 8. 备份与恢复

### 8.1 数据库备份

```bash
# PostgreSQL 备份
pg_dump -h localhost -U amazing amazing > backup.sql

# 恢复
psql -h localhost -U amazing amazing < backup.sql
```

### 8.2 Redis 备份

```bash
# 备份
redis-cli SAVE
cp /var/lib/redis/dump.rdb backup/

# 恢复
cp backup/dump.rdb /var/lib/redis/
redis-cli SHUTDOWN
redis-server
```

## 9. 故障排查

### 9.1 常见问题

**服务无法启动**:
```bash
# 检查端口占用
lsof -i :8000
lsof -i :8080
lsof -i :3000

# 检查日志
docker-compose logs python-api
kubectl logs deployment/python-api -n amazing
```

**数据库连接失败**:
```bash
# 测试连接
psql -h localhost -U amazing -d amazing

# 检查配置
echo $DATABASE_URL
```

**前端无法访问后端**:
```bash
# 检查 CORS 配置
# 检查 API URL 配置
# 检查网络连通性
curl http://localhost:8000/health
```

### 9.2 性能问题

```bash
# 查看资源使用
docker stats
kubectl top pods -n amazing

# 查看慢查询
# PostgreSQL
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

# 查看 API 性能
# 使用 Prometheus + Grafana
```

## 10. 升级指南

### 10.1 滚动升级

```bash
# K8s 滚动升级
kubectl set image deployment/python-api \
  python-api=amazing/python-api:v2.0.0 \
  -n amazing

# 查看升级状态
kubectl rollout status deployment/python-api -n amazing
```

### 10.2 回滚

```bash
# 回滚到上一版本
kubectl rollout undo deployment/python-api -n amazing

# 回滚到指定版本
kubectl rollout undo deployment/python-api \
  --to-revision=2 \
  -n amazing
```

## 11. 安全加固

### 11.1 网络安全

```bash
# 配置防火墙
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# 配置 SSL/TLS
# 使用 Let's Encrypt
certbot --nginx -d amazing.example.com
```

### 11.2 应用安全

```bash
# 定期更新依赖
pip install --upgrade -r requirements.txt
go get -u ./...
npm update

# 扫描漏洞
pip-audit
go list -json -m all | nancy sleuth
npm audit
```
