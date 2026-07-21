# Agent Skills

Claude Code 技能仓库，提供可复用的自动化工作流。

## 技能列表

| 技能 | 版本 | 说明 |
|------|------|------|
| [design-analysis](#design-analysis) | 1.26.1 | 设计稿分析，产出 UI 分析清单 |
| [frontend-code-review](#frontend-code-review) | 1.2.0 | 前端代码审查，输出结构化报告 |
| [frontend-rules-generator](#frontend-rules-generator) | 1.0.0 | 前端规范生成，创建 Claude Rules 文件 |
| [build-frontend-zip](#build-frontend-zip) | 1.0.0 | 前端项目打包，生成 zip 分发包 |
| [git-commit](#git-commit) | 1.3.0 | Git 提交，生成规范 commit 消息 |
| [daily-report](#daily-report) | 2.0.0 | 工作日报，从 Git 提交归纳为 reportContent 风格日报 |

---

### design-analysis

通用设计稿分析技能，支持 `.pen`、Figma、MasterGo 设计稿及本地图片。

**核心功能：**
- 建立 UI 布局结构
- 提取文字、图片、布局、层级信息
- 汇总样式规范（颜色、字体、圆角、间距等）
- 产出标准化 UI 分析清单文档

**使用方式：** `/design-analysis`

**详细文档：** [doc/design-analysis.md](doc/design-analysis.md)

---

### frontend-code-review

前端代码审查技能，适用于 Vue 3 + TypeScript + pnpm 项目。

**核心功能：**
- 运行 ESLint、TypeScript 静态检查
- 代码质量、类型安全、Vue 规范审查
- npm 依赖安全审计
- 输出结构化审查报告

**使用方式：** `/frontend-code-review`

**详细文档：** [doc/frontend-code-review.md](doc/frontend-code-review.md)

---

### frontend-rules-generator

前端规范生成技能，分析项目代码结构，自动生成 `.claude/rules/` 开发规范文件。

**核心功能：**
- 自动检测项目类型（Vue/React）
- 扫描项目目录结构，识别关键模块
- 提取代码命名模式和目录组织方式
- 根据项目实际代码生成开发规范
- 生成符合 Claude Code 规范的 rules 文件

**使用方式：** `/frontend-rules-generator`

**详细文档：** [doc/frontend-rules-generator.md](doc/frontend-rules-generator.md)

---

### build-frontend-zip

前端项目打包技能，将构建产物压缩为可分发的 zip 文件。

**核心功能：**
- 自动检测项目路径和包管理器
- 运行构建命令并打包 dist 目录
- 输出构建汇总信息（分支、耗时、文件数量等）
- 生成带时间戳的 zip 文件

**使用方式：** `/build-frontend-zip`

**详细文档：** [doc/build-frontend-zip.md](doc/build-frontend-zip.md)

---

### git-commit

Git 提交技能，生成符合项目规范的 commit 消息。

**核心功能：**
- 检查仓库结构（主仓库、子仓库、子模块）
- 确认修改目录范围
- 拉取远程代码确保同步
- 分析 git 变更内容
- 根据项目 commit 风格生成多个候选消息
- 用户选择确认后执行提交
- 询问是否推送远程仓库

**使用方式：** `/git-commit`

**详细文档：** [doc/git-commit.md](doc/git-commit.md)

---

### daily-report

工作日报生成技能，从 Git 提交记录出发，经 AI 归纳生成 reportContent 风格的工作日报，可直接粘贴到 OA 系统。

**核心功能：**
- 获取 Git 用户信息，筛选当日提交记录（含 commit body）
- 支持今天、昨天、自定义日期统计
- 按工作主题归纳为「动作+对象」条目，去掉 commit type 前缀
- 按业务模块标注前缀（`模块-`），跨模块时各自标注
- 输出序号列表（顿号串联），贴合 reportContent 口语化风格

**使用方式：** `/daily-report`

**详细文档：** [doc/daily-report.md](doc/daily-report.md)

---

## 安装说明

### 方法一：网络拉取（推荐）

使用 `npx skills add` 从远程仓库直接安装：

```bash
# 安装 design-analysis 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/design-analysis

# 安装 frontend-code-review 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/frontend-code-review

# 安装 build-frontend-zip 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/build-frontend-zip

# 安装 git-commit 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/git-commit

# 安装 frontend-rules-generator 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/frontend-rules-generator

# 安装 daily-report 技能
npx skills add https://github.com/best-fan/agent-skills/tree/main/skills/daily-report
```

### 方法二：复制到项目

将需要的技能文件夹复制到项目的 `.claude/skills/` 目录：

```bash
# 安装 design-analysis 技能
cp -r skills/design-analysis /path/to/your/project/.claude/skills/

# 安装 frontend-code-review 技能
cp -r skills/frontend-code-review /path/to/your/project/.claude/skills/

# 安装 build-frontend-zip 技能
cp -r skills/build-frontend-zip /path/to/your/project/.claude/skills/

# 安装 git-commit 技能
cp -r skills/git-commit /path/to/your/project/.claude/skills/

# 安装 frontend-rules-generator 技能
cp -r skills/frontend-rules-generator /path/to/your/project/.claude/skills/

# 安装 daily-report 技能
cp -r skills/daily-report /path/to/your/project/.claude/skills/
```

### 方法三：全局安装

将技能文件夹复制到 Claude Code 全局配置目录：

```bash
# Windows
cp -r skills/design-analysis %USERPROFILE%\.claude\skills\

# macOS / Linux
cp -r skills/design-analysis ~/.claude/skills/
```

### 验证安装

安装后，在 Claude Code 中运行：

```
/design-analysis
```

或

```
/build-frontend-zip
```

技能将自动加载并执行。

---

## 更新技能

### 方法一：网络更新（推荐）

使用 `npx skills update` 更新已安装的技能：

```bash
# 更新 design-analysis 技能
npx skills update https://github.com/best-fan/agent-skills/tree/main/skills/design-analysis

# 更新 frontend-code-review 技能
npx skills update https://github.com/best-fan/agent-skills/tree/main/skills/frontend-code-review

# 更新 build-frontend-zip 技能
npx skills update https://github.com/best-fan/agent-skills/tree/main/skills/build-frontend-zip

# 更新 git-commit 技能
npx skills update https://github.com/best-fan/agent-skills/tree/main/skills/git-commit

# 更新 frontend-rules-generator 技能
npx skills update https://github.com/best-fan/agent-skills/tree/main/skills/frontend-rules-generator

# 更新 daily-report 技能
npx skills update https://github.com/best-fan/agent-skills/tree/main/skills/daily-report
```

### 方法二：手动更新

重新复制技能文件夹覆盖原有文件：

```bash
# 更新 design-analysis 技能
cp -r skills/design-analysis /path/to/your/project/.claude/skills/

# 更新 frontend-code-review 技能
cp -r skills/frontend-code-review /path/to/your/project/.claude/skills/

# 更新 build-frontend-zip 技能
cp -r skills/build-frontend-zip /path/to/your/project/.claude/skills/

# 更新 git-commit 技能
cp -r skills/git-commit /path/to/your/project/.claude/skills/

# 更新 frontend-rules-generator 技能
cp -r skills/frontend-rules-generator /path/to/your/project/.claude/skills/

# 更新 daily-report 技能
cp -r skills/daily-report /path/to/your/project/.claude/skills/
```

### 方法三：全局更新

```bash
# Windows
cp -r skills/design-analysis %USERPROFILE%\.claude\skills\

# macOS / Linux
cp -r skills/design-analysis ~/.claude/skills/
```

### 查看版本信息

技能版本信息存储在 SKILL.md 的 frontmatter 中：

```yaml
---
metadata:
  version: 1.x.x
  updatedAt: YYYY-MM-DD
---
```

---

## 目录结构

```
agent-skills/
├── README.md                    # 本文件
├── CLAUDE.md                    # 项目级 Claude Code 配置
├── doc/                         # 详细文档
│   ├── design-analysis.md       # 设计稿分析技能详细文档
│   ├── frontend-code-review.md  # 前端代码审查技能详细文档
│   ├── frontend-rules-generator.md  # 前端规范生成技能详细文档
│   ├── build-frontend-zip.md    # 前端打包技能详细文档
│   ├── git-commit.md            # Git 提交技能详细文档
│   └── daily-report.md          # 工作日报技能详细文档
└── skills/                      # 技能定义
    ├── design-analysis/
    │   ├── SKILL.md             # 技能入口
    │   ├── references/          # 参考文档
    │   ├── scripts/             # 工具脚本
    │   └── assets/              # 示例资源
    ├── frontend-code-review/
    │   ├── SKILL.md             # 技能入口
    │   └── references/          # 参考文档
    ├── frontend-rules-generator/
    │   ├── SKILL.md             # 技能入口
    │   ├── references/          # 参考文档（模板）
    │   └── scripts/             # 工具脚本
    ├── build-frontend-zip/
    │   ├── SKILL.md             # 技能入口
    │   └── scripts/             # 工具脚本
    ├── git-commit/
    │   └── SKILL.md             # 技能入口
    └── daily-report/
        └── SKILL.md             # 技能入口
```

---

## 扩展阅读

- [Claude Code 技能开发指南](https://docs.anthropic.com/claude-code/skills)
- [提交问题或建议](https://github.com/best-fan/agent-skills/issues)

---

## 附录

### 1. 核心命令速查

| 命令 | 作用 |
|------|------|
| `npx skills add <来源>` | 安装技能包（GitHub 短名/URL/本地路径） |
| `npx skills find [关键词]` | 搜索可用技能 |
| `npx skills list` | 列出已安装技能 |
| `npx skills update` | 更新所有技能 |
| `npx skills remove <技能名>` | 移除指定技能 |
| `npx skills init <名称>` | 创建新技能模板 |