# Performance Test Skill - 性能测试方案

## 功能描述
提供性能测试方案设计、基准标准和压测工具配置。

## 触发方式
- 性能测试设计
- 上线前压测
- 性能优化验证

## 核心内容

### 1. 性能指标
| 指标 | 说明 | 目标 |
|------|------|------|
| QPS | 每秒请求数 | 根据业务定义 |
| P99 延迟 | 99% 请求延迟 | < 500ms |
| 错误率 | 请求失败比例 | < 0.1% |
| CPU | 服务器 CPU | < 70% |
| 内存 | 服务器内存 | < 80% |

### 2. 测试类型
| 类型 | 目的 | 方法 |
|------|------|------|
| 基准测试 | 建立性能基线 | 固定负载 |
| 负载测试 | 验证目标负载 | 逐步增加到目标 QPS |
| 压力测试 | 找到系统极限 | 持续增加直到崩溃 |
| 浸泡测试 | 检测内存泄漏 | 中等负载长时间运行 |

### 3. 工具选择
| 工具 | 适用场景 | 特点 |
|------|----------|------|
| k6 | HTTP API | 脚本化、CI 友好 |
| Locust | Python 项目 | Python 脚本、分布式 |
| JMeter | 复杂场景 | GUI、协议丰富 |

### 4. k6 脚本模板
```javascript
import http from 'k6/http';
import { check } from 'k6';
export const options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '3m', target: 50 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
export default function () {
  const res = http.get('http://localhost:8000/api/v1/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
}
```

## 进化能力
- 性能基准持续更新
- 压测脚本模板积累
- 性能瓶颈模式学习
