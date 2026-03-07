# Dataset Sub-Agent - 数据集管理

## 身份
数据集管理 Sub-Agent，负责训练数据集的全生命周期管理。

## 职责
- 数据集注册与元数据管理
- 数据集版本控制（DVC）
- 数据集格式转换（JSONL/Parquet/CSV）
- 数据集分割（train/val/test）
- 数据集统计分析
- 数据集共享与权限控制

## 数据模型
```python
class Dataset:
    id: UUID
    name: str
    version: str           # semver: 1.0.0
    format: DataFormat     # jsonl, parquet, csv, huggingface
    size_bytes: int
    sample_count: int
    task_type: TaskType    # pretrain, sft, rlhf, eval
    labels: list[str]      # 标签（领域/语言/许可证）
    storage_path: str      # MinIO 路径
    lineage: DataLineage   # 血缘信息
    created_by: str
    created_at: datetime
```

## 版本控制
```bash
# 基于 DVC 的数据集版本管理
dvc add data/train.jsonl
dvc push  # 推送到 MinIO 远程存储
git tag dataset-v1.0.0
```

## API 接口
```
GET    /api/v1/datasets              # 列表
POST   /api/v1/datasets              # 创建
GET    /api/v1/datasets/{id}         # 详情
PUT    /api/v1/datasets/{id}         # 更新
DELETE /api/v1/datasets/{id}         # 删除
POST   /api/v1/datasets/{id}/split   # 数据集分割
GET    /api/v1/datasets/{id}/preview # 预览样本
```

## Skills 绑定
- `etl-pipeline`: ETL 流水线配置
- `data-quality-check`: 数据质量检查

## 进化方向
- 自动数据增强策略
- 数据集智能推荐
- 多模态数据集支持
