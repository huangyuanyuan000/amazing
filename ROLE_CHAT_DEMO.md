# 对话式角色申请演示

## 🎯 功能特点

- ✅ 自然语言交互
- ✅ 智能关键词识别
- ✅ 多角色匹配处理
- ✅ 友好的用户体验
- ✅ 支持交互式和命令式

---

## 📝 使用演示

### 演示 1: 清晰描述 (单一匹配)

```bash
$ python3 scripts/amazing-cli.py role chat "我是前端开发"

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

### 演示 2: 多关键词 (多角色匹配)

```bash
$ python3 scripts/amazing-cli.py role chat "我负责前端开发和测试"

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

### 演示 3: 模糊描述 (未匹配)

```bash
$ python3 scripts/amazing-cli.py role chat "我想加入团队"

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

### 演示 4: 交互式对话

```bash
$ python3 scripts/amazing-cli.py role chat

👋 你好！我是 Amazing 角色助手
请告诉我你想申请什么角色，或者描述你的工作内容
例如: '我是前端开发' 或 '我负责产品需求'
输入 'quit' 退出

你: 我负责React开发
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

你: quit
👋 再见！
```

---

## 🔍 关键词识别

系统支持以下关键词识别：

| 角色 | 关键词 |
|------|--------|
| **产品经理** | 产品、需求、PRD、产品经理、product |
| **前端开发** | 前端、UI、界面、页面、React、Vue、前端开发 |
| **后端开发** | 后端、API、接口、数据库、服务、后端开发 |
| **测试工程师** | 测试、质量、Bug、测试工程师、quality |
| **运维工程师** | 运维、部署、监控、DevOps、运维工程师 |
| **运营人员** | 运营、数据分析、用户运营、运营人员 |

---

## 💡 使用技巧

### 1. 包含关键词

**好的描述**:
- ✅ "我是前端开发，负责React组件"
- ✅ "我负责后端API和数据库"
- ✅ "我做自动化测试"

**不好的描述**:
- ❌ "我是开发"
- ❌ "我想加入"
- ❌ "给我一个角色"

### 2. 描述工作内容

```bash
# 描述技术栈
"我会React和TypeScript"  → 前端开发

# 描述工作职责
"我负责API开发"  → 后端开发

# 描述工作内容
"我做产品需求分析"  → 产品经理
```

### 3. 多次尝试

如果第一次没匹配成功，换个说法：

```bash
# 第一次
"我是开发"  → 未匹配

# 第二次
"我是前端开发"  → 匹配成功
```

---

## 🆚 命令对比

| 命令 | 使用场景 | 优点 | 缺点 |
|------|---------|------|------|
| `role chat` | 新用户、不确定角色 | 自然、友好、智能 | 需要输入描述 |
| `role set` | 熟悉用户、明确角色 | 快速、精确 | 需要知道角色名 |
| `role select` | 想浏览所有角色 | 完整列表 | 需要交互选择 |

---

## 🎬 实际场景

### 场景 1: 新人入职

```bash
# 新人不知道选什么
$ python3 scripts/amazing-cli.py role chat

你: 我刚入职，不知道选什么角色
# 系统会显示所有角色让你选择

你: 我会React
# 系统识别到前端关键词，推荐前端开发角色
```

### 场景 2: 快速申请

```bash
# 熟悉的用户快速申请
$ python3 scripts/amazing-cli.py role chat "我是后端开发"
# 直接匹配，快速完成
```

### 场景 3: 角色切换

```bash
# 从前端切换到全栈
$ python3 scripts/amazing-cli.py role chat "我现在也负责后端"
# 系统识别到后端关键词，推荐后端角色
```

---

## 🔗 相关文档

- [对话申请指南](./docs/ROLE_CHAT_GUIDE.md) - 完整使用指南
- [角色命令参考](./ROLE_COMMANDS.md) - 所有角色命令
- [角色接入指南](./docs/ROLE_ONBOARDING.md) - 各工种接入

---

## 🎉 总结

对话式角色申请让新用户更容易上手，通过自然语言描述即可快速找到合适的角色。

**立即尝试**:
```bash
python3 scripts/amazing-cli.py role chat "我是前端开发"
```

---

<div align="center">

**Made with ❤️ by Amazing Team**

</div>
