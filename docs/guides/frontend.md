# 前端开发指南

## 1. 角色职责

作为前端开发，你负责:
- UI/UX 实现
- 组件开发
- 状态管理
- 性能优化
- 前端部署

## 2. 技术栈

- **框架**: React 18
- **语言**: TypeScript
- **构建**: Vite
- **样式**: TailwindCSS
- **状态**: Zustand
- **HTTP**: Axios
- **UI 库**: Ant Design

## 3. 工作流程

### 3.1 开发环境

```bash
# 启动开发服务器
cd frontend
npm run dev

# 访问
open http://localhost:3000
```

### 3.2 创建组件

```bash
# 使用 Claude Code
claude-code "创建 UserList 组件"

# 或使用 Codex
codex "创建 UserList 组件"
```

### 3.3 状态管理

```typescript
// 使用 Zustand
import { create } from 'zustand'

interface UserStore {
  users: User[]
  fetchUsers: () => Promise<void>
}

export const useUserStore = create<UserStore>((set) => ({
  users: [],
  fetchUsers: async () => {
    const response = await axios.get('/api/v1/users')
    set({ users: response.data.data })
  }
}))
```

### 3.4 API 调用

```typescript
// src/api/user.ts
import axios from 'axios'

export const userApi = {
  getUsers: () => axios.get('/api/v1/users'),
  getUser: (id: number) => axios.get(`/api/v1/users/${id}`),
  createUser: (data: CreateUserDto) => axios.post('/api/v1/users', data),
}
```

## 4. Skills

### 4.1 react-component

生成 React 组件。

**使用**:
```bash
amazing skill run react-component --name UserList
```

### 4.2 ui-design

UI 设计与实现。

**使用**:
```bash
amazing skill run ui-design --feature "用户列表"
```

### 4.3 state-management

状态管理方案。

**使用**:
```bash
amazing skill run state-management --store user
```

## 5. 代码规范

### 5.1 组件规范

```typescript
// 使用函数式组件
interface UserListProps {
  users: User[]
  onSelect: (user: User) => void
}

export const UserList: React.FC<UserListProps> = ({ users, onSelect }) => {
  return (
    <div className="user-list">
      {users.map(user => (
        <div key={user.id} onClick={() => onSelect(user)}>
          {user.name}
        </div>
      ))}
    </div>
  )
}
```

### 5.2 样式规范

```typescript
// 使用 TailwindCSS
<div className="flex items-center justify-between p-4 bg-white rounded-lg shadow">
  <h2 className="text-xl font-bold">{title}</h2>
  <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
    确定
  </button>
</div>
```

### 5.3 类型定义

```typescript
// src/types/user.ts
export interface User {
  id: number
  name: string
  email: string
  createdAt: string
}

export interface CreateUserDto {
  name: string
  email: string
}
```

## 6. 测试

### 6.1 单元测试

```typescript
import { render, screen } from '@testing-library/react'
import { UserList } from './UserList'

describe('UserList', () => {
  it('should render users', () => {
    const users = [{ id: 1, name: '张三', email: 'test@example.com' }]
    render(<UserList users={users} onSelect={() => {}} />)
    expect(screen.getByText('张三')).toBeInTheDocument()
  })
})
```

### 6.2 运行测试

```bash
npm run test
```

## 7. 构建部署

### 7.1 本地构建

```bash
npm run build
```

### 7.2 预览

```bash
npm run preview
```

### 7.3 部署

```bash
# Docker
make docker-up

# K8s
make k8s-deploy
```

## 8. 权限

作为前端开发，你拥有以下权限:
- `ui:develop` - UI 开发
- `component:create` - 组件创建
- `style:edit` - 样式编辑
- `frontend:deploy` - 前端部署

## 9. 最佳实践

### 9.1 性能优化

- 使用 React.memo 避免不必要的渲染
- 使用 useMemo/useCallback 缓存计算结果
- 懒加载路由和组件
- 图片优化

### 9.2 代码组织

```
src/
├── components/     # 通用组件
├── pages/          # 页面组件
├── api/            # API 调用
├── stores/         # 状态管理
├── types/          # 类型定义
├── utils/          # 工具函数
└── styles/         # 全局样式
```

### 9.3 错误处理

```typescript
try {
  await userApi.createUser(data)
  message.success('创建成功')
} catch (error) {
  message.error('创建失败')
  console.error(error)
}
```
