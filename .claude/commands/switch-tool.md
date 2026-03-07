# 切换 AI 工具链

在 Claude Code 和 Codex 之间切换开发工具。

## 用法
```
/switch-tool <claude|codex|codex-desktop>
```

## 优先级策略
1. **claude** (默认): Claude Code CLI，最强能力
2. **codex**: Codex CLI，本地开发降级方案
3. **codex-desktop**: Codex 桌面端，可视化操作

## 切换逻辑
- 检测当前网络/API 可用性
- 自动降级: claude → codex → codex-desktop
- 保持相同的规范约束（CLAUDE.md / standards/）
