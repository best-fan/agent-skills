---
name: frontend-rules-generator
description: 前端 Rules 生成技能（v1.0.0）。分析前端项目代码结构和模式，生成 `.claude/rules` 开发规范文件。适用于 Vue/React 前端项目，根据项目实际代码提取命名约定、文件组织、代码模板等规范。自动识别项目类型，生成对应框架的组件规范。
metadata:
  version: 1.0.0
  updatedAt: 2026-10-09
---

# 前端 Rules 生成器

分析前端项目代码，自动生成 `.claude/rules/` 目录下的开发规范文件，帮助 Claude Code 在开发过程中遵循项目特定的编码约定。

## 触发场景

- 用户请求"生成 rules"、"创建开发规范"、"生成项目规则"
- 用户希望让 Claude Code 更好地理解项目编码约定
- 新项目建立时需要规范化开发流程
- 现有项目需要整理和固化开发规范

## Rules 文件结构

每个 rules 文件由两部分组成：

### 1. YAML Frontmatter

```yaml
---
paths:
  - "src/**/*.ts"    # 规则适用的文件路径模式
---
```

`paths` 使用 glob 模式匹配文件，决定规则生效范围。

### 2. Markdown 内容

标准内容结构：

```markdown
# {模块名} 开发规范

## 开发前检查流程

### 1. 检查全局是否已存在类似内容
### 2. 判断归属目录
### 3. 评估是否应添加到全局
### 4. 扩展现有模块

## 文件组织
## 命名规范
## 代码模板示例
## 禁止事项
```

## 项目类型识别

自动检测项目类型，决定生成的规则文件：

```bash
# 检查 package.json 依赖
grep -E '"vue"|"@vue' package.json    # Vue 项目
grep -E '"react"|"react-dom"' package.json  # React 项目

# 检查文件扩展名
ls src/**/*.vue   # Vue 项目特征
ls src/**/*.tsx   # React 项目特征（.tsx/.jsx）
```

## Rules 文件对照表

### Vue 项目

| Rule 文件名 | 适用路径 | 核心内容 |
|------------|---------|---------|
| `vue-component.md` | `src/components/**/*.vue` | Vue 组件开发规范 |
| `services.md` | `src/services/*.ts` | API 接口规范 |
| `store.md` | `src/store/**/*.ts` | Pinia/Vuex 状态管理规范 |
| `utils.md` | `src/utils/*.ts` | 工具函数规范 |
| `type.md` | `src/types/**/*.ts` | TypeScript 类型定义规范 |
| `composables.md` | `src/composables/**/*.ts` | Vue Composables 规范 |
| `router.md` | `src/router/*.ts` | Vue Router 配置规范 |
| `style.md` | `src/**/*.scss` / `*.vue` | 样式规范 |
| `page.md` | `src/pages/**/*.vue` | 页面组件规范（可选） |
| `code-quality.md` | `src/**/*.ts` / `*.vue` | 通用代码质量规范 |

### React 项目

| Rule 文件名 | 适用路径 | 核心内容 |
|------------|---------|---------|
| `react-component.md` | `src/components/**/*.tsx` | React 组件开发规范 |
| `services.md` | `src/services/*.ts` | API 接口规范 |
| `store.md` | `src/store/**/*.ts` | Redux/Zustand 状态管理规范 |
| `utils.md` | `src/utils/*.ts` | 工具函数规范 |
| `type.md` | `src/types/**/*.ts` | TypeScript 类型定义规范 |
| `hooks.md` | `src/hooks/**/*.ts` | React Hooks 规范 |
| `router.md` | `src/router/*.ts` | React Router 配置规范 |
| `style.md` | `src/**/*.css` / `*.scss` | 样式规范（CSS Modules / Tailwind） |
| `page.md` | `src/pages/**/*.tsx` | 页面组件规范（可选） |
| `code-quality.md` | `src/**/*.ts` / `*.tsx` | 通用代码质量规范 |

## 生成流程

### Step 1: 项目分析

扫描项目目录结构，识别关键模块：

```bash
# 识别项目类型
ls package.json          # Vue/React/其他
ls src/                  # 源码目录结构

# Vue 项目核心模块
ls src/components/       # 公共组件
ls src/composables/      # 组合式函数
ls src/store/            # Pinia/Vuex 状态管理

# React 项目核心模块
ls src/components/       # 公共组件
ls src/hooks/            # 自定义 Hooks
ls src/store/            # Redux/Zustand 状态管理

# 公共模块
ls src/services/         # API 请求
ls src/utils/            # 工具函数
ls src/types/            # 类型定义
ls src/pages/            # 页面（或 views）
```

### Step 2: 模式提取

对每个模块进行代码分析，提取：

**命名模式**:
- 文件命名风格（camelCase / PascalCase / kebab-case）
- 函数命名前缀（use / get / set / format / is）
- 类型命名前缀（I / T 或无前缀）

**目录结构**:
- 是否使用子目录组织
- 是否有 index.ts 统一导出
- 是否分离样式文件（Vue: scoped / React: CSS Modules）

**代码模板**:
- 选取典型文件作为模板参考
- 提取常用代码片段

### Step 3: Rules 文件生成

根据项目类型生成规则文件。对于组件规范，使用对应模板：

- Vue 项目：参考 `references/vue-component.md` 填充 `vue-component.md`
- React 项目：参考 `references/react-component.md` 填充 `react-component.md`

其他模块规范根据实际代码模式生成。

### Step 4: 生成后验证

生成 rules 文件后，执行验证：

1. **检查 YAML frontmatter**：确保每个文件有正确的 `paths` 配置
2. **检查路径匹配**：确保 paths 模式能正确匹配目标文件
3. **检查内容完整性**：确保包含「开发前检查流程」「命名规范」「禁止事项」

### Step 5: 已有 rules 文件处理

如果目标目录已有 rules 文件：

- **同名文件**：询问用户是覆盖还是追加内容
- **新文件**：直接生成
- **建议**：优先保留用户自定义的内容，仅更新框架相关的模板部分

## 用户交互

通过 AskUserQuestion 工具确认关键决策：

### 1. 项目类型确认

当检测到项目类型时，确认检测结果：

```
问题：检测到这是 {Vue/React} 项目，是否正确？
选项：确认 / 手动选择（Vue / React）
```

### 2. 目标目录

```
问题：Rules 文件存放位置
选项：.claude/rules/（默认） / 自定义路径
```

### 3. 生成范围

```
问题：需要生成哪些模块的规范？
选项：全部模块 / 仅组件 / 仅公共模块（services/utils/types） / 自定义选择
```

### 4. 已有文件处理

```
问题：发现已有 rules 文件 {文件名}，如何处理？
选项：覆盖 / 追加内容 / 跳过
```

### 5. 命名约定确认

提取命名模式后确认：

```
问题：检测到文件命名风格为 {PascalCase}，是否符合预期？
选项：确认 / 使用其他风格（camelCase / kebab-case）
```

## 参考资源

详细模板和示例见 `references/` 目录：

| 文件 | 用途 |
|------|------|
| `rule-template.md` | Rules 文件通用模板结构 |
| `vue-component.md` | Vue 组件规范模板（含 Composition API / Options API） |
| `react-component.md` | React 组件规范模板（含 Hooks / 函数组件） |

## 输出规范

生成的 rules 文件应满足以下要求：

1. **实用优先**：规范来源于实际代码，而非理论
2. **可执行**：检查流程提供具体的搜索命令
3. **示例丰富**：包含正确/错误的代码对比
4. **约束明确**：禁止事项列表清晰
5. **框架适配**：Vue/React 组件规范需区分框架特性
6. **路径正确**：YAML frontmatter 的 paths 必须能匹配目标文件

## 注意事项

1. Rules 文件是 `.claude/rules/` 目录下的 Markdown 文件
2. 每个文件必须有 YAML frontmatter 指定 `paths`
3. 内容结构遵循「开发前检查 → 文件组织 → 命名规范 → 代码模板 → 禁止事项」
4. Vue 项目使用 `vue-component.md`，React 项目使用 `react-component.md`
5. 使用中文编写所有规范内容
6. 已有 rules 文件时，优先保留用户自定义内容