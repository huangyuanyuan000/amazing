# Skill: ETL Pipeline
# Version: 1.0.0
# Agent: data
# Tags: etl, pipeline, data-processing

## 描述
数据处理流水线生成模板。

## 流水线定义
```python
from dataclasses import dataclass
from typing import List, Callable, Any
from enum import Enum

class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

@dataclass
class PipelineStep:
    name: str
    func: Callable
    depends_on: List[str] = None
    status: StepStatus = StepStatus.PENDING
    retry_count: int = 3

class ETLPipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[PipelineStep] = []

    def add_step(self, step: PipelineStep):
        self.steps.append(step)
        return self

    async def run(self):
        for step in self._topological_sort():
            step.status = StepStatus.RUNNING
            for attempt in range(step.retry_count):
                try:
                    await step.func()
                    step.status = StepStatus.SUCCESS
                    break
                except Exception as e:
                    if attempt == step.retry_count - 1:
                        step.status = StepStatus.FAILED
                        raise
```

## 常用 ETL 模板
### 数据清洗
```python
async def clean_data(df):
    df = df.dropna(subset=["required_field"])
    df = df.drop_duplicates()
    df["text"] = df["text"].str.strip()
    return df
```

### 数据标注格式转换
```python
async def convert_annotation(input_path, output_path, format="jsonl"):
    # 支持 COCO / VOC / JSONL / CSV 格式互转
    pass
```
