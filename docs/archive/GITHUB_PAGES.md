# GitHub Pages 部署指南

## 📖 概述

Amazing 项目的架构图和文档已部署到 GitHub Pages，可以在线访问。

---

## 🌐 在线访问

### 主页
**https://z58362026.github.io/amazing/**

### 架构图
- **AI 协同开发范式**: https://z58362026.github.io/amazing/
- **系统架构**: https://z58362026.github.io/amazing/docs/architecture/system-architecture.html
- **开发流程**: https://z58362026.github.io/amazing/docs/workflows/development.html
- **Bug 修复流程**: https://z58362026.github.io/amazing/docs/workflows/bug-fix.html

---

## ⚙️ 部署步骤

### 1. 启用 GitHub Pages

1. 访问 GitHub 仓库: https://github.com/z58362026/amazing
2. 点击 **Settings** (设置)
3. 在左侧菜单找到 **Pages**
4. 在 **Source** 下选择:
   - Branch: `main`
   - Folder: `/ (root)`
5. 点击 **Save** (保存)
6. 等待几分钟，GitHub Pages 会自动部署

### 2. 验证部署

访问: https://z58362026.github.io/amazing/

如果看到 "Amazing - AI 协同开发范式架构" 页面，说明部署成功！

---

## 📁 文件结构

```
amazing/
├── index.html                              # 主页 (AI 范式架构)
├── .nojekyll                               # 禁用 Jekyll 处理
├── docs/
│   ├── architecture/
│   │   └── system-architecture.html        # 系统架构图
│   └── workflows/
│       ├── development.html                # 开发流程图
│       └── bug-fix.html                    # Bug 修复流程图
└── README.md                               # 项目文档
```

---

## 🎨 自定义域名 (可选)

### 1. 添加 CNAME 文件

```bash
echo "amazing.yourdomain.com" > CNAME
git add CNAME
git commit -m "docs: 添加自定义域名"
git push
```

### 2. 配置 DNS

在你的域名提供商添加 CNAME 记录:

```
Type: CNAME
Name: amazing
Value: z58362026.github.io
```

### 3. 在 GitHub 设置自定义域名

1. 进入 Settings → Pages
2. 在 **Custom domain** 输入: `amazing.yourdomain.com`
3. 点击 **Save**
4. 勾选 **Enforce HTTPS**

---

## 🔄 更新部署

每次推送到 `main` 分支，GitHub Pages 会自动更新:

```bash
# 修改 HTML 文件
vim index.html

# 提交更新
git add index.html
git commit -m "docs: 更新架构图"
git push origin main

# 等待 1-2 分钟，访问网站查看更新
```

---

## 🐛 故障排查

### 问题 1: 404 错误

**原因**: GitHub Pages 未启用或分支选择错误

**解决**:
1. 检查 Settings → Pages 是否已启用
2. 确认选择了 `main` 分支和 `/ (root)` 目录
3. 等待几分钟让 GitHub 完成部署

### 问题 2: 样式丢失

**原因**: Jekyll 处理了 HTML 文件

**解决**:
1. 确保项目根目录有 `.nojekyll` 文件
2. 重新推送代码

### 问题 3: 更新未生效

**原因**: 浏览器缓存或 GitHub Pages 缓存

**解决**:
1. 清除浏览器缓存 (Ctrl+Shift+R 或 Cmd+Shift+R)
2. 等待 5-10 分钟让 GitHub Pages 更新
3. 使用隐私模式访问

---

## 📊 访问统计 (可选)

### 添加 Google Analytics

在 `index.html` 的 `<head>` 标签中添加:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/z58362026/amazing
- **GitHub Pages 文档**: https://docs.github.com/en/pages
- **自定义域名**: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

---

## 📞 联系我们

- **Email**: 305068308@qq.com
- **Issues**: https://github.com/z58362026/amazing/issues

---

<div align="center">

**Made with ❤️ by Amazing Team**

</div>
