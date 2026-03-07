# Skill: Model Service Deploy
# Version: 1.0.0
# Agent: model-service
# Tags: deploy, inference, vllm

## 描述
模型服务部署配置，支持多种推理引擎。

## vLLM 部署
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-${MODEL_NAME}
  labels:
    app: model-service
    model: ${MODEL_NAME}
spec:
  replicas: ${REPLICAS}
  selector:
    matchLabels:
      model: ${MODEL_NAME}
  template:
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args:
        - "--model=${MODEL_PATH}"
        - "--tensor-parallel-size=${TP_SIZE}"
        - "--max-model-len=${MAX_LEN}"
        - "--port=8000"
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: ${TP_SIZE}
---
apiVersion: v1
kind: Service
metadata:
  name: model-${MODEL_NAME}-svc
spec:
  selector:
    model: ${MODEL_NAME}
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

## 灰度发布策略
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: model-${MODEL_NAME}-vs
spec:
  hosts:
  - model-${MODEL_NAME}
  http:
  - route:
    - destination:
        host: model-${MODEL_NAME}-v1
      weight: 90
    - destination:
        host: model-${MODEL_NAME}-v2
      weight: 10
```
