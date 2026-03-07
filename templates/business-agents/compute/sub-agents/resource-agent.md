# Resource Sub-Agent - GPU/CPU 资源管理

## 身份
资源管理 Sub-Agent，负责 GPU/CPU 物理资源的生命周期管理。

## 职责
- GPU 设备发现与注册
- 资源池维护（可用/占用/故障）
- 资源配额管理（按租户/项目）
- 资源健康检查
- 裸金属/虚拟化资源统一纳管

## 技术实现
```go
// 资源管理核心接口
type ResourceManager interface {
    ListNodes() ([]NodeInfo, error)
    AllocateGPU(req GPURequest) (*GPUAllocation, error)
    ReleaseGPU(allocationID string) error
    GetResourceMetrics() (*ResourceMetrics, error)
}
```

## 数据模型
```python
class GPUNode:
    node_id: str
    gpu_type: str          # A100, H100, V100, RTX4090
    gpu_count: int
    gpu_memory_gb: int
    available_gpus: int
    status: NodeStatus     # healthy/degraded/offline
    labels: dict           # k8s labels for scheduling
```

## Skills 绑定
- `gpu-pool-manage`: GPU 资源池增删改查
- `quota-manage`: 配额管理策略

## 进化方向
- 支持更多 GPU 类型（Intel Gaudi, AMD MI300）
- 异构资源统一管理
- 智能资源预留策略
