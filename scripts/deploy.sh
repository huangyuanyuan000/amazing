#!/bin/bash

# Amazing 一键部署脚本

set -e

echo "🚀 Amazing 一键部署脚本"
echo "========================"

# 检测部署模式
MODE=${1:-"local"}

case $MODE in
  "local")
    echo "📦 本地开发模式"
    echo "检查依赖..."

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 未安装"
        exit 1
    fi

    # 检查 Node.js
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js 未安装"
        exit 1
    fi

    # 检查 Go
    if ! command -v go &> /dev/null; then
        echo "❌ Go 未安装"
        exit 1
    fi

    echo "✅ 依赖检查通过"
    echo "初始化项目..."
    make init

    echo "✅ 部署完成"
    echo "运行 'make dev' 启动开发环境"
    ;;

  "docker")
    echo "🐳 Docker 模式"
    echo "检查 Docker..."

    if ! command -v docker &> /dev/null; then
        echo "❌ Docker 未安装"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose 未安装"
        exit 1
    fi

    echo "✅ Docker 检查通过"
    echo "启动服务..."
    make docker-up

    echo "✅ 部署完成"
    echo "访问 http://localhost:3000"
    ;;

  "k8s")
    echo "☸️  Kubernetes 模式"
    echo "检查 kubectl..."

    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl 未安装"
        exit 1
    fi

    echo "✅ kubectl 检查通过"
    echo "部署到 K8s..."
    make k8s-deploy

    echo "✅ 部署完成"
    echo "运行 'kubectl get svc -n amazing' 查看服务"
    ;;

  "offline")
    echo "📦 离线部署模式"
    echo "检查部署包..."

    if [ ! -f "amazing-deploy.tar.gz" ]; then
        echo "❌ 部署包不存在"
        exit 1
    fi

    echo "解压部署包..."
    tar -xzf amazing-deploy.tar.gz

    echo "加载镜像..."
    docker load < python-api.tar
    docker load < go-api.tar
    docker load < frontend.tar
    docker load < postgres.tar
    docker load < redis.tar

    echo "启动服务..."
    make docker-up

    echo "✅ 部署完成"
    echo "访问 http://localhost:3000"
    ;;

  *)
    echo "❌ 未知部署模式: $MODE"
    echo "支持的模式: local, docker, k8s, offline"
    exit 1
    ;;
esac
