# Commit 规范参考

本文档包含 Commit 消息的格式、类型定义和 Scope 命名规范。

## Commit 消息格式

```
<type>(<scope>): <subject>

<body>

Authored-By: Claude Code AI
```

## Commit 类型定义

| 类型 | 说明 | 适用场景示例 |
|------|------|-------------|
| feat | 新功能 | 新增组件、新页面、新API |
| fix | 修复问题 | Bug修复、兼容性问题 |
| docs | 文档变更 | README更新、注释修改 |
| style | 代码格式调整 | 缩进、空格、格式化（不影响功能） |
| refactor | 重构代码 | 代码优化、结构调整 |
| perf | 性能优化 | 加载速度、内存优化 |
| test | 测试相关 | 单元测试、集成测试 |
| chore | 构建/工具相关 | 依赖更新、配置修改 |

## Scope 命名规范

Scope 应对应变更的主要目录或模块：

| 目录 | Scope 示例 | 说明 |
|------|------------|------|
| `src/components/` | `ui`, `components` | 通用组件 |
| `src/routes/<page>/` | `<page-name>` | 页面级变更 |
| `src/stores/` | `store`, `state` | 状态管理 |
| `src/hooks/` | `hooks` | 自定义 Hooks |
| `src/http/` | `api`, `http` | API 请求相关 |
| `src/utils/` | `utils` | 工具函数 |
| `src/constants/` | `constants` | 常量定义 |
| `.claude/skills/` | `skill`, `<skill-name>` | Skill 技能 |
| 根目录配置文件 | `config`, `chore` | 项目配置 |

## Subject 写作规范

- 使用中文描述
- 简洁明了，不超过 50 字
- 以动词开头（添加、修复、更新、删除等）
- 不以句号结尾

示例：
- ✅ `feat(user-profile): 添加用户头像上传功能`
- ✅ `fix(api): 修复登录接口超时问题`
- ❌ `feat: 添加了一个新功能。`（过于模糊）

## Body 写作规范（可选）

当变更较复杂时，添加 Body 详细描述：

```markdown
feat(dashboard): 添加数据导出功能

新增功能：
- 支持导出 CSV/Excel 格式
- 支持自定义导出字段
- 添加导出进度提示

技术实现：
- 使用 xlsx 库处理 Excel 导出
- 导出接口支持分页处理大数据量
```

## 多 Commit 场景处理

当一次提交涉及多个类型变更时：

1. **优先使用主要类型**：如有新功能 + Bug修复，优先标记为 feat
2. **可使用复合 Scope**：`feat(ui,api): 添加组件并对接接口`
3. **Body 中详细说明**：列出所有变更类型

## Authored-By 标识

所有 AI 生成的 Commit 消息末尾添加：

```
Authored-By: Claude Code AI
```

用于标识 AI 辅助生成的提交，便于追溯。