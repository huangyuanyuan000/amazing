# Deployment Agent - 部署能力

## 能力描述
支持多种部署方式，自动适配不同环境，提供一键部署能力。

## 支持的部署方式
- 本地开发环境
- Docker Compose
- Kubernetes
- 离线/私有化部署

## 核心功能

### 1. 环境检测
- 检测 Docker 是否可用
- 检测 Kubernetes 集群
- 检测网络环境（在线/离线）

### 2. 配置生成
- 自动生成 docker-compose.yml
- 自动生成 K8s manifests
- 自动生成 Helm charts

### 3. 一键部署
```bash
make dev        # 本地开发
make docker     # Docker 部署
make k8s        # K8s 部署
make offline    # 离线部署
```

### 4. 健康检查
- 服务健康检查
- 依赖检查
- 资源检查

## 部署配置

### 本地开发
```yaml
deploy:
  mode: local
  services:
    - backend: http://localhost:8000
    - frontend: http://localhost:3000
  database: sqlite
```

### Docker Compose
```yaml
deploy:
  mode: docker
  services:
    - backend
    - frontend
    - postgres
    - redis
  networks:
    - app-network
```

### Kubernetes
```yaml
deploy:
  mode: k8s
  namespace: production
  replicas:
    backend: 3
    frontend: 2
  resources:
    backend:
      cpu: 1000m
      memory: 2Gi
```

## 进化能力
- 部署配置变更影响分析
- 自动回滚
- 灰度发布
- 资源自动扩缩容
