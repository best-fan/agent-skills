# Frontend Rules Generator 技能文档

## 使用时机

在以下情况使用此技能：

- 新项目建立时需要规范化开发流程
- 现有项目需要整理和固化开发规范
- 用户希望让 Claude Code 更好地理解项目编码约定
- 需要生成 `.claude/rules/` 目录下的开发规范文件

---

## 核心功能

- 自动检测项目类型（Vue/React）
- 扫描项目目录结构，识别关键模块
- 提取代码命名模式和目录组织方式
- 根据项目实际代码生成开发规范
- 生成符合 Claude Code 规范的 rules 文件

---

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

1. **开发前检查流程** - 检查是否已存在类似内容、判断归属目录
2. **文件组织** - 文件命名规范、目录结构
3. **命名规范** - 各类型的命名约定
4. **代码模板示例** - 正确/错误的代码对比
5. **禁止事项** - 明确的禁止清单

---

## 项目类型识别

自动检测项目类型，决定生成的规则文件：

| 检测方式 | Vue 项目特征 | React 项目特征 |
|----------|-------------|----------------|
| package.json | `"vue"` / `"@vue"` | `"react"` / `"react-dom"` |
| 文件扩展名 | `.vue` 文件 | `.tsx` / `.jsx` 文件 |

---

## Rules 文件对照表

### Vue 项目

| Rule 文件 | 适用路径 | 核心内容 |
|-----------|----------|----------|
| `vue-component.md` | `src/components/**/*.vue` | Vue 组件开发规范 |
| `services.md` | `src/services/*.ts` | API 接口规范 |
| `store.md` | `src/store/**/*.ts` | Pinia/Vuex 状态管理规范 |
| `composables.md` | `src/composables/**/*.ts` | Vue Composables 规范 |
| `utils.md` | `src/utils/*.ts` | 工具函数规范 |
| `type.md` | `src/types/**/*.ts` | TypeScript 类型定义规范 |
| `router.md` | `src/router/*.ts` | Vue Router 配置规范 |
| `style.md` | `src/**/*.scss` | 样式规范 |
| `code-quality.md` | `src/**/*.ts` / `*.vue` | 通用代码质量规范 |

### React 项目

| Rule 文件 | 适用路径 | 核心内容 |
|-----------|----------|----------|
| `react-component.md` | `src/components/**/*.tsx` | React 组件开发规范 |
| `services.md` | `src/services/*.ts` | API 接口规范 |
| `store.md` | `src/store/**/*.ts` | Redux/Zustand 状态管理规范 |
| `hooks.md` | `src/hooks/**/*.ts` | React Hooks 规范 |
| `utils.md` | `src/utils/*.ts` | 工具函数规范 |
| `type.md` | `src/types/**/*.ts` | TypeScript 类型定义规范 |
| `router.md` | `src/router/*.ts` | React Router 配置规范 |
| `style.md` | `src/**/*.css` | 样式规范（CSS Modules / Tailwind） |
| `code-quality.md` | `src/**/*.ts` / `*.tsx` | 通用代码质量规范 |

---

## 执行步骤

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

**命名模式：**
- 文件命名风格（camelCase / PascalCase / kebab-case）
- 函数命名前缀（use / get / set / format / is）
- 类型命名前缀（I / T 或无前缀）

**目录结构：**
- 是否使用子目录组织
- 是否有 index.ts 统一导出
- 是否分离样式文件

**代码模板：**
- 选取典型文件作为模板参考
- 提取常用代码片段

### Step 3: Rules 文件生成

根据项目类型生成规则文件：

- Vue 项目：参考 `references/vue-component.md`
- React 项目：参考 `references/react-component.md`

### Step 4: 生成后验证

验证生成的 rules 文件：

1. 检查 YAML frontmatter 的 `paths` 配置
2. 确保路径模式能正确匹配目标文件
3. 确保包含「开发前检查流程」「命名规范」「禁止事项」

### Step 5: 已有 rules 文件处理

如果目标目录已有 rules 文件：

- **同名文件**：询问用户是覆盖还是追加内容
- **新文件**：直接生成
- **建议**：优先保留用户自定义的内容

---

## 用户交互

技能会通过 AskUserQuestion 确认关键决策：

| 决策点 | 问题 | 选项 |
|--------|------|------|
| 项目类型 | 检测到这是 {Vue/React} 项目，是否正确？ | 确认 / 手动选择 |
| 目标目录 | Rules 文件存放位置 | `.claude/rules/`（默认） / 自定义路径 |
| 生成范围 | 需要生成哪些模块的规范？ | 全部 / 仅组件 / 仅公共模块 / 自定义 |
| 已有文件 | 发现已有 rules 文件，如何处理？ | 覆盖 / 追加内容 / 跳过 |
| 命名约定 | 检测到文件命名风格为 {PascalCase}，是否符合预期？ | 确认 / 使用其他风格 |

---

## 执行脚本

```bash
python scripts/generate_rules.py <src_dir> [options]

# 参数
<src_dir>           源码目录路径（如 src/）
--output, -o        输出目录（默认 .claude/rules）
--type, -t          项目类型：vue / react
```

**使用示例：**

```bash
# 自动检测项目类型
python scripts/generate_rules.py frontend/src

# 指定 Vue 项目
python scripts/generate_rules.py frontend/src --type vue

# 指定输出目录
python scripts/generate_rules.py frontend/src --output frontend/.claude/rules
```

---

## 参考资源

| 文件 | 用途 |
|------|------|
| `references/rule-template.md` | Rules 文件通用模板结构 |
| `references/vue-component.md` | Vue 组件规范模板（含 Composition API） |
| `references/react-component.md` | React 组件规范模板（含 Hooks） |

---

## 输出规范

生成的 rules 文件应满足以下要求：

| 要求 | 说明 |
|------|------|
| 实用优先 | 规范来源于实际代码，而非理论 |
| 可执行 | 检查流程提供具体的搜索命令 |
| 示例丰富 | 包含正确/错误的代码对比 |
| 约束明确 | 禁止事项列表清晰 |
| 框架适配 | Vue/React 组件规范需区分框架特性 |
| 路径正确 | YAML frontmatter 的 paths 必须能匹配目标文件 |

---

## 注意事项

| 注意点 | 说明 |
|--------|------|
| 语言 | 使用中文编写所有规范内容 |
| paths 必填 | 每个文件必须有 YAML frontmatter 指定 `paths` |
| 结构顺序 | 开发前检查 → 文件组织 → 命名规范 → 代码模板 → 禁止事项 |
| 框架区分 | Vue 项目使用 `vue-component.md`，React 项目使用 `react-component.md` |
| 内容保留 | 已有 rules 文件时，优先保留用户自定义内容 |

---

## 技能文件结构

```
skills/frontend-rules-generator/
├── SKILL.md                     # 技能入口定义
├── references/
│   ├── rule-template.md         # Rules 文件通用模板
│   ├── vue-component.md         # Vue 组件规范模板
│   └── react-component.md       # React 组件规范模板
└── scripts/
    └── generate_rules.py        # 生成脚本
```

---

## 版本信息

- 当前版本：1.0.0
- 更新日期：2026-10-09