# 前端开发专属工作流

## 1. UI 开发工作流

### 流程概览
需求理解 → 组件设计 → 编码实现 → 单元测试 → 集成测试 → Code Review → 部署

### 详细步骤

#### 1.1 需求理解
**目标**: 充分理解 UI 需求和交互逻辑

**输入**:
- 产品需求文档（PRD）
- UI 设计稿（Figma/Sketch）
- 交互原型
- API 接口文档

**执行**:
1. 阅读需求文档，理解业务逻辑
2. 查看设计稿，确认 UI 细节
3. 与产品经理确认交互流程
4. 与后端开发确认 API 接口
5. 识别技术难点和风险

**输出**:
- 需求理解文档
- 技术方案草案
- 风险评估

**检查点**:
- [ ] 是否理解所有业务逻辑？
- [ ] 是否确认所有交互细节？
- [ ] 是否确认 API 接口？
- [ ] 是否识别技术难点？

#### 1.2 组件设计
**目标**: 设计组件结构和状态管理方案

**执行**:
1. 拆分页面为组件树
2. 设计组件 Props 接口
3. 设计状态管理方案
4. 设计数据流和副作用
5. 评估性能和可复用性

**输出**:
- 组件结构图
- Props 类型定义
- 状态管理设计
- 技术方案文档

**示例**:
```typescript
// 组件结构
UserManagement/
├── UserList/
│   ├── UserTable/
│   ├── UserFilter/
│   └── UserPagination/
├── UserDetail/
│   ├── UserInfo/
│   ├── UserRoles/
│   └── UserActivity/
└── UserForm/
    ├── BasicInfo/
    └── RoleSelector/

// Props 设计
interface UserListProps {
  filters?: UserFilters;
  onUserSelect?: (user: User) => void;
  onUserEdit?: (userId: string) => void;
  onUserDelete?: (userId: string) => void;
}

// 状态管理设计
const useUserStore = create<UserStore>((set) => ({
  users: [],
  selectedUser: null,
  filters: {},
  fetchUsers: async () => { /* ... */ },
  selectUser: (user) => set({ selectedUser: user }),
  updateFilters: (filters) => set({ filters }),
}));
```

**检查点**:
- [ ] 组件职责是否单一？
- [ ] Props 接口是否清晰？
- [ ] 状态管理是否合理？
- [ ] 是否考虑性能优化？

#### 1.3 编码实现
**目标**: 实现高质量的前端代码

**执行**:
1. 创建组件文件和目录结构
2. 实现组件逻辑和 UI
3. 实现状态管理和数据流
4. 实现样式和响应式布局
5. 实现错误处理和加载状态
6. 添加代码注释和文档

**最佳实践**:
```typescript
// 1. 使用 TypeScript 严格模式
interface UserCardProps {
  user: User;
  onEdit: (userId: string) => void;
  onDelete: (userId: string) => void;
}

export const UserCard: FC<UserCardProps> = ({ user, onEdit, onDelete }) => {
  // 2. 使用自定义 Hooks 封装逻辑
  const { isDeleting, handleDelete } = useUserDelete(user.id, onDelete);

  // 3. 使用 useCallback 优化性能
  const handleEditClick = useCallback(() => {
    onEdit(user.id);
  }, [user.id, onEdit]);

  // 4. 提供加载和错误状态
  if (isDeleting) {
    return <LoadingSpinner />;
  }

  // 5. 使用语义化 HTML 和 ARIA
  return (
    <article className="user-card" aria-label={`用户 ${user.name}`}>
      <header>
        <h3>{user.name}</h3>
        <span className="user-role">{user.role}</span>
      </header>

      <div className="user-actions">
        <button
          onClick={handleEditClick}
          aria-label="编辑用户"
        >
          编辑
        </button>
        <button
          onClick={handleDelete}
          aria-label="删除用户"
          disabled={isDeleting}
        >
          删除
        </button>
      </div>
    </article>
  );
};
```

**检查点**:
- [ ] 代码是否符合 TypeScript 规范？
- [ ] 是否遵循 ESLint 规则？
- [ ] 是否有适当的错误处理？
- [ ] 是否有加载状态？
- [ ] 是否支持可访问性？

#### 1.4 单元测试
**目标**: 确保组件功能正确

**执行**:
1. 编写渲染测试
2. 编写 Props 测试
3. 编写交互测试
4. 编写边界测试
5. 检查测试覆盖率

**示例**:
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { UserCard } from './user-card';

describe('UserCard', () => {
  const mockUser = {
    id: '1',
    name: 'John Doe',
    role: 'Admin',
  };

  const mockOnEdit = vi.fn();
  const mockOnDelete = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders user information', () => {
    render(<UserCard user={mockUser} onEdit={mockOnEdit} onDelete={mockOnDelete} />);

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('Admin')).toBeInTheDocument();
  });

  it('calls onEdit when edit button is clicked', () => {
    render(<UserCard user={mockUser} onEdit={mockOnEdit} onDelete={mockOnDelete} />);

    fireEvent.click(screen.getByLabelText('编辑用户'));
    expect(mockOnEdit).toHaveBeenCalledWith('1');
  });

  it('shows loading state when deleting', async () => {
    render(<UserCard user={mockUser} onEdit={mockOnEdit} onDelete={mockOnDelete} />);

    fireEvent.click(screen.getByLabelText('删除用户'));
    await waitFor(() => {
      expect(screen.getByRole('status')).toBeInTheDocument();
    });
  });
});
```

**检查点**:
- [ ] 测试覆盖率 > 80%？
- [ ] 是否测试所有交互？
- [ ] 是否测试边界情况？
- [ ] 测试是否可维护？

#### 1.5 集成测试
**目标**: 确保组件集成正确

**执行**:
1. 测试组件间交互
2. 测试数据流
3. 测试路由跳转
4. 测试 API 调用

**示例**:
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { UserManagement } from './user-management';

describe('UserManagement Integration', () => {
  const queryClient = new QueryClient();

  it('loads and displays users', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <UserManagement />
      </QueryClientProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
  });

  it('filters users when filter is applied', async () => {
    render(
      <QueryClientProvider client={queryClient}>
        <UserManagement />
      </QueryClientProvider>
    );

    fireEvent.change(screen.getByLabelText('搜索用户'), {
      target: { value: 'John' },
    });

    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
      expect(screen.queryByText('Jane Smith')).not.toBeInTheDocument();
    });
  });
});
```

**检查点**:
- [ ] 是否测试关键用户流程？
- [ ] 是否测试错误场景？
- [ ] 是否测试加载状态？

#### 1.6 Code Review
**目标**: 确保代码质量

**执行**:
1. 提交 Pull Request
2. 运行自动化检查（CI）
3. 同行评审
4. 架构师审批（如需要）
5. 修复反馈问题
6. 合并代码

**PR 模板**:
```markdown
## 变更说明
实现用户管理模块的 UI 界面

## 变更内容
- 新增 UserList 组件
- 新增 UserDetail 组件
- 新增 UserForm 组件
- 实现用户 CRUD 功能

## 测试
- [x] 单元测试通过
- [x] 集成测试通过
- [x] 手动测试通过

## 截图
[附上 UI 截图]

## 检查清单
- [x] 代码符合规范
- [x] 测试覆盖率 > 80%
- [x] 无 ESLint 错误
- [x] 无 TypeScript 错误
- [x] 支持可访问性
- [x] 性能优化完成
```

**检查点**:
- [ ] CI 检查是否通过？
- [ ] 是否有同行评审？
- [ ] 是否修复所有反馈？

#### 1.7 部署
**目标**: 将代码部署到目标环境

**执行**:
1. 合并代码到主分支
2. 触发 CI/CD 流程
3. 构建生产版本
4. 部署到测试环境
5. 验证功能
6. 部署到生产环境

**检查点**:
- [ ] 构建是否成功？
- [ ] 测试环境是否正常？
- [ ] 生产环境是否正常？

---

## 2. 组件开发工作流

### 流程概览
组件设计 → Props 定义 → 实现 → 测试 → 文档 → 发布

### 详细步骤

#### 2.1 组件设计
**目标**: 设计可复用的组件

**执行**:
1. 分析组件使用场景
2. 设计组件 API
3. 设计组件变体
4. 设计组件状态
5. 评估可复用性

**设计原则**:
- **单一职责**: 组件只做一件事
- **可组合**: 组件可以组合使用
- **可配置**: 通过 Props 配置行为
- **可扩展**: 支持自定义样式和行为

**示例**:
```typescript
// 设计 Button 组件
// 1. 使用场景：表单提交、操作触发、导航跳转
// 2. 变体：primary, secondary, outline, ghost
// 3. 尺寸：sm, md, lg
// 4. 状态：normal, hover, active, disabled, loading
```

#### 2.2 Props 定义
**目标**: 定义清晰的组件接口

**执行**:
1. 定义必需 Props
2. 定义可选 Props
3. 定义默认值
4. 添加 Props 注释
5. 考虑向后兼容

**示例**:
```typescript
interface ButtonProps {
  /** 按钮内容 */
  children: React.ReactNode;

  /** 按钮变体 */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';

  /** 按钮尺寸 */
  size?: 'sm' | 'md' | 'lg';

  /** 是否禁用 */
  disabled?: boolean;

  /** 是否加载中 */
  loading?: boolean;

  /** 按钮类型 */
  type?: 'button' | 'submit' | 'reset';

  /** 点击事件 */
  onClick?: (event: React.MouseEvent<HTMLButtonElement>) => void;

  /** 自定义类名 */
  className?: string;

  /** 左侧图标 */
  leftIcon?: React.ReactNode;

  /** 右侧图标 */
  rightIcon?: React.ReactNode;
}
```

#### 2.3 实现
**目标**: 实现高质量的组件

**执行**:
1. 实现组件逻辑
2. 实现样式系统
3. 实现可访问性
4. 实现性能优化
5. 添加注释和文档

**示例**:
```typescript
import { forwardRef } from 'react';
import { cn } from '@/utils/cn';
import { Loader } from '@/components/ui/loader';

const buttonVariants = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700',
  secondary: 'bg-gray-600 text-white hover:bg-gray-700',
  outline: 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50',
  ghost: 'text-blue-600 hover:bg-blue-50',
};

const buttonSizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      disabled = false,
      loading = false,
      type = 'button',
      onClick,
      className,
      leftIcon,
      rightIcon,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        type={type}
        disabled={isDisabled}
        onClick={onClick}
        className={cn(
          'inline-flex items-center justify-center gap-2',
          'rounded-lg font-medium transition-colors',
          'focus:outline-none focus:ring-2 focus:ring-offset-2',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          buttonVariants[variant],
          buttonSizes[size],
          className
        )}
        {...props}
      >
        {loading && <Loader size="sm" />}
        {!loading && leftIcon}
        {children}
        {!loading && rightIcon}
      </button>
    );
  }
);

Button.displayName = 'Button';
```

#### 2.4 测试
**目标**: 确保组件质量

**执行**:
1. 编写单元测试
2. 测试所有变体
3. 测试所有状态
4. 测试可访问性
5. 检查覆盖率

#### 2.5 文档
**目标**: 提供清晰的使用文档

**执行**:
1. 编写 README
2. 编写使用示例
3. 编写 Storybook 故事
4. 生成 API 文档

**Storybook 示例**:
```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Primary Button',
    variant: 'primary',
  },
};

export const WithIcons: Story = {
  args: {
    children: 'Save',
    leftIcon: <SaveIcon />,
  },
};

export const Loading: Story = {
  args: {
    children: 'Loading',
    loading: true,
  },
};
```

#### 2.6 发布
**目标**: 发布组件供使用

**执行**:
1. 更新版本号
2. 更新 CHANGELOG
3. 提交代码
4. 发布到组件库
5. 通知团队

---

## 3. 性能优化工作流

### 流程概览
性能分析 → 瓶颈识别 → 优化方案 → 实施验证 → 监控跟踪

### 详细步骤

#### 3.1 性能分析
**目标**: 识别性能问题

**工具**:
- Chrome DevTools Performance
- React DevTools Profiler
- Lighthouse
- WebPageTest

**执行**:
1. 录制性能 Profile
2. 分析加载时间
3. 分析渲染性能
4. 分析内存使用
5. 生成性能报告

**指标**:
- **FCP** (First Contentful Paint): < 1.8s
- **LCP** (Largest Contentful Paint): < 2.5s
- **FID** (First Input Delay): < 100ms
- **CLS** (Cumulative Layout Shift): < 0.1
- **TTI** (Time to Interactive): < 3.8s

#### 3.2 瓶颈识别
**目标**: 找出性能瓶颈

**常见瓶颈**:
- 大型 bundle 体积
- 不必要的重渲染
- 未优化的图片
- 阻塞的 JavaScript
- 未使用的代码
- 慢速 API 请求

**分析方法**:
```typescript
// 1. 使用 React DevTools Profiler
import { Profiler } from 'react';

<Profiler id="UserList" onRender={onRenderCallback}>
  <UserList />
</Profiler>

// 2. 使用 Performance API
const start = performance.now();
// 执行操作
const end = performance.now();
console.log(`耗时: ${end - start}ms`);

// 3. 使用 webpack-bundle-analyzer
npm run build -- --analyze
```

#### 3.3 优化方案
**目标**: 制定优化策略

**常见优化**:

**代码分割**:
```typescript
// 路由懒加载
const Dashboard = lazy(() => import('./pages/dashboard'));

// 组件懒加载
const HeavyComponent = lazy(() => import('./components/heavy-component'));
```

**图片优化**:
```typescript
// 使用 next/image 或类似工具
<Image
  src="/hero.jpg"
  alt="Hero"
  width={800}
  height={600}
  loading="lazy"
  placeholder="blur"
/>
```

**缓存优化**:
```typescript
// 使用 React Query 缓存
const { data } = useQuery({
  queryKey: ['users'],
  queryFn: fetchUsers,
  staleTime: 5 * 60 * 1000, // 5 分钟
  cacheTime: 10 * 60 * 1000, // 10 分钟
});
```

**渲染优化**:
```typescript
// 使用 memo
const ExpensiveComponent = memo(({ data }) => {
  return <div>{/* ... */}</div>;
});

// 使用 useMemo
const sortedData = useMemo(() => {
  return data.sort((a, b) => a.value - b.value);
}, [data]);

// 使用 useCallback
const handleClick = useCallback(() => {
  console.log('clicked');
}, []);
```

#### 3.4 实施验证
**目标**: 实施优化并验证效果

**执行**:
1. 实施优化方案
2. 运行性能测试
3. 对比优化前后
4. 验证功能正常
5. 记录优化结果

**验证清单**:
- [ ] 性能指标是否改善？
- [ ] 功能是否正常？
- [ ] 是否引入新问题？
- [ ] 用户体验是否提升？

#### 3.5 监控跟踪
**目标**: 持续监控性能

**执行**:
1. 配置性能监控
2. 设置告警阈值
3. 定期查看报告
4. 持续优化改进

**监控工具**:
- Sentry Performance
- Google Analytics
- New Relic
- DataDog RUM

---

## 4. 前端部署工作流

### 流程概览
构建 → 测试 → 部署 → 验证 → 监控

### 详细步骤

#### 4.1 构建
**目标**: 生成生产版本

**执行**:
```bash
# 1. 安装依赖
npm ci

# 2. 运行 lint
npm run lint

# 3. 运行测试
npm run test

# 4. 构建生产版本
npm run build

# 5. 分析 bundle
npm run analyze
```

**检查点**:
- [ ] 构建是否成功？
- [ ] 是否有 lint 错误？
- [ ] 测试是否通过？
- [ ] Bundle 大小是否合理？

#### 4.2 测试
**目标**: 验证构建产物

**执行**:
1. 本地预览构建产物
2. 运行 E2E 测试
3. 检查资源加载
4. 验证功能正常

```bash
# 预览构建产物
npm run preview

# 运行 E2E 测试
npm run test:e2e
```

#### 4.3 部署
**目标**: 部署到目标环境

**部署策略**:
- **开发环境**: 自动部署（每次 push）
- **测试环境**: 自动部署（合并到 develop）
- **生产环境**: 手动触发（合并到 main）

**CI/CD 配置**:
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm run test

      - name: Build
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.API_URL }}

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
          vercel-args: '--prod'
```

#### 4.4 验证
**目标**: 验证部署成功

**执行**:
1. 访问部署 URL
2. 检查页面加载
3. 验证核心功能
4. 检查错误日志
5. 验证性能指标

**验证清单**:
- [ ] 页面是否正常加载？
- [ ] 核心功能是否正常？
- [ ] 是否有 JavaScript 错误？
- [ ] 性能指标是否正常？

#### 4.5 监控
**目标**: 持续监控应用状态

**监控内容**:
- 错误率
- 性能指标
- 用户行为
- 资源加载

**告警配置**:
```typescript
// Sentry 配置
Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,
  beforeSend(event) {
    // 过滤敏感信息
    return event;
  },
});

// 性能监控
Sentry.setTag('page', window.location.pathname);
Sentry.setUser({ id: user.id });
```

---

## 5. Bug 修复工作流

### 流程概览
Bug 报告 → 问题复现 → 原因分析 → 修复实现 → 测试验证 → 部署上线

### 详细步骤

#### 5.1 Bug 报告
**目标**: 记录 Bug 信息

**Bug 模板**:
```markdown
## Bug 描述
[清晰描述 Bug]

## 复现步骤
1. 打开页面
2. 点击按钮
3. 观察结果

## 预期行为
[应该发生什么]

## 实际行为
[实际发生了什么]

## 环境信息
- 浏览器: Chrome 120
- 操作系统: macOS 14
- 版本: v1.2.3

## 截图/视频
[附上截图或视频]

## 错误日志
[附上错误日志]
```

#### 5.2 问题复���
**目标**: 在本地复现 Bug

**执行**:
1. 按照步骤复现
2. 检查控制台错误
3. 使用 debugger 调试
4. 记录复现条件

#### 5.3 原因分析
**目标**: 找出 Bug 根因

**分析方法**:
- 检查代码逻辑
- 检查状态管理
- 检查 API 调用
- 检查浏览器兼容性
- 检查依赖库版本

#### 5.4 修复实现
**目标**: 修复 Bug

**执行**:
1. 编写修复代码
2. 添加防御性代码
3. 添加错误处理
4. 更新相关文档

#### 5.5 测试验证
**目标**: 验证修复有效

**执行**:
1. 验证 Bug 已修复
2. 运行相关测试
3. 添加回归测试
4. 检查是否引入新问题

#### 5.6 部署上线
**目标**: 将修复部署到生产

**执行**:
1. 提交 PR
2. Code Review
3. 合并代码
4. 部署到生产
5. 验证修复生效

---

## 工作流最佳实践

### 1. 使用 Git 分支策略
```bash
# 功能开发
git checkout -b feature/user-management

# Bug 修复
git checkout -b fix/login-error

# 紧急修复
git checkout -b hotfix/security-patch
```

### 2. 编写清晰的 Commit 信息
```bash
# 功能
git commit -m "feat: 添加用户管理模块"

# 修复
git commit -m "fix: 修复登录页面样式问题"

# 优化
git commit -m "perf: 优化列表渲染性能"

# 重构
git commit -m "refactor: 重构用户状态管理"
```

### 3. 使用 PR 模板
确保每个 PR 包含：
- 变更说明
- 测试结果
- 截图/视频
- 检查清单

### 4. 自动化检查
配置 CI/CD 自动运行：
- Lint 检查
- 类型检查
- 单元测试
- E2E 测试
- 构建验证

### 5. 持续改进
- 定期回顾工作流
- 收集团队反馈
- 优化流程效率
- 更新最佳实践
