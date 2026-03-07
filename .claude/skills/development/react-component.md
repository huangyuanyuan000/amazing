# React Component Skill - React 组件规范

## 功能描述
提供 React 组件开发规范、Hooks 模式和组件设计最佳实践。

## 触发方式
- 新组件开发
- 组件重构
- 前端代码审查

## 核心内容

### 1. 组件分类
| 类型 | 职责 | 示例 |
|------|------|------|
| 页面组件 | 路由入口，数据获取 | UserListPage |
| 容器组件 | 状态管理，业务逻辑 | UserListContainer |
| 展示组件 | 纯 UI 渲染 | UserCard |
| 通用组件 | 可复用 UI 元素 | Button, Modal |

### 2. 组件模板
```tsx
interface UserCardProps {
  user: User;
  onEdit?: (id: string) => void;
}

export const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  return (
    <div className="user-card" role="article" aria-label={user.name}>
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      {onEdit && <button onClick={() => onEdit(user.id)}>编辑</button>}
    </div>
  );
};
```

### 3. Hooks 规范
- `useState`: 简单状态
- `useReducer`: 复杂状态逻辑
- `useEffect`: 副作用（数据获取、订阅）
- `useMemo/useCallback`: 性能优化（按需使用）
- 自定义 Hook: `use` 前缀，封装可复用逻辑

### 4. 文件组织
```
components/UserCard/
├── index.tsx         # 组件实现
├── UserCard.test.tsx # 测试
└── types.ts          # 类型定义
```

## 示例
### 自定义 Hook
```tsx
function useUsers() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetchUsers().then(setUsers).finally(() => setLoading(false));
  }, []);
  return { users, loading };
}
```

## 进化能力
- 组件模式库持续扩充
- 从代码审查中提炼规范
- 新 React 特性自动适配
