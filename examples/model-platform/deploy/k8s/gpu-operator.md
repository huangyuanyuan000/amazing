# GPU Operator 配置

## 前置条件

1. 安装 NVIDIA GPU Operator

```bash
# 添加 NVIDIA Helm 仓库
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update

# 安装 GPU Operator
helm install --wait --generate-name \
  -n gpu-operator --create-namespace \
  nvidia/gpu-operator
```

2. 验证 GPU Operator 安装

```bash
kubectl get pods -n gpu-operator
```

## GPU 节点标签

为 GPU 节点打标签：

```bash
# 标记 GPU 节点
kubectl label nodes <node-name> gpu=true

# 查看节点标签
kubectl get nodes --show-labels | grep gpu
```

## GPU 资源配置

### 1. 节点资源

查看节点 GPU 资源：

```bash
kubectl describe node <gpu-node-name> | grep nvidia.com/gpu
```

### 2. Pod GPU 请求

在 Deployment 中请求 GPU：

```yaml
resources:
  requests:
    nvidia.com/gpu: 1  # 请求 1 个 GPU
  limits:
    nvidia.com/gpu: 1  # 限制 1 个 GPU
```

### 3. GPU 共享

如果需要 GPU 共享（多个 Pod 共享一个 GPU）：

```bash
# 安装 GPU Sharing Scheduler
kubectl apply -f https://raw.githubusercontent.com/AliyunContainerService/gpushare-scheduler-extender/master/config/gpushare-schd-extender.yaml
```

## 训练任务 GPU 配置

### 单 GPU 训练

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: training-job-single-gpu
  namespace: model-platform
spec:
  template:
    spec:
      containers:
      - name: trainer
        image: model-platform/trainer:latest
        resources:
          limits:
            nvidia.com/gpu: 1
      restartPolicy: Never
```

### 多 GPU 训练（单节点）

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: training-job-multi-gpu
  namespace: model-platform
spec:
  template:
    spec:
      containers:
      - name: trainer
        image: model-platform/trainer:latest
        resources:
          limits:
            nvidia.com/gpu: 4  # 4 个 GPU
      restartPolicy: Never
```

### 分布式训练（多节点）

使用 PyTorch Distributed 或 Horovod：

```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: distributed-training
  namespace: model-platform
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      template:
        spec:
          containers:
          - name: pytorch
            image: model-platform/trainer:latest
            resources:
              limits:
                nvidia.com/gpu: 1
    Worker:
      replicas: 4
      template:
        spec:
          containers:
          - name: pytorch
            image: model-platform/trainer:latest
            resources:
              limits:
                nvidia.com/gpu: 1
```

## GPU 监控

### 1. 安装 DCGM Exporter

```bash
helm install --generate-name \
  -n gpu-operator \
  nvidia/dcgm-exporter
```

### 2. Prometheus 配置

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    scrape_configs:
    - job_name: 'dcgm'
      static_configs:
      - targets: ['dcgm-exporter:9400']
```

### 3. Grafana Dashboard

导入 NVIDIA DCGM Dashboard (ID: 12239)

## GPU 资源配额

限制命名空间的 GPU 使用：

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-quota
  namespace: model-platform
spec:
  hard:
    requests.nvidia.com/gpu: "10"
    limits.nvidia.com/gpu: "10"
```

## 故障排查

### 1. GPU 不可用

```bash
# 检查 GPU Operator 状态
kubectl get pods -n gpu-operator

# 检查节点 GPU 资源
kubectl describe node <node-name> | grep nvidia.com/gpu

# 查看 GPU 驱动日志
kubectl logs -n gpu-operator <nvidia-driver-pod>
```

### 2. Pod 无法调度到 GPU 节点

```bash
# 检查节点标签
kubectl get nodes --show-labels | grep gpu

# 检查节点污点
kubectl describe node <node-name> | grep Taints

# 查看 Pod 事件
kubectl describe pod <pod-name> -n model-platform
```

### 3. GPU 内存不足

```bash
# 查看 GPU 使用情况
kubectl exec -it <pod-name> -n model-platform -- nvidia-smi

# 调整 GPU 内存分配
# 在代码中设置 GPU 内存增长
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
```

## 最佳实践

1. **资源请求和限制**: 始终设置 GPU 资源的 requests 和 limits
2. **节点选择器**: 使用 nodeSelector 确保 Pod 调度到 GPU 节点
3. **容忍度**: 配置 tolerations 以处理 GPU 节点的污点
4. **资源配额**: 设置命名空间级别的 GPU 配额
5. **监控**: 部署 DCGM Exporter 监控 GPU 使用情况
6. **自动扩缩容**: 根据 GPU 使用率配置 HPA
7. **优先级**: 为训练任务设置合适的优先级类

## 参考文档

- [NVIDIA GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/getting-started.html)
- [Kubernetes GPU Support](https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/)
- [DCGM Exporter](https://github.com/NVIDIA/dcgm-exporter)
