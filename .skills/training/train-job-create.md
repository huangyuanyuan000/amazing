# Skill: Train Job Create
# Version: 1.0.0
# Agent: training
# Tags: training, job, distributed

## 描述
创建模型训练任务模板，支持单机和分布式训练。

## 训练任务配置
```yaml
# training-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: ${JOB_NAME}
  labels:
    app: amazing-training
    job-type: training
spec:
  backoffLimit: 3
  template:
    spec:
      containers:
      - name: trainer
        image: ${REGISTRY}/trainer:${VERSION}
        command: ["python", "-m", "torch.distributed.launch"]
        args:
        - "--nproc_per_node=${GPU_PER_NODE}"
        - "--nnodes=${NUM_NODES}"
        - "train.py"
        - "--config=${CONFIG_PATH}"
        - "--output_dir=${OUTPUT_DIR}"
        resources:
          limits:
            nvidia.com/gpu: ${GPU_PER_NODE}
            memory: "${MEMORY}Gi"
          requests:
            nvidia.com/gpu: ${GPU_PER_NODE}
            memory: "${MEMORY}Gi"
        volumeMounts:
        - name: data
          mountPath: /data
        - name: output
          mountPath: /output
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: training-data-pvc
      - name: output
        persistentVolumeClaim:
          claimName: training-output-pvc
      restartPolicy: OnFailure
```

## Python 训练入口模板
```python
import torch
import torch.distributed as dist
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

def main():
    training_args = TrainingArguments(
        output_dir="./output",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=8,
        learning_rate=2e-5,
        num_train_epochs=3,
        fp16=True,
        deepspeed="./ds_config.json",
        logging_steps=10,
        save_steps=500,
        evaluation_strategy="steps",
        eval_steps=500,
    )

    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    trainer.train()

if __name__ == "__main__":
    main()
```
