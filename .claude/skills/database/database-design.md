# Database Design Skill - Schema 设计规范

## 功能描述
提供数据库 Schema 设计规范、范式理论和索引策略。

## 触发方式
- 新模块数据库设计
- Schema 优化
- 数据库审查

## 核心内容

### 1. 设计流程
1. 业务实体识别 → 2. 关系分析 → 3. 字段定义 → 4. 索引策略 → 5. 范式优化

### 2. 命名规范
- 表名: 小写下划线，复数（`users`, `order_items`）
- 字段名: 小写下划线（`created_at`, `user_id`）
- 索引: `idx_{表}_{字段}`，外键: `fk_{表}_{关联表}`

### 3. 必备字段
```sql
id          BIGSERIAL PRIMARY KEY,
created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
deleted_at  TIMESTAMP WITH TIME ZONE  -- 软删除
```

### 4. 索引策略
| 场景 | 索引类型 | 说明 |
|------|----------|------|
| 等值查询 | B-Tree | WHERE email = ? |
| 范围查询 | B-Tree | WHERE created_at > ? |
| 全文搜索 | GIN | 文本搜索 |
| JSON 查询 | GIN | JSONB 字段 |

## 示例
```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    status SMALLINT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status) WHERE deleted_at IS NULL;
```

## 进化能力
- 设计模式库持续扩充
- 从查询模式反推索引优化
- 新数据库特性自动适配
