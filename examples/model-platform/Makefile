.PHONY: help dev docker k8s offline clean test lint

help:
	@echo "大模型管理平台 - 快捷命令"
	@echo ""
	@echo "开发命令:"
	@echo "  make dev        - 启动本地开发环境"
	@echo "  make test       - 运行测试"
	@echo "  make lint       - 代码检查"
	@echo ""
	@echo "部署命令:"
	@echo "  make docker     - Docker Compose 部署"
	@echo "  make k8s        - Kubernetes 部署"
	@echo "  make offline    - 离线部署包"
	@echo ""
	@echo "清理命令:"
	@echo "  make clean      - 清理临时文件"

# 本地开发环境
dev:
	@echo "🚀 启动本地开发环境..."
	@echo ""
	@echo "1️⃣  启动数据库..."
	docker-compose -f deploy/local/docker-compose.yml up -d postgres redis mongodb
	@echo ""
	@echo "2️⃣  等待数据库就绪..."
	@sleep 5
	@echo ""
	@echo "3️⃣  初始化数据库..."
	@bash scripts/init-db.sh
	@echo ""
	@echo "4️⃣  启动后端服务..."
	@echo "   - Common Service (Python): http://localhost:8001"
	@echo "   - Data Service (Python): http://localhost:8002"
	@echo "   - Training Service (Python): http://localhost:8003"
	@echo "   - Compute Service (Go): http://localhost:8004"
	@echo "   - Model Service (Go): http://localhost:8005"
	@echo "   - API Gateway (Go): http://localhost:8000"
	@echo ""
	@echo "5️⃣  启动前端服务..."
	@echo "   - Frontend: http://localhost:3000"
	@echo ""
	@echo "✅ 开发环境已启动！"
	@echo ""
	@echo "📝 下一步："
	@echo "   - 访问前端: http://localhost:3000"
	@echo "   - 访问 API 文档: http://localhost:8000/docs"
	@echo "   - 查看日志: docker-compose -f deploy/local/docker-compose.yml logs -f"

# Docker Compose 部署
docker:
	@echo "🐳 Docker Compose 部署..."
	@echo ""
	@echo "1️⃣  构建镜像..."
	docker-compose -f deploy/docker/docker-compose.yml build
	@echo ""
	@echo "2️⃣  启动服务..."
	docker-compose -f deploy/docker/docker-compose.yml up -d
	@echo ""
	@echo "3️⃣  等待服务就绪..."
	@sleep 10
	@echo ""
	@echo "4️⃣  初始化数据库..."
	docker-compose -f deploy/docker/docker-compose.yml exec backend-common python scripts/init-db.py
	@echo ""
	@echo "✅ 部署完成！"
	@echo ""
	@echo "📝 服务地址："
	@echo "   - 前端: http://localhost:3000"
	@echo "   - API 网关: http://localhost:8000"
	@echo "   - API 文档: http://localhost:8000/docs"
	@echo ""
	@echo "📊 监控地址："
	@echo "   - Grafana: http://localhost:3001 (admin/admin)"
	@echo "   - Prometheus: http://localhost:9090"

# Kubernetes 部署
k8s:
	@echo "☸️  Kubernetes 部署..."
	@echo ""
	@echo "1️⃣  创建命名空间..."
	kubectl create namespace model-platform --dry-run=client -o yaml | kubectl apply -f -
	@echo ""
	@echo "2️⃣  部署数据库..."
	kubectl apply -f deploy/k8s/base/databases/
	@echo ""
	@echo "3️⃣  等待数据库就绪..."
	kubectl wait --for=condition=ready pod -l app=postgres -n model-platform --timeout=300s
	@echo ""
	@echo "4️⃣  部署后端服务..."
	kubectl apply -f deploy/k8s/base/backend/
	@echo ""
	@echo "5️⃣  部署前端服务..."
	kubectl apply -f deploy/k8s/base/frontend/
	@echo ""
	@echo "6️⃣  部署 Ingress..."
	kubectl apply -f deploy/k8s/base/ingress/
	@echo ""
	@echo "✅ 部署完成！"
	@echo ""
	@echo "📝 获取访问地址："
	@echo "   kubectl get ingress -n model-platform"

# 离线部署包
offline:
	@echo "📦 生成离线部署包..."
	@echo ""
	@echo "1️⃣  导出 Docker 镜像..."
	@mkdir -p deploy/offline/images
	docker save -o deploy/offline/images/backend-common.tar model-platform/backend-common:latest
	docker save -o deploy/offline/images/backend-data.tar model-platform/backend-data:latest
	docker save -o deploy/offline/images/backend-training.tar model-platform/backend-training:latest
	docker save -o deploy/offline/images/backend-compute.tar model-platform/backend-compute:latest
	docker save -o deploy/offline/images/backend-model-service.tar model-platform/backend-model-service:latest
	docker save -o deploy/offline/images/backend-api-gateway.tar model-platform/backend-api-gateway:latest
	docker save -o deploy/offline/images/frontend.tar model-platform/frontend:latest
	@echo ""
	@echo "2️⃣  复制配置文件..."
	@cp -r deploy/docker deploy/offline/
	@cp -r deploy/k8s deploy/offline/
	@echo ""
	@echo "3️⃣  打包..."
	@cd deploy/offline && tar -czf ../model-platform-offline.tar.gz .
	@echo ""
	@echo "✅ 离线部署包已生成: deploy/model-platform-offline.tar.gz"
	@echo ""
	@echo "📝 使用方法："
	@echo "   1. 复制到目标机器"
	@echo "   2. tar -xzf model-platform-offline.tar.gz"
	@echo "   3. bash install.sh"

# 运行测试
test:
	@echo "🧪 运行测试..."
	@echo ""
	@echo "1️⃣  后端单元测试..."
	@cd src/backend/common && pytest tests/unit/
	@cd src/backend/data && pytest tests/unit/
	@cd src/backend/training && pytest tests/unit/
	@echo ""
	@echo "2️⃣  前端单元测试..."
	@cd src/frontend && npm run test
	@echo ""
	@echo "3️⃣  集成测试..."
	@pytest tests/integration/
	@echo ""
	@echo "4️⃣  E2E 测试..."
	@cd tests/e2e && npm run test
	@echo ""
	@echo "✅ 测试完成！"

# 代码检查
lint:
	@echo "🔍 代码检查..."
	@echo ""
	@echo "1️⃣  Python 代码检查..."
	@cd src/backend/common && black . && ruff check .
	@cd src/backend/data && black . && ruff check .
	@cd src/backend/training && black . && ruff check .
	@echo ""
	@echo "2️⃣  Go 代码检查..."
	@cd src/backend/compute && gofmt -w . && golangci-lint run
	@cd src/backend/model-service && gofmt -w . && golangci-lint run
	@cd src/backend/api-gateway && gofmt -w . && golangci-lint run
	@echo ""
	@echo "3️⃣  前端代码检查..."
	@cd src/frontend && npm run lint
	@echo ""
	@echo "✅ 代码检查完成！"

# 清理
clean:
	@echo "🧹 清理临时文件..."
	@docker-compose -f deploy/local/docker-compose.yml down -v
	@docker-compose -f deploy/docker/docker-compose.yml down -v
	@rm -rf deploy/offline/images
	@rm -f deploy/model-platform-offline.tar.gz
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "node_modules" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@echo "✅ 清理完成！"
