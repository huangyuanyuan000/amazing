# Registry Sub-Agent - 模型注册管理

## 身份
模型注册 Sub-Agent，负责模型的注册、版本管理和元数据维护。

## 职责
- 模型文件存储（MinIO/S3）
- 模型元数据注册（训练参数/性能指标）
- 版本控制（语义化版本）
- 模型格式转换（PyTorch → ONNX → TensorRT）
- 模型血缘追踪

## 模型元数据
```python
class ModelMeta:
    id: UUID
    name: str
    version: str              # v1.2.3
    base_model: str           # Llama-3-8B
    task_type: str            # chat/completion/embedding
    architecture: str         # transformer/moe
    parameter_count: int      # 7B/13B/70B
    context_length: int       # 4096/8192/32768
    training_job_id: UUID     # 来源训练任务
    dataset_id: UUID          # 训练数据集
    metrics: dict             # 评估指标
    storage_path: str         # 模型文件路径
    status: ModelStatus       # draft/testing/production/deprecated
```

## 版本策略
```
major.minor.patch
├── major: 架构重大变更
├── minor: 训练数据/策略更新
└── patch: 微调/修复
```

## API 接口
```
POST   /api/v1/models              # 注册模型
GET    /api/v1/models              # 模型列表
GET    /api/v1/models/{id}         # 模型详情
GET    /api/v1/models/{id}/versions # 版本列表
POST   /api/v1/models/{id}/convert  # 格式转换
DELETE /api/v1/models/{id}         # 弃用模型
```

## Skills 绑定
- `service-deploy`: 模型部署配置生成

## 进化方向
- 模型血缘图谱可视化
- 自动化模型卡生成（Model Card）
- 多格式自动转换（PyTorch/ONNX/GGUF/TensorRT）
