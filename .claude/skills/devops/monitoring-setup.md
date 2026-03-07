# Monitoring Setup Skill - 监控告警配置

## 功能描述
提供监控告警配置方案、指标定义和告警规则模板。

## 触发方式
- 监控系统搭建
- 告警规则配置
- 可观测性设计

## 核心内容

### 1. 监控三支柱
| 支柱 | 工具 | 用途 |
|------|------|------|
| 指标 | Prometheus + Grafana | 系统/业务指标 |
| 日志 | ELK / Loki | 日志收集分析 |
| 追踪 | Jaeger / Tempo | 分布式链路追踪 |

### 2. 关键指标（RED 方法）
| 指标 | 说明 | 告警阈值 |
|------|------|----------|
| Rate | 请求速率 | 突增/突降 50% |
| Errors | 错误率 | > 1% |
| Duration | 响应时间 | P99 > 500ms |

### 3. 告警规则
```yaml
groups:
  - name: api
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
        for: 5m
        labels: { severity: critical }
      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 5m
        labels: { severity: warning }
```

### 4. Grafana Dashboard
- 系统概览: CPU、内存、磁盘、网络
- API 监控: QPS、延迟、错误率
- 数据库: 连接数、查询延迟、慢查询
- 业务指标: 用户数、订单数、收入

## 进化能力
- 告警规则持续优化
- 误报率持续降低
- 新监控工具自动评估
