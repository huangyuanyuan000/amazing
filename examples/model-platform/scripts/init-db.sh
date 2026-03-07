#!/bin/bash

echo "🗄️  初始化数据库..."
echo ""

# 加载环境变量
if [ -f deploy/local/.env ]; then
    export $(cat deploy/local/.env | grep -v '^#' | xargs)
else
    echo "⚠️  未找到 .env 文件，使用默认配置"
    export POSTGRES_HOST=localhost
    export POSTGRES_PORT=5432
    export POSTGRES_DB=model_platform
    export POSTGRES_USER=admin
    export POSTGRES_PASSWORD=admin123
fi

# 等待 PostgreSQL 就绪
echo "1️⃣  等待 PostgreSQL 就绪..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -c '\q' 2>/dev/null; do
    echo "   等待 PostgreSQL..."
    sleep 2
done
echo "   ✅ PostgreSQL 已就绪"
echo ""

# 创建数据库（如果不存在）
echo "2️⃣  创建数据库..."
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || \
PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d postgres -c "CREATE DATABASE $POSTGRES_DB"
echo "   ✅ 数据库已创建"
echo ""

# 创建表结构
echo "3️⃣  创建表结构..."

PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB << 'SQL'

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 资源表
CREATE TABLE IF NOT EXISTS resources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available',
    specs JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 数据集表
CREATE TABLE IF NOT EXISTS datasets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    size BIGINT,
    format VARCHAR(20),
    path VARCHAR(255),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 训练任务表
CREATE TABLE IF NOT EXISTS training_jobs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    dataset_id INTEGER REFERENCES datasets(id),
    model_config JSONB,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 模型表
CREATE TABLE IF NOT EXISTS models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20),
    training_job_id INTEGER REFERENCES training_jobs(id),
    path VARCHAR(255),
    metrics JSONB,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SQL

echo "   ✅ 表结构已创建"
echo ""

# 插入初始数据
echo "4️⃣  插入初始数据..."

PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB << 'SQL'

-- 插入管理员用户（密码: admin123）
INSERT INTO users (username, email, password_hash, role)
VALUES ('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqVr/qvQqK', 'admin')
ON CONFLICT (username) DO NOTHING;

-- 插入测试用户（密码: user123）
INSERT INTO users (username, email, password_hash, role)
VALUES ('testuser', 'user@example.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'user')
ON CONFLICT (username) DO NOTHING;

-- 插入测试资源
INSERT INTO resources (name, type, status, specs)
VALUES 
    ('GPU-001', 'gpu', 'available', '{"model": "NVIDIA A100", "memory": "40GB"}'),
    ('GPU-002', 'gpu', 'available', '{"model": "NVIDIA A100", "memory": "40GB"}'),
    ('CPU-001', 'cpu', 'available', '{"cores": 32, "memory": "128GB"}')
ON CONFLICT DO NOTHING;

SQL

echo "   ✅ 初始数据已插入"
echo ""

echo "✅ 数据库初始化完成！"
echo ""
echo "📝 默认账号："
echo "   管理员: admin / admin123"
echo "   测试用户: testuser / user123"
