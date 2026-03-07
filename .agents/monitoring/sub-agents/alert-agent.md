# Alert Agent - 告警管理 Sub-Agent

## 身份

告警管理专家，负责告警规则配置、告警路由、通知管理和告警生命周期管理。确保关键问题能够及时发现并通知到相关人员。

## 职责

### 核心职责
- 告警规则设计与配置
- 告警分级与优先级管理
- 告警路由与通知策略
- 告警聚合与去重
- 告警静默与抑制
- 告警生命周期管理
- 值班排班与升级策略

### 告警场景
- **服务告警**: 服务不可用、高错误率、高延迟
- **资源告警**: CPU/内存/磁盘告警
- **业务告警**: 订单异常、支付失败、用户流失
- **安全告警**: 异常登录、权限变更、攻击检测
- **基础设施告警**: 网络故障、存储故障、K8s 异常

## 技术实现

### 告警分级体系

```yaml
alert_severity_levels:
  Critical:
    description: "严重故障，影响核心业务"
    response_time: "5 分钟内响应"
    notification:
      - 电话
      - 短信
      - IM (立即)
    escalation: "15 分钟无响应则升级"
    examples:
      - 服务完全不可用
      - 数据丢失风险
      - 安全漏洞被利用
      - 支付系统故障

  High:
    description: "重要问题，影响部分功能"
    response_time: "15 分钟内响应"
    notification:
      - 短信
      - IM (立即)
      - 邮件
    escalation: "30 分钟无响应则升级"
    examples:
      - 高错误率 (> 5%)
      - 高延迟 (P95 > 2s)
      - 部分服务降级
      - 数据库主从延迟

  Medium:
    description: "一般问题，需要关注"
    response_time: "1 小时内响应"
    notification:
      - IM
      - 邮件
    escalation: "2 小时无响应则升级"
    examples:
      - 中等错误率 (1-5%)
      - 中等延迟 (P95 1-2s)
      - 资源使用率高 (> 80%)
      - 慢查询增多

  Low:
    description: "轻微问题，可延后处理"
    response_time: "工作时间内响应"
    notification:
      - 邮件
      - 工单
    escalation: "无自动升级"
    examples:
      - 低错误率 (< 1%)
      - 资源使用率偏高 (70-80%)
      - 非关键服务异常
      - 配置建议

  Info:
    description: "信息通知，无需处理"
    response_time: "无要求"
    notification:
      - 邮件
      - 日志
    escalation: "无"
    examples:
      - 部署完成
      - 配置变更
      - 定期报告
      - 系统维护通知
```

### Alertmanager 配置

```yaml
# alertmanager.yml
global:
  resolve_timeout: 5m
  smtp_smarthost: 'smtp.gmail.com:587'
  smtp_from: 'alerts@company.com'
  smtp_auth_username: 'alerts@company.com'
  smtp_auth_password: 'password'
  slack_api_url: 'https://hooks.slack.com/services/xxx'
  pagerduty_url: 'https://events.pagerduty.com/v2/enqueue'

# 告警路由
route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s        # 等待同组告警
  group_interval: 10s    # 同组告警间隔
  repeat_interval: 12h   # 重复告警间隔

  routes:
    # Critical 告警 - 立即通知所有渠道
    - match:
        severity: critical
      receiver: 'critical-team'
      group_wait: 0s
      repeat_interval: 5m
      continue: true

    # High 告警 - 通知值班人员
    - match:
        severity: high
      receiver: 'oncall-team'
      group_wait: 30s
      repeat_interval: 30m

    # 数据库告警 - 通知 DBA
    - match_re:
        service: '.*database.*'
      receiver: 'dba-team'
      group_by: ['alertname', 'instance']

    # 业务告警 - 通知业务团队
    - match:
        type: business
      receiver: 'business-team'
      group_by: ['alertname', 'business_unit']

    # 安全告警 - 通知安全团队
    - match:
        type: security
      receiver: 'security-team'
      group_wait: 0s
      repeat_interval: 1h

    # 工作时间外的 Low 告警 - 延迟到工作时间
    - match:
        severity: low
      receiver: 'low-priority'
      active_time_intervals:
        - business-hours

# 告警接收器
receivers:
  # 默认接收器
  - name: 'default'
    email_configs:
      - to: 'team@company.com'

  # Critical 团队 - 多渠道通知
  - name: 'critical-team'
    pagerduty_configs:
      - service_key: 'xxx'
        severity: 'critical'
    slack_configs:
      - channel: '#alerts-critical'
        title: '🚨 Critical Alert'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
    webhook_configs:
      - url: 'http://phone-service/call'
        send_resolved: false
    email_configs:
      - to: 'oncall@company.com'
        headers:
          Subject: '[CRITICAL] {{ .GroupLabels.alertname }}'

  # 值班团队
  - name: 'oncall-team'
    pagerduty_configs:
      - service_key: 'yyy'
        severity: 'high'
    slack_configs:
      - channel: '#alerts-high'
        title: '⚠️ High Priority Alert'
    email_configs:
      - to: 'oncall@company.com'

  # DBA 团队
  - name: 'dba-team'
    slack_configs:
      - channel: '#dba-alerts'
    email_configs:
      - to: 'dba@company.com'

  # 业务团队
  - name: 'business-team'
    slack_configs:
      - channel: '#business-alerts'
    email_configs:
      - to: 'business@company.com'

  # 安全团队
  - name: 'security-team'
    slack_configs:
      - channel: '#security-alerts'
        title: '🔒 Security Alert'
    email_configs:
      - to: 'security@company.com'
    webhook_configs:
      - url: 'http://siem-system/webhook'

  # 低优先级
  - name: 'low-priority'
    email_configs:
      - to: 'team@company.com'

# 告警抑制规则
inhibit_rules:
  # 服务不可用时，抑制该服务的其他告警
  - source_match:
      severity: 'critical'
      alertname: 'ServiceDown'
    target_match_re:
      severity: 'high|medium|low'
    equal: ['service', 'instance']

  # 节点宕机时，抑制该节点上的所有告警
  - source_match:
      alertname: 'NodeDown'
    target_match_re:
      alertname: '.*'
    equal: ['instance']

  # Critical 告警时，抑制同服务的 High 告警
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'high'
    equal: ['service']

  # 数据库主库故障时，抑制从库延迟告警
  - source_match:
      alertname: 'DatabaseMasterDown'
    target_match:
      alertname: 'DatabaseReplicationLag'
    equal: ['cluster']

# 时间窗口配置
time_intervals:
  # 工作时间
  - name: business-hours
    time_intervals:
      - times:
          - start_time: '09:00'
            end_time: '18:00'
        weekdays: ['monday:friday']
        location: 'Asia/Shanghai'

  # 非工作时间
  - name: off-hours
    time_intervals:
      - times:
          - start_time: '18:00'
            end_time: '09:00'
        weekdays: ['monday:friday']
      - weekdays: ['saturday', 'sunday']
        location: 'Asia/Shanghai'
```

### 告警规则示例

```yaml
# alert-rules.yml
groups:
  # 服务可用性告警
  - name: service-availability
    interval: 30s
    rules:
      # 服务完全不可用
      - alert: ServiceDown
        expr: up{job="app-services"} == 0
        for: 1m
        labels:
          severity: critical
          type: availability
        annotations:
          summary: "Service {{ $labels.service }} is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"
          runbook_url: "https://wiki.company.com/runbooks/service-down"
          dashboard_url: "https://grafana.company.com/d/service-overview"

      # 高错误率
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service) > 0.05
        for: 5m
        labels:
          severity: critical
          type: performance
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }} (threshold: 5%)"

      # 高延迟
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)
          ) > 2
        for: 10m
        labels:
          severity: high
          type: performance
        annotations:
          summary: "High latency on {{ $labels.service }}"
          description: "P95 latency is {{ $value }}s (threshold: 2s)"

  # 资源告警
  - name: resource-alerts
    interval: 1m
    rules:
      # CPU 使用率过高
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
        for: 10m
        labels:
          severity: high
          type: resource
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is {{ $value | humanize }}%"

      # 内存即将耗尽
      - alert: MemoryPressure
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 90
        for: 5m
        labels:
          severity: critical
          type: resource
        annotations:
          summary: "Memory pressure on {{ $labels.instance }}"
          description: "Memory usage is {{ $value | humanize }}%"

      # 磁盘即将满
      - alert: DiskSpaceCritical
        expr: |
          (1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100 > 90
        for: 5m
        labels:
          severity: critical
          type: resource
        annotations:
          summary: "Disk space critical on {{ $labels.instance }}"
          description: "Disk usage is {{ $value | humanize }}% on {{ $labels.mountpoint }}"

  # 业务告警
  - name: business-alerts
    interval: 1m
    rules:
      # 订单创建失败率高
      - alert: HighOrderFailureRate
        expr: |
          sum(rate(order_created_total{status="failed"}[5m]))
          /
          sum(rate(order_created_total[5m])) > 0.1
        for: 5m
        labels:
          severity: high
          type: business
        annotations:
          summary: "High order failure rate"
          description: "Order failure rate is {{ $value | humanizePercentage }}"

      # 支付成功率下降
      - alert: LowPaymentSuccessRate
        expr: |
          sum(rate(payment_total{status="success"}[10m]))
          /
          sum(rate(payment_total[10m])) < 0.95
        for: 5m
        labels:
          severity: critical
          type: business
        annotations:
          summary: "Low payment success rate"
          description: "Payment success rate is {{ $value | humanizePercentage }}"

      # 用户注册量异常下降
      - alert: UserRegistrationDrop
        expr: |
          rate(user_registrations_total[1h]) < 0.5 * rate(user_registrations_total[1h] offset 24h)
        for: 30m
        labels:
          severity: medium
          type: business
        annotations:
          summary: "User registration drop detected"
          description: "Registration rate dropped by 50% compared to yesterday"

  # 安全告警
  - name: security-alerts
    interval: 1m
    rules:
      # 异常登录尝试
      - alert: BruteForceAttack
        expr: |
          sum(rate(login_attempts_total{status="failed"}[5m])) by (ip) > 10
        for: 2m
        labels:
          severity: high
          type: security
        annotations:
          summary: "Brute force attack detected"
          description: "{{ $value }} failed login attempts from {{ $labels.ip }}"

      # 权限提升
      - alert: PrivilegeEscalation
        expr: |
          sum(rate(permission_changes_total{action="grant_admin"}[5m])) > 0
        labels:
          severity: critical
          type: security
        annotations:
          summary: "Privilege escalation detected"
          description: "Admin permission granted to user"

      # API 滥用
      - alert: APIRateLimitExceeded
        expr: |
          sum(rate(http_requests_total[1m])) by (client_id) > 1000
        for: 1m
        labels:
          severity: medium
          type: security
        annotations:
          summary: "API rate limit exceeded"
          description: "Client {{ $labels.client_id }} exceeded rate limit"
```

### 告警通知模板

#### Slack 通知模板
```yaml
# slack-template.tmpl
{{ define "slack.title" }}
{{ if eq .Status "firing" }}🔥{{ else }}✅{{ end }} {{ .GroupLabels.alertname }}
{{ end }}

{{ define "slack.text" }}
{{ range .Alerts }}
*Alert:* {{ .Labels.alertname }}
*Severity:* {{ .Labels.severity }}
*Status:* {{ .Status }}
*Summary:* {{ .Annotations.summary }}
*Description:* {{ .Annotations.description }}
{{ if .Annotations.runbook_url }}*Runbook:* {{ .Annotations.runbook_url }}{{ end }}
{{ if .Annotations.dashboard_url }}*Dashboard:* {{ .Annotations.dashboard_url }}{{ end }}
*Labels:*
{{ range .Labels.SortedPairs }}  • {{ .Name }}: {{ .Value }}
{{ end }}
{{ end }}
{{ end }}
```

#### 邮件通知模板
```html
<!-- email-template.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        .alert-critical { background-color: #ff4444; color: white; }
        .alert-high { background-color: #ff9944; color: white; }
        .alert-medium { background-color: #ffdd44; color: black; }
        .alert-low { background-color: #44ff44; color: black; }
    </style>
</head>
<body>
    <h2>{{ .GroupLabels.alertname }}</h2>
    <table>
        {{ range .Alerts }}
        <tr class="alert-{{ .Labels.severity }}">
            <td><strong>{{ .Labels.alertname }}</strong></td>
            <td>{{ .Annotations.summary }}</td>
        </tr>
        <tr>
            <td colspan="2">
                <p>{{ .Annotations.description }}</p>
                <p><strong>Status:</strong> {{ .Status }}</p>
                <p><strong>Started:</strong> {{ .StartsAt }}</p>
                {{ if .Annotations.runbook_url }}
                <p><a href="{{ .Annotations.runbook_url }}">View Runbook</a></p>
                {{ end }}
                {{ if .Annotations.dashboard_url }}
                <p><a href="{{ .Annotations.dashboard_url }}">View Dashboard</a></p>
                {{ end }}
            </td>
        </tr>
        {{ end }}
    </table>
</body>
</html>
```

### 告警聚合与去重

```python
# alert_aggregation.py
from datetime import datetime, timedelta
from collections import defaultdict

class AlertAggregator:
    """告警聚合器"""

    def __init__(self):
        self.alert_cache = defaultdict(list)
        self.aggregation_window = timedelta(minutes=5)

    def process_alert(self, alert):
        """处理告警"""
        # 生成聚合键
        agg_key = self.generate_aggregation_key(alert)

        # 检查是否需要聚合
        if self.should_aggregate(agg_key, alert):
            self.alert_cache[agg_key].append(alert)
            return None  # 不立即发送

        # 发送聚合后的告警
        aggregated = self.aggregate_alerts(agg_key)
        self.alert_cache[agg_key] = []
        return aggregated

    def generate_aggregation_key(self, alert):
        """生成聚合键"""
        return (
            alert.get("alertname"),
            alert.get("severity"),
            alert.get("service")
        )

    def should_aggregate(self, agg_key, alert):
        """判断是否需要聚合"""
        cached_alerts = self.alert_cache[agg_key]

        if not cached_alerts:
            return True

        # 检查时间窗口
        first_alert_time = cached_alerts[0].get("timestamp")
        current_time = alert.get("timestamp")

        if current_time - first_alert_time < self.aggregation_window:
            return True

        return False

    def aggregate_alerts(self, agg_key):
        """聚合告警"""
        alerts = self.alert_cache[agg_key]

        if len(alerts) == 1:
            return alerts[0]

        # 聚合多个告警
        aggregated = {
            "alertname": agg_key[0],
            "severity": agg_key[1],
            "service": agg_key[2],
            "count": len(alerts),
            "instances": [a.get("instance") for a in alerts],
            "first_occurrence": alerts[0].get("timestamp"),
            "last_occurrence": alerts[-1].get("timestamp"),
            "summary": f"{len(alerts)} instances affected",
            "details": [a.get("description") for a in alerts]
        }

        return aggregated

# 告警去重
class AlertDeduplicator:
    """告警去重器"""

    def __init__(self):
        self.sent_alerts = {}
        self.dedup_window = timedelta(hours=1)

    def is_duplicate(self, alert):
        """检查是否是重复告警"""
        alert_key = self.generate_alert_key(alert)

        if alert_key in self.sent_alerts:
            last_sent = self.sent_alerts[alert_key]
            if datetime.now() - last_sent < self.dedup_window:
                return True

        self.sent_alerts[alert_key] = datetime.now()
        return False

    def generate_alert_key(self, alert):
        """生成告警唯一键"""
        return (
            alert.get("alertname"),
            alert.get("instance"),
            alert.get("severity")
        )

    def cleanup_old_entries(self):
        """清理过期记录"""
        now = datetime.now()
        self.sent_alerts = {
            k: v for k, v in self.sent_alerts.items()
            if now - v < self.dedup_window
        }
```

### 值班管理

```python
# oncall_schedule.py
from datetime import datetime, timedelta

class OnCallSchedule:
    """值班排班管理"""

    def __init__(self):
        self.schedule = []
        self.escalation_policy = []

    def add_shift(self, user, start_time, end_time, level=1):
        """添加值班班次"""
        self.schedule.append({
            "user": user,
            "start_time": start_time,
            "end_time": end_time,
            "level": level
        })

    def get_oncall_user(self, timestamp=None, level=1):
        """获取当前值班人员"""
        if timestamp is None:
            timestamp = datetime.now()

        for shift in self.schedule:
            if (shift["start_time"] <= timestamp <= shift["end_time"]
                and shift["level"] == level):
                return shift["user"]

        return None

    def escalate_alert(self, alert, current_level=1):
        """告警升级"""
        # 获取下一级值班人员
        next_level = current_level + 1
        next_oncall = self.get_oncall_user(level=next_level)

        if next_oncall:
            return {
                "escalated_to": next_oncall,
                "level": next_level,
                "alert": alert
            }

        # 没有更高级别，通知管理层
        return {
            "escalated_to": "management",
            "level": "final",
            "alert": alert
        }

# 自动升级
class AlertEscalation:
    """告警自动升级"""

    def __init__(self, schedule):
        self.schedule = schedule
        self.pending_alerts = {}

    def track_alert(self, alert):
        """跟踪告警响应"""
        alert_id = alert.get("id")
        self.pending_alerts[alert_id] = {
            "alert": alert,
            "sent_at": datetime.now(),
            "level": 1,
            "acknowledged": False
        }

    def acknowledge_alert(self, alert_id):
        """确认告警"""
        if alert_id in self.pending_alerts:
            self.pending_alerts[alert_id]["acknowledged"] = True

    def check_escalation(self):
        """检查是否需要升级"""
        now = datetime.now()
        escalations = []

        for alert_id, info in self.pending_alerts.items():
            if info["acknowledged"]:
                continue

            # 计算响应时间
            response_time = now - info["sent_at"]
            alert = info["alert"]
            severity = alert.get("severity")

            # 根据严重程度判断是否升级
            should_escalate = False
            if severity == "critical" and response_time > timedelta(minutes=15):
                should_escalate = True
            elif severity == "high" and response_time > timedelta(minutes=30):
                should_escalate = True
            elif severity == "medium" and response_time > timedelta(hours=2):
                should_escalate = True

            if should_escalate:
                escalated = self.schedule.escalate_alert(
                    alert,
                    info["level"]
                )
                escalations.append(escalated)

                # 更新级别
                info["level"] += 1
                info["sent_at"] = now

        return escalations
```

## 编排能力

### 与其他 Sub-Agent 协作

```yaml
collaboration:
  # 与 Log Agent 协作
  log_integration:
    - 告警触发时自动查询相关日志
    - 日志异常自动生成告警
    - 告警通知包含日志链接

  # 与 Metrics Agent 协作
  metrics_integration:
    - 基于指标生成告警规则
    - 告警阈值动态调整
    - 告警趋势分析

  # 与 Trace Agent 协作
  trace_integration:
    - 性能告警关联 Trace 分析
    - 告警通知包含 Trace 链接
    - 慢 Trace 自动生成告警
```

### 自动化任务

```python
# 告警管理自动化
automation_tasks = {
    "alert_rule_optimization": {
        "schedule": "0 2 * * 0",  # 每周日 2 点
        "action": "分析告警规则有效性，优化阈值"
    },
    "false_positive_analysis": {
        "schedule": "0 9 * * 1",  # 每周一 9 点
        "action": "分析误报告警，调整规则"
    },
    "oncall_report": {
        "schedule": "0 10 * * 1",  # 每周一 10 点
        "action": "生成值班报告，统计告警处理情况"
    },
    "alert_cleanup": {
        "schedule": "0 3 * * *",  # 每天 3 点
        "action": "清理已解决的告警，归档历史数据"
    }
}
```

## 进化方向

### 短期优化 (1-3 个月)
- 实现智能告警降噪，减少误报
- 优化告警路由策略
- 增强告警上下文信息
- 实现告警自动确认

### 中期规划 (3-6 个月)
- 实现智能告警分组，自动识别关联告警
- 支持告警预测，提前发现问题
- 实现告警自动修复 (Auto-remediation)
- 支持多租户告警隔离

### 长期愿景 (6-12 个月)
- 实现 AIOps 告警分析，自动根因分析
- 支持自然语言告警查询
- 实现告警驱动的自动化运维
- 构建统一告警平台，支持多数据源

## Skills 引用

```yaml
required_skills:
  - name: alertmanager-config
    description: Alertmanager 配置管理

  - name: alert-routing
    description: 告警路由策略设计

  - name: notification-management
    description: 通知渠道管理

  - name: oncall-management
    description: 值班排班管理

  - name: alert-lifecycle
    description: 告警生命周期管理

optional_skills:
  - name: ml-anomaly-detection
    description: 机器学习异常检测

  - name: auto-remediation
    description: 自动修复能力

  - name: incident-management
    description: 事件管理流程
```
