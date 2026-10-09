---
name: frontend-code-review
description: 前端代码审查技能（v1.2.1）。当用户请求代码审查、运行 /frontend-code-review 命令、提交前检查代码、或进行 npm 安全审计时触发。审查代码质量、类型安全、Vue 最佳实践、样式规范、npm 包安全，输出结构化审查报告。
metadata:
  version: 1.2.1
  updatedAt: 2026-10-09
---
# 前端代码审查

## 使用时机

- 用户请求代码审查
- 手动调用 `/frontend-code-review` 命令
- 提交代码前检查
- npm 安全审计

---

## 项目配置

本技能默认配置适用于 **Vue 3 + TypeScript + pnpm** 项目。

### 默认配置

| 配置项 | 默认值 |
|--------|--------|
| 源码目录 | `frontend/src/` |
| 包管理器 | `pnpm` |
| 框架 | Vue 3 |
| 静态检查 | `pnpm lint`、`pnpm type-check` |

### 外部规则文件

本技能引用以下外部规则文件（不包含在技能包中）：

| 文件 | 说明 |
|------|------|
| `frontend/.claude/rules/code-quality.md` | 代码质量规范 |
| `frontend/.claude/rules/type.md` | 类型安全规范 |
| `frontend/.claude/rules/vue-component.md` | Vue 组件规范 |
| `frontend/.claude/rules/style.md` | 样式规范 |

**处理方式**：审查开始时检查文件是否存在，不存在则跳过对应检查项。

---

## 工作流程

### 步骤 1：初始化

1. 检查外部规则文件是否存在
2. 检查 `reports/` 目录是否存在（不存在则询问用户是否创建）
3. 使用 `AskUserQuestion` 让用户选择审查范围

| 选项 | 说明 | 后续步骤 |
|------|------|---------|
| 全量审查 | 审查源码目录下所有文件 | 执行步骤 2-5 |
| npm 安全检查 | 仅检查依赖安全 | 跳过步骤 2-3 |
| 指定目录/文件 | 用户指定具体路径 | 执行步骤 2-5 |
| 变更文件 | 审查 git 变更文件 | 执行步骤 2-5 |

**变更文件的获取方式**（选择「变更文件」时）：

```bash
# 已跟踪文件的未提交变更（暂存 + 未暂存）
git diff --name-only HEAD

# 未跟踪的新文件
git ls-files --others --exclude-standard

# 仅审查暂存区（提交前检查）
git diff --cached --name-only
```

按用户场景选取（默认未提交变更 + 未跟踪文件），合并去重后作为审查文件列表。

---

### 步骤 2：运行静态检查

读取 `references/review-checklist.md`。先读取 `frontend/package.json` 的 `scripts`，确认静态检查命令是否存在及其实际名称（可能是 `typecheck`、`tsc`、`lint:eslint` 等变体，以实际 scripts 为准，禁止臆造命令），然后运行：

```bash
pnpm lint           # ESLint 检查（实际命令以 package.json scripts 为准）
pnpm type-check     # TypeScript 类型检查（实际命令以 package.json scripts 为准）
```

**错误处理**：
| 错误类型 | 处理方式 |
|---------|---------|
| 命令不存在 | 跳过该检查，报告中标注「命令不可用」 |
| 命令超时 | 记录超时，继续执行后续步骤 |
| 命令失败 | 收集错误输出，记录到审查结果 |

---

### 步骤 3：逐文件审查

读取外部规则文件（如存在），按规范进行审查。

审查类别详见 `references/review-checklist.md`。

---

### 步骤 4：npm 安全检查

读取 `references/npm-security-check.md`，然后运行：

```bash
cd frontend

pnpm audit --registry https://registry.npmjs.org/ --json
pnpm outdated
pnpm licenses list
```

**错误处理**：
| 错误类型 | 处理方式 |
|---------|---------|
| 网络超时 | 重试一次，仍失败则报告中标注「网络错误」 |
| registry 不可达 | 报告中标注「无法连接 npm registry」 |
| JSON 解析失败 | 使用非 JSON 格式重试 |
| 非零退出码 | `pnpm audit` 发现漏洞、`pnpm outdated` 发现过时依赖时退出码非 0，属正常「有发现」，解析输出而非视为失败 |

---

### 步骤 5：生成报告

读取 `references/report-template.md` 和 `references/severity-rules.md`。

#### 报告章节

| 章节 | 必要性 | 说明 |
|------|--------|------|
| 报告头部 | 必须 | 审查时间、范围、文件数、类型 |
| 摘要统计 | 必须 | 各类别问题统计表格 |
| 问题列表 | 必须 | 按严重等级分类的问题详情 |
| npm 安全检查 | 条件必须 | 执行安全检查时包含 |
| 静态检查输出 | 条件必须 | 执行步骤 2 时包含 |
| 审查文件列表 | 条件必须 | 执行步骤 3 时包含 |
| 总结与建议 | 必须 | 总体评价和优先处理建议 |

#### 报告存储

- 存储位置：仓库根目录的 `reports/`（不存在时已在步骤 1 询问用户是否创建）
- 命名格式：`frontend-code-review-{YYYYMMDD}-{HHMMSS}.md`

---

## 对话输出格式

```
📋 代码审查完成

**审查时间**：{YYYY-MM-DD HH:mm:ss}
**审查范围**：{路径}
**审查文件数**：{数量}

| 类别 | 严重 | 中等 | 轻微 | 总计 |
|------|------|------|------|------|
| 代码质量 | X | X | X | X |
| 类型安全 | X | X | X | X |
| Vue 规范 | X | X | X | X |
| 样式规范 | X | X | X | X |
| npm 安全 | X | X | X | X |
| **总计** | **X** | **X** | **X** | **X** |

**静态检查结果**：
- ESLint：{通过/发现 X 个问题}
- TypeScript：{通过/发现 X 个错误}

🔴 严重问题：
1. [{文件}:{行号}] {问题描述}
   建议：{修复建议}

📁 详细报告：reports/frontend-code-review-{时间戳}.md
```

---

## 参考文档

| 文件 | 用途 | 读取时机 |
|------|------|---------|
| `references/review-checklist.md` | 审查清单 | 步骤 2-3 |
| `references/severity-rules.md` | 严重等级规则 | 步骤 5 |
| `references/npm-security-check.md` | npm 安全检查规则 | 步骤 4 |
| `references/report-template.md` | 报告模板 | 步骤 5 |
| `references/report-example.md` | 报告示例 | 需要参考时 |
| `references/CHANGELOG.md` | 版本更新记录 | 需要参考时 |