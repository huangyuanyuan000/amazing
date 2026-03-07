# Data Analysis Skill - 数据分析方法

## 功能描述
提供数据分析方法论、报表生成模板和数据可视化方案。

## 触发方式
- 数据分析需求
- 报表生成
- 运营决策支持

## 核心内容

### 1. 分析流程
1. 明确分析目标 → 2. 数据收集 → 3. 数据清洗 → 4. 数据分析 → 5. 可视化 → 6. 结论

### 2. 常用分析维度
| 维度 | 指标 | SQL 示例 |
|------|------|----------|
| 用户 | DAU/MAU/留存 | `COUNT(DISTINCT user_id)` |
| 业务 | 转化率/客单价 | `SUM(amount)/COUNT(*)` |
| 性能 | 响应时间/错误率 | `AVG(duration)` |
| 增长 | 环比/同比 | `LAG() OVER()` |

### 3. 报表模板
```markdown
## {报表名称}
- 时间范围: {开始} ~ {结束}
- 核心指标:
  | 指标 | 本期 | 上期 | 环比 |
- 分析结论: {结论}
- 建议措施: {建议}
```

### 4. 数据可视化
| 图表类型 | 适用场景 |
|----------|----------|
| 折线图 | 趋势变化 |
| 柱状图 | 对比分析 |
| 饼图 | 占比分析 |
| 漏斗图 | 转化分析 |

## 示例
```sql
SELECT cohort_date,
  COUNT(DISTINCT CASE WHEN day_diff = 1 THEN user_id END)::float /
  COUNT(DISTINCT CASE WHEN day_diff = 0 THEN user_id END) AS day1_retention
FROM user_activity_cohort GROUP BY cohort_date;
```

## 进化能力
- 分析模板持续扩充
- 自动化报表生成
- 异常检测能力
