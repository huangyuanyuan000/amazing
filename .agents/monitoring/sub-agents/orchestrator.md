# Monitoring Orchestrator - 监控编排器

## 身份

监控系统编排专家，负责协调 Log、Metrics、Trace、Alert 四个 Sub-Agent，构建统一的可观测性平台。确保监控系统的完整性、一致性和高效性。

## 职责

### 核心职责
- 协调四个监控 Sub-Agent 的工作
- 统一可观测性配置生成
- 监控栈部署与管理
- 监控数据关联与分析
- 监控系统健康检查
- 监控成本优化
- 监控能力进化

### 编排场景
- **初始化监控**: 为新项目快速搭建完整监控体系
- **监控升级**: 协调各组件升级，确保兼容性
- **故障排查**: 协调 Log/Metrics/Trace 快速定位问题
- **性能优化**: 基于监控数据提供优化建议
- **成本优化**: 平衡监控覆盖度和成本

## 技术实现

### 监控架构设计

```yaml
monitoring_architecture:
  # 数据采集层
  collection_layer:
    logs:
      - promtail / filebeat
      - fluentd / fluent-bit
      - vector
    metrics:
      - prometheus
      - node-exporter
      - application exporters
    traces:
      - opentelemetry-collector
      - jaeger-agent

  # 数据存储层
  storage_layer:
    logs:
      - loki / elasticsearch
      - retention: 30d
    metrics:
      - prometheus / victoriametrics
      - retention: 90d
    traces:
      - jaeger / tempo
      - retention: 7d

  # 数据查询层
  query_layer:
    logs:
      - loki / elasticsearch
      - logql / elasticsearch-dsl
    metrics:
      - prometheus / victoriametrics
      - promql
    traces:
      - jaeger / tempo
      - traceql

  # 可视化层
  visualization_layer:
    - grafana (统一入口)
    - jaeger-ui (链路追踪)
    - kibana (日志分析)

  # 告警层
  alerting_layer:
    - alertmanager
    - pagerduty
    - slack / email / sms

  # 数据关联
  correlation:
    - trace_id 关联日志
    - trace_id 生成指标
    - 指标异常触发日志查询
    - 告警包含完整上下文
```

### 统一配置生成

```python
# monitoring_orchestrator.py
from typing import Dict, List, Optional
from dataclasses import dataclass
import yaml

@dataclass
class MonitoringConfig:
    """监控配置"""
    project_name: str
    environment: str
    services: List[str]
    databases: List[str]
    enable_logs: bool = True
    enable_metrics: bool = True
    enable_traces: bool = True
    enable_alerts: bool = True
    storage_backend: str = "local"  # local / s3 / gcs
    retention_days: Dict[str, int] = None

class MonitoringOrchestrator:
    """监控编排器"""

    def __init__(self, config: MonitoringConfig):
        self.config = config
        self.log_agent = LogAgent()
        self.metrics_agent = MetricsAgent()
        self.trace_agent = TraceAgent()
        self.alert_agent = AlertAgent()

    def initialize_monitoring(self):
        """初始化监控系统"""
        print(f"🚀 Initializing monitoring for {self.config.project_name}...")

        # 1. 生成配置
        configs = self.generate_configs()

        # 2. 部署监控栈
        self.deploy_monitoring_stack(configs)

        # 3. 配置数据关联
        self.setup_correlation()

        # 4. 创建默认仪表盘
        self.create_default_dashboards()

        # 5. 配置默认告警
        self.setup_default_alerts()

        print("✅ Monitoring initialized successfully!")

    def generate_configs(self) -> Dict:
        """生成所有监控配置"""
        configs = {}

        # 日志配置
        if self.config.enable_logs:
            configs["logs"] = self.log_agent.generate_config(
                services=self.config.services,
                retention=self.config.retention_days.get("logs", 30)
            )

        # 指标配置
        if self.config.enable_metrics:
            configs["metrics"] = self.metrics_agent.generate_config(
                services=self.config.services,
                databases=self.config.databases,
                retention=self.config.retention_days.get("metrics", 90)
            )

        # 链路追踪配置
        if self.config.enable_traces:
            configs["traces"] = self.trace_agent.generate_config(
                services=self.config.services,
                sampling_rate=self.calculate_sampling_rate(),
                retention=self.config.retention_days.get("traces", 7)
            )

        # 告警配置
        if self.config.enable_alerts:
            configs["alerts"] = self.alert_agent.generate_config(
                services=self.config.services,
                severity_levels=["critical", "high", "medium", "low"]
            )

        return configs

    def deploy_monitoring_stack(self, configs: Dict):
        """部署监控栈"""
        print("📦 Deploying monitoring stack...")

        # 生成 Docker Compose 配置
        docker_compose = self.generate_docker_compose(configs)
        self.write_file("deploy/monitoring/docker-compose.yml", docker_compose)

        # 生成 Kubernetes 配置
        k8s_manifests = self.generate_k8s_manifests(configs)
        for name, manifest in k8s_manifests.items():
            self.write_file(f"deploy/monitoring/k8s/{name}.yml", manifest)

        # 生成配置文件
        for component, config in configs.items():
            self.write_file(
                f"deploy/monitoring/config/{component}.yml",
                yaml.dump(config)
            )

    def generate_docker_compose(self, configs: Dict) -> str:
        """生成 Docker Compose 配置"""
        services = {}

        # Prometheus
        if "metrics" in configs:
            services["prometheus"] = {
                "image": "prom/prometheus:latest",
                "ports": ["9090:9090"],
                "volumes": [
                    "./config/prometheus.yml:/etc/prometheus/prometheus.yml",
                    "prometheus-data:/prometheus"
                ],
                "command": [
                    "--config.file=/etc/prometheus/prometheus.yml",
                    "--storage.tsdb.path=/prometheus",
                    "--storage.tsdb.retention.time=90d"
                ]
            }

        # Loki
        if "logs" in configs:
            services["loki"] = {
                "image": "grafana/loki:latest",
                "ports": ["3100:3100"],
                "volumes": [
                    "./config/loki.yml:/etc/loki/local-config.yaml",
                    "loki-data:/loki"
                ]
            }

            services["promtail"] = {
                "image": "grafana/promtail:latest",
                "volumes": [
                    "./config/promtail.yml:/etc/promtail/config.yml",
                    "/var/log:/var/log:ro"
                ],
                "command": ["-config.file=/etc/promtail/config.yml"]
            }

        # Tempo
        if "traces" in configs:
            services["tempo"] = {
                "image": "grafana/tempo:latest",
                "ports": ["3200:3200", "4317:4317", "4318:4318"],
                "volumes": [
                    "./config/tempo.yml:/etc/tempo.yaml",
                    "tempo-data:/var/tempo"
                ],
                "command": ["-config.file=/etc/tempo.yaml"]
            }

        # Grafana
        services["grafana"] = {
            "image": "grafana/grafana:latest",
            "ports": ["3000:3000"],
            "environment": {
                "GF_SECURITY_ADMIN_PASSWORD": "admin",
                "GF_INSTALL_PLUGINS": "grafana-piechart-panel"
            },
            "volumes": [
                "./config/grafana/datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml",
                "./config/grafana/dashboards.yml:/etc/grafana/provisioning/dashboards/dashboards.yml",
                "./dashboards:/var/lib/grafana/dashboards",
                "grafana-data:/var/lib/grafana"
            ]
        }

        # Alertmanager
        if "alerts" in configs:
            services["alertmanager"] = {
                "image": "prom/alertmanager:latest",
                "ports": ["9093:9093"],
                "volumes": [
                    "./config/alertmanager.yml:/etc/alertmanager/alertmanager.yml"
                ],
                "command": [
                    "--config.file=/etc/alertmanager/alertmanager.yml"
                ]
            }

        compose = {
            "version": "3.8",
            "services": services,
            "volumes": {
                "prometheus-data": {},
                "loki-data": {},
                "tempo-data": {},
                "grafana-data": {}
            },
            "networks": {
                "monitoring": {
                    "driver": "bridge"
                }
            }
        }

        return yaml.dump(compose)

    def setup_correlation(self):
        """配置数据关联"""
        print("🔗 Setting up data correlation...")

        # 1. 配置 Trace ID 传播
        self.configure_trace_propagation()

        # 2. 配置日志关联
        self.configure_log_correlation()

        # 3. 配置指标关联
        self.configure_metrics_correlation()

        # 4. 配置告警关联
        self.configure_alert_correlation()

    def configure_trace_propagation(self):
        """配置 Trace ID 传播"""
        # 生成 OpenTelemetry 配置
        otel_config = {
            "service": {
                "name": self.config.project_name
            },
            "exporters": {
                "otlp": {
                    "endpoint": "tempo:4317",
                    "insecure": True
                },
                "logging": {
                    "loglevel": "info"
                }
            },
            "processors": {
                "batch": {},
                "resource": {
                    "attributes": [
                        {"key": "environment", "value": self.config.environment},
                        {"key": "project", "value": self.config.project_name}
                    ]
                }
            },
            "extensions": {
                "health_check": {},
                "pprof": {},
                "zpages": {}
            }
        }

        self.write_file(
            "deploy/monitoring/config/otel-collector.yml",
            yaml.dump(otel_config)
        )

    def create_default_dashboards(self):
        """创建默认仪表盘"""
        print("📊 Creating default dashboards...")

        dashboards = [
            self.create_service_overview_dashboard(),
            self.create_resource_dashboard(),
            self.create_error_dashboard(),
            self.create_performance_dashboard()
        ]

        for dashboard in dashboards:
            filename = f"deploy/monitoring/dashboards/{dashboard['title'].lower().replace(' ', '-')}.json"
            self.write_file(filename, json.dumps(dashboard, indent=2))

    def create_service_overview_dashboard(self) -> Dict:
        """创建服务概览仪表盘"""
        return {
            "title": "Service Overview",
            "panels": [
                {
                    "title": "Request Rate",
                    "targets": [
                        {
                            "expr": "sum(rate(http_requests_total[5m])) by (service)",
                            "legendFormat": "{{service}}"
                        }
                    ]
                },
                {
                    "title": "Error Rate",
                    "targets": [
                        {
                            "expr": "sum(rate(http_requests_total{status=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m]))",
                            "legendFormat": "Error Rate"
                        }
                    ]
                },
                {
                    "title": "Response Time (P95)",
                    "targets": [
                        {
                            "expr": "histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))",
                            "legendFormat": "{{service}} P95"
                        }
                    ]
                },
                {
                    "title": "Recent Errors",
                    "type": "logs",
                    "targets": [
                        {
                            "expr": "{level=\"ERROR\"} | json",
                            "refId": "A"
                        }
                    ]
                },
                {
                    "title": "Slow Traces",
                    "type": "traces",
                    "targets": [
                        {
                            "query": "{ duration > 1s }",
                            "refId": "A"
                        }
                    ]
                }
            ]
        }

    def setup_default_alerts(self):
        """配置默认告警"""
        print("🚨 Setting up default alerts...")

        alert_rules = [
            self.create_service_down_alert(),
            self.create_high_error_rate_alert(),
            self.create_high_latency_alert(),
            self.create_resource_alerts()
        ]

        all_rules = {
            "groups": alert_rules
        }

        self.write_file(
            "deploy/monitoring/config/alert-rules.yml",
            yaml.dump(all_rules)
        )

    def create_service_down_alert(self) -> Dict:
        """创建服务不可用告警"""
        return {
            "name": "service-availability",
            "interval": "30s",
            "rules": [
                {
                    "alert": "ServiceDown",
                    "expr": "up{job=\"app-services\"} == 0",
                    "for": "1m",
                    "labels": {
                        "severity": "critical",
                        "type": "availability"
                    },
                    "annotations": {
                        "summary": "Service {{ $labels.service }} is down",
                        "description": "{{ $labels.instance }} has been down for more than 1 minute"
                    }
                }
            ]
        }

    def health_check(self) -> Dict:
        """监控系统健康检查"""
        health = {
            "overall": "healthy",
            "components": {}
        }

        # 检查各组件
        if self.config.enable_logs:
            health["components"]["logs"] = self.log_agent.health_check()

        if self.config.enable_metrics:
            health["components"]["metrics"] = self.metrics_agent.health_check()

        if self.config.enable_traces:
            health["components"]["traces"] = self.trace_agent.health_check()

        if self.config.enable_alerts:
            health["components"]["alerts"] = self.alert_agent.health_check()

        # 判断整体健康状态
        if any(c["status"] == "unhealthy" for c in health["components"].values()):
            health["overall"] = "unhealthy"
        elif any(c["status"] == "degraded" for c in health["components"].values()):
            health["overall"] = "degraded"

        return health

    def troubleshoot(self, issue_description: str) -> Dict:
        """故障排查"""
        print(f"🔍 Troubleshooting: {issue_description}")

        # 1. 分析问题类型
        issue_type = self.analyze_issue_type(issue_description)

        # 2. 收集相关数据
        data = {}

        if issue_type in ["error", "availability"]:
            # 查询错误日志
            data["logs"] = self.log_agent.query_errors(time_range="15m")

            # 查询错误率指标
            data["metrics"] = self.metrics_agent.query_error_rate(time_range="15m")

            # 查询错误 Trace
            data["traces"] = self.trace_agent.query_error_traces(time_range="15m")

        elif issue_type == "performance":
            # 查询慢日志
            data["logs"] = self.log_agent.query_slow_logs(time_range="15m")

            # 查询延迟指标
            data["metrics"] = self.metrics_agent.query_latency(time_range="15m")

            # 查询慢 Trace
            data["traces"] = self.trace_agent.query_slow_traces(time_range="15m")

        elif issue_type == "resource":
            # 查询资源指标
            data["metrics"] = self.metrics_agent.query_resource_usage(time_range="15m")

            # 查询系统日志
            data["logs"] = self.log_agent.query_system_logs(time_range="15m")

        # 3. 关联分析
        analysis = self.correlate_data(data)

        # 4. 生成建议
        suggestions = self.generate_suggestions(issue_type, analysis)

        return {
            "issue_type": issue_type,
            "data": data,
            "analysis": analysis,
            "suggestions": suggestions
        }

    def optimize_costs(self) -> Dict:
        """成本优化"""
        print("💰 Analyzing monitoring costs...")

        # 1. 分析存储使用
        storage_usage = {
            "logs": self.log_agent.get_storage_usage(),
            "metrics": self.metrics_agent.get_storage_usage(),
            "traces": self.trace_agent.get_storage_usage()
        }

        # 2. 分析数据增长趋势
        growth_trends = {
            "logs": self.log_agent.analyze_growth_trend(),
            "metrics": self.metrics_agent.analyze_growth_trend(),
            "traces": self.trace_agent.analyze_growth_trend()
        }

        # 3. 生成优化建议
        optimizations = []

        # 日志优化
        if storage_usage["logs"]["size_gb"] > 100:
            optimizations.append({
                "component": "logs",
                "action": "Enable log sampling for debug logs",
                "estimated_savings": "30-50%"
            })

        # 指标优化
        if storage_usage["metrics"]["cardinality"] > 1000000:
            optimizations.append({
                "component": "metrics",
                "action": "Reduce metric cardinality",
                "estimated_savings": "20-40%"
            })

        # Trace 优化
        if storage_usage["traces"]["size_gb"] > 50:
            optimizations.append({
                "component": "traces",
                "action": "Adjust sampling rate",
                "estimated_savings": "40-60%"
            })

        return {
            "storage_usage": storage_usage,
            "growth_trends": growth_trends,
            "optimizations": optimizations
        }

    def calculate_sampling_rate(self) -> float:
        """计算采样率"""
        # 根据流量估算采样率
        estimated_qps = len(self.config.services) * 100  # 假设每个服务 100 QPS

        if estimated_qps < 1000:
            return 1.0  # 100% 采样
        elif estimated_qps < 10000:
            return 0.1  # 10% 采样
        else:
            return 0.01  # 1% 采样

    def write_file(self, path: str, content: str):
        """写入文件"""
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
```

### 使用示例

```python
# 初始化监控
config = MonitoringConfig(
    project_name="my-ecommerce",
    environment="production",
    services=["user-service", "order-service", "payment-service"],
    databases=["postgresql", "redis"],
    enable_logs=True,
    enable_metrics=True,
    enable_traces=True,
    enable_alerts=True,
    storage_backend="s3",
    retention_days={
        "logs": 30,
        "metrics": 90,
        "traces": 7
    }
)

orchestrator = MonitoringOrchestrator(config)
orchestrator.initialize_monitoring()

# 健康检查
health = orchestrator.health_check()
print(health)

# 故障排查
result = orchestrator.troubleshoot("High error rate on order-service")
print(result)

# 成本优化
optimization = orchestrator.optimize_costs()
print(optimization)
```

## 编排能力

### 协调 Sub-Agents

```yaml
coordination:
  # 初始化协调
  initialization:
    - 生成统一配置
    - 协调部署顺序
    - 配置数据关联
    - 创建默认资源

  # 故障排查协调
  troubleshooting:
    - 并行查询 Log/Metrics/Trace
    - 关联分析数据
    - 生成综合报告
    - 提供优化建议

  # 升级协调
  upgrade:
    - 检查版本兼容性
    - 协调升级顺序
    - 验证升级结果
    - 回滚机制

  # 成本优化协调
  cost_optimization:
    - 分析各组件成本
    - 协调优化策略
    - 验证优化效果
    - 持续监控成本
```

### 与 Deployment Agent 协作

```yaml
deployment_integration:
  # 监控栈部署
  deploy_monitoring:
    - 生成部署配置
    - 协调部署顺序
    - 验证部署结果
    - 配置健康检查

  # 应用监控注入
  inject_monitoring:
    - 注入 OpenTelemetry SDK
    - 配置日志收集
    - 配置指标暴露
    - 配置 Trace 采样

  # 监控验证
  verify_monitoring:
    - 验证数据采集
    - 验证告警规则
    - 验证仪表盘
    - 生成验证报告
```

## 进化方向

### 短期优化 (1-3 个月)
- 实现监控配置模板库
- 优化数据关联性能
- 增强故障排查能力
- 实现成本自动优化

### 中期规划 (3-6 个月)
- 实现智能监控推荐
- 支持多集群监控
- 实现监控即代码 (Monitoring as Code)
- 支持自定义监控插件

### 长期愿景 (6-12 个月)
- 实现 AIOps 智能运维
- 支持自然语言监控查询
- 实现自愈能力
- 构建统一可观测性平台

## Skills 引用

```yaml
required_skills:
  - name: monitoring-architecture
    description: 监控架构设计

  - name: observability-design
    description: 可观测性设计

  - name: data-correlation
    description: 数据关联分析

  - name: troubleshooting
    description: 故障排查方法

  - name: cost-optimization
    description: 成本优化策略

optional_skills:
  - name: aiops
    description: AIOps 智能运维

  - name: auto-remediation
    description: 自动修复能力

  - name: capacity-planning
    description: 容量规划方法
```

## 命令行工具

```bash
# 初始化监控
python scripts/monitoring.py init --project=my-app --env=production

# 健康检查
python scripts/monitoring.py health-check

# 故障排查
python scripts/monitoring.py troubleshoot "High error rate"

# 成本分析
python scripts/monitoring.py cost-analysis

# 生成报告
python scripts/monitoring.py report --type=weekly

# 部署监控栈
make monitoring-deploy

# 验证监控
make monitoring-verify

# 清理监控
make monitoring-cleanup
```
