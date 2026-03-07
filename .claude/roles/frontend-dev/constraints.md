# 前端开发约束规则

## 代码规范

### TypeScript 规范

#### 类型定义
- **必须**: 所有函数参数和返回值必须有明确的类型定义
- **必须**: 所有组件 Props 必须定义接口或类型
- **必须**: 禁止使用 `any` 类型，特殊情况使用 `unknown`
- **推荐**: 使用 `type` 定义联合类型，使用 `interface` 定义对象类型
- **推荐**: 使用泛型提高代码复用性

```typescript
// ✅ 正确
interface UserProfileProps {
  userId: string;
  onUpdate?: (user: User) => void;
}

function UserProfile({ userId, onUpdate }: UserProfileProps) {
  // ...
}

// ❌ 错误
function UserProfile(props: any) {
  // ...
}
```

#### 命名规范
- **组件**: PascalCase（如 `UserProfile`, `ProductCard`）
- **函数/变量**: camelCase（如 `getUserData`, `isLoading`）
- **常量**: UPPER_SNAKE_CASE（如 `API_BASE_URL`, `MAX_RETRY_COUNT`）
- **类型/接口**: PascalCase（如 `User`, `ApiResponse`）
- **文件名**: kebab-case（如 `user-profile.tsx`, `api-client.ts`）

#### 文件组织
```
src/
├── components/          # 可复用组件
│   ├── ui/             # 基础 UI 组件
│   ├── forms/          # 表单组件
│   └── layouts/        # 布局组件
├── pages/              # 页面组件
├── hooks/              # 自定义 Hooks
├── stores/             # 状态管理
├── services/           # API 服务
├── utils/              # 工具函数
├── types/              # 类型定义
└── constants/          # 常量定义
```

### ESLint 规则

#### 必须遵循的规则
```json
{
  "rules": {
    "no-console": "warn",                    // 禁止 console，使用 logger
    "no-debugger": "error",                  // 禁止 debugger
    "no-unused-vars": "error",               // 禁止未使用的变量
    "prefer-const": "error",                 // 优先使用 const
    "react-hooks/rules-of-hooks": "error",   // Hooks 规则
    "react-hooks/exhaustive-deps": "warn",   // Hooks 依赖检查
    "@typescript-eslint/no-explicit-any": "error",  // 禁止 any
    "@typescript-eslint/explicit-function-return-type": "warn"  // 函数返回类型
  }
}
```

#### 代码风格
- **缩进**: 2 空格
- **引号**: 单引号
- **分号**: 必须使用
- **行宽**: 最大 100 字符
- **尾逗号**: 多行时必须使用

### Prettier 配置
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100,
  "arrowParens": "always"
}
```

## 组件规范

### 组件结构

#### 标准组件模板
```typescript
import { FC } from 'react';
import { cn } from '@/utils/cn';

// 1. Props 类型定义
interface ComponentNameProps {
  // 必需属性
  id: string;
  // 可选属性
  className?: string;
  // 回调函数
  onClick?: (id: string) => void;
}

// 2. 组件实现
export const ComponentName: FC<ComponentNameProps> = ({
  id,
  className,
  onClick
}) => {
  // 3. Hooks（按顺序）
  const [state, setState] = useState();
  const data = useQuery();
  const handleClick = useCallback(() => {}, []);

  // 4. 副作用
  useEffect(() => {}, []);

  // 5. 渲染逻辑
  return (
    <div className={cn('base-class', className)}>
      {/* JSX */}
    </div>
  );
};

// 6. 默认导出（可选）
export default ComponentName;
```

### Props 定义规范

#### 必须包含的内容
- **类型��义**: 所有 Props 必须有明确的类型
- **注释说明**: 复杂 Props 必须有注释
- **默认值**: 可选 Props 应该有默认值
- **验证**: 使用 Zod 或 PropTypes 进行运行时验证（可选）

```typescript
interface ButtonProps {
  /** 按钮文本 */
  children: React.ReactNode;
  /** 按钮变体 */
  variant?: 'primary' | 'secondary' | 'outline';
  /** 按钮尺寸 */
  size?: 'sm' | 'md' | 'lg';
  /** 是否禁用 */
  disabled?: boolean;
  /** 是否加载中 */
  loading?: boolean;
  /** 点击事件 */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;
  /** 自定义类名 */
  className?: string;
}

// 默认值
const defaultProps: Partial<ButtonProps> = {
  variant: 'primary',
  size: 'md',
  disabled: false,
  loading: false,
};
```

### 组件测试规范

#### 必须测试的内容
- **渲染测试**: 组件能否正常渲染
- **Props 测试**: Props 是否正确传递和生效
- **交互测试**: 用户交互是否正常工作
- **边界测试**: 边界情况和错误处理

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('disables when loading', () => {
    render(<Button loading>Click me</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});
```

#### 测试覆盖率要求
- **单元测试**: 覆盖率 > 80%
- **集成测试**: 核心流程必须覆盖
- **E2E 测试**: 关键用户路径必须覆盖

## 性能约束

### 加载性能

#### 首屏加载
- **必须**: 首屏加载时间 < 3 秒（3G 网络）
- **推荐**: 首屏加载时间 < 1.5 秒（4G 网络）
- **优化**: 使用代码分割和懒加载
- **优化**: 优化图片和资源大小

```typescript
// ✅ 正确：路由懒加载
const Dashboard = lazy(() => import('./pages/dashboard'));
const UserProfile = lazy(() => import('./pages/user-profile'));

// ❌ 错误：全部同步加载
import Dashboard from './pages/dashboard';
import UserProfile from './pages/user-profile';
```

#### 资源大小
- **必须**: 单个 JS bundle < 500KB（gzip 后）
- **必须**: 单个 CSS bundle < 100KB（gzip 后）
- **推荐**: 图片使用 WebP 格式，单张 < 200KB
- **推荐**: 使用 CDN 加载第三方库

### 运行时性能

#### 交互响应
- **必须**: 用户交互响应时间 < 100ms
- **必须**: 列表滚动帧率 > 60fps
- **推荐**: 使用防抖和节流优化高频事件
- **推荐**: 使用虚拟滚动处理长列表

```typescript
// ✅ 正确：使用防抖
const handleSearch = useDebouncedCallback((value: string) => {
  searchAPI(value);
}, 300);

// ❌ 错误：每次输入都触发
const handleSearch = (value: string) => {
  searchAPI(value);
};
```

#### 渲染优化
- **必须**: 避免不必要的重渲染
- **必须**: 合理使用 `memo`, `useMemo`, `useCallback`
- **推荐**: 使用 React DevTools Profiler 分析性能
- **推荐**: 使用 `key` 优化列表渲染

```typescript
// ✅ 正确：使用 memo 避免重渲染
const ExpensiveComponent = memo(({ data }: Props) => {
  return <div>{/* 复杂渲染逻辑 */}</div>;
});

// ✅ 正确：使用 useMemo 缓存计算结果
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// ✅ 正确：使用 useCallback 缓存函数
const handleClick = useCallback((id: string) => {
  console.log(id);
}, []);
```

### 内存管理
- **必须**: 组件卸载时清理定时器和事件监听
- **必须**: 避免内存泄漏
- **推荐**: 使用 `useEffect` 返回清理函数
- **推荐**: 使用 WeakMap 和 WeakSet 管理引用

```typescript
// ✅ 正确：清理副作用
useEffect(() => {
  const timer = setInterval(() => {
    // ...
  }, 1000);

  return () => {
    clearInterval(timer);
  };
}, []);

// ❌ 错误：未清理定时器
useEffect(() => {
  setInterval(() => {
    // ...
  }, 1000);
}, []);
```

## 可访问性约束

### 语义化 HTML
- **必须**: 使用语义化标签（`<header>`, `<nav>`, `<main>`, `<footer>`）
- **必须**: 使用正确的标题层级（`<h1>` 到 `<h6>`）
- **必须**: 表单元素必须有 `<label>`
- **推荐**: 使用 `<button>` 而不是 `<div>` 实现按钮

```tsx
// ✅ 正确
<button onClick={handleClick}>提交</button>

// ❌ 错误
<div onClick={handleClick}>提交</div>
```

### ARIA 标签
- **必须**: 交互元素必须有 `aria-label` 或可见文本
- **必须**: 动态内容必须有 `aria-live` 区域
- **必须**: 模态框必须有 `role="dialog"` 和 `aria-modal`
- **推荐**: 使用 `aria-describedby` 提供额外说明

```tsx
// ✅ 正确
<button aria-label="关闭对话框" onClick={onClose}>
  <XIcon />
</button>

<div role="alert" aria-live="polite">
  {errorMessage}
</div>

// ❌ 错误
<button onClick={onClose}>
  <XIcon />
</button>
```

### 键盘导航
- **必须**: 所有交互元素支持键盘访问
- **必须**: 焦点顺序符合逻辑
- **必须**: 焦点可见（不能移除 outline）
- **推荐**: 支持快捷键（Esc 关闭、Enter 确认等）

```tsx
// ✅ 正确：支持键盘事件
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleClick();
    }
  }}
>
  点击我
</div>
```

### 颜色对比度
- **必须**: 文本和背景对比度 ≥ 4.5:1（正常文本）
- **必须**: 文本和背景对比度 ≥ 3:1（大文本）
- **推荐**: 使用工具检查对比度（如 axe DevTools）
- **推荐**: 不仅依赖颜色传达信息

## 浏览器兼容性

### 支持的浏览器
- **必须**: Chrome 最新两个版本
- **必须**: Firefox 最新两个版本
- **必须**: Safari 最新两个版本
- **必须**: Edge 最新两个版本
- **可选**: IE 11（需要 polyfills）

### 兼容性检查
- **必须**: 使用 Browserslist 配置目标浏览器
- **必须**: 使用 Autoprefixer 自动添加前缀
- **推荐**: 使用 @babel/preset-env 自动 polyfill
- **推荐**: 在多个浏览器中测试

```json
// package.json
{
  "browserslist": [
    "last 2 Chrome versions",
    "last 2 Firefox versions",
    "last 2 Safari versions",
    "last 2 Edge versions"
  ]
}
```

### 渐进增强
- **必须**: 核心功能在所有浏览器中可用
- **推荐**: 使用 Feature Detection 而不是 Browser Detection
- **推荐**: 提供降级方案

```typescript
// ✅ 正确：Feature Detection
if ('IntersectionObserver' in window) {
  // 使用 IntersectionObserver
} else {
  // 降级方案
}

// ❌ 错误：Browser Detection
if (navigator.userAgent.includes('Chrome')) {
  // ...
}
```

## 安全约束

### XSS 防护
- **必须**: 禁止使用 `dangerouslySetInnerHTML`（特殊情况需审批）
- **必须**: 用户输入必须转义
- **必须**: 使用 Content Security Policy (CSP)
- **推荐**: 使用 DOMPurify 清理 HTML

```typescript
// ✅ 正确：使用 DOMPurify
import DOMPurify from 'dompurify';

const cleanHTML = DOMPurify.sanitize(userInput);
<div dangerouslySetInnerHTML={{ __html: cleanHTML }} />

// ❌ 错误：直接使用用户输入
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

### 敏感信息
- **必须**: 不在前端存储敏感信息（密码、密钥等）
- **必须**: 使用 HTTPS 传输数据
- **必须**: Token 存储在 HttpOnly Cookie 或 Memory
- **推荐**: 使用环境变量管理配置

### 依赖安全
- **必须**: 定期更新依赖库
- **必须**: 使用 `npm audit` 检查漏洞
- **推荐**: 使用 Dependabot 自动更新
- **推荐**: 锁定依赖版本（package-lock.json）

## 错误处理

### 错误边界
- **必须**: 使用 Error Boundary 捕获组件错误
- **必须**: 提供友好的错误提示
- **推荐**: 错误上报到监控系统
- **推荐**: 提供错误恢复机制

```typescript
// ✅ 正确：使用 Error Boundary
<ErrorBoundary fallback={<ErrorPage />}>
  <App />
</ErrorBoundary>
```

### 异步错误
- **必须**: 所有 Promise 必须处理 rejection
- **必须**: 使用 try-catch 捕获 async/await 错误
- **推荐**: 使用 React Query 的错误处理
- **推荐**: 提供重试机制

```typescript
// ✅ 正确
try {
  const data = await fetchData();
} catch (error) {
  handleError(error);
}

// ❌ 错误
const data = await fetchData(); // 未处理错误
```

## 文档要求

### 组件文档
- **必须**: 每个公共组件必须有使用文档
- **必须**: 文档包含 Props 说明和示例
- **推荐**: 使用 Storybook 展示组件
- **推荐**: 提供 TypeScript 类型定义

### 代码注释
- **必须**: 复杂逻辑必须有注释
- **必须**: 公共 API 必须有 JSDoc 注释
- **推荐**: 使用 TODO/FIXME 标记待办事项
- **推荐**: 注释解释"为什么"而不是"是什么"

```typescript
/**
 * 用户资料组件
 * @param userId - 用户 ID
 * @param onUpdate - 更新回调函数
 * @returns React 组件
 */
export function UserProfile({ userId, onUpdate }: UserProfileProps) {
  // 使用 SWR 缓存用户数据，避免重复请求
  const { data, error } = useSWR(`/api/users/${userId}`);

  // TODO: 添加骨架屏加载状态
  if (!data) return <Loading />;

  return <div>{/* ... */}</div>;
}
```

## 违规处理

### 警告级别
- **代码审查**: 指出问题，要求修改
- **自动检查**: ESLint/TypeScript 错误必须修复
- **性能问题**: 提供优化建议

### 阻断级别
- **安全漏洞**: 必须立即修复
- **严重性能问题**: 必须优化后才能合并
- **可访问性严重问题**: 必须修复后才能上线
- **测试覆盖率不足**: 必须补充测试

### 豁免流程
特殊情况需要豁免约束时：
1. 提交豁免申请，说明原因
2. 架构师审批
3. 记录豁免原因和风险
4. 设置技术债务跟踪
