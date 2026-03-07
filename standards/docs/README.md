# 文档规范

## 代码注释
### Python
```python
def calculate_gpu_utilization(node_id: str, time_range: int = 3600) -> float:
    """计算指定节点的 GPU 利用率。

    Args:
        node_id: 集群节点 ID
        time_range: 统计时间范围（秒），默认 1 小时

    Returns:
        GPU 利用率百分比 (0.0 - 100.0)

    Raises:
        NodeNotFoundError: 节点不存在
    """
```

### Go
```go
// ScheduleTrainingJob 调度训练任务到合适的 GPU 节点。
// 根据任务资源需求和节点可用资源进行匹配，支持亲和性和反亲和性策略。
func ScheduleTrainingJob(job *TrainingJob) (*Node, error) {
```

### TypeScript
```typescript
/**
 * 模型服务部署面板组件
 * @param modelId - 模型 ID
 * @param onDeploy - 部署成功回调
 */
```

## README 模板
每个模块/服务必须包含 README.md：
```markdown
# 模块名称

## 概述
一句话描述模块功能。

## 快速开始
​```bash
# 安装依赖
# 启动服务
# 运行测试
​```

## API 文档
Swagger 地址: http://localhost:PORT/docs

## 配置说明
| 变量 | 描述 | 默认值 |
|------|------|--------|

## 目录结构
​```
├── app/
│   ├── api/        # API 路由
│   ├── models/     # 数据模型
│   ├── schemas/    # 请求/响应模型
│   ├── services/   # 业务逻辑
│   └── core/       # 核心配置
└── tests/
​```
```

## 变更日志
遵循 Keep a Changelog 格式：
```markdown
## [1.2.0] - 2026-03-06
### Added
- 新增 GPU 资源池管理功能
### Fixed
- 修复分页偏移量计算错误
### Changed
- 优化训练任务调度算法
```
