# Design Analysis 技能文档

## 使用时机

在以下情况使用此技能：

- 分析设计稿（`.pen`、Figma 链接、MasterGo 链接、其它设计图或标注），梳理界面结构、样式、元素
- 分析本地图片（设计稿截图、UI 图片），通过视觉识别提取信息
- 产出 UI 分析清单文档，供开发实现或验收对照

不限定阶段：可在写提案前、提案中、或单独进行「只分析不写提案」。

---

## 核心原则

**按「从上到下、从左到右、从外到里」顺序分析，逐条准确记录文字、图片、布局、层级四类重中之重。**

**输出后必须检查：区域顺序与设计稿一致、布局数据精准无误。若存在问题，必须补充和修正。**

详见：
- `../skills/design-analysis/references/01-analysis-basics.md` - 分析顺序、四类重中之重

---

## 演示示例

以下是使用 design-analysis 技能分析 `.pen` 设计稿的实际工作截图：

### 示例：协同办公系统 — 任务列表页

| 阶段 | 截图 |
|------|------|
| 分析界面（全局视图） | ![分析界面](images/analysis-demo-1.jpg) |
| 分析界面（节点反馈区域） | ![节点反馈区域](images/analysis-demo-2.jpg) |

---

## ⚠️ 强制执行机制

> **规范写得再清楚，如果执行者没有建立强制执行机制，就会被绕过。**

**必须遵守 `../skills/design-analysis/references/04-verification.md` 中的校验清单（校验零到校验二十七）。**

关键禁止行为：
- ❌ 凭经验推断图表类型 → ✅ 读取节点 name 字段确认实际类型
- ❌ 凭经验推断子元素归属 → ✅ 用 MCP 工具读取实际 children 数据
- ❌ 虚构模块 → ✅ 在设计稿中验证每个模块存在
- ❌ 假设「已经够了」 → ✅ 检查所有子节点坐标和数量
- ❌ 使用 readDepth: 1 或 2 → ✅ 强制使用 readDepth: 4+
- ❌ 不检查组件状态字段 → ✅ 分析阶段检查 enabled/visible 字段
- ❌ 虚构表格列 → ✅ 逐列读取设计稿实际列名和状态
- ❌ 层级结构中显示 enabled: false 元素 → ✅ 禁用元素不显示在层级结构中

**详细校验清单见 `../skills/design-analysis/references/04-verification.md`。**

---

## 目标产出

| 产出物 | 路径 | 用途 |
|--------|------|------|
| UI 分析清单 | `openspec/ui-checklist/{序号}-{模块名}.md` | 开发时精确还原；验收时对照基准 |

### 示例文件

参考示例：`../skills/design-analysis/assets/example-ui-checklist.md`

### 命名约束

| 约束项 | 规范 | 示例 |
|--------|------|------|
| 序号 | 三位数字递增，不可重复 | `001`、`002`...`010` |
| 模块名 | 英文 kebab-case | `login-page`、`dashboard-header` |
| 文件名 | `{序号}-{模块名}.md` | `001-login-page.md` |

**文件创建规则：**
1. 查看 `openspec/ui-checklist/` 目录已有文件
2. 新序号 = 现有最大序号 + 1（空目录从 `001` 开始）
3. 序号复用：仅当最后一个序号被删除时可复用，中间序号删除后永久空置

## 必须遵守
- 不允许修改已存在的文件，必须创建新文件
- **必须严格按照 `../skills/design-analysis/references/03-output-template.md` 模板生成文档**，包含所有章节，不得遗漏或使用自创格式

---

## 工作流程

根据设计稿类型选择分析路径：

### 路径 A：结构化设计稿（.pen / Figma / MasterGo）

1. **建立布局 Map** - 获取设计稿结构、页面状态、整体尺寸、区域划分
   - ⚠️ 🔴 记录每个区域的边界值（左边界、右边界）
   - 详见：`../skills/design-analysis/references/07-boundary-validation.md`
   - 工具使用详见 `../skills/design-analysis/references/05-tools-guide.md`

2. **区域与元素提取** - 对每个区域按「从外到里」逐项提取
   - readDepth: 4+
   - 检查 enabled/visible 状态字段
   - 每个子元素验证 x 坐标是否在区域边界内
   - 详见 `../skills/design-analysis/references/02-workflow-main.md`

3. **样式规范汇总** - 汇总颜色、字体、圆角、间距、阴影等
   - 详见 `../skills/design-analysis/references/02-workflow-main.md`

4. **输出 UI 分析清单** - **必须严格按照模板输出文档**
   - 模板路径：`../skills/design-analysis/references/03-output-template.md`
   - **生成后必须执行校验**：详见 `../skills/design-analysis/references/04-verification.md`
   - 校验零到校验二十七逐项执行，不通过必须修正后再继续

5. **区域检查与对比完善** - 按模块区域逐一检查对比
   - 详见 `../skills/design-analysis/references/02-workflow-main.md`

6. **截图交叉验证** - 执行 Agent Team 模式验证
   - 详见 `../skills/design-analysis/references/09-screenshot-validation.md`

### 路径 B：本地图片（设计稿截图 / UI 图片）

1. **图像识别** - 使用视觉能力读取图片
   - 分析顺序遵守 `../skills/design-analysis/references/01-analysis-basics.md`
   - 详见 `../skills/design-analysis/references/05-tools-guide.md`「本地图片处理」

2. **结构化整理** - 将识别信息按区域整理，建立布局 Map
   - 参考 `../skills/design-analysis/references/02-workflow-main.md`

3. **样式规范汇总** - 提取颜色、字体、圆角、间距等
   - 详见 `../skills/design-analysis/references/02-workflow-main.md`

4. **输出 UI 分析清单** - 按模板输出文档
   - 模板路径：`../skills/design-analysis/references/03-output-template.md`

5. **区域检查与对比完善** - 按模块区域逐一检查对比
   - 详见 `../skills/design-analysis/references/02-workflow-main.md`

6. **截图交叉验证** - 执行视觉验证
   - 详见 `../skills/design-analysis/references/09-screenshot-validation.md`

---

## 快速参考

### ⚠️ 强制执行机制
- `../skills/design-analysis/references/04-verification.md` - 校验清单（校验零到校验二十七）

### 强制流程
- `../skills/design-analysis/references/07-boundary-validation.md` - 区域边界验证流程
- `../skills/design-analysis/references/08-error-correction.md` - 异常修正强制流程
- `../skills/design-analysis/references/09-screenshot-validation.md` - 截图交叉验证流程
- `../skills/design-analysis/references/10-multi-agent.md` - 多 Agent 协作机制（启用判定、角色分工、分析/验证阶段分派）

### Analysis Rules
- `../skills/design-analysis/references/01-analysis-basics.md` - 分析顺序、四类重中之重、常见遗漏检查点

### Workflow Rules
- `../skills/design-analysis/references/02-workflow-main.md` - 完整工作流程（第一步到第五步）

### Output Rules
- `../skills/design-analysis/references/03-output-template.md` - UI 分析清单文档模板

### Tools Rules
- `../skills/design-analysis/references/05-tools-guide.md` - 设计稿工具使用指南

### Implementation Rules
- `../skills/design-analysis/references/06-implementation.md` - 主流网页设计常识、常见错误模式

### 工具脚本
| 脚本 | 路径 | 用途 |
|------|------|------|
| MasterGo DSL 分析器 | `../skills/design-analysis/scripts/mastergo-dsl-analyzer.py` | 统计主要区域、提取文字和样式 |
| 详细区域分析 | `../skills/design-analysis/scripts/detailed_region_analysis.py` | 深入分析子元素、图表类型 |

---

## 版本信息

- 当前版本：1.30.1
- 更新日期：2026-10-09