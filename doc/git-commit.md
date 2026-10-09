# Git Commit 技能文档

## 使用时机

在以下情况使用此技能：

- 用户请求提交代码
- 手动调用 `/git-commit` 命令
- 完成代码修改后需要提交
- 需要生成规范的 commit 消息

---

## 核心功能

- 检查仓库结构（主仓库、子仓库、子模块）
- 确认修改目录范围
- 拉取远程代码确保同步
- 分析 git 变更内容（status、diff）
- 查看项目 commit 消息风格
- 生成多个候选 commit 消息供用户选择
- 执行 git add 和 git commit
- 询问是否推送远程仓库

---

## 执行步骤

### 第一阶段：确认修改目录（必须先执行）

#### 步骤 1：检查仓库结构

```bash
git rev-parse --show-toplevel    # 获取当前仓库根目录
git submodule status             # 检查子模块
```

检查是否存在子仓库（独立 .git 目录）。

#### 步骤 2：选择目标仓库

如果存在子仓库/子模块，使用 `AskUserQuestion` 让用户选择：

| 选项 | 说明 |
|------|------|
| 主仓库 | 在根目录操作 |
| 子仓库A | 进入指定子仓库操作 |
| 所有仓库 | 依次处理所有仓库 |

#### 步骤 3：分析变更目录

```bash
git status              # 查看未提交的文件
```

按目录分组展示变更文件，标识每个目录的变更类型（新增/修改/删除）。

#### 步骤 4：确认提交范围

使用 `AskUserQuestion` 展示目录变更概览：

| 选项 | 说明 |
|------|------|
| 全部提交 | 提交所有变更 |
| 按目录选择 | 选择特定目录 |
| 手动选择文件 | 精确选择文件 |

---

### 第二阶段：拉取远程代码（提交前必须执行）

#### 步骤 5：检查远程仓库状态

```bash
git remote -v           # 确认远程仓库配置
git fetch               # 获取远程最新状态（不合并）
git status              # 检查本地分支状态
```

#### 步骤 6：询问是否拉取

如果远程有新提交，使用 `AskUserQuestion` 询问用户是否拉取远程代码。

#### 步骤 7：执行拉取（用户确认后）

```bash
git pull                # 拉取远程代码
```

**处理拉取结果：**

| 结果 | 处理方式 |
|------|---------|
| 成功无冲突 | 继续下一阶段 |
| 有冲突 | 提示用户解决冲突后再继续 |

#### 步骤 8：冲突处理（如有冲突）

运行 `git status` 查看冲突文件列表，使用 `AskUserQuestion` 让用户选择：

| 选项 | 说明 |
|------|------|
| 查看冲突详情 | 展示冲突内容 |
| 我已解决冲突 | 用户确认后继续 |
| 取消提交 | 结束本次提交流程 |

---

### 第三阶段：生成 Commit 消息

```bash
git diff --stat         # 查看修改统计
git log --oneline -5    # 查看最近的 commit 消息风格
```

分析修改内容，生成 **多个候选 commit 消息**供用户选择。

使用 `AskUserQuestion` 展示候选消息，让用户选择确认。

---

### 第四阶段：执行 Git 操作

```bash
# 添加修改的文件（仅添加用户选择的文件）
git add {文件路径}

# 创建提交（使用 HEREDOC 格式）
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

Authored-By: Claude Code AI
EOF
)"
```

使用 `AskUserQuestion` 让用户确认是否推送远程，用户确认后执行 `git push`。

---

### 第五阶段：多仓库处理

如果选择了"所有仓库"，依次返回第一阶段处理下一个仓库。完成所有仓库提交后，展示提交汇总报告。

---

## 目录变更展示格式

向用户展示目录变更时，使用以下格式：

```
变更目录概览：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 src/components/
   ├── 新增: Button.tsx, Modal.tsx (2 files)
   └── 修改: Input.tsx (1 file)

📁 src/routes/user-profile/
   ├── 修改: Page.tsx, index.module.scss (2 files)

📁 src/stores/
   └── 新增: userStore.ts (1 file)

📁 docs/
   └── 修改: README.md (1 file)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计: 新增 3 文件, 修改 4 文件
```

---

## Commit 消息格式

```
<type>(<scope>): <subject>

<body>

Authored-By: Claude Code AI
```

### 格式说明

| 部分 | 说明 | 示例 |
|------|------|------|
| type | commit 类型 | `feat`、`fix`、`docs` |
| scope | 影响范围（可选） | `skills`、`build` |
| subject | 简短描述 | `添加 git-commit 技能` |
| body | 详细说明（可选） | 多行描述 |
| Authored-By | AI 标识 | 固定值 |

---

## Commit 类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| feat | 新功能 | 添加新技能、新特性 |
| fix | 修复问题 | 修复 bug、错误 |
| docs | 文档变更 | 更新文档、README |
| style | 代码格式调整 | 不影响功能的格式修改 |
| refactor | 重构代码 | 代码重构、优化 |
| perf | 性能优化 | 性能改进 |
| test | 测试相关 | 添加或修改测试 |
| chore | 构建/工具相关 | 构建配置、工具更新 |

---

## Scope 命名规范

Scope 应对应变更的主要目录或模块：

| 目录 | Scope 示例 |
|------|------------|
| `src/components/` | `ui`, `components` |
| `src/routes/<page>/` | `<page-name>` |
| `src/stores/` | `store`, `state` |
| `src/hooks/` | `hooks` |
| `src/http/` | `api`, `http` |
| `.claude/skills/` | `skill`, `<skill-name>` |

---

## 重要约束

### 必须先确认目标仓库

| 约束项 | 说明 |
|--------|------|
| 禁止跳过仓库选择步骤 | 必须先检查是否存在子仓库/子模块 |
| 多仓库必须让用户选择 | 如果存在多个仓库，必须让用户选择目标仓库 |
| 确认后才能进入下一阶段 | 确认目标仓库后才能进入下一阶段 |

### 必须先确认目录

| 约束项 | 说明 |
|--------|------|
| 禁止跳过目录确认步骤 | 必须先展示变更目录概览 |
| 必须让用户明确选择提交范围 | 确认后才能进入下一阶段 |

### 提交前必须拉取（如有远程仓库）

| 约束项 | 说明 |
|--------|------|
| 禁止在有远程新提交时跳过拉取步骤 | 必须先运行 `git fetch` 检查远程状态 |
| 有冲突必须让用户解决 | 拉取成功后才能继续执行 `git add` |
| 无远程仓库或无新提交可跳过 | 无远程仓库或无新提交时可跳过拉取步骤 |

### Git 操作规范

| 约束项 | 说明 |
|--------|------|
| HEREDOC 格式 | 使用 HEREDOC 传递 commit 消息，避免换行问题 |
| Authored-By 标识 | commit 消息末尾添加 `Authored-By: Claude Code AI` |
| 文件选择 | 只 commit 用户明确确认的文件 |
| hooks | 不要使用 `--no-verify` 跳过 hooks |
| 添加文件 | 不要使用 `-A` 或 `.` 添加所有文件，要明确指定文件 |
| 强制推送 | 不要使用 `--force` 强制推送，除非用户明确要求并理解风险 |

### 文件过滤

以下文件类型默认不提交（需用户明确指定才能提交）：

| 文件类型 | 说明 |
|----------|------|
| `.env`, `.env.local`, `.env.*.local` | 环境配置 |
| `*.log` | 日志文件 |
| `.DS_Store` | macOS 系统文件 |
| `node_modules/` | 依赖目录 |
| `dist/`, `build/` | 构建产物 |
| `*.zip`, `*.tar.gz` | 压缩包 |

---

## 示例输出

```
📝 Git 提交分析完成

**变更文件**：3 个
- README.md（修改）
- doc/git-commit.md（新增）
- skills/git-commit/SKILL.md（新增）

**候选 commit 消息**：

1. feat(skills): 添加 git-commit 技能并更新 README
2. docs: 新增 git-commit 技能文档
3. chore: 添加 git-commit 技能配置

请选择 commit 消息：[1/2/3/其他]

是否推送远程仓库？[是/否]
```

---

## 技能文件结构

```
skills/git-commit/
├── SKILL.md                        # 技能入口定义
└── references/
    ├── commit-conventions.md       # Commit 类型定义、Scope 规范、消息写作规范
    └── git-constraints.md          # Git 操作规范、文件过滤规则、冲突处理
```

---

## 版本信息

- 当前版本：1.4.0
- 更新日期：2026-04-14