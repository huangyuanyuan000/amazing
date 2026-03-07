# 固定 Agent 说明

## 概述

固定 Agent 是 Amazing 架构中的**通用部门**，提供所有业务 Agent 都需要的通用能力。

就像公司的 HR、财务、IT 部门一样，固定 Agent 是基础设施。

---

## 为什么需要固定 Agent？

### 1. 避免重复开发

如果每个业务 Agent 都实现用户管理、权限控制，会导致：
- ❌ 重复开发，浪费资源
- ❌ 实现不一致，难以维护
- ❌ 安全风险，难以统一管理

**固定 Agent 的好处**：
- ✅ 统一实现，一次开发
- ✅ 统一标准，易于维护
- ✅ 统一管理，安全可控

### 2. 提供基础能力

固定 Agent 提供基础能力，业务 Agent 专注业务逻辑：

```
业务 Agent（专注业务）
    ↓ 调用
固定 Agent（提供基础能力）
```

---

## Common Agent（通用部门）

### 职责

Common Agent 提供所有系统都需要的通用功能：

1. **用户管理**
   - 用户注册和登录
   - 用户信息管理
   - 用户状态管理
   - 用户搜索和筛选

2. **权限控制**
   - 角色管理（RBAC）
   - 权限分配
   - 权限检查
   - 资源授权

3. **日志审计**
   - 操作日志记录
   - 审计日志查询
   - 日志分析
   - 合规报告

4. **配置管理**
   - 系统配置
   - 功能开关
   - 参数配置
   - 配置版本管理

### 技术架构

```
Common Agent
├── API 层
│   ├── 用户 API
│   ├── 权限 API
│   ├── 日志 API
│   └── 配置 API
│
├── 服务层
│   ├── 用户服务
│   ├── 权限服务
│   ├── 日志服务
│   └── 配置服务
│
├── 数据层
│   ├── 用户表
│   ├── 角色表
│   ├── 权限表
│   ├── 日志表
│   └── 配置表
│
└── 缓存层
    ├── 用户缓存
    ├── 权限缓存
    └── 配置缓存
```

### 默认技术栈

```
后端：Python + FastAPI
数据库：PostgreSQL
缓存：Redis
认证：JWT
```

### API 示例

**用户管理 API**：

```
POST   /api/v1/users              # 创建用户
GET    /api/v1/users              # 获取用户列表
GET    /api/v1/users/{id}         # 获取用户详情
PUT    /api/v1/users/{id}         # 更新用户
DELETE /api/v1/users/{id}         # 删除用户
POST   /api/v1/users/login        # 用户登录
POST   /api/v1/users/logout       # 用户登出
```

**权限管理 API**：

```
POST   /api/v1/roles              # 创建角色
GET    /api/v1/roles              # 获取角色列表
POST   /api/v1/roles/{id}/permissions  # 分配权限
GET    /api/v1/users/{id}/permissions  # 获取用户权限
POST   /api/v1/check-permission   # 检查权限
```

### 使用示例

业务 Agent 调用 Common Agent：

```python
# 业务 Agent 代码
from common_client import CommonClient

common = CommonClient()

# 检查用户权限
if common.check_permission(user_id, "compute:create"):
    # 创建算力资源
    create_compute_resource()
else:
    raise PermissionDenied()

# 记录操作日志
common.log_action(
    user_id=user_id,
    action="compute:create",
    resource_id=resource_id,
    result="success"
)
```

---

## Review Agent（质量审核部门）

### 职责

Review Agent 负责质量把控和审核：

1. **代码审查**
   - 代码规范检查
   - 代码质量分析
   - 安全漏洞扫描
   - 最佳实践检查

2. **安全审查**
   - SQL 注入检查
   - XSS 漏洞检查
   - 敏感信息检查
   - 依赖安全检查

3. **性能审查**
   - 性能瓶颈分析
   - 资源使用分析
   - 数据库查询优化
   - API 响应时间分析

4. **合规检查**
   - 代码许可证检查
   - 数据隐私合规
   - 安全合规检查
   - 行业标准检查

### 技术架构

```
Review Agent
├── 代码审查
│   ├── ESLint（JavaScript/TypeScript）
│   ├── Pylint（Python）
│   ├── Golangci-lint（Go）
│   └── SonarQube（综合）
│
├── 安全审查
│   ├── Bandit（Python 安全）
│   ├── Safety（依赖安全）
│   ├── Trivy（容器安全）
│   └── OWASP ZAP（Web 安全）
│
├── 性能审查
│   ├── Profiler（性能分析）
│   ├── Load Testing（负载测试）
│   └── APM（应用性能监控）
│
└── 合规检查
    ├── License Checker（许可证）
    ├── GDPR Checker（数据隐私）
    └── Security Audit（安全审计）
```

### 默认技术栈

```
代码审查：SonarQube
安全扫描：Trivy + Bandit
性能分析：Prometheus + Grafana
合规检查：自定义规则引擎
```

### 审查流程

```
1. 代码提交
   ↓
2. Review Agent 自动触发
   ├── 代码规范检查
   ├── 安全漏洞扫描
   ├── 性能分析
   └── 合规检查
   ↓
3. 生成审查报告
   ├── 问题列表
   ├── 严重程度
   ├── 修复建议
   └── 通过/不通过
   ↓
4. 架构师审查
   ├── 查看报告
   ├── 人工审查
   └── 批准/拒绝
```

### 审查报告示例

```json
{
  "review_id": "REV-001",
  "commit": "abc123",
  "timestamp": "2025-03-15T10:30:00Z",
  "status": "failed",
  "summary": {
    "total_issues": 15,
    "critical": 2,
    "high": 5,
    "medium": 6,
    "low": 2
  },
  "issues": [
    {
      "type": "security",
      "severity": "critical",
      "file": "api/auth.py",
      "line": 45,
      "message": "SQL injection vulnerability",
      "suggestion": "Use parameterized queries"
    },
    {
      "type": "code_quality",
      "severity": "high",
      "file": "api/user.py",
      "line": 120,
      "message": "Function too complex (cyclomatic complexity: 15)",
      "suggestion": "Refactor into smaller functions"
    }
  ],
  "metrics": {
    "code_coverage": 75,
    "code_quality": 6.5,
    "security_score": 65,
    "performance_score": 80
  }
}
```

---

## 固定 Agent 的配置

### Common Agent 配置

**.agents/common/config.json**：

```json
{
  "name": "common",
  "type": "fixed",
  "displayName": "通用部门",
  "description": "提供用户管理、权限控制、日志审计等通用功能",
  "techStack": {
    "backend": "Python + FastAPI",
    "database": "PostgreSQL",
    "cache": "Redis",
    "auth": "JWT"
  },
  "services": [
    {
      "name": "user",
      "description": "用户管理服务",
      "api": "/api/v1/users"
    },
    {
      "name": "permission",
      "description": "权限控制服务",
      "api": "/api/v1/permissions"
    },
    {
      "name": "audit",
      "description": "日志审计服务",
      "api": "/api/v1/audit"
    },
    {
      "name": "config",
      "description": "配置管理服务",
      "api": "/api/v1/config"
    }
  ],
  "subAgents": [
    "pm",
    "frontend",
    "backend",
    "qa",
    "ops"
  ]
}
```

### Review Agent 配置

**.agents/review/config.json**：

```json
{
  "name": "review",
  "type": "fixed",
  "displayName": "质量审核部门",
  "description": "负责代码审查、安全审查、性能审查和合规检查",
  "techStack": {
    "code_review": "SonarQube",
    "security_scan": "Trivy + Bandit",
    "performance": "Prometheus + Grafana"
  },
  "checks": [
    {
      "name": "code_quality",
      "enabled": true,
      "threshold": 7.0
    },
    {
      "name": "security",
      "enabled": true,
      "threshold": 80
    },
    {
      "name": "performance",
      "enabled": true,
      "threshold": 75
    },
    {
      "name": "compliance",
      "enabled": true,
      "threshold": 90
    }
  ],
  "subAgents": [
    "qa",
    "architect"
  ]
}
```

---

## 固定 Agent 的部署

### 部署架构

```
┌─────────────────────────────────────┐
│         API Gateway                 │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌──────▼──────┐
│  Common    │    │   Review    │
│  Agent     │    │   Agent     │
└───┬────────┘    └──────┬──────┘
    │                    │
┌───▼────────────────────▼──────┐
│      PostgreSQL + Redis       │
└───────────────────────────────┘
```

### Docker Compose 配置

```yaml
version: '3.8'

services:
  common-agent:
    build: ./backend/common
    ports:
      - "8001:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/common
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  review-agent:
    build: ./backend/review
    ports:
      - "8002:8000"
    environment:
      - SONARQUBE_URL=http://sonarqube:9000
    depends_on:
      - sonarqube

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

  sonarqube:
    image: sonarqube:community
    ports:
      - "9000:9000"

volumes:
  postgres_data:
  redis_data:
```

---

## 最佳实践

### 1. 统一使用固定 Agent

**建议**：
- ✅ 所有业务 Agent 都使用 Common Agent 的用户管理
- ✅ 所有代码都通过 Review Agent 审查
- ✅ 不要在业务 Agent 中重复实现

### 2. 保持固定 Agent 稳定

**原则**：
- 固定 Agent 的 API 要保持稳定
- 向后兼容，不要破坏性变更
- 充分测试，确保质量

### 3. 合理扩展固定 Agent

**何时扩展**：
- 所有业务 Agent 都需要的功能
- 通用的基础能力
- 需要统一管理的功能

**何时不扩展**：
- 只有个别业务 Agent 需要
- 业务特定的功能
- 频繁变化的功能

---

## 相关文档

- [Agent-Teams 层说明](../README.md)
- [业务 Agent 创建指南](../business-agents/create-guide.md)
- [技术选型层说明](../../04-tech-stack/README.md)
