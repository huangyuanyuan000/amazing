# TypeScript/JavaScript 代码规范

基于 Airbnb Style Guide，结合 Amazing 框架最佳实践。

## 1. 代码格式化

### 工具链
- **Prettier**: 代码格式化
- **ESLint**: 代码检查

### 配置文件
```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}

// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "react/react-in-jsx-scope": "off"
  }
}
```

## 2. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件 | kebab-case | `user-service.ts` |
| 组件文件 | PascalCase | `UserCard.tsx` |
| 类/接口 | PascalCase | `UserService`, `IUser` |
| 函数/变量 | camelCase | `getUserById()`, `userCount` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 类型/接口 | PascalCase | `User`, `UserCreateDto` |
| 枚举 | PascalCase | `UserRole.Admin` |

## 3. TypeScript 类型定义

### 接口 vs 类型别名
```typescript
// ✅ 接口用于对象结构
interface User {
  id: number;
  username: string;
  email: string;
  role: UserRole;
}

// ✅ 类型别名用于联合类型、工具类型
type UserId = number | string;
type UserResponse = User | null;
type PartialUser = Partial<User>;
```

### 严格类型
```typescript
// ✅ 避免 any
function getUser(id: number): User | null {
  return users.find(u => u.id === id) ?? null;
}

// ❌ 不要使用 any
function getUser(id: any): any {
  return users.find(u => u.id === id);
}
```

## 4. React 组件规范

### 函数组件
```typescript
// ✅ 使用 FC 类型 + Props 接口
interface UserCardProps {
  user: User;
  onEdit?: (id: number) => void;
}

export const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  return (
    <div className="user-card">
      <h3>{user.username}</h3>
      <p>{user.email}</p>
      {onEdit && <button onClick={() => onEdit(user.id)}>编辑</button>}
    </div>
  );
};
```

### Hooks 规范
```typescript
// ✅ 自定义 Hook
function useUser(userId: number) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUser(userId)
      .then(setUser)
      .finally(() => setLoading(false));
  }, [userId]);

  return { user, loading };
}

// ✅ 使用
const { user, loading } = useUser(123);
```

## 5. 异步处理

### Async/Await
```typescript
// ✅ 正确的错误处理
async function fetchUser(id: number): Promise<User> {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

### Promise 链
```typescript
// ✅ 并行请求
const [user, orders] = await Promise.all([
  fetchUser(userId),
  fetchOrders(userId),
]);

// ❌ 串行请求（性能差）
const user = await fetchUser(userId);
const orders = await fetchOrders(userId);
```

## 6. 状态管理（Zustand）

```typescript
// stores/userStore.ts
interface UserStore {
  users: User[];
  loading: boolean;
  fetchUsers: () => Promise<void>;
  addUser: (user: User) => void;
}

export const useUserStore = create<UserStore>((set) => ({
  users: [],
  loading: false,
  fetchUsers: async () => {
    set({ loading: true });
    const users = await api.getUsers();
    set({ users, loading: false });
  },
  addUser: (user) => set((state) => ({ users: [...state.users, user] })),
}));
```

## 7. API 调用

```typescript
// api/users.ts
export const userApi = {
  getAll: async (): Promise<User[]> => {
    const response = await fetch('/api/v1/users');
    return response.json();
  },

  getById: async (id: number): Promise<User> => {
    const response = await fetch(`/api/v1/users/${id}`);
    if (!response.ok) throw new Error('User not found');
    return response.json();
  },

  create: async (data: UserCreate): Promise<User> => {
    const response = await fetch('/api/v1/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return response.json();
  },
};
```

## 8. 错误处理

```typescript
// ✅ 自定义错误类
class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
    public data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

// ✅ 错误边界
class ErrorBoundary extends React.Component<Props, State> {
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}
```

## 9. 测试规范

```typescript
// UserCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { UserCard } from './UserCard';

describe('UserCard', () => {
  const mockUser: User = {
    id: 1,
    username: 'testuser',
    email: 'test@example.com',
    role: UserRole.User,
  };

  it('renders user information', () => {
    render(<UserCard user={mockUser} />);
    expect(screen.getByText('testuser')).toBeInTheDocument();
    expect(screen.getByText('test@example.com')).toBeInTheDocument();
  });

  it('calls onEdit when edit button clicked', () => {
    const onEdit = jest.fn();
    render(<UserCard user={mockUser} onEdit={onEdit} />);
    fireEvent.click(screen.getByText('编辑'));
    expect(onEdit).toHaveBeenCalledWith(1);
  });
});
```

## 10. 性能优化

```typescript
// ✅ useMemo 缓存计算结果
const expensiveValue = useMemo(() => {
  return computeExpensiveValue(data);
}, [data]);

// ✅ useCallback 缓存函数
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);

// ✅ React.memo 避免不必要的重渲染
export const UserCard = React.memo<UserCardProps>(({ user, onEdit }) => {
  // ...
});
```

## 11. 文件组织

```
src/
├── components/          # 可复用组件
│   ├── UserCard/
│   │   ├── index.tsx
│   │   ├── UserCard.test.tsx
│   │   └── types.ts
├── pages/              # 页面组件
│   └── UserListPage.tsx
├── stores/             # 状态管理
│   └── userStore.ts
├── api/                # API 调用
│   └── users.ts
├── hooks/              # 自定义 Hooks
│   └── useUser.ts
├── types/              # 类型定义
│   └── user.ts
└── utils/              # 工具函数
    └── format.ts
```

## 12. 禁止事项

- ❌ 使用 `var`（使用 `const`/`let`）
- ❌ 使用 `any` 类型
- ❌ 直接修改 state（使用不可变更新）
- ❌ 在循环中使用 `useEffect`/`useState`
- ❌ 忘记清理副作用（定时器、订阅）
- ❌ 内联样式（使用 CSS Modules 或 Tailwind）

## 13. 安全规范

```typescript
// ✅ XSS 防护
import DOMPurify from 'dompurify';
const sanitized = DOMPurify.sanitize(userInput);

// ✅ CSRF 防护
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
fetch('/api/users', {
  headers: { 'X-CSRF-Token': csrfToken },
});

// ✅ 敏感数据不存储在 localStorage
// 使用 httpOnly cookie 存储 token
```

## 自动化检查

```bash
# 格式化
npm run format  # prettier --write .

# Lint
npm run lint    # eslint . --ext .ts,.tsx

# 类型检查
npm run type-check  # tsc --noEmit

# 测试
npm test        # jest --coverage
```
