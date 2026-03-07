# 初始化角色

根据用户角色加载对应的 Agent 能力和权限。

## 用法
```
/init-role <role-name>
```

## 支持的角色
- `product-manager` - 产品经理
- `frontend-dev` - 前端开发
- `backend-dev` - 后端开发
- `tester` - 测试工程师
- `devops` - 运维工程师
- `operator` - 运营人员

## 流程
1. 读取 .claude/settings.json 中角色配置
2. 加载对应 agents 和 skills
3. 设置权限边界
4. 输出当前可用能力列表
