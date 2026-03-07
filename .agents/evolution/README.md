# Evolution Agent - 进化能力

## 能力描述
提供变更影响分析、智能通知、自动更新等进化能力，确保系统持续优化。

## 核心功能

### 1. 影响分析
分析代码、配置、架构变更的影响范围。

#### 分析维度
- **代码层面**: 函数调用链、依赖关系
- **模块层面**: Agent/Sub-Agent 依赖
- **服务层面**: API 依赖、数据流
- **部署层面**: 配置变更影响

#### 分析结果
```json
{
  "change": "修改用户认证 API",
  "impact": {
    "agents": ["common", "model-service"],
    "roles": ["backend-dev", "frontend-dev", "test-engineer"],
    "services": ["backend-api", "frontend-app"],
    "tests": ["test_auth.py", "test_api.py"]
  }
}
```

### 2. 智能通知
根据影响分析结果，自动通知相关人员。

#### 通知规则
```yaml
rules:
  - trigger: api_change
    notify:
      - frontend-dev
      - test-engineer

  - trigger: database_schema_change
    notify:
      - backend-dev
      - devops-engineer
      - test-engineer

  - trigger: deployment_config_change
    notify:
      - devops-engineer

  - trigger: business_logic_change
    notify:
      - product-manager
      - test-engineer
```

#### 通知方式
- Claude Code 内通知
- Slack/钉钉/企业微信
- 邮件
- Git Issue/PR 评论

### 3. 自动更新
根据变更自动更新相关 Agent/Sub-Agent/Skill。

#### 更新策略
```yaml
auto_update:
  - source: common/auth
    targets:
      - model-service/auth
      - compute/auth
    strategy: sync  # 同步更新

  - source: database/schema
    targets:
      - all_agents
    strategy: notify  # 仅通知，手动更新
```

### 4. 依赖追踪
维护全链路依赖关系图。

#### 依赖类型
- **代码依赖**: 函数/类/模块调用
- **数据依赖**: 数据库表/字段依赖
- **服务依赖**: API 调用依赖
- **配置依赖**: 环境变量/配置文件依赖

## 使用方式

### 分析变更影响
```bash
python3 scripts/evolve.py analyze --change="修改用户认证 API"
```

### 查看依赖关系
```bash
python3 scripts/evolve.py deps --module=common/auth
```

### 执行自动更新
```bash
python3 scripts/evolve.py update --source=common/auth
```

## 配置示例

### 影响分析配置
```yaml
# .agents/evolution/config.yml
analysis:
  code:
    enabled: true
    depth: 3  # 分析深度

  module:
    enabled: true
    track_agents: true
    track_skills: true

  service:
    enabled: true
    track_api: true
    track_data_flow: true
```

### 通知配置
```yaml
# .agents/evolution/notify.yml
notifications:
  slack:
    enabled: true
    webhook: ${SLACK_WEBHOOK}
    channels:
      - dev-team
      - ops-team

  email:
    enabled: false

  claude_code:
    enabled: true
```

## 进化能力
- 学习历史变更模式
- 优化影响分析准确度
- 智能推荐更新策略
- 自动生成测试用例
