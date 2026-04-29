---
name: daily-report
description: 此技能用于生成工作日报。当用户请求日报、工作总结、提交记录汇总，或运行 /daily-report 命令时触发。从 Git 提交记录生成交互式日报，按项目 scope 分组展示工作内容。
metadata:
  version: 1.0.0
  updatedAt: 2026-04-29
---

# Daily Report Skill

从 Git 提交记录生成交互式日报。

## 使用场景

此 Skill 在以下情况下触发：

- 用户请求生成日报、工作总结、提交记录汇总
- 用户运行 `/daily-report` 命令
- 用户询问"今天做了什么"、"工作进度"等

## 执行步骤

### Step 1: 获取 Git 用户信息

获取当前 Git 用户名和邮箱，用于筛选提交记录。

```bash
git config user.name
git config user.email
```

### Step 2: 询问统计日期

询问用户统计日期，提供三个选项：

- 今天（默认，格式 YYYY-MM-DD）
- 昨天（格式 YYYY-MM-DD）
- 自定义日期

### Step 3: 询问统计信息

询问是否包含统计信息：

- 否（默认）
- 是（显示提交次数、新增/删除行数）

### Step 4: 获取提交记录

使用 Git 命令获取指定日期的提交记录：

```bash
# 基础提交记录
git log --author="<用户名>" --since="<日期> 00:00:00" --until="<日期> 23:59:59" --format="%h %s"

# 包含统计信息时
git log --author="<用户名>" --since="<日期> 00:00:00" --until="<日期> 23:59:59" --shortstat --format="%h %s"
```

### Step 5: 解析并分组

按项目(scope)分组提交记录：

- 解析 commit message 格式 `<type>(<scope>): <subject>`
- 无 scope 的归入"其他"
- 同一 scope 的多个 subject 用分号连接

### Step 6: 生成日报

按格式输出日报：

```text
日报 (日期)

scope名称：提交内容1；提交内容2
其他：无scope的提交内容

统计：共 X 次提交
```

包含统计信息时：

```text
统计：共 X 次提交，新增 Y 行，删除 Z 行
```

## Commit 解析规则

- 格式：`<type>(<scope>): <subject>` 或 `<type>: <subject>`
- 提取 scope 作为项目分组依据
- 提取 subject 作为工作内容描述
- 示例：`feat(hr-delivery): 新增考评卡片` → scope=`hr-delivery`，subject=`新增考评卡片`

## 技术要点

- 使用 `git config user.name` 获取用户名
- 使用 `git log --shortstat` 获取行数统计（当用户选择包含统计信息时）
- 日期格式统一为 YYYY-MM-DD
- 支持跨多个仓库的日报生成（可选扩展）

## 输出示例

```text
日报 (2026-04-29)

hr-delivery：新增考评卡片；修复绩效计算逻辑
git-commit：完善技能支持子仓库和拉取流程
其他：更新项目文档

统计：共 5 次提交，新增 120 行，删除 35 行
```