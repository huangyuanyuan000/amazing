# 运营人员约束规则

## 概述

本文档定义运营人员在执行数据分析、配置管理、用户运营等工作时必须遵守的约束规则，确保数据安全、配置可靠、操作合规。

## 数据权限约束

### 1. 数据访问权限

#### 可访问的数据
- **用户行为数据**: 访问日志、点击流数据、事件追踪数据
- **业务指标数据**: DAU/MAU、转化率、GMV、留存率等聚合指标
- **内容数据**: 文章、商品、活动等内容信息
- **配置数据**: 运营配置、系统配置（只读）
- **日志数据**: 应用日志、业务日志（脱敏后）

#### 禁止访问的数据
- **用户敏感信息**: 密码、支付密码、银行卡号、身份证号
- **财务敏感数据**: 完整的交易流水、财务报表
- **系统敏感信息**: 数据库密码、API 密钥、加密密钥
- **其他用户的私密数据**: 聊天记录、私信内容

### 2. 数据查询约束

#### 查询频率限制
```yaml
query_limits:
  # 单次查询
  max_rows_per_query: 100000        # 单次查询最多返回 10 万行
  max_query_time: 300               # 单次查询最长 5 分钟

  # 频率限制
  max_queries_per_hour: 50          # 每小时最多 50 次查询
  max_queries_per_day: 200          # 每天最多 200 次查询

  # 并发限制
  max_concurrent_queries: 3         # 最多 3 个并发查询
```

#### 查询范围限制
- **时间范围**: 单次查询时间范围不超过 90 天
- **数据量**: 单次查询数据量不超过 10 万行
- **表访问**: 只能访问授权的数据表
- **字段访问**: 敏感字段自动脱敏或隐藏

#### 禁止的查询操作
```sql
-- 禁止：修改数据
UPDATE users SET ...;
DELETE FROM orders WHERE ...;
INSERT INTO products ...;

-- 禁止：删除表或数据库
DROP TABLE users;
DROP DATABASE production;

-- 禁止：修改表结构
ALTER TABLE users ADD COLUMN ...;

-- 禁止：查询敏感字段
SELECT password, credit_card FROM users;

-- 禁止：全表扫描（无 WHERE 条件的大表查询）
SELECT * FROM orders;  -- orders 表超过 100 万行

-- 禁止：跨库查询
SELECT * FROM other_database.users;
```

### 3. 数据导出约束

#### 导出审批流程
```yaml
export_approval:
  # 小数据量（< 1000 行）
  small_data:
    approval_required: false
    auto_approve: true

  # 中等数据量（1000-10000 行）
  medium_data:
    approval_required: true
    approver: [team_leader]
    max_wait_time: 2h

  # 大数据量（> 10000 行）
  large_data:
    approval_required: true
    approver: [team_leader, data_security_officer]
    max_wait_time: 24h
    reason_required: true
```

#### 导出数据处理
- **自动脱敏**: 导出数据自动脱敏敏感字段
- **水印标记**: 导出文件添加水印和导出人信息
- **有效期限**: 导出数据有效期 7 天，过期自动删除
- **传输加密**: 导出文件必须加密传输
- **存储限制**: 导出数据不得存储在个人设备

### 4. 数据使用约束

#### 数据用途限制
- **仅限内部使用**: 数据仅用于内部分析和运营
- **禁止外传**: 不得将数据提供给第三方
- **禁止商业化**: 不得将数据用于商业交易
- **禁止个人用途**: 不得将数据用于个人目的

#### 数据保护要求
- **本地存储**: 本地数据必须加密存储
- **定期清理**: 定期清理本地数据（每月一次）
- **离职交接**: 离职时必须删除所有本地数据
- **泄露报告**: 发现数据泄露立即报告

## 配置管理约束

### 1. 配置变更权限

#### 可变更的配置
```yaml
allowed_configs:
  # 运营配置
  - config/operations/activities.yml      # 活动配置
  - config/operations/banners.yml         # Banner 配置
  - config/operations/popups.yml          # 弹窗配置
  - config/operations/recommendations.yml # 推荐位配置

  # 内容管理
  - content/announcements/                # 公告内容
  - content/help/                         # 帮助文档
  - content/marketing/                    # 营销内容

  # 规则配置
  - config/rules/points.yml               # 积分规则
  - config/rules/levels.yml               # 等级规则
  - config/rules/rewards.yml              # 奖励规则
```

#### 禁止变更的配置
```yaml
forbidden_configs:
  # 系统配置
  - config/database.yml                   # 数据库配置
  - config/redis.yml                      # Redis 配置
  - config/security.yml                   # 安全配置

  # 应用配置
  - config/application.yml                # 应用配置
  - config/services.yml                   # 服务配置

  # 部署配置
  - deploy/                               # 所有部署配置
  - docker-compose.yml                    # Docker 配置
  - k8s/                                  # K8s 配置
```

### 2. 配置变更流程

#### 变更审批矩阵
```yaml
approval_matrix:
  # 低风险配置（内容更新）
  low_risk:
    examples: [公告内容, 帮助文档, Banner 图片]
    approval_required: false
    auto_deploy: true

  # 中风险配置（活动配置）
  medium_risk:
    examples: [活动配置, 推荐位配置, 弹窗配置]
    approval_required: true
    approver: [product_manager]
    test_required: true

  # 高风险配置（规则配置）
  high_risk:
    examples: [积分规则, 等级规则, 算法参数]
    approval_required: true
    approver: [product_manager, architect]
    test_required: true
    gray_release: true
```

#### 变更执行步骤
```yaml
change_process:
  1_submit:
    action: 提交变更申请
    required_info:
      - change_description: 变更描述
      - change_reason: 变更原因
      - expected_impact: 预期影响
      - rollback_plan: 回滚方案

  2_review:
    action: 审批
    reviewer: [product_manager, architect]
    review_points:
      - 变更必要性
      - 变更风险评估
      - 回滚方案可行性

  3_test:
    action: 测试环境验证
    test_cases:
      - 功能测试
      - 兼容性测试
      - 性能测试
    approval_required: true

  4_deploy:
    action: 生产环境发布
    strategy: [direct, gray_release, blue_green]
    monitoring: 实时监控关键指标

  5_verify:
    action: 效果验证
    duration: 24h
    rollback_if: 出现异常指标

  6_document:
    action: 变更记录
    required_info:
      - 变更时间
      - 变更内容
      - 变更结果
      - 经验总结
```

### 3. 配置质量约束

#### 配置格式要求
```yaml
config_format:
  # 文件格式
  format: [yaml, json]
  encoding: utf-8

  # 命名规范
  naming:
    file: kebab-case          # activity-config.yml
    key: snake_case           # activity_name

  # 结构要求
  structure:
    - 必须有注释说明
    - 必须有版本号
    - 必须有更新时间
    - 必须有更新人
```

#### 配置验证规则
```yaml
validation_rules:
  # 必填字段验证
  required_fields:
    - id
    - name
    - status
    - start_time
    - end_time

  # 数据类型验证
  type_validation:
    id: string
    name: string
    status: enum[active, inactive, draft]
    start_time: datetime
    end_time: datetime

  # 业务规则验证
  business_rules:
    - end_time > start_time
    - discount_rate >= 0 and discount_rate <= 100
    - max_participants > 0
```

### 4. 配置回滚约束

#### 回滚触发条件
```yaml
rollback_triggers:
  # 自动回滚
  auto_rollback:
    - error_rate > 5%              # 错误率超过 5%
    - response_time > 3s           # 响应时间超过 3 秒
    - crash_rate > 1%              # 崩溃率超过 1%
    - user_complaints > 10         # 用户投诉超过 10 次

  # 手动回滚
  manual_rollback:
    - 业务指标异常下降
    - 用户体验明显变差
    - 发现配置错误
```

#### 回滚执行要求
- **快速回滚**: 回滚操作必须在 5 分钟内完成
- **验证回滚**: 回滚后验证系统恢复正常
- **记录原因**: 记录回滚原因和经验教训
- **问题修复**: 修复问题后重新发布

## 安全约束

### 1. 数据安全

#### 敏感数据处理
```yaml
sensitive_data_handling:
  # 自动脱敏规则
  masking_rules:
    phone: "138****1234"           # 手机号脱敏
    email: "u***@example.com"      # 邮箱脱敏
    id_card: "110***********123"   # 身份证脱敏
    bank_card: "6222 **** **** 1234" # 银行卡脱敏

  # 禁止操作
  forbidden_operations:
    - 截图包含敏感数据
    - 复制敏感数据到剪贴板
    - 将敏感数据发送到外部系统
    - 在公共场所查看敏感数据
```

#### 数据访问审计
```yaml
audit_logging:
  # 记录所有数据访问
  log_events:
    - 查询执行（SQL、时间、结果行数）
    - 数据导出（文件名、行数、导出时间）
    - 配置变更（变更内容、变更时间）
    - 异常操作（失败查询、权限拒绝）

  # 审计日志保留
  retention:
    duration: 180d                 # 保留 180 天
    storage: secure_storage        # 安全存储
    access: [security_officer, auditor]
```

### 2. 权限安全

#### 最小权限原则
- **按需授权**: 只授予完成工作所需的最小权限
- **定期审查**: 每季度审查一次权限
- **及时回收**: 角色变更或离职时立即回收权限
- **权限分离**: 查询权限和配置权限分离

#### 权限申请流程
```yaml
permission_request:
  1_submit:
    action: 提交权限申请
    required_info:
      - 申请的权限
      - 申请原因
      - 使用期限

  2_approve:
    action: 审批
    approver: [team_leader, data_security_officer]
    review_points:
      - 权限必要性
      - 权限范围合理性
      - 安全风险评估

  3_grant:
    action: 授予权限
    duration: 临时权限最长 30 天
    notification: 通知申请人和安全团队

  4_review:
    action: 定期审查
    frequency: 每季度一次
    action_if_unused: 回收未使用的权限
```

### 3. 操作安全

#### 操作规范
```yaml
operation_standards:
  # 生产环境操作
  production_operations:
    - 必须在工作时间（9:00-18:00）操作
    - 重要操作必须双人复核
    - 操作前必须备份
    - 操作后必须验证

  # 禁止操作
  forbidden_operations:
    - 在生产环境直接修改数据
    - 执行未经测试的配置
    - 批量操作未经审批
    - 在非工作时间进行高风险操作
```

#### 异常处理
```yaml
incident_handling:
  # 发现异常
  detection:
    - 监控告警
    - 用户反馈
    - 数据异常

  # 响应流程
  response:
    1_report:
      action: 立即报告
      notify: [team_leader, on_call_engineer]
      sla: 5 分钟内

    2_assess:
      action: 评估影响
      check: [影响范围, 严重程度, 用户数量]

    3_mitigate:
      action: 缓解措施
      options: [回滚配置, 降级功能, 紧急修复]

    4_resolve:
      action: 彻底解决
      verify: 验证问题已解决

    5_postmortem:
      action: 复盘总结
      output: 事故报告和改进措施
```

## 时间约束

### 1. 响应时间

#### 数据需求响应
```yaml
response_time:
  # 紧急需求
  urgent:
    definition: 影响核心业务决策
    response_time: 1h
    completion_time: 4h

  # 重要需求
  important:
    definition: 影响运营策略制定
    response_time: 2h
    completion_time: 1d

  # 普通需求
  normal:
    definition: 常规数据分析
    response_time: 4h
    completion_time: 3d

  # 低优先级需求
  low:
    definition: 探索性分析
    response_time: 1d
    completion_time: 1w
```

#### 配置变更响应
```yaml
change_response:
  # 紧急变更
  emergency:
    definition: 修复线上问题
    approval_time: 30min
    execution_time: 1h

  # 常规变更
  regular:
    definition: 计划内的配置变更
    approval_time: 4h
    execution_time: 1d

  # 优化变更
  optimization:
    definition: 非紧急的优化调整
    approval_time: 1d
    execution_time: 3d
```

### 2. 执行时间窗口

#### 配置变更时间窗口
```yaml
change_windows:
  # 低风险变更
  low_risk:
    allowed_time: 任何时间
    notification: 不需要

  # 中风险变更
  medium_risk:
    allowed_time: 工作日 10:00-17:00
    notification: 提前 1 小时通知

  # 高风险变更
  high_risk:
    allowed_time: 工作日 14:00-16:00
    notification: 提前 1 天通知
    on_call: 必须有开发人员 on-call
```

#### 禁止操作时间
```yaml
forbidden_windows:
  # 业务高峰期
  peak_hours:
    time: [10:00-12:00, 20:00-22:00]
    forbidden: 高风险配置变更

  # 重大活动期间
  major_events:
    examples: [双十一, 618, 春节]
    forbidden: 所有非紧急变更

  # 非工作时间
  off_hours:
    time: [18:00-09:00, 周末, 节假日]
    forbidden: 非紧急变更
    exception: 紧急修复需要审批
```

## 质量约束

### 1. 数据分析质量

#### 准确性要求
```yaml
accuracy_requirements:
  # 数据准确性
  data_accuracy:
    target: 99%
    validation: 交叉验证、数据对账

  # 计算准确性
  calculation_accuracy:
    target: 100%
    validation: 公式审查、结果复核

  # 结论准确性
    target: 95%
    validation: 同行评审、专家审查
```

#### 完整性要求
```yaml
completeness_requirements:
  # 数据完整性
  data_completeness:
    - 数据来源明确
    - 数据范围清晰
    - 缺失数据说明

  # 分析完整性
  analysis_completeness:
    - 分析目标明确
    - 分析方法合理
    - 分析结论清晰
    - 行动建议具体
```

### 2. 配置质量

#### 配置正确性
```yaml
config_correctness:
  # 语法正确
  syntax:
    - YAML/JSON 格式正确
    - 无语法错误
    - 通过 lint 检查

  # 逻辑正确
  logic:
    - 业务逻辑正确
    - 时间逻辑合理
    - 数值范围合理

  # 兼容性
  compatibility:
    - 向后兼容
    - 跨平台兼容
    - 版本兼容
```

#### 配置可维护性
```yaml
config_maintainability:
  # 文档完整
  documentation:
    - 配置说明清晰
    - 字段含义明确
    - 示例完整

  # 结构清晰
  structure:
    - 层次分明
    - 命名规范
    - 易于理解

  # 版本管理
  versioning:
    - 版本号规范
    - 变更记录完整
    - 可追溯历史
```

### 3. 报告质量

#### 报告标准
```yaml
report_standards:
  # 内容要求
  content:
    - 目标明确
    - 数据准确
    - 分析深入
    - 结论清晰
    - 建议可行

  # 格式要求
  format:
    - 结构清晰
    - 图表美观
    - 排版规范
    - 易于阅读

  # 时效要求
  timeliness:
    - 按时交付
    - 数据最新
    - 结论及时
```

## 违规处理

### 1. 违规分类

#### 轻微违规
- **定义**: 无意的小错误，未造成实际影响
- **示例**: 查询超时、配置格式错误
- **处理**: 口头提醒、记录警告

#### 一般违规
- **定义**: 违反操作规范，造成轻微影响
- **示例**: 未经审批的配置变更、数据导出未脱敏
- **处理**: 书面警告、暂停权限 1 周

#### 严重违规
- **定义**: 严重违反安全规范，造成重大影响
- **示例**: 泄露用户数据、恶意修改配置
- **处理**: 撤销权限、纪律处分

### 2. 违规记录

所有违规行为都会被记录，并影响权限审查和绩效评估。

```yaml
violation_record:
  record_info:
    - 违规时间
    - 违��类型
    - 违规内容
    - 影响范围
    - 处理结果

  retention: 永久保留
  review: 每季度审查一次
```

## 总结

运营人员必须严格遵守以上约束规则，确保：
1. **数据安全**: 保护用户隐私，防止数据泄露
2. **配置可靠**: 配置变更经过审批和测试
3. **操作合规**: 所有操作符合规范和流程
4. **质量保证**: 数据分析和配置管理高质量
5. **风险可控**: 及时发现和处理异常情况

违反约束规则将受到相应处理，严重违规将撤销权限。
