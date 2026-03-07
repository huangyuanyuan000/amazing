# State Management Skill - 前端状态管理

## 功能描述
提供前端状态管理方案选择、实现模式和最佳实践。

## 触发方式
- 新项目状态管理设计
- 状态管理重构
- 性能优化

## 核心内容

### 1. 方案选择
| 方案 | 适用场景 | 复杂度 |
|------|----------|--------|
| useState/useReducer | 组件内状态 | 低 |
| Context API | 跨组件共享（低频更新） | 低 |
| Zustand | 中小型应用全局状态 | 中 |
| Redux Toolkit | 大型应用复杂状态 | 高 |
| Jotai/Recoil | 原子化状态管理 | 中 |

### 2. Zustand 模式（推荐）
```typescript
import { create } from 'zustand';

interface UserStore {
  users: User[];
  loading: boolean;
  fetchUsers: () => Promise<void>;
}

export const useUserStore = create<UserStore>((set) => ({
  users: [],
  loading: false,
  fetchUsers: async () => {
    set({ loading: true });
    const users = await api.getUsers();
    set({ users, loading: false });
  },
}));
```

### 3. 状态设计原则
- 最小化状态：能计算的不存储
- 单一数据源：避免状态重复
- 不可变更新：使用 immer 或展开运算符
- 状态归一化：扁平化嵌套数据

### 4. 服务端状态
使用 TanStack Query 管理服务端状态：自动缓存、后台刷新、乐观更新。

## 示例
```tsx
function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => api.getUsers(),
    staleTime: 5 * 60 * 1000,
  });
}
```

## 进化能力
- 状态管理模式持续优化
- 性能优化策略积累
- 新方案自动评估
