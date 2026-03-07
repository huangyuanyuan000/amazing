.PHONY: help init dev docker-up docker-down k8s-deploy k8s-clean test lint

help:
	@echo "Amazing - 大模型管理平台"
	@echo ""
	@echo "可用命令:"
	@echo "  make init          - 初始化项目"
	@echo "  make dev           - 启动本地开发环境"
	@echo "  make docker-up     - 启动 Docker 环境"
	@echo "  make docker-down   - 停止 Docker 环境"
	@echo "  make k8s-deploy    - 部署到 Kubernetes"
	@echo "  make k8s-clean     - 清理 Kubernetes 资源"
	@echo "  make test          - 运行测试"
	@echo "  make lint          - 代码检查"

init:
	@echo "🚀 初始化项目..."
	@chmod +x scripts/amazing-cli.py
	@cd frontend && npm install
	@cd backend/python && python3 -m pip install -r requirements.txt
	@if command -v go >/dev/null 2>&1; then \
		cd backend/go && go mod download; \
	else \
		echo "⚠️  Go 未安装，跳过 Go 依赖"; \
	fi
	@echo "✅ 初始化完成"

dev:
	@echo "🚀 启动本地开发环境..."
	@echo "启动 Python API (端口 8000)..."
	@cd backend/python && python3 main.py &
	@echo "启动 Go API (端口 8080)..."
	@cd backend/go && go run main.go &
	@echo "启动前端 (端口 3000)..."
	@cd frontend && npm run dev

docker-up:
	@echo "🐳 启动 Docker 环境..."
	@cd infra/docker && docker-compose up -d
	@echo "✅ Docker 环境已启动"

docker-down:
	@echo "🐳 停止 Docker 环境..."
	@cd infra/docker && docker-compose down
	@echo "✅ Docker 环境已停止"

k8s-deploy:
	@echo "☸️  部署到 Kubernetes..."
	@kubectl apply -f infra/k8s/base/
	@echo "✅ 部署完成"

k8s-clean:
	@echo "☸️  清理 Kubernetes 资源..."
	@kubectl delete namespace amazing
	@echo "✅ 清理完成"

test:
	@echo "🧪 运行测试..."
	@cd backend/python && pytest
	@cd backend/go && go test ./...
	@cd frontend && npm run test

lint:
	@echo "🔍 代码检查..."
	@cd backend/python && black . && ruff check .
	@cd backend/go && golangci-lint run
	@cd frontend && npm run lint
