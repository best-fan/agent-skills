---
name: git-commit
description: Git 提交技能（v1.4.0）。运行 /git-commit 命令、或完成代码修改后需要提交时触发此技能。技能会先确认修改的目录范围，拉取远程代码确保同步，分析 git 变更，生成多个候选 commit 消息供用户选择，确认后执行 git add 和 git commit，并询问是否推送远程仓库。
metadata:
  version: 1.4.0
  updatedAt: 2026-04-14
---

# Git Commit Skill

生成符合项目规范的 git commit，确保提交前与远程仓库同步。

## 执行步骤

### 第一阶段：确认修改目录

1. **检查仓库结构**：`git rev-parse --show-toplevel` + `git submodule status`
2. **选择目标仓库**：如有子仓库/子模块，使用 AskUserQuestion 让用户选择
3. **切换目录**：进入目标仓库
4. **查看变更**：`git status` 分类整理（新增/修改/删除）
5. **分析目录结构**：按目录分组展示
6. **确认提交范围**：AskUserQuestion 选择提交范围（全部/按目录/手动）
7. **展示文件清单**：确认后进入下一阶段

### 第二阶段：拉取远程代码

8. **检查远程状态**：`git remote -v` + `git fetch`
9. **检查差异**：检查是否有远程新提交
10. **询问拉取**：如有新提交，AskUserQuestion 询问是否拉取
11. **执行拉取**：`git pull`，处理结果
12. **处理冲突**：如有冲突，展示冲突文件，用户确认解决后继续

### 第三阶段：生成 Commit 消息

13. **查看统计**：`git diff --stat`（仅确认的文件）
14. **查看历史**：`git log --oneline -5`
15. **生成候选消息**：多个候选 commit 消息
16. **用户选择**：AskUserQuestion 展示候选消息

### 第四阶段：执行 Git 操作

17. **添加文件**：`git add`（仅确认的文件）
18. **创建提交**：`git commit`
19. **确认推送**：AskUserQuestion 询问是否推送
20. **推送远程**：`git push`
21. **多仓库处理**：如选择"所有仓库"，依次处理

## 目录变更展示格式

```
变更目录概览：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 src/components/
   ├── 新增: Button.tsx, Modal.tsx (2 files)
   └── 修改: Input.tsx (1 file)

📁 src/routes/user-profile/
   └── 修改: Page.tsx, index.module.scss (2 files)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总计: 新增 2 文件, 修改 3 文件
```

## Commit 消息格式

```
<type>(<scope>): <subject>

<body>

Authored-By: Claude Code AI
```

详细规范见 `references/commit-conventions.md`。

## 重要约束

### 必须先确认目标仓库

- 禁止跳过仓库选择步骤
- 必须检查子仓库/子模块
- 多仓库时必须让用户选择

### 必须先确认目录

- 禁止跳过目录确认步骤
- 必须展示变更目录概览
- 必须让用户选择提交范围

### 提交前必须拉取

- 禁止在有远程新提交时跳过拉取
- 必须运行 `git fetch` 检查状态
- 有冲突必须让用户解决

详细规范见 `references/git-constraints.md`。

## 参考文档

| 文档 | 内容 |
|------|------|
| `references/commit-conventions.md` | Commit 类型定义、Scope 规范、消息写作规范 |
| `references/git-constraints.md` | Git 操作规范、文件过滤规则、冲突处理 |