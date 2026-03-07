#!/usr/bin/env python3
"""
Phase 5: 前端代码生成

生成前端代码骨架、页面组件、路由配置和状态管理
"""

from pathlib import Path
from typing import Dict


def execute(context: Dict) -> Dict:
    """执行前端代码生成"""
    project_path = context["project_path"]
    phase_results = context["phase_results"]

    # 获取业务模块和 API 信息
    business_agents = phase_results.get("business-agent-gen", {}).get("business_agents", [])
    api_endpoints = phase_results.get("backend-gen", {}).get("api_endpoints", [])

    print("🎨 生成前端代码...")

    frontend_path = project_path / "src" / "frontend"

    # 创建前端目录结构
    directories = [
        "src/pages",
        "src/components",
        "src/services",
        "src/stores",
        "src/routes",
        "src/utils",
        "public"
    ]

    for dir_path in directories:
        (frontend_path / dir_path).mkdir(parents=True, exist_ok=True)

    # 生成 package.json
    generate_package_json(frontend_path, context["project_name"])

    # 生成 vite.config.ts
    generate_vite_config(frontend_path)

    # 生成 tsconfig.json
    generate_tsconfig(frontend_path)

    # 生成工具函数
    generate_utils(frontend_path)

    # 为每个业务模块生成前端代码
    generated_files = []
    routes = []

    for agent in business_agents:
        agent_name = agent["name"]
        display_name = agent["displayName"]

        # 生成页面组件
        generate_pages(frontend_path, agent_name, display_name)
        generated_files.extend([
            f"src/pages/{agent_name}/List.tsx",
            f"src/pages/{agent_name}/Detail.tsx"
        ])

        # 生成 API 服务
        generate_service(frontend_path, agent_name, display_name)
        generated_files.append(f"src/services/{agent_name}.ts")

        # 生成状态管理
        generate_store(frontend_path, agent_name, display_name)
        generated_files.append(f"src/stores/{agent_name}Store.ts")

        routes.extend([
            f"/{agent_name}",
            f"/{agent_name}/:id"
        ])

    # 生成路由配置
    generate_routes(frontend_path, business_agents)
    generated_files.append("src/routes/index.tsx")

    # 生成主入口
    generate_main(frontend_path)
    generated_files.extend(["src/App.tsx", "src/main.tsx"])

    print(f"\n✅ 已生成 {len(generated_files)} 个前端文件")

    return {
        "generated_files": generated_files,
        "routes": routes,
        "components": [f"{agent['name']}List" for agent in business_agents]
    }


def generate_package_json(frontend_path: Path, project_name: str):
    """生成 package.json"""
    content = f'''{{
  "name": "{project_name}-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "antd": "^5.12.0",
    "zustand": "^4.4.7",
    "axios": "^1.6.2"
  }},
  "devDependencies": {{
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }}
}}
'''

    with open(frontend_path / "package.json", "w") as f:
        f.write(content)
    print("  ✓ package.json")


def generate_vite_config(frontend_path: Path):
    """生成 vite.config.ts"""
    content = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
'''

    with open(frontend_path / "vite.config.ts", "w") as f:
        f.write(content)
    print("  ✓ vite.config.ts")


def generate_tsconfig(frontend_path: Path):
    """生成 tsconfig.json"""
    content = '''{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
'''

    with open(frontend_path / "tsconfig.json", "w") as f:
        f.write(content)
    print("  ✓ tsconfig.json")


def generate_utils(frontend_path: Path):
    """生成工具函数"""
    # request.ts
    request_content = '''import axios from 'axios';

const request = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
});

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('Request failed:', error);
    return Promise.reject(error);
  }
);

export default request;
'''

    with open(frontend_path / "src" / "utils" / "request.ts", "w") as f:
        f.write(request_content)
    print("  ✓ utils/request.ts")


def generate_pages(frontend_path: Path, agent_name: str, display_name: str):
    """生成页面组件"""
    pages_path = frontend_path / "src" / "pages" / agent_name
    pages_path.mkdir(parents=True, exist_ok=True)

    # List.tsx
    list_content = f'''import {{ useEffect }} from 'react';
import {{ Table, Button, Space }} from 'antd';
import {{ useNavigate }} from 'react-router-dom';
import {{ use{agent_name.title().replace('-', '')}Store }} from '@/stores/{agent_name}Store';

export default function {agent_name.title().replace('-', '')}List() {{
  const navigate = useNavigate();
  const {{ items, loading, fetchList }} = use{agent_name.title().replace('-', '')}Store();

  useEffect(() => {{
    fetchList();
  }}, []);

  const columns = [
    {{ title: 'ID', dataIndex: 'id', key: 'id' }},
    {{ title: '名称', dataIndex: 'name', key: 'name' }},
    {{
      title: '操作',
      key: 'action',
      render: (_: any, record: any) => (
        <Space>
          <Button type="link" onClick={{() => navigate(`/{agent_name}/${{record.id}}`)}}>
            查看
          </Button>
        </Space>
      ),
    }},
  ];

  return (
    <div>
      <div style={{{{ marginBottom: 16 }}}}>
        <Button type="primary">新建</Button>
      </div>
      <Table
        dataSource={{items}}
        columns={{columns}}
        loading={{loading}}
        rowKey="id"
      />
    </div>
  );
}}
'''

    with open(pages_path / "List.tsx", "w") as f:
        f.write(list_content)

    # Detail.tsx
    detail_content = f'''import {{ useEffect }} from 'react';
import {{ useParams }} from 'react-router-dom';
import {{ Descriptions, Spin }} from 'antd';
import {{ use{agent_name.title().replace('-', '')}Store }} from '@/stores/{agent_name}Store';

export default function {agent_name.title().replace('-', '')}Detail() {{
  const {{ id }} = useParams();
  const {{ current, loading, fetchDetail }} = use{agent_name.title().replace('-', '')}Store();

  useEffect(() => {{
    if (id) {{
      fetchDetail(Number(id));
    }}
  }}, [id]);

  if (loading) return <Spin />;
  if (!current) return <div>未找到数据</div>;

  return (
    <Descriptions title="{display_name}详情" bordered>
      <Descriptions.Item label="ID">{{current.id}}</Descriptions.Item>
      <Descriptions.Item label="名称">{{current.name}}</Descriptions.Item>
    </Descriptions>
  );
}}
'''

    with open(pages_path / "Detail.tsx", "w") as f:
        f.write(detail_content)

    print(f"  ✓ pages/{agent_name}/")


def generate_service(frontend_path: Path, agent_name: str, display_name: str):
    """生成 API 服务"""
    content = f'''import request from '@/utils/request';

export interface {agent_name.title().replace('-', '')} {{
  id: number;
  name: string;
  created_at?: string;
  updated_at?: string;
}}

export const {agent_name.replace('-', '_')}Service = {{
  list: () => request.get<{agent_name.title().replace('-', '')}[]>('/{agent_name}'),
  get: (id: number) => request.get<{agent_name.title().replace('-', '')}>(`/{agent_name}/${{id}}`),
  create: (data: Partial<{agent_name.title().replace('-', '')}>) =>
    request.post<{agent_name.title().replace('-', '')}>('/{agent_name}', data),
  update: (id: number, data: Partial<{agent_name.title().replace('-', '')}>) =>
    request.put<{agent_name.title().replace('-', '')}>(`/{agent_name}/${{id}}`, data),
  delete: (id: number) => request.delete(`/{agent_name}/${{id}}`),
}};
'''

    with open(frontend_path / "src" / "services" / f"{agent_name}.ts", "w") as f:
        f.write(content)
    print(f"  ✓ services/{agent_name}.ts")


def generate_store(frontend_path: Path, agent_name: str, display_name: str):
    """生成状态管理"""
    content = f'''import {{ create }} from 'zustand';
import {{ {agent_name.replace('-', '_')}Service, {agent_name.title().replace('-', '')} }} from '@/services/{agent_name}';

interface {agent_name.title().replace('-', '')}Store {{
  items: {agent_name.title().replace('-', '')}[];
  current: {agent_name.title().replace('-', '')} | null;
  loading: boolean;
  fetchList: () => Promise<void>;
  fetchDetail: (id: number) => Promise<void>;
  create: (data: Partial<{agent_name.title().replace('-', '')}>) => Promise<void>;
}}

export const use{agent_name.title().replace('-', '')}Store = create<{agent_name.title().replace('-', '')}Store>((set) => ({{
  items: [],
  current: null,
  loading: false,

  fetchList: async () => {{
    set({{ loading: true }});
    try {{
      const items = await {agent_name.replace('-', '_')}Service.list();
      set({{ items, loading: false }});
    }} catch (error) {{
      console.error('Failed to fetch list:', error);
      set({{ loading: false }});
    }}
  }},

  fetchDetail: async (id: number) => {{
    set({{ loading: true }});
    try {{
      const current = await {agent_name.replace('-', '_')}Service.get(id);
      set({{ current, loading: false }});
    }} catch (error) {{
      console.error('Failed to fetch detail:', error);
      set({{ loading: false }});
    }}
  }},

  create: async (data) => {{
    await {agent_name.replace('-', '_')}Service.create(data);
  }},
}}));
'''

    with open(frontend_path / "src" / "stores" / f"{agent_name}Store.ts", "w") as f:
        f.write(content)
    print(f"  ✓ stores/{agent_name}Store.ts")


def generate_routes(frontend_path: Path, business_agents: list):
    """生成路由配置"""
    imports = []
    routes = []

    for agent in business_agents:
        agent_name = agent["name"]
        component_name = agent_name.title().replace('-', '')

        imports.append(f"import {component_name}List from '@/pages/{agent_name}/List';")
        imports.append(f"import {component_name}Detail from '@/pages/{agent_name}/Detail';")

        routes.append(f"    {{ path: '/{agent_name}', element: <{component_name}List /> }},")
        routes.append(f"    {{ path: '/{agent_name}/:id', element: <{component_name}Detail /> }},")

    content = f'''import {{ createBrowserRouter }} from 'react-router-dom';
{chr(10).join(imports)}

export const router = createBrowserRouter([
  {{
    path: '/',
    element: <div>Home</div>,
  }},
{chr(10).join(routes)}
]);
'''

    with open(frontend_path / "src" / "routes" / "index.tsx", "w") as f:
        f.write(content)
    print("  ✓ routes/index.tsx")


def generate_main(frontend_path: Path):
    """生成主入口"""
    # App.tsx
    app_content = '''import { RouterProvider } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { router } from './routes';

function App() {
  return (
    <ConfigProvider locale={zhCN}>
      <RouterProvider router={router} />
    </ConfigProvider>
  );
}

export default App;
'''

    with open(frontend_path / "src" / "App.tsx", "w") as f:
        f.write(app_content)
    print("  ✓ App.tsx")

    # main.tsx
    main_content = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import 'antd/dist/reset.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
'''

    with open(frontend_path / "src" / "main.tsx", "w") as f:
        f.write(main_content)
    print("  ✓ main.tsx")
