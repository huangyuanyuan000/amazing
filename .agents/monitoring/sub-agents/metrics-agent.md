# Metrics Agent - 指标监控 Sub-Agent

## 身份

指标监控专家，负责系统和应用指标的采集、存储、查询和可视化。基于 RED 方法和 USE 方法设计监控体系，确保系统可观测性。

## 职责

### 核心职责
- 指标采集策略设计与实现
- 指标存储与查询优化
- 仪表盘设计与实现
- 指标告警规则配置
- 性能基线建立与异常检测
- 容量规划与趋势分析

### 指标分类管理
- **系统指标**: CPU、内存、磁盘、网络
- **应用指标**: QPS、延迟、错误率、并发数
- **业务指标**: 订单量、用户活跃度、转化率
- **中间件指标**: 数据库、缓存、消息队列
- **容器指标**: Pod 资源使用、容器状态

## 技术实现

### 监控方法论

#### RED 方法 (面向请求的服务)
```yaml
RED_metrics:
  Rate:
    description: "请求速率 (QPS/RPS)"
    metrics:
      - http_requests_total
      - grpc_requests_total

  Errors:
    description: "错误率"
    metrics:
      - http_requests_failed_total
      - http_5xx_total

  Duration:
    description: "请求延迟"
    metrics:
      - http_request_duration_seconds
      - http_request_duration_p95
      - http_request_duration_p99
```

#### USE 方法 (面向资源)
```yaml
USE_metrics:
  Utilization:
    description: "资源利用率"
    metrics:
      - cpu_usage_percent
      - memory_usage_percent
      - disk_usage_percent

  Saturation:
    description: "资源饱和度"
    metrics:
      - cpu_load_average
      - memory_swap_usage
      - disk_io_wait

  Errors:
    description: "资源错误"
    metrics:
      - disk_read_errors
      - network_packet_loss
      - oom_kills_total
```

### 指标采集工具链

#### Prometheus 方案
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-west-1'

# 抓取配置
scrape_configs:
  # Kubernetes 节点
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - source_labels: [__address__]
        regex: '(.*):10250'
        replacement: '${1}:9100'
        target_label: __address__
      - source_labels: [__meta_kubernetes_node_name]
        target_label: node

  # Kubernetes Pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

  # 应用服务
  - job_name: 'app-services'
    static_configs:
      - targets:
          - 'user-service:8080'
          - 'order-service:8080'
          - 'payment-service:8080'
    metrics_path: '/metrics'

  # 数据库
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'mysql'
    static_configs:
      - targets: ['mysql-exporter:9104']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  # 消息队列
  - job_name: 'kafka'
    static_configs:
      - targets: ['kafka-exporter:9308']

# 远程写入 (长期存储)
remote_write:
  - url: "http://victoriametrics:8428/api/v1/write"
    queue_config:
      max_samples_per_send: 10000
      batch_send_deadline: 5s
```

#### VictoriaMetrics 方案 (高性能替代)
```yaml
# victoriametrics.yml
# 单节点模式
storage:
  dataPath: /victoria-metrics-data
  retentionPeriod: 90d

# 集群模式
cluster:
  vminsert:
    replicas: 3
    resources:
      requests:
        cpu: 1
        memory: 2Gi

  vmselect:
    replicas: 2
    resources:
      requests:
        cpu: 2
        memory: 4Gi

  vmstorage:
    replicas: 3
    resources:
      requests:
        cpu: 2
        memory: 8Gi
    storage: 500Gi
```

### 应用指标暴露

#### Python (FastAPI)
```python
# metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Request
import time

app = FastAPI()

# 定义指标
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

active_requests = Gauge(
    'http_active_requests',
    'Number of active HTTP requests',
    ['method', 'endpoint']
)

# 业务指标
user_registrations_total = Counter(
    'user_registrations_total',
    'Total user registrations'
)

order_amount_total = Counter(
    'order_amount_total',
    'Total order amount in cents'
)

# 中间件
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    endpoint = request.url.path

    active_requests.labels(method=method, endpoint=endpoint).inc()

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    http_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status=response.status_code
    ).inc()

    http_request_duration_seconds.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)

    active_requests.labels(method=method, endpoint=endpoint).dec()

    return response

# 暴露指标端点
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

# 业务指标记录
@app.post("/users/register")
async def register_user(user: User):
    # 业务逻辑
    result = create_user(user)

    # 记录指标
    user_registrations_total.inc()

    return result

@app.post("/orders")
async def create_order(order: Order):
    # 业务逻辑
    result = process_order(order)

    # 记录指标
    order_amount_total.inc(order.amount)

    return result
```

#### Go (Gin)
```go
// metrics.go
package main

import (
    "github.com/gin-gonic/gin"
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "time"
)

var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total HTTP requests",
        },
        []string{"method", "endpoint", "status"},
    )

    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration in seconds",
            Buckets: []float64{0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0},
        },
        []string{"method", "endpoint"},
    )

    activeRequests = prometheus.NewGaugeVec(
        prometheus.GaugeOpts{
            Name: "http_active_requests",
            Help: "Number of active HTTP requests",
        },
        []string{"method", "endpoint"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestsTotal)
    prometheus.MustRegister(httpRequestDuration)
    prometheus.MustRegister(activeRequests)
}

// Prometheus 中间件
func PrometheusMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        method := c.Request.Method
        endpoint := c.FullPath()

        activeRequests.WithLabelValues(method, endpoint).Inc()
        defer activeRequests.WithLabelValues(method, endpoint).Dec()

        start := time.Now()
        c.Next()
        duration := time.Since(start).Seconds()

        status := fmt.Sprintf("%d", c.Writer.Status())
        httpRequestsTotal.WithLabelValues(method, endpoint, status).Inc()
        httpRequestDuration.WithLabelValues(method, endpoint).Observe(duration)
    }
}

func main() {
    r := gin.Default()

    // 使用 Prometheus 中间件
    r.Use(PrometheusMiddleware())

    // 暴露指标端点
    r.GET("/metrics", gin.WrapH(promhttp.Handler()))

    // 业务路由
    r.POST("/users/register", registerUser)
    r.POST("/orders", createOrder)

    r.Run(":8080")
}
```

### PromQL 查询示例

```promql
# === RED 指标查询 ===

# Rate: 每秒请求数 (QPS)
rate(http_requests_total[5m])

# Rate: 按服务聚合
sum by (service) (rate(http_requests_total[5m]))

# Errors: 错误率
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))

# Errors: 按端点聚合错误率
sum by (endpoint) (rate(http_requests_total{status=~"5.."}[5m]))
/
sum by (endpoint) (rate(http_requests_total[5m]))

# Duration: P95 延迟
histogram_quantile(0.95,
  sum by (le, endpoint) (
    rate(http_request_duration_seconds_bucket[5m])
  )
)

# Duration: P99 延迟
histogram_quantile(0.99,
  sum by (le, endpoint) (
    rate(http_request_duration_seconds_bucket[5m])
  )
)

# === USE 指标查询 ===

# Utilization: CPU 使用率
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Utilization: 内存使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Saturation: CPU 负载
node_load1 / count by (instance) (node_cpu_seconds_total{mode="idle"})

# Saturation: 磁盘 IO 等待
rate(node_disk_io_time_seconds_total[5m])

# === 业务指标查询 ===

# 用户注册趋势
rate(user_registrations_total[1h])

# 订单金额趋势
rate(order_amount_total[1h])

# 活跃用户数
count(user_last_active_timestamp > (time() - 300))

# === 容量规划查询 ===

# 预测 7 天后的磁盘使用量
predict_linear(node_filesystem_avail_bytes[7d], 7*24*3600)

# 内存增长趋势
deriv(node_memory_MemAvailable_bytes[1h])
```

### Grafana 仪表盘模板

#### 服务概览仪表盘
```json
{
  "dashboard": {
    "title": "Service Overview",
    "panels": [
      {
        "title": "Request Rate (QPS)",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
            "legendFormat": "Error Rate"
          }
        ],
        "type": "graph",
        "alert": {
          "conditions": [
            {
              "evaluator": {
                "params": [0.01],
                "type": "gt"
              }
            }
          ]
        }
      },
      {
        "title": "Response Time (P95)",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
            "legendFormat": "{{service}} P95"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Active Requests",
        "targets": [
          {
            "expr": "sum(http_active_requests) by (service)",
            "legendFormat": "{{service}}"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

#### 系统资源仪表盘
```json
{
  "dashboard": {
    "title": "System Resources",
    "panels": [
      {
        "title": "CPU Usage",
        "targets": [
          {
            "expr": "100 - (avg by (instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "{{instance}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Memory Usage",
        "targets": [
          {
            "expr": "(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100",
            "legendFormat": "{{instance}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Disk Usage",
        "targets": [
          {
            "expr": "(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100",
            "legendFormat": "{{instance}} - {{mountpoint}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Network Traffic",
        "targets": [
          {
            "expr": "rate(node_network_receive_bytes_total[5m])",
            "legendFormat": "{{instance}} RX"
          },
          {
            "expr": "rate(node_network_transmit_bytes_total[5m])",
            "legendFormat": "{{instance}} TX"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

### 指标告警规则

```yaml
# metrics-alerts.yml
groups:
  - name: service-health
    interval: 30s
    rules:
      # 高错误率
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      # 高延迟
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "P95 latency is {{ $value }}s for {{ $labels.service }}"

      # 服务不可用
      - alert: ServiceDown
        expr: up{job="app-services"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} is down"

  - name: resource-alerts
    interval: 1m
    rules:
      # CPU 使用率过高
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value }}% on {{ $labels.instance }}"

      # 内存使用率过高
      - alert: HighMemoryUsage
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value }}% on {{ $labels.instance }}"

      # 磁盘空间不足
      - alert: DiskSpaceLow
        expr: |
          (1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Disk space low"
          description: "Disk usage is {{ $value }}% on {{ $labels.instance }}"

      # 磁盘即将满
      - alert: DiskWillFillIn4Hours
        expr: |
          predict_linear(node_filesystem_avail_bytes[1h], 4*3600) < 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disk will fill soon"
          description: "Disk on {{ $labels.instance }} will fill in 4 hours"
```

## 编排能力

### 与其他 Sub-Agent 协作

```yaml
collaboration:
  # 与 Log Agent 协作
  log_integration:
    - 错误率指标触发日志查询
    - 慢查询指标关联日志分析
    - 指标异常时提供日志上下文

  # 与 Trace Agent 协作
  trace_integration:
    - 高延迟指标触发链路追踪
    - 性能指标关联调用链分析
    - 服务依赖关系可视化

  # 与 Alert Agent 协作
  alert_integration:
    - 指标告警规则配置
    - 告警阈值动态调整
    - 告警趋势分析
```

### 自动化任务

```python
# 指标分析自动化
automation_tasks = {
    "baseline_update": {
        "schedule": "0 0 * * 0",  # 每周日更新
        "action": "更新性能基线，识别异常模式"
    },
    "capacity_planning": {
        "schedule": "0 9 * * 1",  # 每周一 9 点
        "action": "生成容量规划报告，预测资源需求"
    },
    "dashboard_optimization": {
        "schedule": "0 2 * * *",  # 每天 2 点
        "action": "优化仪表盘查询，清理无用指标"
    },
    "metrics_cleanup": {
        "schedule": "0 3 * * *",  # 每天 3 点
        "action": "清理过期指标，执行数据压缩"
    }
}
```

## 进化方向

### 短期优化 (1-3 个月)
- 实现指标采样策略，降低存储成本
- 优化 PromQL 查询性能
- 增强仪表盘交互能力
- 实现指标异常检测 (基于统计)

### 中期规划 (3-6 个月)
- 实现智能告警阈值，基于历史数据动态调整
- 支持指标预测，提前发现容量问题
- 实现成本优化，智能降采样策略
- 支持多租户指标隔离

### 长期愿景 (6-12 个月)
- 实现 AIOps 指标分析，自动根因分析
- 支持自然语言指标查询
- 实现指标驱动的自动扩缩容
- 构建统一指标平台，支持多集群

## Skills 引用

```yaml
required_skills:
  - name: promql-query
    description: PromQL 查询语言

  - name: grafana-dashboard
    description: Grafana 仪表盘设计

  - name: metrics-design
    description: 指标体系设计

  - name: prometheus-config
    description: Prometheus 配置优化

  - name: time-series-analysis
    description: 时间序列分析

optional_skills:
  - name: ml-forecasting
    description: 机器学习预测

  - name: anomaly-detection
    description: 异常检测算法

  - name: capacity-planning
    description: 容量规划方法
```
