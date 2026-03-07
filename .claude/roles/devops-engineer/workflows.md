# 运维工程师专属工作流

## 1. 部署工作流

### 1.1 常规部署流程

```yaml
workflow: regular-deployment
trigger: deployment_request
owner: devops-engineer

steps:
  - name: 接收部署请求
    actor: devops-engineer
    inputs:
      - 部署环境（dev/staging/production）
      - 部署版本号
      - 变更说明
      - 影响范围
    actions:
      - 检查部署请求完整性
      - 确认部署时间窗口
      - 评估部署风险
    outputs:
      - 部署计划文档

  - name: 部署准备
    actor: devops-engineer
    actions:
      - 备份当前版本配置
      - 备份数据库（如有变更）
      - 准备回滚脚本
      - 检查资源容量
      - 通知相关团队
    checks:
      - 备份完成且可恢复
      - 回滚脚本已测试
      - 资源容量充足
    outputs:
      - 备份文件
      - 回滚脚本

  - name: 配置检查
    actor: devops-engineer
    actions:
      - 验证配置文件语法
      - 检查环境变量
      - 验证密钥和证书
      - 检查依赖服务状态
      - 验证网络连通性
    checks:
      - 所有配置文件有效
      - 密钥未过期
      - 依赖服务正常
    outputs:
      - 配置检查报告

  - name: 执行部署
    actor: devops-engineer
    condition:
      - 配置检查通过
      - 在部署时间窗口内
      - 已获得审批（生产环境）
    actions:
      - 拉取新版本镜像/代码
      - 更新配置文件
      - 执行数据库迁移（如需要）
      - 滚动更新服务
      - 等待服务启动
    monitoring:
      - 实时监控部署进度
      - 监控错误日志
      - 监控资源使用
    rollback_trigger:
      - 启动失败率 > 10%
      - 错误率突增
      - 响应时间超时

  - name: 健康检查
    actor: devops-engineer
    actions:
      - 检查服务健康状态
      - 验证 API 端点可用性
      - 检查数据库连接
      - 验证依赖服务连接
      - 检查日志输出
    checks:
      - 所有实例健康
      - API 响应正常
      - 无错误日志
    timeout: 5分钟

  - name: 烟雾测试
    actor: devops-engineer
    actions:
      - 执行核心功能测试
      - 验证关键业务流程
      - 检查数据一致性
      - 验证监控指标
    checks:
      - 核心功能正常
      - 业务流程通畅
      - 监控指标正常
    timeout: 10分钟

  - name: 监控观察
    actor: devops-engineer
    duration: 30分钟
    actions:
      - 持续监控系统指标
      - 观察错误率变化
      - 监控响应时间
      - 检查资源使用
      - 收集用户反馈
    alert_on:
      - 错误率 > 0.1%
      - 响应时间 P99 > 500ms
      - CPU/内存使用 > 90%

  - name: 部署确认
    actor: devops-engineer
    condition: 监控观察期无异常
    actions:
      - 标记部署成功
      - 更新部署记录
      - 通知相关团队
      - 归档部署文档
    outputs:
      - 部署报告
      - 部署记录

  - name: 回滚处理
    actor: devops-engineer
    condition: 部署失败或监控异常
    actions:
      - 立即执行回滚脚本
      - 恢复配置文件
      - 恢复数据库（如需要）
      - 验证回滚结果
      - 通知相关团队
      - 记录失败原因
    outputs:
      - 回滚报告
      - 失败分析报告
```

### 1.2 灰度发布流程

```yaml
workflow: canary-deployment
trigger: canary_deployment_request
owner: devops-engineer

steps:
  - name: 灰度准备
    actor: devops-engineer
    actions:
      - 确定灰度策略（5% → 25% → 50% → 100%）
      - 准备灰度配置
      - 配置流量分发规则
      - 设置监控指标
    outputs:
      - 灰度发布计划

  - name: 第一阶段（5%）
    actor: devops-engineer
    actions:
      - 部署到 5% 实例
      - 配置流量分发到 5%
      - 监控 30 分钟
    checks:
      - 错误率无异常
      - 响应时间正常
      - 无用户投诉
    rollback_on_failure: true

  - name: 第二阶段（25%）
    actor: devops-engineer
    condition: 第一阶段成功
    actions:
      - 扩大到 25% 实例
      - 调整流量分发到 25%
      - 监控 30 分钟
    checks:
      - 错误率 < 0.1%
      - 响应时间 P99 < 500ms
    rollback_on_failure: true

  - name: 第三阶段（50%）
    actor: devops-engineer
    condition: 第二阶段成功
    actions:
      - 扩大到 50% 实例
      - 调整流量分发到 50%
      - 监控 1 小时
    checks:
      - 系统稳定
      - 业务指标正常
    rollback_on_failure: true

  - name: 全量发布（100%）
    actor: devops-engineer
    condition: 第三阶段成功
    actions:
      - 部署到所有实例
      - 流量全部切换
      - 监控 2 小时
      - 清理旧版本
    outputs:
      - 灰度发布报告
```

### 1.3 蓝绿部署流程

```yaml
workflow: blue-green-deployment
trigger: blue_green_deployment_request
owner: devops-engineer

steps:
  - name: 准备绿色环境
    actor: devops-engineer
    actions:
      - 创建绿色环境（与蓝色环境相同配置）
      - 部署新版本到绿色环境
      - 配置数据库连接
      - 预热缓存
    checks:
      - 绿色环境健康
      - 配置正确
      - 缓存预热完成

  - name: 绿色环境测试
    actor: devops-engineer
    actions:
      - 执行健康检查
      - 运行烟雾测试
      - 验证核心功能
      - 性能测试
    checks:
      - 所有测试通过
      - 性能满足要求

  - name: 流量切换
    actor: devops-engineer
    condition: 绿色环境测试通过
    actions:
      - 将负载均衡器指向绿色环境
      - 监控流量切换过程
      - 验证用户请求正常
    duration: 5分钟

  - name: 监控验证
    actor: devops-engineer
    duration: 1小时
    actions:
      - 监控绿色环境指标
      - 对比蓝绿环境指标
      - 收集用户反馈
    alert_on:
      - 错误率异常
      - 响应时间异常
      - 资源使用异常

  - name: 清理蓝色环境
    actor: devops-engineer
    condition: 绿色环境稳定运行
    actions:
      - 保留蓝色环境 24 小时（用于快速回滚）
      - 24 小时后清理蓝色环境资源
    outputs:
      - 蓝绿部署报告

  - name: 快速回滚
    actor: devops-engineer
    condition: 绿色环境异常
    actions:
      - 立即将流量切回蓝色环境
      - 验证蓝色环境正常
      - 分析绿色环境问题
    outputs:
      - 回滚报告
```

## 2. 监控配置工作流

### 2.1 监控系统部署流程

```yaml
workflow: monitoring-setup
trigger: new_service_deployment
owner: devops-engineer

steps:
  - name: 指标定义
    actor: devops-engineer
    collaborate_with: [architect, backend-dev]
    actions:
      - 定义系统指标（CPU、内存、磁盘、网络）
      - 定义应用指标（QPS、响应时间、错误率）
      - 定义业务指标（订单量、用户数等）
      - 确定指标采集频率
    outputs:
      - 指标定义文档
      - monitoring/metrics.yml

  - name: 配置 Prometheus
    actor: devops-engineer
    actions:
      - 配置 Prometheus 抓取规则
      - 配置服务发现
      - 配置数据保留策略
      - 部署 Prometheus
    outputs:
      - monitoring/prometheus/prometheus.yml
      - monitoring/prometheus/rules/*.yml

  - name: 配置告警规则
    actor: devops-engineer
    actions:
      - 定义告警阈值
      - 配置告警分级（P0/P1/P2/P3）
      - 配置告警通知渠道
      - 配置告警抑制规则
      - 配置告警聚合规则
    outputs:
      - monitoring/alertmanager/alertmanager.yml
      - monitoring/prometheus/alerts/*.yml

  - name: 创建 Grafana 仪表盘
    actor: devops-engineer
    actions:
      - 创建系统监控仪表盘
      - 创建应用监控仪表盘
      - 创建业务监控仪表盘
      - 配置仪表盘权限
      - 配置仪表盘变量
    outputs:
      - monitoring/grafana/dashboards/*.json

  - name: 配置日志聚合
    actor: devops-engineer
    actions:
      - 部署 Loki
      - 配置日志采集规则
      - 配置日志解析规则
      - 配置日志保留策略
      - 集成到 Grafana
    outputs:
      - monitoring/loki/loki.yml
      - monitoring/promtail/promtail.yml

  - name: 配置链路追踪
    actor: devops-engineer
    actions:
      - 部署 Jaeger
      - 配置采样策略
      - 配置存储后端
      - 集成到应用
    outputs:
      - monitoring/jaeger/jaeger.yml

  - name: 测试验证
    actor: devops-engineer
    actions:
      - 验证指标采集正常
      - 触发测试告警
      - 验证告警通知正常
      - 验证仪表盘显示正常
      - 验证日志查询正常
    checks:
      - 所有指标正常采集
      - 告警正常触发和通知
      - 仪表盘数据正确

  - name: 文档输出
    actor: devops-engineer
    actions:
      - 编写监控使用文档
      - 编写告警处理手册
      - 编写故障排查指南
    outputs:
      - docs/operations/monitoring-guide.md
      - docs/operations/alert-handbook.md
```

### 2.2 告警优化流程

```yaml
workflow: alert-optimization
trigger: alert_fatigue_detected
owner: devops-engineer

steps:
  - name: 告警分析
    actor: devops-engineer
    duration: 1周
    actions:
      - 统计告警频率
      - 分析误报原因
      - 识别告警疲劳源
      - 评估告警价值
    outputs:
      - 告警分析报告

  - name: 阈值调整
    actor: devops-engineer
    actions:
      - 调整不合理的阈值
      - 增加告警条件
      - 配置告警抑制
      - 配置告警聚合
    outputs:
      - 优化后的告警规则

  - name: 测试验证
    actor: devops-engineer
    duration: 1周
    actions:
      - 观察告警触发情况
      - 收集团队反馈
      - 评估优化效果
    metrics:
      - 告警数量减少 > 50%
      - 误报率 < 5%
      - 漏报率 < 1%

  - name: 持续优化
    actor: devops-engineer
    frequency: 每月
    actions:
      - 定期审查告警规则
      - 根据反馈持续优化
      - 更新告警文档
```

## 3. 故障排查工作流

### 3.1 故障响应流程

```yaml
workflow: incident-response
trigger: alert_triggered
owner: devops-engineer

steps:
  - name: 接收告警
    actor: devops-engineer
    response_time:
      - P0: 5分钟
      - P1: 15分钟
      - P2: 1小时
      - P3: 4小时
    actions:
      - 确认告警信息
      - 评估影响范围
      - 确定故障级别
      - 通知相关人员

  - name: 快速评估
    actor: devops-engineer
    duration: 5分钟
    actions:
      - 检查监控仪表盘
      - 查看错误日志
      - 检查最近变更
      - 评估影响范围
    outputs:
      - 初步评估报告

  - name: 紧急处理
    actor: devops-engineer
    condition: P0/P1 故障
    actions:
      - 执行应急预案
      - 回滚最近变更（如适用）
      - 扩容资源（如需要）
      - 切换备用系统（如需要）
      - 降级非核心功能（如需要）
    goal: 尽快恢复服务

  - name: 根因分析
    actor: devops-engineer
    actions:
      - 分析错误日志
      - 分析监控指标
      - 检查链路追踪
      - 复现问题（如可能）
      - 定位故障根因
    outputs:
      - 根因分析报告

  - name: 修复实施
    actor: devops-engineer
    collaborate_with: [backend-dev, frontend-dev]
    actions:
      - 制定修复方案
      - 实施修复措施
      - 验证修复效果
      - 监控系统状态
    checks:
      - 故障已解决
      - 系统恢复正常
      - 无新问题引入

  - name: 验证恢复
    actor: devops-engineer
    duration: 30分钟
    actions:
      - 验证服务健康
      - 检查监控指标
      - 验证业务功能
      - 收集用户反馈
    checks:
      - 所有指标正常
      - 用户反馈正常

  - name: 故障复盘
    actor: devops-engineer
    collaborate_with: [architect, product-manager]
    timing: 故障解决后 24 小时内
    actions:
      - 编写故障报告
      - 分析故障原因
      - 总结经验教训
      - 制定改进措施
      - 更新应急预案
    outputs:
      - docs/operations/incident-reports/{date}-{incident}.md
      - 改进措施清单

  - name: 改进实施
    actor: devops-engineer
    actions:
      - 实施改进措施
      - 完善监控告警
      - 优化应急预案
      - 加强预防措施
    tracking: 改进措施跟踪表
```

### 3.2 性能问题排查流程

```yaml
workflow: performance-troubleshooting
trigger: performance_degradation
owner: devops-engineer

steps:
  - name: 问题确认
    actor: devops-engineer
    actions:
      - 确认性能指标异常
      - 对比历史数据
      - 确定影响范围
      - 评估严重程度

  - name: 数据收集
    actor: devops-engineer
    actions:
      - 收集监控指标
      - 收集应用日志
      - 收集链路追踪数据
      - 收集系统资源使用情况
      - 收集数据库慢查询日志

  - name: 瓶颈定位
    actor: devops-engineer
    actions:
      - 分析 CPU 使用情况
      - 分析内存使用情况
      - 分析磁盘 I/O
      - 分析网络带宽
      - 分析数据库性能
      - 分析应用代码性能
    outputs:
      - 性能瓶颈分析报告

  - name: 优化方案
    actor: devops-engineer
    collaborate_with: [architect, backend-dev]
    actions:
      - 制定优化方案
      - 评估优化效果
      - 评估优化风险
      - 制定实施计划

  - name: 优化实施
    actor: devops-engineer
    actions:
      - 实施优化措施
      - 监控优化效果
      - 对比优化前后数据
      - 验证无副作用

  - name: 效果验证
    actor: devops-engineer
    duration: 1周
    actions:
      - 持续监控性能指标
      - 收集用户反馈
      - 评估优化效果
    outputs:
      - 性能优化报告
```

## 4. 基础设施管理工作流

### 4.1 Kubernetes 集群管理流程

```yaml
workflow: k8s-cluster-management
trigger: cluster_management_task
owner: devops-engineer

steps:
  - name: 集群健康检查
    actor: devops-engineer
    frequency: 每天
    actions:
      - 检查节点状态
      - 检查 Pod 状态
      - 检查资源使用
      - 检查事件日志
      - 检查证书有效期
    outputs:
      - 集群健康报告

  - name: 资源规划
    actor: devops-engineer
    frequency: 每月
    actions:
      - 分析资源使用趋势
      - 预测未来资源需求
      - 规划节点扩容
      - 优化资源分配
    outputs:
      - 资源规划报告

  - name: 集群升级
    actor: devops-engineer
    frequency: 每季度
    actions:
      - 评估升级必要性
      - 制定升级计划
      - 备份集群配置
      - 在测试环境验证
      - 执行生产环境升级
      - 验证升级结果
    outputs:
      - 集群升级报告

  - name: 安全加固
    actor: devops-engineer
    frequency: 每月
    actions:
      - 审查 RBAC 配置
      - 审查网络策略
      - 审查 Pod 安全策略
      - 扫描安全漏洞
      - 实施安全加固措施
    outputs:
      - 安全加固报告
```

### 4.2 基础设施即代码管理流程

```yaml
workflow: infrastructure-as-code
trigger: infrastructure_change
owner: devops-engineer

steps:
  - name: 需求分析
    actor: devops-engineer
    collaborate_with: architect
    actions:
      - 理解基础设施需求
      - 评估技术方案
      - 确定实施范围

  - name: 代码编写
    actor: devops-engineer
    actions:
      - 编写 Terraform 配置
      - 编写 Ansible Playbook
      - 配置变量和密钥
      - 编写文档
    outputs:
      - infrastructure/terraform/*.tf
      - infrastructure/ansible/*.yml

  - name: 代码审查
    actor: architect
    actions:
      - 审查代码质量
      - 审查安全配置
      - 审查成本影响
      - 提出改进建议

  - name: 测试验证
    actor: devops-engineer
    actions:
      - 在测试环境执行
      - 验证资源创建正确
      - 验证配置正确
      - 验证幂等性
    checks:
      - 所有资源创建成功
      - 配置符合预期
      - 可重复执行

  - name: 生产部署
    actor: devops-engineer
    condition: 测试通过且已审批
    actions:
      - 执行 Terraform apply
      - 执行 Ansible playbook
      - 验证部署结果
      - 更新文档
    outputs:
      - 基础设施变更报告

  - name: 状态管理
    actor: devops-engineer
    actions:
      - 备份 Terraform state
      - 版本控制配置文件
      - 记录变更历史
```

## 5. CI/CD 管道工作流

### 5.1 CI/CD 流水线配置流程

```yaml
workflow: cicd-pipeline-setup
trigger: new_project_setup
owner: devops-engineer

steps:
  - name: 需求分析
    actor: devops-engineer
    collaborate_with: [architect, backend-dev, frontend-dev]
    actions:
      - 了解项目技术栈
      - 确定构建流程
      - 确定测试策略
      - 确定部署策略

  - name: 流水线设计
    actor: devops-engineer
    actions:
      - 设计构建阶段
      - 设计测试阶段
      - 设计部署阶段
      - 设计审批流程
      - 设计通知机制
    outputs:
      - CI/CD 流水线设计文档

  - name: 流水线实现
    actor: devops-engineer
    actions:
      - 编写 GitHub Actions 工作流
      - 配置构建环境
      - 集成自动化测试
      - 配置部署脚本
      - 配置通知
    outputs:
      - .github/workflows/*.yml

  - name: 测试验证
    actor: devops-engineer
    actions:
      - 触发测试构建
      - 验证构建成功
      - 验证测试执行
      - 验证部署流程
      - 验证通知正常

  - name: 文档输出
    actor: devops-engineer
    actions:
      - 编写 CI/CD 使用文档
      - 编写故障排查指南
    outputs:
      - docs/operations/cicd-guide.md

  - name: 持续优化
    actor: devops-engineer
    frequency: 每月
    actions:
      - 分析流水线性能
      - 优化构建速度
      - 优化资源使用
      - 改进用户体验
```

## 6. 容量规划工作流

```yaml
workflow: capacity-planning
trigger: monthly_review
owner: devops-engineer
frequency: 每月

steps:
  - name: 数据收集
    actor: devops-engineer
    duration: 1周
    actions:
      - 收集资源使用数据
      - 收集业务增长数据
      - 收集性能指标数据
      - 收集成本数据

  - name: 趋势分析
    actor: devops-engineer
    actions:
      - 分析资源使用趋势
      - 分析业务增长趋势
      - 预测未来需求
      - 识别潜在瓶颈

  - name: 容量规划
    actor: devops-engineer
    collaborate_with: architect
    actions:
      - 制定扩容计划
      - 评估成本影响
      - 制定实施时间表
      - 制定风险应对措施
    outputs:
      - 容量规划报告

  - name: 审批执行
    actor: architect
    actions:
      - 审批容量规划
      - 批准预算
      - 授权执行

  - name: 实施跟踪
    actor: devops-engineer
    actions:
      - 执行扩容计划
      - 跟踪实施进度
      - 验证扩容效果
      - 更新容量记录
```

## 7. 成本优化工作流

```yaml
workflow: cost-optimization
trigger: monthly_cost_review
owner: devops-engineer
frequency: 每月

steps:
  - name: 成本分析
    actor: devops-engineer
    actions:
      - 收集成本数据
      - 分析成本构成
      - 识别成本浪费
      - 对比预算

  - name: 优化方案
    actor: devops-engineer
    actions:
      - 识别闲置资源
      - 评估预留实例
      - 评估 Spot 实例
      - 评估自动扩缩容
      - 评估存储优化
    outputs:
      - 成本优化方案

  - name: 实施优化
    actor: devops-engineer
    actions:
      - 清理闲置资源
      - 购买预留实例
      - 配置自动扩缩容
      - 优化存储策略
      - 监控优化效果

  - name: 效果评估
    actor: devops-engineer
    duration: 1个月
    actions:
      - 对比优化前后成本
      - 评估优化效果
      - 总结经验教训
    outputs:
      - 成本优化报告
```

## 工作流协作

### 与其他角色的协作

- **架构师**: 审批重大变更、技术决策、容量规划
- **开发团队**: 协助部署、故障排查、性能优化
- **测试团队**: 配合测试环境、提供日志支持
- **产品团队**: 汇报系统状态、评估部署风险

### 工作流触发方式

- **定时触发**: 日常巡检、容量规划、成本优化
- **事件触发**: 告警响应、部署请求、故障处理
- **手动触发**: 紧急部署、应急响应、特殊操作

### 工作流监控

- 所有工作流执行必须记录日志
- 关键步骤必须有审批记录
- 异常情况必须有告警通知
- 定期审查工作流执行情况
