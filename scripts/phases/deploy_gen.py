#!/usr/bin/env python3
"""
Phase 6: 部署配置生成

生成 Docker、Kubernetes 和离线部署配置
"""

from pathlib import Path
from typing import Dict


def execute(context: Dict) -> Dict:
    """执行部署配置生成"""
    project_path = context["project_path"]
    project_name = context["project_name"]
    phase_results = context["phase_results"]

    # 获取技术栈和数据库配置
    tech_stack = phase_results.get("business-agent-gen", {}).get("tech_stack", {})
    database_config = phase_results.get("business-agent-gen", {}).get("database_config", {})

    print("🚀 生成部署配置...")

    generated_files = []

    # 生成 Docker 配置
    generate_docker_config(project_path, project_name, tech_stack, database_config)
    generated_files.extend([
        "deploy/docker/backend.Dockerfile",
        "deploy/docker/frontend.Dockerfile",
        "deploy/docker/docker-compose.yml",
        "deploy/docker/docker-compose.dev.yml"
    ])

    # 生成 Kubernetes 配置
    generate_k8s_config(project_path, project_name)
    generated_files.extend([
        "deploy/k8s/backend-deployment.yaml",
        "deploy/k8s/frontend-deployment.yaml",
        "deploy/k8s/postgres-deployment.yaml"
    ])

    # 生成离线部署脚本
    generate_offline_config(project_path, project_name)
    generated_files.extend([
        "deploy/offline/build.sh",
        "deploy/offline/install.sh"
    ])

    print(f"\n✅ 已生成 {len(generated_files)} 个部署配置文件")

    return {
        "docker_files": [f for f in generated_files if "docker" in f],
        "k8s_files": [f for f in generated_files if "k8s" in f],
        "offline_files": [f for f in generated_files if "offline" in f]
    }


def generate_docker_config(project_path: Path, project_name: str, tech_stack: dict, database_config: dict):
    """生成 Docker 配置"""
    docker_path = project_path / "deploy" / "docker"

    # backend.Dockerfile
    backend_dockerfile = '''FROM python:3.11-slim

WORKDIR /app

COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''

    with open(docker_path / "backend.Dockerfile", "w") as f:
        f.write(backend_dockerfile)
    print("  ✓ backend.Dockerfile")

    # frontend.Dockerfile
    frontend_dockerfile = '''FROM node:20-alpine AS builder

WORKDIR /app

COPY src/frontend/package*.json ./
RUN npm ci

COPY src/frontend/ .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY deploy/docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
'''

    with open(docker_path / "frontend.Dockerfile", "w") as f:
        f.write(frontend_dockerfile)
    print("  ✓ frontend.Dockerfile")

    # nginx.conf
    nginx_conf = '''server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
'''

    with open(docker_path / "nginx.conf", "w") as f:
        f.write(nginx_conf)
    print("  ✓ nginx.conf")

    # docker-compose.yml
    compose_content = f'''version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: {project_name}
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ../..
      dockerfile: deploy/docker/backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres:5432/{project_name}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped

  frontend:
    build:
      context: ../..
      dockerfile: deploy/docker/frontend.Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
'''

    with open(docker_path / "docker-compose.yml", "w") as f:
        f.write(compose_content)
    print("  ✓ docker-compose.yml")

    # docker-compose.dev.yml
    dev_compose = f'''version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: {project_name}
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  backend:
    build:
      context: ../..
      dockerfile: deploy/docker/backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://admin:secret@postgres:5432/{project_name}
      REDIS_URL: redis://redis:6379
      DEBUG: "true"
    volumes:
      - ../../src/backend:/app
    depends_on:
      - postgres
      - redis
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:
'''

    with open(docker_path / "docker-compose.dev.yml", "w") as f:
        f.write(dev_compose)
    print("  ✓ docker-compose.dev.yml")


def generate_k8s_config(project_path: Path, project_name: str):
    """生成 Kubernetes 配置"""
    k8s_path = project_path / "deploy" / "k8s"

    # namespace.yaml
    namespace_yaml = f'''apiVersion: v1
kind: Namespace
metadata:
  name: {project_name}
'''

    with open(k8s_path / "namespace.yaml", "w") as f:
        f.write(namespace_yaml)
    print("  ✓ namespace.yaml")

    # postgres-deployment.yaml
    postgres_yaml = f'''apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
  namespace: {project_name}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: {project_name}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_DB
          value: {project_name}
        - name: POSTGRES_USER
          value: admin
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: postgres-password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: {project_name}
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
'''

    with open(k8s_path / "postgres-deployment.yaml", "w") as f:
        f.write(postgres_yaml)
    print("  ✓ postgres-deployment.yaml")

    # backend-deployment.yaml
    backend_yaml = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: {project_name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: {project_name}/backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: REDIS_URL
          value: redis://redis:6379
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: {project_name}
spec:
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
'''

    with open(k8s_path / "backend-deployment.yaml", "w") as f:
        f.write(backend_yaml)
    print("  ✓ backend-deployment.yaml")

    # frontend-deployment.yaml
    frontend_yaml = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: {project_name}
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: {project_name}/frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: {project_name}
spec:
  type: LoadBalancer
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
'''

    with open(k8s_path / "frontend-deployment.yaml", "w") as f:
        f.write(frontend_yaml)
    print("  ✓ frontend-deployment.yaml")

    # secrets.yaml (template)
    secrets_yaml = f'''apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: {project_name}
type: Opaque
stringData:
  postgres-password: "CHANGE_ME"
  database-url: "postgresql://admin:CHANGE_ME@postgres:5432/{project_name}"
'''

    with open(k8s_path / "secrets.yaml.template", "w") as f:
        f.write(secrets_yaml)
    print("  ✓ secrets.yaml.template")


def generate_offline_config(project_path: Path, project_name: str):
    """生成离线部署配置"""
    offline_path = project_path / "deploy" / "offline"

    # build.sh
    build_script = f'''#!/bin/bash
set -e

echo "🚀 构建离线部署包..."

PACKAGE_DIR="offline-package"
rm -rf $PACKAGE_DIR
mkdir -p $PACKAGE_DIR/{{images,config,scripts}}

# 构建 Docker 镜像
echo "📦 构建 Docker 镜像..."
cd ../..
docker-compose -f deploy/docker/docker-compose.yml build

# 导出镜像
echo "💾 导出 Docker 镜像..."
docker save {project_name}/backend:latest -o deploy/offline/$PACKAGE_DIR/images/backend.tar
docker save {project_name}/frontend:latest -o deploy/offline/$PACKAGE_DIR/images/frontend.tar
docker save postgres:15 -o deploy/offline/$PACKAGE_DIR/images/postgres.tar
docker save redis:7-alpine -o deploy/offline/$PACKAGE_DIR/images/redis.tar

# 复制配置文件
echo "📋 复制配置文件..."
cp deploy/docker/docker-compose.yml deploy/offline/$PACKAGE_DIR/config/
cp deploy/docker/nginx.conf deploy/offline/$PACKAGE_DIR/config/

# 复制安装脚本
cp deploy/offline/install.sh deploy/offline/$PACKAGE_DIR/

# 打包
echo "📦 打包..."
cd deploy/offline
tar -czf {project_name}-offline.tar.gz $PACKAGE_DIR

echo "✅ 离线部署包已生成: deploy/offline/{project_name}-offline.tar.gz"
'''

    with open(offline_path / "build.sh", "w") as f:
        f.write(build_script)
    (offline_path / "build.sh").chmod(0o755)
    print("  ✓ build.sh")

    # install.sh
    install_script = f'''#!/bin/bash
set -e

echo "🚀 安装 {project_name}..."

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ 未安装 Docker，请先安装 Docker"
    exit 1
fi

# 加载镜像
echo "📦 加载 Docker 镜像..."
docker load -i images/backend.tar
docker load -i images/frontend.tar
docker load -i images/postgres.tar
docker load -i images/redis.tar

# 复制配置
echo "📋 配置服务..."
cp config/docker-compose.yml .
cp config/nginx.conf .

# 启动服务
echo "🚀 启动服务..."
docker-compose up -d

echo "✅ 安装完成！"
echo ""
echo "访问地址: http://localhost"
echo "查看状态: docker-compose ps"
echo "查看日志: docker-compose logs -f"
'''

    with open(offline_path / "install.sh", "w") as f:
        f.write(install_script)
    (offline_path / "install.sh").chmod(0o755)
    print("  ✓ install.sh")

    # README
    readme = f'''# {project_name} 离线部署包

## 系统要求
- Docker 20.10+
- Docker Compose 2.0+
- 2GB+ 可用内存
- 10GB+ 可用磁盘空间

## 安装步骤

1. 解压部署包
```bash
tar -xzf {project_name}-offline.tar.gz
cd offline-package
```

2. 运行安装脚本
```bash
bash install.sh
```

3. 访问应用
```
http://localhost
```

## 管理命令

查看服务状态:
```bash
docker-compose ps
```

查看日志:
```bash
docker-compose logs -f
```

停止服务:
```bash
docker-compose down
```

重启服务:
```bash
docker-compose restart
```
'''

    with open(offline_path / "README.md", "w") as f:
        f.write(readme)
    print("  ✓ README.md")
