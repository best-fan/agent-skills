---
name: design-analysis
description: 通用设计稿分析技能（v1.30.1，支持多 Agent 并行分析与验证）。分析设计稿（.pen、Figma、MasterGo、本地图片）并产出 UI 分析清单供开发实现或验收对照时，使用此技能。
metadata:
  version: 1.30.1
  updatedAt: 2026-10-09
---

# 设计稿分析

## 使用时机

- 分析设计稿（`.pen`、Figma 链接、MasterGo 链接、本地图片）
- 产出 UI 分析清单文档，供开发实现或验收对照

---

## 核心原则

**按「从上到下、从左到右、从外到里」顺序分析，逐条准确记录文字、图片、布局、层级四类重中之重。**

### 禁止行为

- ❌ 凭经验推断图表类型 → ✅ 读取节点 name 字段确认
- ❌ 凭经验推断子元素归属 → ✅ 用工具读取实际 children 数据
- ❌ 虚构模块 → ✅ 在设计稿中验证每个模块存在
- ❌ 假设「已经够了」→ ✅ 检查所有子节点坐标和数量
- ❌ 使用 readDepth: 1 或 2 → ✅ 强制使用 readDepth: 4+
- ❌ 不检查组件状态字段 → ✅ 分析阶段检查 enabled/visible 字段
- ❌ 虚构表格列 → ✅ 逐列读取设计稿实际列名和状态
- ❌ **🔴🔴🔴 凭经验跳过表格列** → ✅ **系统性遍历所有列节点，逐一读取表头内容**
- ❌ **🔴🔴🔴 遗漏表格列** → ✅ **验证列宽总和 ≈ 表格宽度**
- ❌ **省略层级结构** → ✅ **每个区域包含 `#### 层级` 小节**
- ❌ **凭视觉判断元素归属** → ✅ **验证元素坐标是否在区域边界内**
- ❌ **区域名称与标题不一致** → ✅ **区域名称与区域内文字标题一致**
- ❌ **合并独立卡片为左右布局** → ✅ **独立卡片作为独立区域**
- ❌ **省略图表类型子章节** → ✅ **图表区域包含图表类型、图表数据、图表文字、图表布局四个子章节**
- ❌ **未读取 INSTANCE 组件内部标题** → ✅ **MasterGo 标题从 INSTANCE 内部 TEXT 节点提取**
- ❌ **仅凭 y 坐标相同就合并区域** → ✅ **左右并排 GROUP 检查是否有独立标题 INSTANCE**
- ❌ **⚠️⚠️⚠️ 仅读取顶层 GROUP 节点** → ✅ **MasterGo 递归遍历 INSTANCE 内部（深度至少 4 层）**
- ❌ **⚠️⚠️⚠️ 层级结构中出现空 Tab 列表** → ✅ **提取 INSTANCE 内部 Tab 的实际文字，无文字时明确说明**
- ❌ **⚠️⚠️⚠️ 遗漏年份选择器** → ✅ **搜索 INSTANCE 内部「年」「月」「日」关键词**
- ❌ **🔴 层级结构中显示 `enabled: false` 元素** → ✅ **禁用元素不显示在层级结构中，只记录可见组件**
- ❌ **🔴 文档中记录禁用列（`enabled: false`）** → ✅ **禁用列不在文档中记录，只记录 `enabled: true` 的可见列**

---

## 目标产出

| 产出物 | 路径 | 用途 |
|--------|------|------|
| UI 分析清单 | `openspec/ui-checklist/{序号}-{模块名}.md` | 开发时精确还原；验收时对照基准 |

### 命名规则

- 序号：三位数字递增（001, 002...）
- 模块名：英文 kebab-case（如 `login-page`）

---

## 工作流程

根据设计稿类型选择分析路径：

| 设计稿类型 | 工具 | 详见 |
|-----------|------|------|
| `.pen` 文件 | Pencil MCP | `05-tools-guide.md` |
| Figma 链接 | Figma MCP | `05-tools-guide.md` |
| MasterGo 链接 | MasterGo MCP | `05-tools-guide.md` |
| 本地图片 | 视觉识别 | `05-tools-guide.md` |

### 步骤概览

1. **建立布局 Map** → `02-workflow-main.md`
   - ⚠️ 🔴 记录每个区域的边界值（左边界、右边界）
   - 详见：`07-boundary-validation.md`
   - 完成后执行**多 Agent 启用判定** → `10-multi-agent.md`
2. **区域与元素提取** → `02-workflow-main.md`
   - readDepth: 4+
   - 检查 enabled/visible 状态字段
   - 每个子元素验证 x 坐标是否在区域边界内
   - ⚡ 满足启用条件时，按区域并行分派 `analyze-NN` 子代理 → `10-multi-agent.md`
3. **样式规范汇总** → `02-workflow-main.md`
4. **输出 UI 分析清单** → `03-output-template.md`
   - ⚠️ 生成后**及时清理临时文件**（详见 `02-workflow-main.md`「清理临时文件」章节）
5. **执行校验** → `04-verification.md`
   - ⚡ 满足启用条件时，按校验组并行分派 `verify-NN` 子代理 → `10-multi-agent.md`
6. **截图交叉验证** → `09-screenshot-validation.md`
   - Agent Team 模式按区域并行验证

---

## 🔴 强制流程（详见 references）

| 流程 | 文件 | 说明 |
|------|------|------|
| 区域边界验证 | `07-boundary-validation.md` | 建立布局 Map 时立即执行 |
| 异常修正流程 | `08-error-correction.md` | 发现错误时执行 5 步修正 |
| 截图交叉验证 | `09-screenshot-validation.md` | 生成文档后执行 Agent Team 验证 |
| 多 Agent 协作 | `10-multi-agent.md` | 分析/验证过程必要时启用子代理并行执行 |

---

## 强制执行机制

详见 `04-verification.md` 获取完整校验清单（校验零到校验二十七）。

### 关键校验项

| 校验项 | 目的 | 常见遗漏 |
|--------|------|----------|
| **校验零** | 区域数量校验 | 遗漏整个区域 |
| 校验三 | 标题文字一致性 | 文字内容不一致 |
| 校验六 | 表格列标题专项 | 禁用列误认为可见 |
| 校验十 | 层级结构校验 | 层级嵌套错误 |
| 校验十八 | 组件状态字段校验 | enabled: false 组件误认为可见 |
| 校验二十 | 子元素坐标归属校验 | 元素坐标不在归属区域内 |
| 校验二十五 | 区域边界验证表必填校验 | 第一步未记录区域边界值 |
| 校验二十六 | 异常修正完整性校验 | 发现异常后只改一处 |
| 校验二十七 | 头部信息完整性校验 | 遗漏模型名称、设计稿来源 |

---

## 快速参考

### 分析规则

| 文件 | 内容 |
|------|------|
| `01-analysis-basics.md` | 分析顺序、四类重中之重、常见遗漏检查点 |

### 工作流程

| 文件 | 内容 |
|------|------|
| `02-workflow-main.md` | 完整工作流程（第一步到第五步） |
| `03-output-template.md` | UI 分析清单文档模板 |
| `04-verification.md` | 校验清单（校验零到校验二十七） |

### 工具指南

| 文件 | 内容 |
|------|------|
| `05-tools-guide.md` | Pencil / Figma / MasterGo MCP 工具使用 |

### 强制流程

| 文件 | 内容 |
|------|------|
| `07-boundary-validation.md` | 区域边界验证流程 |
| `08-error-correction.md` | 异常修正强制流程 |
| `09-screenshot-validation.md` | 截图交叉验证流程 |
| `10-multi-agent.md` | 多 Agent 协作机制（启用判定、角色分工、分析/验证阶段分派） |

### 实现建议

| 文件 | 内容 |
|------|------|
| `06-implementation.md` | 主流网页设计常识、常见错误模式 |

---

## 工具脚本

| 脚本 | 路径 | 用途 |
|------|------|------|
| MasterGo DSL 分析器 | `scripts/mastergo-dsl-analyzer.py` | 统计主要区域、提取文字和样式 |
| 详细区域分析 | `scripts/detailed_region_analysis.py` | 深入分析子元素、图表类型 |

---

## 示例文件

参考示例：`assets/example-ui-checklist.md`

---

## grep 搜索模式

快速定位 references 文件中的内容：

```bash
# 分析顺序
grep -n "从上到下\|从左到右\|从外到里" references/01-analysis-basics.md

# 校验清单
grep -n "校验零\|校验三\|校验十\|校验二十" references/04-verification.md

# 区域边界验证
grep -n "边界验证\|左边界\|右边界" references/07-boundary-validation.md

# 异常修正
grep -n "异常修正\|修正流程" references/08-error-correction.md

# 截图验证
grep -n "截图验证\|Agent Team" references/09-screenshot-validation.md

# 多 Agent 协作
grep -n "启用判定\|Team Lead\|analyze-\|verify-\|recheck-" references/10-multi-agent.md
```