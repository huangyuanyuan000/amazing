# 电商平台案例

## 项目概述

这是一个基于 Amazing 架构的 B2C 电商平台完整案例，展示如何使用 Amazing 快速构建电商系统。

## 产品形态

### 产品描述

```
我要构建一个 B2C 电商平台，主要解决中小企业在线销售的需求。

目标用户：
- 消费者（浏览和购买商品）
- 商家（管理商品和订单）
- 平台运营（管理平台和数据）

使用场景：
- 在线购物
- 商家入驻
- 平台运营

核心功能包括：

1. 商品管理
   - 商品发布和编辑
   - 商品分类和标签
   - 商品搜索和筛选
   - 商品推荐

2. 订单管理
   - 购物车
   - 下单和支付
   - 订单跟踪
   - 退款和售后

3. 支付管理
   - 多种支付方式（支付宝、微信、银行卡）
   - 支付安全
   - 对账和结算

4. 物流管理
   - 物流跟踪
   - 配送管理
   - 物流商对接

5. 用户管理
   - 用户注册和登录
   - 用户信息管理
   - 会员体系
   - 积分和优惠券

技术要求：
- 高并发（支持秒杀活动）
- 高可用（24/7 在线）
- 数据安全（支付和用户数据）

预期规模：
- 用户数：10 万 - 100 万
- 商品数：1 万 - 10 万
- 日订单量：1000 - 10000
```

## 业务划分

### AI 推荐方案

**方案 A：按业务流程划分（推荐）**

```
├── 商品 Agent - 商品管理
│   ├── 商品发布和编辑
│   ├── 商品分类和标签
│   ├── 商品搜索和筛选
│   └── 商品推荐
│
├── 订单 Agent - 订单和购物车
│   ├── 购物车管理
│   ├── 下单流程
│   ├── 订单跟踪
│   └── 退款和售后
│
├── 支付 Agent - 支付和结算
│   ├── 支付接口对接
│   ├── 支付安全
│   ├── 对账和结算
│   └── 退款处理
│
└── 物流 Agent - 配送和跟踪
    ├── 物流跟踪
    ├── 配送管理
    ├── 物流商对接
    └── 配送费计算
```

**选择理由**：
- 符合用户购物流程
- 用户视角直观
- 便于理解和使用

## 技术架构

### 技术栈选择

#### 商品 Agent
```json
{
  "backend": "Python + FastAPI",
  "database": "PostgreSQL",
  "cache": "Redis",
  "search": "Elasticsearch"
}
```

#### 订单 Agent
```json
{
  "backend": "Python + FastAPI",
  "database": "PostgreSQL",
  "cache": "Redis",
  "queue": "RabbitMQ"
}
```

#### 支付 Agent
```json
{
  "backend": "Go + Gin",
  "database": "MySQL",
  "cache": "Redis",
  "queue": "RabbitMQ"
}
```

#### 物流 Agent
```json
{
  "backend": "Python + FastAPI",
  "database": "PostgreSQL",
  "cache": "Redis"
}
```

#### 前端
```json
{
  "framework": "React",
  "language": "TypeScript",
  "ui": "Ant Design",
  "stateManagement": "Zustand"
}
```

### 数据库设计

#### 商品数据库（PostgreSQL）

```sql
-- 商品表
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    category_id INT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 分类表
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_id INT,
    level INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 商品图片表
CREATE TABLE product_images (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    url VARCHAR(500) NOT NULL,
    sort_order INT DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

#### 订单数据库（PostgreSQL）

```sql
-- 订单表
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_no VARCHAR(50) UNIQUE NOT NULL,
    user_id INT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    payment_status VARCHAR(20) DEFAULT 'unpaid',
    shipping_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 订单明细表
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    product_name VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- 购物车表
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 支付数据库（MySQL）

```sql
-- 支付记录表
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_no VARCHAR(50) UNIQUE NOT NULL,
    order_no VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    transaction_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_order_no (order_no),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 退款记录表
CREATE TABLE refunds (
    id INT AUTO_INCREMENT PRIMARY KEY,
    refund_no VARCHAR(50) UNIQUE NOT NULL,
    payment_no VARCHAR(50) NOT NULL,
    order_no VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_payment_no (payment_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## 部署方式

### 本地开发环境

```bash
# 进入项目目录
cd examples/e-commerce

# 启动所有服务
make dev

# 或使用 Docker Compose
docker-compose -f deploy/local/docker-compose.yml up
```

**访问地址**：
- 前端：http://localhost:3000
- 商品服务：http://localhost:8001
- 订单服务：http://localhost:8002
- 支付服务：http://localhost:8003
- 物流服务：http://localhost:8004

### Kubernetes 部署

```bash
# 部署到 K8s
make k8s-deploy

# 或手动部署
kubectl apply -f deploy/k8s/
```

### 私有化部署

```bash
# 使用私有化部署脚本
./deploy/private/install.sh

# 配置私有化参数
vim deploy/private/config.yaml
```

## 快速开始

### 1. 初始化项目

```bash
# 使用 Amazing CLI 初始化
amazing-cli init e-commerce --template e-commerce

# 或手动克隆
git clone https://github.com/z58362026/amazing.git
cd amazing/examples/e-commerce
```

### 2. 配置环境

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置
vim .env
```

### 3. 启动服务

```bash
# 本地开发
make dev

# 生产部署
make deploy
```

## 目录结构

```
e-commerce/
├── docs/
│   ├── README.md              # 本文档
│   ├── architecture.md        # 架构设计
│   ├── api.md                 # API 文档
│   └── database.md            # 数据库设计
│
├── backend/
│   ├── product/               # 商品服务
│   ├── order/                 # 订单服务
│   ├── payment/               # 支付服务
│   └── logistics/             # 物流服务
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── product/      # 商品页面
│   │   │   ├── order/        # 订单页面
│   │   │   ├── cart/         # 购物车页面
│   │   │   └── user/         # 用户中心
│   │   └── components/
│   └── package.json
│
├── deploy/
│   ├── local/
│   │   ├── docker-compose.yml
│   │   └── Makefile
│   ├── k8s/
│   │   ├── product.yaml
│   │   ├── order.yaml
│   │   ├── payment.yaml
│   │   └── logistics.yaml
│   └── private/
│       ├── install.sh
│       └── config.yaml
│
├── .env.example
├── Makefile
└── README.md
```

## 核心功能演示

### 商品浏览

```
用户访问首页
    ↓
查看商品列表（分页、筛选）
    ↓
查看商品详情
    ↓
加入购物车
```

### 下单流程

```
查看购物车
    ↓
选择商品
    ↓
填写收货地址
    ↓
选择支付方式
    ↓
确认订单
    ↓
支付
    ↓
支付成功
    ↓
订单跟踪
```

### 商家管理

```
商家登录
    ↓
发布商品
    ↓
管理库存
    ↓
处理订单
    ↓
查看数据统计
```

## 性能指标

### 目标指标

- **并发用户**：10000+
- **QPS**：5000+
- **响应时间**：< 200ms
- **可用性**：99.9%

### 优化措施

1. **缓存策略**
   - 商品信息缓存（Redis）
   - 热门商品缓存
   - 用户会话缓存

2. **数据库优化**
   - 读写分离
   - 分库分表
   - 索引优化

3. **搜索优化**
   - Elasticsearch 全文搜索
   - 搜索结果缓存

4. **CDN 加速**
   - 静态资源 CDN
   - 图片 CDN

## 相关文档

- [架构设计](./architecture.md)
- [API 文档](./api.md)
- [数据库设计](./database.md)
- [部署指南](./deployment.md)
