# Skill: K8s Scheduling
# Version: 1.0.0
# Agent: compute
# Tags: kubernetes, scheduling, gpu

## 描述
Kubernetes 集群调度策略配置，包括 GPU 调度、优先级、亲和性。

## GPU 调度配置
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: gpu-training-job
spec:
  containers:
  - name: training
    image: ${REGISTRY}/training:${VERSION}
    resources:
      limits:
        nvidia.com/gpu: 4
      requests:
        nvidia.com/gpu: 4
        memory: "64Gi"
        cpu: "16"
    env:
    - name: NVIDIA_VISIBLE_DEVICES
      value: "all"
  nodeSelector:
    gpu-type: a100
  tolerations:
  - key: "nvidia.com/gpu"
    operator: "Exists"
    effect: "NoSchedule"
```

## 优先级配置
```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority-training
value: 1000000
globalDefault: false
description: "高优先级训练任务"
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low-priority-inference
value: 100000
globalDefault: false
description: "低优先级推理任务"
```

## 弹性伸缩
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: inference-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-inference
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Pods
    pods:
      metric:
        name: gpu_utilization
      target:
        type: AverageValue
        averageValue: "80"
```
