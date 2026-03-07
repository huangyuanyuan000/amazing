.PHONY: help dev build start stop restart logs clean deploy k8s-deploy

# 默认目标
help:
	@echo "电商平台 - 可用命令："
	@echo "  make dev          - 启动本地开发环境"
	@echo "  make build        - 构建所有服务"
	@echo "  make start        - 启动所有服务"
	@echo "  make stop         - 停止所有服务"
	@echo "  make restart      - 重启所有服务"
	@echo "  make logs         - 查看服务日志"
	@echo "  make clean        - 清理所有容器和数据"
	@echo "  make deploy       - 部署到生产环境"
	@echo "  make k8s-deploy   - 部署到 Kubernetes"

# 本地开发环境
dev:
	@echo "🚀 启动本地开发环境..."
	docker-compose -f deploy/local/docker-compose.yml up -d
	@echo "✅ 开发环境已启动！"
	@echo ""
	@echo "访问地址："
	@echo "  前端:         http://localhost:3000"
	@echo "  通用服务:     http://localhost:8000"
	@echo "  商品服务:     http://localhost:8001"
	@echo "  订单服务:     http://localhost:8002"
	@echo "  支付服务:     http://localhost:8003"
	@echo "  物流服务:     http://localhost:8004"
	@echo "  Prometheus:   http://localhost:9090"
	@echo "  Grafana:      http://localhost:3001 (admin/admin)"
	@echo "  RabbitMQ:     http://localhost:15672 (ecommerce/ecommerce123)"

# 构建所有服务
build:
	@echo "🔨 构建所有服务..."
	docker-compose -f deploy/local/docker-compose.yml build

# 启动所有服务
start:
	@echo "▶️  启动所有服务..."
	docker-compose -f deploy/local/docker-compose.yml start

# 停止所有服务
stop:
	@echo "⏸️  停止所有服务..."
	docker-compose -f deploy/local/docker-compose.yml stop

# 重启所有服务
restart:
	@echo "🔄 重启所有服务..."
	docker-compose -f deploy/local/docker-compose.yml restart

# 查看日志
logs:
	docker-compose -f deploy/local/docker-compose.yml logs -f

# 清理
clean:
	@echo "🧹 清理所有容器和数据..."
	docker-compose -f deploy/local/docker-compose.yml down -v
	@echo "✅ 清理完成！"

# 部署到生产环境
deploy:
	@echo "🚀 部署到生产环境..."
	@echo "请确认已配置生产环境变量！"
	@read -p "继续部署? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	docker-compose -f deploy/local/docker-compose.yml -f deploy/local/docker-compose.prod.yml up -d
	@echo "✅ 部署完成！"

# 部署到 Kubernetes
k8s-deploy:
	@echo "☸️  部署到 Kubernetes..."
	kubectl apply -f deploy/k8s/namespace.yaml
	kubectl apply -f deploy/k8s/configmap.yaml
	kubectl apply -f deploy/k8s/secret.yaml
	kubectl apply -f deploy/k8s/postgres.yaml
	kubectl apply -f deploy/k8s/mysql.yaml
	kubectl apply -f deploy/k8s/redis.yaml
	kubectl apply -f deploy/k8s/elasticsearch.yaml
	kubectl apply -f deploy/k8s/rabbitmq.yaml
	@echo "等待数据库就绪..."
	sleep 30
	kubectl apply -f deploy/k8s/common.yaml
	kubectl apply -f deploy/k8s/product.yaml
	kubectl apply -f deploy/k8s/order.yaml
	kubectl apply -f deploy/k8s/payment.yaml
	kubectl apply -f deploy/k8s/logistics.yaml
	kubectl apply -f deploy/k8s/frontend.yaml
	kubectl apply -f deploy/k8s/ingress.yaml
	@echo "✅ Kubernetes 部署完成！"
	@echo ""
	@echo "查看部署状态："
	@echo "  kubectl get pods -n ecommerce"
	@echo "  kubectl get svc -n ecommerce"

# 初始化数据库
init-db:
	@echo "📊 初始化数据库..."
	docker-compose -f deploy/local/docker-compose.yml exec postgres psql -U ecommerce -d ecommerce -f /docker-entrypoint-initdb.d/init.sql
	docker-compose -f deploy/local/docker-compose.yml exec mysql mysql -u payment -ppassword123 payment < /docker-entrypoint-initdb.d/init.sql
	@echo "✅ 数据库初始化完成！"

# 运行测试
test:
	@echo "🧪 运行测试..."
	docker-compose -f deploy/local/docker-compose.yml exec product-service pytest
	docker-compose -f deploy/local/docker-compose.yml exec order-service pytest
	docker-compose -f deploy/local/docker-compose.yml exec payment-service go test ./...
	docker-compose -f deploy/local/docker-compose.yml exec logistics-service pytest
	@echo "✅ 测试完成！"

# 查看服务状态
status:
	@echo "📊 服务状态："
	docker-compose -f deploy/local/docker-compose.yml ps

# 进入服务容器
shell-product:
	docker-compose -f deploy/local/docker-compose.yml exec product-service /bin/bash

shell-order:
	docker-compose -f deploy/local/docker-compose.yml exec order-service /bin/bash

shell-payment:
	docker-compose -f deploy/local/docker-compose.yml exec payment-service /bin/sh

shell-logistics:
	docker-compose -f deploy/local/docker-compose.yml exec logistics-service /bin/bash
