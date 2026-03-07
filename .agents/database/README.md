# Database Agent - 数据库适配器

## 能力描述
动态适配多种数据库，支持自动检测环境并选择合适的数据库配置。

## 支持的数据库
- PostgreSQL 12+
- MySQL 8.0+
- MongoDB 5.0+
- Redis 6.0+
- SQLite 3 (开发环境)

## 核心功能

### 1. 环境检测
自动检测当前环境中可用的数据库服务。

### 2. 动态配置
根据环境自动生成数据库连接配置。

### 3. 迁移管理
- 自动生成迁移脚本
- 支持多数据库迁移
- 版本管理

### 4. 连接池管理
- 自动配置连接池大小
- 连接健康检查
- 故障转移

## 使用方式

### Python (FastAPI)
```python
from agents.database import get_db_config, init_database

# 自动检测并初始化
config = get_db_config()
db = init_database(config)
```

### Go
```go
import "agents/database"

// 自动检测并初始化
config := database.GetDBConfig()
db := database.InitDatabase(config)
```

## 配置示例

### 开发环境
```yaml
database:
  type: sqlite
  path: ./dev.db
```

### Docker 环境
```yaml
database:
  type: postgresql
  host: postgres
  port: 5432
  database: app_db
```

### K8s 环境
```yaml
database:
  type: postgresql
  host: postgres-service.default.svc.cluster.local
  port: 5432
  database: app_db
```

## 进化能力
- 监控数据库性能
- 自动优化查询
- Schema 变更影响分析
