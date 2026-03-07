#!/usr/bin/env python3
"""
HTML 架构图生成器

自动将 Markdown 文档转换为 HTML 架构图，支持：
- Mermaid.js 图表
- 统一的样式和导航
- GitHub Pages 部署
"""

import re
import markdown
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class HTMLGenerator:
    """HTML 架构图生成器"""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.docs_dir = project_path / "docs"
        self.html_dir = project_path / "docs" / "html"
        self.html_dir.mkdir(parents=True, exist_ok=True)

    def generate_from_markdown(self, md_file: Path, output_file: Optional[Path] = None) -> Path:
        """
        从 Markdown 生成 HTML

        Args:
            md_file: Markdown 文件路径
            output_file: 输出 HTML 文件路径（可选）

        Returns:
            生成的 HTML 文件路径
        """
        if not md_file.exists():
            raise FileNotFoundError(f"Markdown 文件不存在: {md_file}")

        # 读取 Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 确定输出路径
        if output_file is None:
            relative_path = md_file.relative_to(self.docs_dir)
            output_file = self.html_dir / relative_path.with_suffix('.html')

        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 转换为 HTML
        html_content = self._convert_to_html(md_content, md_file.stem)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✓ 生成 HTML: {output_file}")
        return output_file

    def _convert_to_html(self, md_content: str, title: str) -> str:
        """转换 Markdown 到 HTML"""
        # 使用 markdown 库转换
        html_body = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'codehilite']
        )

        # 检测 Mermaid 代码块
        has_mermaid = '```mermaid' in md_content

        # 生成完整 HTML
        html = self._generate_html_template(title, html_body, has_mermaid)

        return html

    def _generate_html_template(self, title: str, body: str, has_mermaid: bool = False) -> str:
        """生成 HTML 模板"""
        mermaid_script = """
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({ startOnLoad: true, theme: 'default' });
    </script>
""" if has_mermaid else ""

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Amazing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            font-size: 1.8em;
            margin-bottom: 5px;
        }}
        .header .breadcrumb {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .header .breadcrumb a {{
            color: white;
            text-decoration: none;
        }}
        .header .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 30px 20px;
        }}
        .content {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .content h1 {{
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .content h2 {{
            color: #667eea;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .content h3 {{
            color: #555;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .content p {{
            margin-bottom: 15px;
        }}
        .content ul, .content ol {{
            margin-left: 25px;
            margin-bottom: 15px;
        }}
        .content li {{
            margin-bottom: 8px;
        }}
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .content table th, .content table td {{
            padding: 12px;
            text-align: left;
            border: 1px solid #e8eef5;
        }}
        .content table th {{
            background: #f5f7fa;
            color: #667eea;
            font-weight: bold;
        }}
        .content table tr:hover {{
            background: #f8f9fa;
        }}
        .content pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        .content code {{
            background: #f5f7fa;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}
        .content pre code {{
            background: none;
            padding: 0;
        }}
        .mermaid {{
            text-align: center;
            margin: 30px 0;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>{mermaid_script}
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="breadcrumb">
            <a href="../index.html">首页</a> /
            <a href="index.html">架构文档</a> /
            {title}
        </div>
    </div>
    <div class="container">
        <div class="content">
            {body}
        </div>
    </div>
    <div class="footer">
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><a href="https://github.com/z58362026/amazing" target="_blank">Amazing Framework</a> | Made with ❤️ by Amazing Team</p>
    </div>
</body>
</html>"""
        return html

    def generate_index(self, docs: List[Dict[str, str]]):
        """
        生成索引页面

        Args:
            docs: 文档列表，每个文档包含 title, path, category
        """
        # 按分类组织文档
        categories = {}
        for doc in docs:
            category = doc.get('category', 'other')
            if category not in categories:
                categories[category] = []
            categories[category].append(doc)

        # 生成索引 HTML
        body = "<h1>架构文档</h1>\n"

        category_names = {
            'product': '📊 产品文档',
            'architecture': '🏗️ 架构文档',
            'development': '💻 开发文档',
            'testing': '🧪 测试文档',
            'operations': '📈 运营文档',
            'other': '📄 其他文档'
        }

        for category, docs_list in sorted(categories.items()):
            category_name = category_names.get(category, category)
            body += f"<h2>{category_name}</h2>\n<ul>\n"

            for doc in sorted(docs_list, key=lambda x: x['title']):
                body += f'  <li><a href="{doc["path"]}">{doc["title"]}</a></li>\n'

            body += "</ul>\n"

        html = self._generate_html_template("架构文档索引", body)

        index_file = self.html_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✓ 生成索引: {index_file}")

    def generate_all(self):
        """生成所有文档的 HTML"""
        print("🚀 生成所有 HTML 架构图\n")

        docs = []

        # 扫描所有 Markdown 文件
        for md_file in self.docs_dir.glob("**/*.md"):
            # 跳过 html 目录
            if 'html' in md_file.parts:
                continue

            # 确定分类
            relative_path = md_file.relative_to(self.docs_dir)
            category = relative_path.parts[0] if len(relative_path.parts) > 1 else 'other'

            # 生成 HTML
            html_file = self.generate_from_markdown(md_file)

            # 记录文档
            docs.append({
                'title': md_file.stem.replace('-', ' ').replace('_', ' ').title(),
                'path': html_file.relative_to(self.html_dir),
                'category': category
            })

        # 生成索引
        self.generate_index(docs)

        print(f"\n✅ 完成！共生成 {len(docs)} 个 HTML 文件")


def main():
    """CLI 入口"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="HTML 架构图生成器")
    parser.add_argument("--file", help="生成单个文件")
    parser.add_argument("--all", action="store_true", help="生成所有文件")

    args = parser.parse_args()

    project_path = Path.cwd()
    generator = HTMLGenerator(project_path)

    if args.file:
        md_file = Path(args.file)
        generator.generate_from_markdown(md_file)
    elif args.all:
        generator.generate_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
