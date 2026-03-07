# Kubernetes 部署指南

## 前置条件

- Kubernetes 1.24+
- kubectl 已配置
- Helm 3+
- 存储类（StorageClass）已配置
- NVIDIA GPU Operator（如需 GPU 支持）

## 快速部署

### 1. 创建命名空间

```bash
kubectl apply -f namespace.yaml
```

### 2. 配置 Secrets

```bash
# 复制模板
cp secret.yaml secret-prod.yaml

# 编辑 secret-prod.yaml，填入实际密码
vim secret-prod.yaml

# 应用配置
kubectl apply -f secret-prod.yaml
```

### 3. 应用配置

```bash
kubectl apply -f configmap.yaml
```

### 4. 部署服务

```bash
# 部署数据库和中间件
kubectl apply -f deployment.yaml

# 等待数据库就绪
kubectl wait --for=condition=ready pod -l app=postgres -n model-platform --timeout=300s

# 部署应用服务
kubectl apply -f service.yaml

# 配置 Ingress
kubectl apply -f ingress.yaml

# 配置自动扩缩容
kubectl apply -f hpa.yaml
```

### 5. 验证部署

```bash
# 查看所有 Pod
kubectl get pods -n model-platform

# 查看服务
kubectl get svc -n model-platform

# 查看 Ingress
kubectl get ingress -n model-platform
```

## GPU 支持

如需 GPU 支持，请参考 [gpu-operator.md](gpu-operator.md)

## 管理命令

### 查看日志

```bash
# 查看后端日志
kubectl logs -f deployment/backend -n model-platform

# 查看训练 Worker 日志
kubectl logs -f deployment/training-worker -n model-platform
```

### 扩容

```bash
# 手动扩容后端
kubectl scale deployment backend --replicas=5 -n model-platform

# 查看 HPA 状态
kubectl get hpa -n model-platform
```

### 更新镜像

```bash
# 更新后端镜像
kubectl set image deployment/backend backend=model-platform/backend:v2 -n model-platform

# 查看滚动更新状态
kubectl rollout status deployment/backend -n model-platform
```

### 回滚

```bash
# 查看历史版本
kubectl rollout history deployment/backend -n model-platform

# 回滚到上一个版本
kubectl rollout undo deployment/backend -n model-platform

# 回滚到指定版本
kubectl rollout undo deployment/backend --to-revision=2 -n model-platform
```

### 进入容器

```bash
# 进入后端容器
kubectl exec -it deployment/backend -n model-platform -- /bin/bash

# 进入数据库容器
kubectl exec -it statefulset/postgres -n model-platform -- psql -U admin -d model_platform
```

## 监控

### Prometheus + Grafana

```bash
# 安装 Prometheus Operator
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# 访问 Grafana
kubectl port-forward svc/prometheus-grafana 3000:80 -n monitoring
```

### 日志聚合

```bash
# 安装 EFK Stack
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch -n logging --create-namespace
helm install kibana elastic/kibana -n logging
helm install filebeat elastic/filebeat -n logging
```

## 备份和恢复

### 数据库备份

```bash
# 创建备份
kubectl exec -it statefulset/postgres -n model-platform -- \
  pg_dump -U admin model_platform > backup_$(date +%Y%m%d).sql

# 恢复备份
kubectl exec -i statefulset/postgres -n model-platform -- \
  psql -U admin model_platform < backup_20240308.sql
```

### 持久化卷备份

使用 Velero 进行集群级备份：

```bash
# 安装 Velero
velero install --provider aws --bucket velero-backups

# 备份命名空间
velero backup create model-platform-backup --include-namespaces model-platform

# 恢复备份
velero restore create --from-backup model-platform-backup
```

## 故障排查

### Pod 无法启动

```bash
# 查看 Pod 状态
kubectl describe pod <pod-name> -n model-platform

# 查看事件
kubectl get events -n model-platform --sort-by='.lastTimestamp'
```

### 服务无法访问

```bash
# 检查 Service
kubectl get svc -n model-platform

# 检查 Endpoints
kubectl get endpoints -n model-platform

# 测试服务连接
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  wget -O- http://backend:8000/health
```

### 存储问题

```bash
# 查看 PVC 状态
kubectl get pvc -n model-platform

# 查看 PV 状态
kubectl get pv

# 查看存储类
kubectl get storageclass
```

## 安全加固

### 1. 网络策略

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: model-platform
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8000
```

### 2. Pod Security Policy

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
  - ALL
  runAsUser:
    rule: MustRunAsNonRoot
  seLinux:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
```

### 3. RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: model-platform-role
  namespace: model-platform
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
```

## 性能优化

### 1. 资源配额

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: model-platform-quota
  namespace: model-platform
spec:
  hard:
    requests.cpu: "50"
    requests.memory: 100Gi
    limits.cpu: "100"
    limits.memory: 200Gi
```

### 2. Pod 优先级

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "High priority for critical services"
```

### 3. 节点亲和性

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: node-type
          operator: In
          values:
          - compute-optimized
```

## 成本优化

1. **使用 HPA**: 根据负载自动扩缩容
2. **Spot 实例**: 训练任务使用 Spot 实例
3. **资源限制**: 合理设置资源 requests 和 limits
4. **集群自动扩缩容**: 使用 Cluster Autoscaler
5. **定时任务**: 非高峰期运行批处理任务
