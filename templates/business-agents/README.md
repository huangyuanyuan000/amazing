# 业务 Agent 模板库

本目录包含可选的业务 Agent 模板，用于快速初始化特定领域的项目。

## 模板列表

### 1. Compute Agent - 算力平台
**适用场景**: GPU/CPU 资源管理、集群调度、算力监控

**核心能力**:
- GPU/CPU 资源池管理
- 集群节点管理与调度
- 资源监控与告警
- 成本核算与优化
- 弹性伸缩策略

**技术栈**: Go + Python/FastAPI + Kubernetes + Prometheus

**使用方式**:
```bash
python3 scripts/init.py my-project --business-agents=compute
```

---

### 2. Data Agent - 数据平台
**适用场景**: 数据集管理、数据标注、数据质量控制

**核心能力**:
- 数据集上传与版本管理
- 数据标注任务管理
- 数据清洗与质量评估
- 数据血缘追踪
- 数据安全与权限控制

**技术栈**: Python/FastAPI + PostgreSQL + MinIO/S3

**使用方式**:
```bash
python3 scripts/init.py my-project --business-agents=data
```

---

### 3. Training Agent - 训推平台
**适用场景**: 模型训练、实验管理、超参调优

**核心能力**:
- 训练任务管理（单机/分布式）
- 实验追踪与参数管理
- 超参数自动调优
- 模型版本管理
- 训练资源调度

**技术栈**: Python/FastAPI + PyTorch/TensorFlow + MLflow

**使用方式**:
```bash
python3 scripts/init.py my-project --business-agents=training
```

---

### 4. Model Service Agent - 模型服务
**适用场景**: 模型部署、推理服务、模型监控

**核心能力**:
- 模型一键部署
- 高性能推理服务
- 模型版本管理与灰度发布
- 推理性能监控
- 负载均衡与自动扩缩容

**技术栈**: Go/Gin + TorchServe/TensorFlow Serving + Kubernetes

**使用方式**:
```bash
python3 scripts/init.py my-project --business-agents=model-service
```

---

## 组合使用

可以同时选择多个业务 Agent：

```bash
# AI 平台完整方案
python3 scripts/init.py my-ai-platform \
  --business-agents=compute,data,training,model-service

# 数据处理平台
python3 scripts/init.py my-data-platform \
  --business-agents=data

# 模型服务平台
python3 scripts/init.py my-model-platform \
  --business-agents=training,model-service
```

---

## 模板结构

每个业务 Agent 模板包含：

```
templates/business-agents/{agent-name}/
├── agent.md              # Agent 定义
├── config.json           # 配置文件
├── sub-agents/           # Sub-Agent 定义
│   ├── *.md
│   └── orchestrator.md
├── skills/               # 专属 Skills
│   └── *.md
├── backend/              # 后端代码模板
│   ├── api/
│   ├── models/
│   ├── services/
│   └── tests/
├── frontend/             # 前端代码模板（可选）
│   └── src/
└── deploy/               # 部署配置
    ├── docker-compose.yml
    └── k8s/
```

---

## 自定义业务 Agent

如需创建自定义业务 Agent：

1. 复制现有模板到 `templates/business-agents/my-agent/`
2. 修改 `agent.md` 和 `config.json`
3. 调整 sub-agents 和 skills
4. 更新代码模板
5. 在 `scripts/init.py` 中注册

---

## 注意事项

1. **按需选择**: 业务 Agent 不会默认携带，只在需要时推荐和创建
2. **独立部署**: 每个业务 Agent 可以独立部署和扩展
3. **技术栈**: 根据性能需求选择合适的技术栈（Python/Go）
4. **数据隔离**: 业务 Agent 之间数据隔离，通过 API 通信
5. **监控集成**: 所有业务 Agent 自动集成 Monitoring Agent

---

## 参考案例

完整的业务 Agent 实现参考：
- `examples/model-platform/` - AI 大模型管理平台（包含所有 4 个业务 Agent）
