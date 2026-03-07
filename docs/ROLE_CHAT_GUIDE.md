# 通过对话申请角色指南

## 概述

Amazing 支持通过自然语言对话的方式申请角色，系统会智能识别你的意图并推荐合适的角色。

---

## 使用方式

### 方式 1: 交互式对话

```bash
python3 scripts/amazing-cli.py role chat
```

**对话示例**:

```
👋 你好！我是 Amazing 角色助手
请告诉我你想申请什么角色，或者描述你的工作内容
例如: '我是前端开发' 或 '我负责产品需求'
输入 'quit' 退出

你: 我是前端开发
🎯 我理解了！你想申请 **前端开发** 角色

角色信息:
  名称: 前端开发
  权限: ui:develop, component:create, style:edit...
  技能: react-component, ui-design, state-management...

确认申请这个角色吗? [Y/n]: y

✅ 已成功申请 前端开发 角色！

你现在可以:
  1. ui:develop
  2. component:create
  3. style:edit
  4. frontend:deploy

💡 提示: 使用 'python3 scripts/amazing-cli.py status' 查看当前状态
```

### 方式 2: 直接传递消息

```bash
python3 scripts/amazing-cli.py role chat "我负责后端API开发"
```

**输出**:
```
🎯 我理解了！你想申请 **后端开发** 角色

角色信息:
  名称: 后端开发
  权限: api:develop, database:design, service:create...
  技能: api-design, database-design, auth-implement...

确认申请这个角色吗? [Y/n]: y

✅ 已成功申请 后端开发 角色！
```

---

## 智能识别

系统会根据你的描述自动识别角色，支持的关键词：

### 产品经理 (PM)
- **关键词**: 产品、需求、PRD、产品经理、product
- **示例**:
  - "我是产品经理"
  - "我负责需求分析"
  - "我要写PRD"

### 前端开发 (Frontend)
- **关键词**: 前端、UI、界面、页面、React、Vue、前端开发
- **示例**:
  - "我是前端开发"
  - "我负责UI实现"
  - "我做React开发"

### 后端开发 (Backend)
- **关键词**: 后端、API、接口、数据库、服务、后端开发
- **示例**:
  - "我是后端开发"
  - "我负责API开发"
  - "我做数据库设计"

### 测试工程师 (QA)
- **关键词**: 测试、质量、Bug、测试工程师、quality
- **示例**:
  - "我是测试工程师"
  - "我负责质量保证"
  - "我做自动化测试"

### 运维工程师 (Ops)
- **关键词**: 运维、部署、监控、DevOps、运维工程师
- **示例**:
  - "我是运维工程师"
  - "我负责部署"
  - "我做DevOps"

### 运营人员 (Operation)
- **关键词**: 运营、数据分析、用户运营、运营人员
- **示例**:
  - "我是运营人员"
  - "我负责数据分析"
  - "我做用户运营"

---

## 多角色匹配

如果你的描述匹配多个角色，系统会让你选择：

```bash
python3 scripts/amazing-cli.py role chat "我负责前端和测试"
```

**输出**:
```
🤔 我找到了 2 个可能的角色:

1. 前端开发 (frontend)
   权限: ui:develop, component:create...
   技能: react-component, ui-design...

2. 测试工程师 (qa)
   权限: test:design, test:execute...
   技能: test-design, automation...

请选择角色 (输入数字) [1]: 1

✅ 已成功申请 前端开发 角色！
```

---

## 未匹配处理

如果系统无法识别你的意图，会显示所有可用角色：

```bash
python3 scripts/amazing-cli.py role chat "我想加入团队"
```

**输出**:
```
🤔 抱歉，我没有理解你的意思
请从以下角色中选择:

1. 产品经理 (pm)
   描述: 负责需求分析、PRD编写、功能验收
   权限: prd:create, prd:edit...

2. 前端开发 (frontend)
   描述: 负责UI/UX实现、组件开发
   权限: ui:develop, component:create...

3. 后端开发 (backend)
   描述: 负责API开发、数据库设计
   权限: api:develop, database:design...

4. 测试工程师 (qa)
   描述: 负责测试设计、自动化测试
   权限: test:design, test:execute...

5. 运维工程师 (ops)
   描述: 负责部署、监控、故障排查
   权限: deploy:execute, monitor:configure...

6. 运营人员 (operation)
   描述: 负责数据分析、用户运营
   权限: data:analyze, config:manage...

请选择角色 (输入数字) [0]: 2

✅ 已成功申请 前端开发 角色！
```

---

## 在 IronClaw 中使用

### Web 界面对话

1. 登录 IronClaw
2. 在聊天框输入: `@IronClaw 我想申请前端开发角色`
3. IronClaw 会识别你的意图并引导你完成申请

**对话示例**:

```
用户: @IronClaw 我想申请前端开发角色
IronClaw:
🎯 我理解了！你想申请 **前端开发** 角色

角色信息:
- 名称: 前端开发
- 权限: UI开发、组件创建、样式编辑、前端部署
- 技能: React组件、UI设计、状态管理、性能优化
- 技术栈: React, TypeScript, Vite, TailwindCSS

这个角色适合你吗？

[确认申请] [查看其他角色]
```

### 自然语言申请

```
用户: @IronClaw 我是做React开发的
IronClaw:
👋 你好！根据你的描述，我推荐你申请 **前端开发** 角色

这个角色需要:
- React 开发经验 ✅ (你已具备)
- TypeScript 知识
- 组件设计能力
- 状态管理经验

你想申请这个角色吗？

[确认申请] [了解更多]
```

### 模糊描述处理

```
用户: @IronClaw 我想参与开发
IronClaw:
🤔 我需要了解更多信息来推荐合适的角色

请告诉我:
1. 你主要负责什么工作？
   - 前端 (UI/界面)
   - 后端 (API/数据库)
   - 测试 (质量保证)
   - 运维 (部署/监控)
   - 其他

2. 你擅长什么技术？
   - React/Vue (前端)
   - Python/Go (后端)
   - 测试框架
   - Docker/K8s (运维)

请描述你的工作内容，我会为你推荐最合适的角色 😊
```

---

## 对话技巧

### 1. 清晰描述

**好的描述**:
- ✅ "我是前端开发，负责React组件开发"
- ✅ "我负责后端API设计和数据库优化"
- ✅ "我做自动化测试和质量保证"

**不好的描述**:
- ❌ "我想加入"
- ❌ "我是开发"
- ❌ "给我一个角色"

### 2. 包含关键词

在描述中包含角色相关的关键词，帮助系统更准确识别：

- 前端: React、Vue、UI、界面
- 后端: API、数据库、服务
- 测试: 测试、质量、自动化
- 运维: 部署、监控、K8s
- 产品: 需求、PRD、产品
- 运营: 数据分析、用户运营

### 3. 多次尝试

如果第一次没有匹配成功，可以换个说法：

```
第一次: "我是开发" (未匹配)
第二次: "我是前端开发" (匹配成功)
```

---

## 命令对比

| 方式 | 命令 | 特点 |
|------|------|------|
| **对话申请** | `role chat` | 自然语言、智能识别、友好 |
| **直接设置** | `role set <role>` | 快速、精确、适合熟悉用户 |
| **交互选择** | `role select` | 列表选择、适合不确定用户 |

---

## 常见问题

### Q: 对话申请和直接设置有什么区别？

A:
- **对话申请**: 使用自然语言，系统智能识别，适合新用户
- **直接设置**: 直接指定角色名，快速精确，适合熟悉用户

### Q: 如果我说错了怎么办？

A: 可以重新申请，系统会覆盖之前的角色设置。

### Q: 可以同时拥有多个角色吗？

A: 当前版本只支持单一角色，但可以随时切换。

### Q: 对话申请需要审批吗？

A:
- CLI 对话申请: 立即生效，无需审批
- IronClaw Web 申请: 需要管理员审批

### Q: 如何查看当前角色？

A: 使用 `python3 scripts/amazing-cli.py status` 查看。

---

## 示例场景

### 场景 1: 新人加入

```bash
# 新人不知道选什么角色
python3 scripts/amazing-cli.py role chat

你: 我刚加入团队，不知道选什么角色
IronClaw:
🤔 没关系！让我帮你找到合适的角色

请告诉我:
1. 你的技术背景是什么？
2. 你在团队中主要负责什么工作？
3. 你擅长什么技术栈？

你: 我会React和TypeScript，负责做页面
IronClaw:
🎯 太好了！根据你的描述，我推荐 **前端开发** 角色

这个角色非常适合你，因为:
- 需要 React 技能 ✅
- 需要 TypeScript 技能 ✅
- 主要工作是页面开发 ✅

确认申请吗？
```

### 场景 2: 快速申请

```bash
# 熟悉的用户快速申请
python3 scripts/amazing-cli.py role chat "我是后端开发"

# 输出:
# ✅ 已成功申请 后端开发 角色！
```

### 场景 3: 角色切换

```bash
# 从前端切换到全栈
python3 scripts/amazing-cli.py role chat "我现在也负责后端开发"

# 系统会识别到后端关键词，推荐后端角色
```

---

## 更多资源

- [角色命令参考](../ROLE_COMMANDS.md)
- [角色接入指南](./ROLE_ONBOARDING.md)
- [IronClaw 使用指南](./IRONCLAW_GUIDE.md)

---

<div align="center">

**[⬆ 回到顶部](#通过对话申请角色指南)**

Made with ❤️ by Amazing Team

</div>
