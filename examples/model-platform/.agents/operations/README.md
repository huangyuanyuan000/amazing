# Operations Agent - 运营管理

## 职责
负责平台运营管理，包括数据分析、用户运营、系统配置等。

## 核心功能

### 1. 数据分析
- 用户分析：活跃用户、用户增长、用户留存
- 资源分析：资源使用率、成本分析
- 业务分析：训练任务统计、模型部署统计

### 2. 用户运营
- 用户画像：用户标签、行为分析
- 运营活动：活动管理、效果评估
- 用户反馈：问题收集、需求管理

### 3. 系统配置
- 系统参数：全局配置、模块配置
- 功能开关：灰度发布、A/B 测试
- 资源配额：用户配额、团队配额

## 技术栈
- **后端**: Python (FastAPI)
- **数据库**: PostgreSQL + MongoDB
- **可视化**: Grafana + Metabase

## API 接口

### 数据分析
- `GET /api/v1/operations/analytics/users` - 用户分析
- `GET /api/v1/operations/analytics/resources` - 资源分析
- `GET /api/v1/operations/analytics/business` - 业务分析

### 用户运营
- `GET /api/v1/operations/users/profile` - 用户画像
- `POST /api/v1/operations/campaigns` - 创建活动
- `GET /api/v1/operations/feedback` - 用户反馈

### 系统配置
- `GET /api/v1/operations/config` - 获取配置
- `PUT /api/v1/operations/config` - 更新配置
- `POST /api/v1/operations/feature-flags` - 功能开关

## 数据模型

### 用户分析
```python
class UserAnalytics:
    date: str
    active_users: int
    new_users: int
    retention_rate: float
```

### 资源分析
```python
class ResourceAnalytics:
    date: str
    gpu_usage: float
    cpu_usage: float
    storage_usage: float
    cost: float
```

### 系统配置
```python
class SystemConfig:
    key: str
    value: Any
    description: str
    updated_at: datetime
```

## Sub-Agents

### Analytics Agent
负责数据分析和报表生成。

### Campaign Agent
负责运营活动管理。

### Config Agent
负责系统配置管理。

## 依赖关系
- 依赖 Common Agent（用户、权限）
- 被 API Gateway 调用
- 读取所有模块的数据

## 监控指标
- 报表生成时间
- 配置更新频率
- 活动参与率
