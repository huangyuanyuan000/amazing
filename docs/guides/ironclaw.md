# IronClaw 使用指南

## 📖 目录

- [什么是 IronClaw](#什么是-ironclaw)
- [架构设计](#架构设计)
- [快速开始](#快速开始)
- [角色申请](#角色申请)
- [对话方式](#对话方式)
- [功能详解](#功能详解)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)

---

## 什么是 IronClaw？

**IronClaw** 是 Amazing 平台的可视化 AI 协同开发工具，提供直观的 Web 界面，支持：

- 🎯 **多角色协作**: PM/Frontend/Backend/QA/Ops/Operation
- 📋 **任务管理**: 创建、分配、跟踪任务
- 💬 **智能对话**: 自然语言交互，AI 辅助开发
- 🔍 **代码审查**: 自动化代码质量检查
- 📊 **可视化监控**: 实时项目状态、进度跟踪
- 📚 **文档中心**: 集成文档、知识库

---

## 架构设计

### 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    IronClaw Dashboard                        │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │角色管理  │任务看板  │代码审查  │监控面板  │文档中心  │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    IronClaw API Gateway                     │
│  ┌──────────┬──────────┬──────────┬──────────┐            │
│  │认证授权  │权限控制  │请求路由  │日志审计  │            │
│  └──────────┴──────────┴──────────┴──────────┘            │
└─────────────────────────────┬─────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    Agent Orchestrator                       │
│  ┌──────────┬──────────┬──────────┬──────────┐            │
│  │任务分发  │状态同步  │进度跟踪  │结果聚合  │            │
│  └──────────┴──────────┴──────────┴──────────┘            │
└─────────────────────────────┬─────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼────────┐  ┌──────▼───────┐
            │  Claude Code   │  │  Codex CLI   │
            │   (AI 引擎)    │  │  (备选引擎)  │
            └────────────────┘  └──────────────┘
```

### 技术栈

- **前端**: React + TypeScript + Ant Design
- **后端**: FastAPI + WebSocket
- **数据库**: PostgreSQL + Redis
- **AI 引擎**: Claude Code / Codex
- **实时通信**: WebSocket + Server-Sent Events

---

## 快速开始

### 1. 启动 IronClaw

**开发模式**:
```bash
# 进入 IronClaw 目录
cd ironclaw

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问: http://localhost:3001
```

**生产模式**:
```bash
# 构建
npm run build

# 启动
npm run start
```

**Docker 模式**:
```bash
# 使用 Docker Compose
docker-compose -f docker-compose.ironclaw.yml up -d

# 访问: http://localhost:3001
```

### 2. 首次登录

1. 访问 http://localhost:3001
2. 点击 "注册账号"
3. 填写信息:
   - 用户名: `your_username`
   - 邮箱: `your_email@example.com`
   - 密码: `your_password`
   - 所属团队: `amazing-team`
4. 提交注册
5. 登录系统

### 3. 配置 AI 引擎

**设置 API Key**:

1. 进入 "设置" → "AI 配置"
2. 选择 AI 引擎:
   - Claude Code (推荐)
   - Codex CLI
3. 输入 API Key
4. 测试连接
5. 保存配置

---

## 角色申请

### 申请流程

#### 方式 1: Web 界面申请

**步骤 1: 进入角色管理**

1. 登录 IronClaw
2. 点击左侧菜单 "角色管理"
3. 查看可用角色列表

**步骤 2: 提交申请**

1. 点击 "申请角色" 按钮
2. 填写申请表单:
   ```
   角色: [选择角色]
   - 产品经理 (PM)
   - 前端开发 (Frontend)
   - 后端开发 (Backend)
   - 测试工程师 (QA)
   - 运维工程师 (Ops)
   - 运营人员 (Operation)

   申请理由: [填写理由]
   例如: 我是前端开发，负责 UI 实现，有 3 年 React 开发经验

   技能标签: [选择标签]
   - React, TypeScript, Vite (Frontend)
   - Python, FastAPI, PostgreSQL (Backend)
   - Pytest, Jest, Playwright (QA)
   - Docker, Kubernetes, Prometheus (Ops)
   ```
3. 上传证明材料 (可选):
   - 简历
   - 项目经验
   - 技能证书
4. 提交申请

**步骤 3: 等待审批**

1. 申请提交后，状态变为 "待审批"
2. 管理员会在 24 小时内审批
3. 审批结果会通过邮件和站内消息通知

**步骤 4: 激活角色**

1. 审批通过后，进入 "我的角色"
2. 点击 "激活角色"
3. 阅读角色权限说明
4. 确认激活

#### 方式 2: CLI 申请

```bash
# 申请角色
python3 scripts/amazing-cli.py role apply \
  --role frontend \
  --reason "我是前端开发，负责 UI 实现" \
  --skills "React,TypeScript,Vite"

# 查看申请状态
python3 scripts/amazing-cli.py role status

# 输出:
# 申请状态: 待审批
# 申请时间: 2024-03-07 10:00:00
# 预计审批时间: 2024-03-08 10:00:00
```

### 角色审批 (管理员)

#### Web 界面审批

1. 登录管理员账号
2. 进入 "管理中心" → "角色审批"
3. 查看待审批申请列表
4. 点击申请查看详情:
   - 申请人信息
   - 申请理由
   - 技能标签
   - 证明材料
5. 做出决定:
   - **批准**: 点击 "批准"，角色立即生效
   - **拒绝**: 点击 "拒绝"，填写拒绝理由
   - **待定**: 点击 "待定"，要求补充材料

#### CLI 审批

```bash
# 查看待审批申请
python3 scripts/amazing-cli.py admin role-requests

# 输出:
# ID    用户      角色        申请时间            状态
# 001   张三      frontend    2024-03-07 10:00   待审批
# 002   李四      backend     2024-03-07 11:00   待审批

# 批准申请
python3 scripts/amazing-cli.py admin approve 001

# 拒绝申请
python3 scripts/amazing-cli.py admin reject 002 \
  --reason "技能不符合要求，建议先学习 TypeScript"
```

### 角色权限

| 角色 | 创建任务 | 分配任务 | 代码审查 | 部署 | 管理用户 |
|------|---------|---------|---------|------|---------|
| **PM** | ✅ | ✅ | ❌ | ❌ | ❌ |
| **Frontend** | ✅ | ❌ | ✅ | ✅ | ❌ |
| **Backend** | ✅ | ❌ | ✅ | ✅ | ❌ |
| **QA** | ✅ | ❌ | ✅ | ❌ | ❌ |
| **Ops** | ✅ | ❌ | ✅ | ✅ | ❌ |
| **Operation** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Admin** | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 对话方式

### 基础对话

#### 1. @提及 IronClaw

```
用户: @IronClaw 你好
IronClaw:
👋 你好！我是 IronClaw，你的 AI 协同开发助手。

我可以帮你:
- 创建和管理任务
- 生成和审查代码
- 协调团队协作
- 回答技术问题
- 监控项目进度

需要什么帮助吗？
```

#### 2. 直接对话

```
用户: 帮我创建一个用户登录功能的任务
IronClaw:
✅ 任务已创建

任务详情:
- ID: TASK-001
- 标题: 实现用户登录功能
- 描述: 实现用户登录功能，包含前后端
- 分配给: Common Agent
- 优先级: 高
- 预计时间: 2 天
- 截止日期: 2024-03-09

需要我生成详细的技术方案吗？
```

### 任务管理对话

#### 创建任务

```
用户: @IronClaw 创建任务: 实现用户权限管理
IronClaw:
✅ 任务已创建

任务详情:
- ID: TASK-002
- 标题: 实现用户权限管理
- Agent: Common Agent
- 优先级: 高
- 预计时间: 3 天

建议的子任务:
1. 设计权限模型 (PM)
2. 实现后端 API (Backend)
3. 实现前端界面 (Frontend)
4. 编写测试用例 (QA)
5. 部署上线 (Ops)

需要我自动创建这些子任务吗？
```

#### 查询任务

```
用户: @IronClaw 查询任务 TASK-001
IronClaw:
📋 任务详情

基本信息:
- ID: TASK-001
- 标题: 实现用户登录功能
- 状态: 进行中 (60%)
- 优先级: 高

负责人:
- PM: @李四
- Frontend: @张三
- Backend: @王五
- QA: @赵六

进度:
✅ 需求分析 (100%)
✅ 后端 API (100%)
🔄 前端界面 (60%)
⏳ 测试 (0%)
⏳ 部署 (0%)

预计完成: 明天 18:00
```

#### 分配任务

```
用户: @IronClaw 把 TASK-001 分配给 @张三
IronClaw:
✅ 任务已分配

任务: TASK-001 - 实现用户登录功能
分配给: @张三 (Frontend)
通知方式: 邮件 + 站内消息

@张三 已收到通知，预计 30 分钟内响应
```

### 代码对话

#### 生成代码

```
用户: @IronClaw 生成用户登录 API
IronClaw:
✅ 代码已生成

```python
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import authenticate_user, create_access_token

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """用户登录"""
    user = await authenticate_user(
        credentials.username,
        credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误"
        )

    token = create_access_token(user.id)
    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )
```

文件位置: backend/python/app/api/auth.py

需要我生成:
1. 对应的测试代码？
2. 前端调用代码？
3. API 文档？
```

#### 代码审查

```
用户: @IronClaw 审查 backend/python/app/api/auth.py
IronClaw:
🔍 代码审查结果

✅ 优点:
1. 使用了异步处理，性能好
2. 错误处理完善，返回清晰的错误信息
3. 符合 RESTful 规范
4. 代码结构清晰，易于维护

⚠️ 建议:
1. 添加请求频率限制 (防止暴力破解)
   建议: 使用 slowapi 限制每分钟 5 次请求

2. 密码错误时不要暴露用户是否存在
   建议: 统一返回 "用户名或密码错误"

3. 添加日志记录
   建议: 记录登录成功/失败的日志

4. 添加单元测试
   建议: 测试覆盖率应 > 80%

🐛 问题:
- 无

📊 质量评分: 85/100

需要我帮你修复这些问题吗？
```

#### 代码重构

```
用户: @IronClaw 重构 backend/python/app/api/auth.py，添加频率限制
IronClaw:
✅ 代码已重构

主要改动:
1. 添加了 slowapi 依赖
2. 添加了频率限制装饰器
3. 优化了错误处理
4. 添加了日志记录

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    credentials: LoginRequest
):
    """用户登录 (限制: 每分钟 5 次)"""
    logger.info(f"Login attempt: {credentials.username}")

    user = await authenticate_user(
        credentials.username,
        credentials.password
    )
    if not user:
        logger.warning(f"Login failed: {credentials.username}")
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误"
        )

    logger.info(f"Login success: {user.username}")
    token = create_access_token(user.id)
    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )
```

文件已更新: backend/python/app/api/auth.py

需要我:
1. 运行测试验证？
2. 生成 Git commit？
3. 创建 PR？
```

### 协作对话

#### @提及协作

```
用户: @IronClaw @张三 请帮忙实现用户登录的前端页面
IronClaw:
✅ 已通知 @张三 (Frontend)

任务详情:
- 标题: 实现用户登录前端页面
- 关联任务: TASK-001
- 优先级: 高
- 技术要求:
  - React + TypeScript
  - Ant Design
  - 表单验证
  - 错误处理

@张三 会在 30 分钟内响应

同时，我已经为你准备了:
1. 后端 API 文档
2. 前端组件模板
3. 测试用例模板

需要查看吗？
```

#### 团队讨论

```
用户: @IronClaw 召集团队讨论用户登录方案
IronClaw:
📢 已创建讨论组

讨论主题: 用户登录方案
参与者:
- @李四 (PM) - 需求确认
- @张三 (Frontend) - UI 实现
- @王五 (Backend) - API 实现
- @赵六 (QA) - 测试方案

会议室: http://localhost:3001/meeting/001
会议时间: 现在 - 1 小时后

议程:
1. 需求确认 (10 分钟)
2. 技术方案讨论 (20 分钟)
3. 任务分配 (10 分钟)
4. Q&A (20 分钟)

已发送会议邀请，请大家在 10 分钟内加入
```

#### 进度同步

```
用户: @IronClaw 同步 TASK-001 的进度
IronClaw:
📊 任务进度同步

TASK-001: 实现用户登录功能

总体进度: 75%

各模块进度:
✅ 需求分析 (100%) - @李四
   - PRD 已完成
   - 技术方案已确认

✅ 后端 API (100%) - @王五
   - API 已实现
   - 测试已通过
   - 已部署到测试环境

🔄 前端界面 (80%) - @张三
   - 登录表单已完成
   - 错误处理已完成
   - 正在优化 UI

⏳ 测试 (30%) - @赵六
   - 单元测试已完成
   - 正在进行集成测试

⏳ 部署 (0%) - @钱七
   - 等待测试完成

预计完成时间: 明天 18:00

需要我:
1. 催促进度？
2. 调整资源？
3. 延期任务？
```

### 智能问答

#### 技术咨询

```
用户: @IronClaw 如何实现 JWT 认证？
IronClaw:
📚 JWT 认证实现方案

1. 安装依赖:
```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

2. 生成 Token:
```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(days=1)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

3. 验证 Token:
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY)
        user_id = payload.get("user_id")
        return await get_user(user_id)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
```

4. 最佳实践:
- Token 有效期: 24 小时
- 使用 Refresh Token 延长会话
- 存储在 HttpOnly Cookie (防止 XSS)
- 使用 HTTPS 传输 (防止中间人攻击)

需要完整的代码示例吗？
```

#### 问题诊断

```
用户: @IronClaw 为什么登录接口返回 500 错误？
IronClaw:
🔍 正在分析日志...

发现问题:
- 错误类型: psycopg2.OperationalError
- 错误信息: could not connect to server
- 错误位置: backend/python/app/core/database.py:15
- 发生时间: 2024-03-07 14:30:25

根本原因:
数据库连接失败，可能原因:
1. 数据库未启动
2. 连接配置错误
3. 网络问题

解决方案:

步骤 1: 检查数据库状态
```bash
docker ps | grep postgres
```

步骤 2: 检查连接配置
```bash
cat backend/python/.env | grep DATABASE_URL
```

步骤 3: 重启数据库
```bash
docker restart amazing-postgres
```

步骤 4: 测试连接
```bash
python3 -c "import psycopg2; psycopg2.connect('postgresql://...')"
```

需要我帮你执行这些命令吗？
```

### 快捷命令

```bash
# 任务管理
@IronClaw task create <title>          # 创建任务
@IronClaw task list                    # 列出任务
@IronClaw task show <id>               # 查看任务
@IronClaw task assign <id> @user       # 分配任务
@IronClaw task close <id>              # 关闭任务
@IronClaw task reopen <id>             # 重新打开任务

# 代码操作
@IronClaw code generate <description>  # 生成代码
@IronClaw code review <file>           # 代码审查
@IronClaw code refactor <file>         # 代码重构
@IronClaw code test <file>             # 生成测试
@IronClaw code fix <file>              # 修复问题

# 协作
@IronClaw notify @user <message>       # 通知用户
@IronClaw meeting create <topic>       # 创建会议
@IronClaw discuss <topic>              # 发起讨论
@IronClaw sync <task-id>               # 同步进度

# 查询
@IronClaw status                       # 项目状态
@IronClaw help                         # 帮助信息
@IronClaw docs <topic>                 # 查询文档
@IronClaw search <keyword>             # 搜索

# 部署
@IronClaw deploy <env>                 # 部署到环境
@IronClaw rollback <version>           # 回滚版本
@IronClaw logs <service>               # 查看日志
```

---

## 功能详解

### 1. 任务看板

**功能**:
- 看板视图 (待办/进行中/已完成)
- 拖拽排序
- 优先级标记
- 截止日期提醒
- 进度跟踪

**使用**:
1. 进入 "任务看板"
2. 查看任务列表
3. 拖拽任务到不同状态
4. 点击任务查看详情

### 2. 代码审查

**功能**:
- 自动代码审查
- 质量评分
- 问题检测
- 修复建议
- 审查报告

**使用**:
1. 进入 "代码审查"
2. 选择文件或 PR
3. 点击 "开始审查"
4. 查看审查结果
5. 应用修复建议

### 3. 监控面板

**功能**:
- 项目进度
- 团队效率
- 代码质量
- 部署状态
- 告警通知

**使用**:
1. 进入 "监控面板"
2. 查看各项指标
3. 设置告警规则
4. 导出报告

### 4. 文档中心

**功能**:
- 文档浏览
- 全文搜索
- 版本管理
- 协作编辑
- 知识库

**使用**:
1. 进入 "文档中心"
2. 浏览文档目录
3. 搜索关键词
4. 编辑文档
5. 发布更新

---

## 最佳实践

### 1. 任务管理

- 任务标题清晰明确
- 添加详细描述
- 设置合理的优先级
- 及时更新进度
- 关联相关任务

### 2. 代码协作

- 提交前先审查
- 编写清晰的 commit 信息
- 及时响应 PR 评论
- 保持代码风格一致
- 添加必要的测试

### 3. 团队沟通

- 使用 @提及通知相关人员
- 在任务中讨论具体问题
- 定期同步进度
- 记录重要决策
- 分享知识和经验

### 4. 问题处理

- 详细描述问题
- 提供复现步骤
- 附上错误日志
- 标记优先级
- 跟踪解决进度

---

## 常见问题

### Q: 如何切换角色？
A: 进入 "角色管理" → "我的角色" → 选择要切换的角色 → 点击 "切换"

### Q: 如何邀请团队成员？
A: 进入 "团队管理" → "邀请成员" → 输入邮箱 → 选择角色 → 发送邀请

### Q: 如何配置 AI 引擎？
A: 进入 "设置" → "AI 配置" → 选择引擎 → 输入 API Key → 测试连接 → 保存

### Q: 如何导出数据？
A: 进入 "设置" → "数据管理" → "导出数据" → 选择格式 (JSON/CSV) → 下载

### Q: 如何备份项目？
A: 进入 "设置" → "备份管理" → "创建备份" → 等待完成 → 下载备份文件

### Q: 遇到问题怎么办？
A:
1. 查看 [文档中心](http://localhost:3001/docs)
2. 搜索 [常见问题](http://localhost:3001/faq)
3. 联系 [技术支持](mailto:support@amazing.com)
4. 提交 [Issue](https://github.com/z58362026/amazing/issues)

---

## 更多资源

- [IronClaw 官方文档](http://localhost:3001/docs)
- [视频教程](http://localhost:3001/tutorials)
- [API 文档](http://localhost:3001/api-docs)
- [更新日志](http://localhost:3001/changelog)

---

<div align="center">

**[⬆ 回到顶部](#ironclaw-使用指南)**

Made with ❤️ by Amazing Team

</div>
