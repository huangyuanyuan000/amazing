# Auth Implement Skill - 认证授权实现

## 功能描述
提供认证授权实现方案，包括 JWT、OAuth2.0 和 RBAC 模式。

## 触发方式
- 用户认证系统开发
- 权限系统设计
- 安全审查

## 核心内容

### 1. 认证方案
| 方案 | 适用场景 | 特点 |
|------|----------|------|
| JWT | API 认证 | 无状态、可扩展 |
| Session | 传统 Web | 服务端状态、安全 |
| OAuth2.0 | 第三方登录 | 标准协议、授权委托 |
| API Key | 服务间调用 | 简单、固定权限 |

### 2. JWT 实现
```python
def create_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id, "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

### 3. RBAC 权限模型
```
用户 ──→ 角色 ──→ 权限
         │
         └── 角色继承（admin > manager > user）
```

### 4. 安全要点
- Token 过期: Access Token 2h, Refresh Token 7d
- 密码存储: bcrypt/argon2 哈希
- HTTPS 强制、CORS 白名单、Rate Limiting

## 示例
```python
@app.post("/api/v1/auth/login")
async def login(credentials: LoginRequest):
    user = await authenticate(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401)
    return {"access_token": create_token(user.id, user.role)}
```

## 进化能力
- 安全方案持续更新
- 新认证标准自动适配
- 漏洞修复模式积累
