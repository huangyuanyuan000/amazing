# K8s Deploy Skill - Kubernetes 部署方案

## 功能描述
提供 Kubernetes 部署方案、Helm Chart 模板和自动扩缩容配置。

## 触发方式
- K8s 部署配置
- Helm Chart 编写
- 集群资源管理

## 核心内容

### 1. 核心资源配置
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate: { maxSurge: 1, maxUnavailable: 0 }
  template:
    spec:
      containers:
        - name: api
          resources:
            requests: { cpu: "100m", memory: "128Mi" }
            limits: { cpu: "500m", memory: "512Mi" }
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
          readinessProbe:
            httpGet: { path: /ready, port: 8000 }
```

### 2. HPA 配置
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 70 }
```

### 3. 部署策略
| 策略 | 适用场景 | 风险 |
|------|----------|------|
| RollingUpdate | 常规更新 | 低 |
| Canary | 高风险更新 | 中 |
| Blue-Green | 零停机 | 低（资源翻倍） |

### 4. Helm Chart 结构
```
chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
```

## 进化能力
- 资源配置自动调优
- 部署策略智能选择
