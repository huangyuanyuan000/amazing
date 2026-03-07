# DB Migration Skill - 数据库迁移管理

## 功能描述
提供数据库迁移脚本生成规范、版本管理策略和安全迁移实践。

## 触发方式
- Schema 变更
- 数据迁移
- 数据库版本升级

## 核心内容

### 1. 迁移规范
- 版本号: `{YYYYMMDD}_{序号}_{描述}.sql`
- 每个迁移必须有对应回滚脚本
- 所有 DDL 在事务中执行
- 大表变更使用在线 DDL

### 2. 安全规则
- 禁止直接 DROP TABLE（先 RENAME）
- ALTER TABLE 避免锁表（使用 CONCURRENTLY）
- 数据迁移分批执行（batch <= 1000）
- 生产迁移前必须在测试环境验证

### 3. 迁移模板
```sql
-- Migration: {描述}
-- Version: {版本号}

-- Up
BEGIN;
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
CREATE INDEX CONCURRENTLY idx_users_phone ON users(phone);
COMMIT;

-- Down
BEGIN;
DROP INDEX IF EXISTS idx_users_phone;
ALTER TABLE users DROP COLUMN IF EXISTS phone;
COMMIT;
```

### 4. 零停机迁移策略
1. 新增字段（可空）→ 部署新代码 → 回填数据 → 添加约束
2. 删除字段: 新代码不使用 → 部署 → 删除字段
3. 重命名: 新增字段 → 双写 → 迁移数据 → 删除旧字段

## 示例
```python
# Alembic
def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20)))
def downgrade():
    op.drop_column('users', 'phone')
```

## 进化能力
- 迁移模式库持续扩充
- 零停机策略持续优化
- 迁移冲突自动检测
