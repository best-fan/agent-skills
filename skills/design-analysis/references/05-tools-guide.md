---
title: 工具使用指南
impact: HIGH
impactDescription: 根据设计稿类型选择 Pencil MCP / Figma MCP / MasterGo MCP 获取布局与节点信息
tags: tools, design, pencil, figma, mastergo
---

# 工具使用指南

## 设计稿类型与工具选择

| 设计稿类型 | 工具 | 第一步操作 |
|-----------|------|-----------|
| `.pen` 文件 | Pencil MCP / Read | `get_app_state` 获取状态，`execute` 读取/修改，`Read` 备选 |
| Figma 链接 | Figma MCP | `mcp__Framelink_Figma_MCP__get_figma_data` |
| MasterGo 链接 | MasterGo MCP | `mcp__mastergo-magic-mcp__mcp__getDsl` |
| 本地图片 | 视觉识别 | 使用模型视觉能力识别 |

---

## .pen（Pencil 设计稿）

### 可用工具

| 工具 | 用途 | 数据返回 |
|------|------|----------|
| `mcp__pencil__get_app_state` | 获取 pen.dev 应用状态、当前打开文件、选中节点等基本信息 | ✅ 返回状态和顶层节点 |
| `mcp__pencil__execute` | **核心工具**：在 pen.dev 上下文中执行 JavaScript，**可通过 Get() 读取节点**，也可修改设计稿 | ⚠️ 返回 "OK"，数据通过 Get()/Print() 获取 |
| `Read` | **备选**：.pen 文件是明文 JSON，当 execute 无法满足时可直接读取 | ✅ 返回完整文件内容 |

### 核心约束

> **⚠️ Pencil MCP `execute` 工具是主要交互方式**。在 `execute` 的 `input` 中可使用 `Get()` 函数读取节点数据，使用 `Insert()`/`Update()` 等修改设计稿。
>
> **注意**：`get_style` 和 `read_skill` 工具当前版本不可用。

### 使用步骤（优先使用 execute）

```javascript
// 步骤 1：使用 get_app_state 获取应用状态
// 返回当前打开文件、选中节点、顶层节点名称等基本信息
mcp__pencil__get_app_state({ filePath: "path/to/design.pen" })
// 返回示例：
// {
//   currentFile: "/path/to/design.pen",
//   selectedNodes: [],
//   topLevelNodes: [{ id: "drWxj", name: "任务列表", type: "frame" }]
// }

// 步骤 2：使用 execute + Get() 读取节点数据
// 在 execute 的 input 中使用 Get() 函数读取节点
mcp__pencil__execute({
  filePath: "path/to/design.pen",
  input: `
    // 读取指定节点及其子树（深度 4）
    const node = Get("drWxj", { depth: 4, resolveInstances: true });
    Print(JSON.stringify(node, null, 2));
  `
})
// 返回 OK，节点数据在 response 中显示

// 步骤 3：遍历文档获取所有文本节点
mcp__pencil__execute({
  filePath: "path/to/design.pen",
  input: `
    const texts = Get(n => n.type === "text" ? { 
      id: n.id, 
      name: n.name, 
      content: n.content,
      fontSize: n.fontSize,
      fill: n.fill
    } : undefined, { depth: 4 });
    Print(JSON.stringify(texts, null, 2));
  `
})

// 步骤 4：获取变量定义
mcp__pencil__execute({
  filePath: "path/to/design.pen",
  input: `
    const vars = GetVariables();
    Print(JSON.stringify(vars, null, 2));
  `
})

// 步骤 5：当 execute 无法满足时，使用 Read 读取完整 JSON
const penData = Read({ filePath: "path/to/design.pen" });
```

### 工具使用决策树

```
需要分析 .pen 文件？
├── 首先：mcp__pencil__get_app_state（验证文件状态）
├── 然后：mcp__pencil__execute + Get()（读取节点数据）
│   ├── 能获取所需数据 → 完成 ✅
│   └── 无法满足复杂查询 → 使用 Read 读取 JSON
└── 需要修改设计稿？
    └── mcp__pencil__execute + Insert/Update/Delete()
```

### 各工具能力边界

| 需求 | get_app_state | execute + Get() | Read |
|------|---------------|-----------------|------|
| 验证文件已打开 | ✅ | ✅ | ✅ |
| 获取顶层节点名称 | ✅ | ✅ | ✅ |
| 获取选中节点 | ✅ | ❌ | ❌ |
| 读取子节点/层级 | ❌ | ✅ | ✅ |
| 读取文字内容 | ❌ | ✅ | ✅ |
| 遍历查找节点 | ❌ | ✅ | ✅ |
| 获取变量定义 | ❌ | ✅ | ✅ |
| 导出截图/HTML | ❌ | ✅ | ❌ |
| 修改节点属性 | ❌ | ✅ | ❌ |
| 创建新节点 | ❌ | ✅ | ❌ |

### execute 工具关键说明

**用途**：在 pen.dev 上下文中执行 JavaScript，支持读取和修改设计稿

**execute 内部可用 API**：

| 函数 | 用途 | 示例 |
|------|------|------|
| `Get(path, options)` | 读取指定节点及其子树 | `Get("drWxj", { depth: 4 })` |
| `Get(visit, options)` | 遍历文档树，访问器返回数据 | `Get(n => n.type === "text" ? n.content : undefined)` |
| `GetVariables()` | 获取变量定义 | `GetVariables()` |
| `Insert(parent, nodeData)` | 插入新节点 | `Insert("parent-id", { type: "text", ... })` |
| `Update(path, updateData)` | 更新节点属性 | `Update("node-id", { fill: "#ff0000" })` |
| `Delete(path)` | 删除节点 | `Delete("node-id")` |
| `TakeScreenshot(nodeIds)` | 截图指定节点 | `TakeScreenshot(["node-id"])` |
| `Export(nodeIds, format, path)` | 导出为图片/HTML | `Export(["node-id"], "png", "/path/output.png")` |
| `Print(...values)` | 打印调试信息到响应 | `Print(JSON.stringify(node))` |

**Get 选项**：
- `depth`: 读取深度（0=自身，1=直接子节点，...）
- `resolveVariables`: 解析变量值为实际值
- `resolveInstances`: 展开组件实例

**返回值**：
- 成功返回 "OK"
- 执行结果通过 `Print()` 输出到响应消息
- 失败返回错误信息和 `editId`（可用于修复）

**重要**：`get_style` 和 `read_skill` 工具当前版本不可用。

---

## Figma 链接

### 可用工具

| 工具 | 用途 |
|------|------|
| `mcp__Framelink_Figma_MCP__get_figma_data` | 获取设计稿数据 |
| `mcp__Framelink_Figma_MCP__download_figma_images` | 下载图像资源 |

### URL 解析

从 Figma URL 中解析 fileKey 和 nodeId：

- URL 格式：`https://www.figma.com/file/{fileKey}/{fileName}?node-id={nodeId}`
- 或：`https://www.figma.com/design/{fileKey}/{fileName}?node-id={nodeId}`
- nodeId 格式：`1234:5678`

### 使用示例

```javascript
// 获取设计稿数据
mcp__Framelink_Figma_MCP__get_figma_data({ fileKey, nodeId, depth })

// 下载图像资源
mcp__Framelink_Figma_MCP__download_figma_images({ fileKey, localPath, nodes })
```

---

## MasterGo 链接

### 可用工具

| 工具 | 用途 |
|------|------|
| `mcp__mastergo-magic-mcp__mcp__getDsl` | 获取 DSL 数据 |
| `mcp__mastergo-magic-mcp__mcp__getComponentLink` | 获取组件文档 |
| `mcp__mastergo-magic-mcp__mcp__getMeta` | 获取元数据信息 |

### URL 解析

- URL 格式：`https://{domain}/file/{fileId}/{name}?layer_id={layerId}`
- 或短链接：`https://{domain}/goto/{shortLink}`

### 使用示例

```javascript
// 获取 DSL 数据
mcp__mastergo-magic-mcp__mcp__getDsl({ fileId, layerId })
// 或使用短链接
mcp__mastergo-magic-mcp__mcp__getDsl({ shortLink })
```

### 分析脚本

```bash
# 基本用法
python scripts/mastergo-dsl-analyzer.py <dsl_json_file>

# 输出 Markdown 校验报告
python scripts/mastergo-dsl-analyzer.py <dsl_json_file> --format markdown

# 提取卡片标题（用于校验三）
python scripts/mastergo-dsl-analyzer.py <dsl_json_file> --titles
```

---

## ⚠️⚠️⚠️ MasterGo INSTANCE 组件深度遍历规范（强制严格执行）

### 核心原则

**MasterGo 的实际内容存储在 INSTANCE 组件内部，不在顶层 GROUP 节点！**

**禁止仅读取顶层节点，必须递归遍历 INSTANCE 内部！**

### INSTANCE 组件结构特性

```
GROUP (组14785, y=552) - 区域容器 ⬅️ 顶层节点
├── INSTANCE (16:1519) - 卡片组件实例 ⬅️ 组件实例，实际内容在这里！
│   └── 内部嵌套结构（深度 3-5 层）
│       ├── GROUP (标题组件)
│       │   └── TEXT「部门成员」⬅️ 实际标题文字
│       └── GROUP (年份选择器)
│           └── TEXT「2026年」⬅️ 实际选择器文字
├── 图表
└── 图例
```

### ❌ 错误做法（严厉禁止）

```python
# ❌ 错误：只读取顶层 GROUP 的直接子节点
for child in region_node.get('children', []):
    if child.get('type') == 'TEXT':  # INSTANCE 内部的 TEXT 不会被找到！
        texts.append(child)
```

**后果**：遗漏 INSTANCE 组件内部的所有文字、选择器、Tab 切换等元素！

### ✅ 正确做法（强制执行）

```python
# ✅ 正确：递归遍历 INSTANCE 组件内部
def extract_texts_from_instance(node, texts, depth=0, max_depth=6):
    """递归提取 INSTANCE 组件内部的所有文字"""

    # 1. 检查当前节点是否为 TEXT 类型
    if node.get('type') == 'TEXT':
        text_arr = node.get('text', [])
        if text_arr and len(text_arr) > 0:
            texts.append({
                'content': text_arr[0].get('text', ''),
                'node_id': node.get('id', ''),
                'node_name': node.get('name', ''),
            })

    # 2. 递归遍历所有子节点（包括 INSTANCE 内部）
    if depth < max_depth:
        for child in node.get('children', []):
            extract_texts_from_instance(child, texts, depth + 1, max_depth)
```

### 强制检查清单（每个区域必须执行）

| 检查项 | 检查方法 | 遗漏后果 |
|--------|----------|----------|
| 识别 INSTANCE 节点 | 遍历区域直接子节点，找出 `type === 'INSTANCE'` | 不知道哪些是组件实例 |
| 递归读取 INSTANCE 内部 | 对 INSTANCE 节点执行深度遍历（至少 4 层） | 遗漏标题、选择器、Tab 等 |
| 提取所有 TEXT 节点 | 递归查找所有 `type === 'TEXT'` 的节点 | 文字内容缺失 |
| 验证标题来源 | 确认标题是否来自 INSTANCE 内部 | 标题不一致 |
| 检查年份/时间选择器 | 搜索「年」「月」「日」等关键词 | 选择器遗漏 |
| 检查 Tab 切换文字 | 搜索 INSTANCE 内部的 Tab 相关节点 | Tab 文字遗漏 |

### ⚠️ 真实遗漏案例（2026-04-08）

**案例：遗漏年份选择器和 Tab 切换文字**

| 问题 | 设计稿实际内容 | 遗漏原因 |
|------|----------------|----------|
| 区域2「全年结算总额」 | 年份选择器「2026年」在 INSTANCE 内部 | 未递归遍历 INSTANCE |
| 区域4「部门成员」 | 年份选择器「2026年」在 INSTANCE 内部 | 未递归遍历 INSTANCE |
| 区域3/5/6 | Tab 切换组件在 INSTANCE 内部 | 只列出空结构，未提取文字 |

**根本原因**：脚本 `find_common_components` 只检查直接 children，未递归进入 INSTANCE 内部。

### 强制规则（违反即错误）

- [ ] **每个区域必须检查是否包含 INSTANCE 节点**
- [ ] **INSTANCE 节点必须递归遍历其内部 children（深度至少 4 层）**
- [ ] **所有文字必须从 TEXT 节点的 text 字段提取，不能凭节点名称推断**
- [ ] **年份选择器必须在 INSTANCE 内部搜索「年」「月」关键词**
- [ ] **Tab 切换文字必须从 INSTANCE 内部的 TEXT 节点提取**
- [ ] **层级结构中不能出现空的节点结构（如空 Tab 列表）**

---

## 本地图片

### 使用步骤

1. **读取图片**：使用模型视觉能力识别图片内容

2. **视觉分析**（遵守从上到下、从左到右、从外到里顺序）
   - 整体布局（页面类型、尺寸比例、结构）
   - 区域划分（按顺序记录各区域位置和内容）
   - 文字内容（按区域记录文字、字号、颜色）
   - 图片与图标（位置、尺寸）
   - 样式规范（主色、背景色、圆角、间距）

3. **注意事项**
   - 视觉识别无法获取精确像素值，需标注为「估算值」
   - 颜色识别为近似值，需标注为「约 #XXXXXX」

---

## .pen 文件节点解析约束规则

### 核心原则

**必须使用 Pencil MCP 工具（`execute` + `Get()`）或 `Read` 工具读取实际节点数据，禁止凭视觉推断组件类型或状态！**

`.pen` 文件本质上是 JSON 对象树，顶层为 `Document`，子节点类型包括 `frame`、`group`、`rectangle`、`text`、`path`、`icon`、`ref` 等。可通过以下方式读取：

1. **首选方式**：`execute` + `Get()` - 在 pen.dev 上下文中读取节点
2. **备选方式**：`Read` - 直接读取 .pen 文件的 JSON 内容

### 读取方式对比

| 方式 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| `execute` + `Get()` | 需要筛选节点、获取变量、导出截图 | 支持遍历查询、获取运行时状态 | 需要熟悉 Get API |
| `Read` | 需要完整节点树、复杂递归分析 | 直接获取完整 JSON | 文件大时分段读取复杂 |

### execute + Get() 使用规范

#### 基本用法

```javascript
// 读取指定节点及其子树（深度 4）
mcp__pencil__execute({
  filePath: "path/to/design.pen",
  input: `
    const node = Get("drWxj", { depth: 4, resolveInstances: true });
    Print(JSON.stringify(node, null, 2));
  `
})

// 遍历查找所有文本节点
mcp__pencil__execute({
  filePath: "path/to/design.pen",
  input: `
    const texts = Get(n => n.type === "text" ? { 
      id: n.id, 
      content: n.content,
      fontSize: n.fontSize 
    } : undefined, { depth: 4 });
    Print(JSON.stringify(texts, null, 2));
  `
})

// 获取变量定义
mcp__pencil__execute({
  filePath: "path/to/design.pen",
  input: `
    const vars = GetVariables();
    Print(JSON.stringify(vars, null, 2));
  `
})
```

#### Get 选项说明

| 选项 | 说明 | 建议值 |
|------|------|--------|
| `depth` | 读取深度（0=自身） | **4（强制建议）**，复杂页面需 5+ |
| `resolveInstances` | 是否展开 `ref` 组件实例 | **true（强制建议）** |
| `resolveVariables` | 是否解析 `$variable` 为实际值 | true（需看实际色值时） |

#### ⚠️ 强制要求：读取深度设置

**读取深度不足会导致遗漏嵌套内容！**

```javascript
// ❌ 错误：depth 为 1 或 2，可能遗漏第二层嵌套
Get("target", { depth: 2 })

// ✅ 正确：depth 为 4，并展开实例
Get("target", { depth: 4, resolveInstances: true })
```

| 设计复杂度 | 推荐 depth | 可能遗漏的风险 |
|------------|------------|----------------|
| 简单页面（单层结构） | 2 | 低 |
| 中等复杂（有嵌套容器） | 3 | 中 - 可能遗漏第二层容器内的内容 |
| 复杂页面（多层嵌套） | **4+** | **高** - 可能遗漏信息行、嵌套标签 |
| 含实例组件的页面 | **4+** | **高** - 必须设置 resolveInstances: true |

---

### Read 工具使用规范（备选）

```javascript
// 读取完整 .pen 文件
const penData = Read({ filePath: "path/to/design.pen" });

// .pen 文件结构：
// {
//   "version": "2.17",
//   "children": [/* 顶层节点数组 */],
//   "variables": { /* 变量定义 */ }
// }
```

#### 参数说明

| 参数 | 说明 | 建议值 |
|------|------|--------|
| `filePath` | .pen 文件路径 | 必填 |
| `limit` | 读取行数限制 | 如需分段读取，设置此值 |
| `offset` | 起始行号 | 分段读取时设置 |

#### ⚠️ 强制要求：递归深度设置

**.pen 文件可能很大，需要递归遍历节点树以读取完整嵌套结构！**

```javascript
// ❌ 错误：只读取第一层 children，可能遗漏深层嵌套
const topNodes = penData.children; // 只得到顶层节点

// ✅ 正确：递归遍历节点树（深度 4+）
function traverseNode(node, depth = 0, maxDepth = 4) {
  if (depth >= maxDepth) return node;
  if (node.children) {
    node.children = node.children.map(child => traverseNode(child, depth + 1, maxDepth));
  }
  // 处理 ref 组件实例
  if (node.type === "ref" && node.ref) {
    // ref 节点需要查找原组件定义
    const original = findComponentById(penData, node.ref);
    node._resolved = original;
  }
  return node;
}
```

| 设计复杂度 | 推荐遍历深度 | 可能遗漏的风险 |
|------------|--------------|----------------|
| 简单页面（单层结构） | 2 | 低 |
| 中等复杂（有嵌套容器） | 3 | 中 - 可能遗漏第二层容器内的内容 |
| 复杂页面（多层嵌套） | **4+** | **高** - 可能遗漏信息行、嵌套标签 |
| 含实例组件的页面 | **4+** | **高** - 必须展开 ref 组件实例 |

#### ⚠️ 真实遗漏案例

**案例：遍历深度不足导致遗漏第二行信息**

| 设置 | 结果 |
|------|------|
| depth: 2 | 只看到第一行4列信息 |
| depth: 4 | 发现还有第二行3列信息 |

**遗漏内容**：约定交付截止日、确收日期、业务经理

#### 关键字段解析

**必须检查以下字段确认组件属性**：

| 字段 | 用途 | 示例判断 |
|------|------|----------|
| `name` | 确认组件类型 | `components/table-column/check-box` → checkbox 列 |
| `type` | 确认节点类型 | `ref` → 组件实例，`frame` → 普通容器 |
| `children` | 确认子元素数量和类型 | 11 个 `table-cell/checkbox` → 11 行 checkbox |
| `enabled` | 确认组件状态 | `false` → 列被禁用 |
| `ref` | 确认引用的组件 ID | 用于追踪组件来源 |
| `reusable` | 确认是否为可复用组件 | `true` → 设计系统组件 |
| `width/height` | 确认尺寸 | 精确像素值 |
| `x/y` | 确认位置 | 精确像素值 |
| `opacity` | 确认透明度 | `0` → 完全透明，等效隐藏 |

#### 节点 name 字段解析规则

通过 `name` 字段识别组件类型：

| name 字段模式 | 实际组件类型 | 验证方法 |
|---------------|--------------|----------|
| `components/table-column/check-box` | Checkbox 列 | 检查 children 是否为 checkbox 单元格 |
| `components/table-column/text` | 文本列 | 检查 children 是否为文本单元格 |
| `components/table-cell/checkbox` | Checkbox 单元格 | 父节点应为 checkbox 列 |
| `components/table-cell/text` | 文本单元格 | 检查 content 字段 |
| `components/checkbox` | Checkbox 组件 | 检查 enabled、checked 字段 |
| `components/button` | Button 组件 | 检查 enabled、variant 字段 |
| `components/input` | Input 组件 | 检查 placeholder、value 字段 |
| `components/tab` | Tab 组件 | 检查 children 数量确认 Tab 数 |
| `components/pagination` | 分页组件 | 检查 currentPage、totalPages |

#### 组件状态字段解析

| 字段 | 值 | 状态说明 | 开发影响 |
|------|-----|----------|----------|
| `enabled` | `false` | 禁用状态 | 需添加 disabled 属性 |
| `enabled` | `true` | 启用状态 | 正常交互 |
| `checked` | `false` | 未选中 | checkbox 默认状态 |
| `checked` | `true` | 已选中 | checkbox 默认选中状态 |
| `visible` | `false` | 隐藏 | 需添加条件渲染 |
| `visible` | `true` | 可见 | 正常显示 |

#### children 字段验证规则

**必须验证 children 数量与预期一致**：

```javascript
// 示例：验证 checkbox 列（使用 Read 读取 .pen 文件）
const penData = Read({ filePath: "path/to/design.pen" });
const col = findNodeById(penData, "checkbox-column-id");

// 验证规则：
// 1. name 字段：components/table-column/check-box → 确认是 checkbox 列
// 2. children 字段：包含 11 个 components/table-cell/checkbox → 确认有 11 行 checkbox
// 3. enabled 字段：false → 确认列被禁用，前端需设置 disabled
```

#### 组件实例解析规则

当节点 `type` 为 `ref` 时，表示这是组件实例：

| 字段 | 说明 | 验证方法 |
|------|------|----------|
| `ref` | 引用的组件 ID | 使用 `Read` 读取 .pen 文件后查找原组件定义 |
| `children` | 覆盖的子元素 | 检查是否有自定义内容 |
| `reusable` | 原组件是否可复用 | 读取原组件的 reusable 字段 |

**解析步骤**：

1. 获取实例节点的 `ref` 字段值
2. 使用 `Read` 读取 .pen 文件，查找原组件定义
3. 对比实例与原组件的差异
4. 记录覆盖的属性和子元素

#### 批量读取示例

```javascript
// 批量读取多个节点详情（使用 Read 读取 .pen 文件）
const penData = Read({ filePath: "path/to/design.pen" });

// 递归查找节点
function findNodeById(node, id) {
  if (node.id === id) return node;
  if (node.children) {
    for (const child of node.children) {
      const found = findNodeById(child, id);
      if (found) return found;
    }
  }
  return null;
}

// 批量读取节点
const nodes = ["node1", "node2", "node3"].map(id => findNodeById(penData, id));

// 搜索特定类型节点（如所有 text 节点）
function findNodesByType(node, type, results = []) {
  if (node.type === type) results.push(node);
  if (node.children) {
    node.children.forEach(child => findNodesByType(child, type, results));
  }
  return results;
}
const allTexts = findNodesByType(penData, "text");

// 搜索可复用组件
const reusableComponents = [];
function findReusable(node) {
  if (node.reusable) reusableComponents.push(node);
  if (node.children) {
    node.children.forEach(child => findReusable(child));
  }
}
findReusable(penData);
```

> **注意**：以上 JS 代码为基于 .pen schema 的示例模式。实际使用时需根据具体文件结构调整。

### 表格专项解析规则

**表格是高频错误区，必须严格按以下步骤解析**:

#### 步骤 1：识别表格结构

```javascript
// 读取表格容器（使用 Read 读取 .pen 文件）
const penData = Read({ filePath: "path/to/design.pen" });
const table = findNodeById(penData, "table-container-id");
// 递归遍历 table.children 获取完整结构
```

验证内容：
- 表格行数：统计 children 中行节点数量
- 表格列数：读取第一行，统计列节点数量

#### 步骤 2：逐列解析

**禁止根据页面名称推断列标题！**

| 验证项 | 字段 | 说明 |
|--------|------|------|
| 列类型 | `name` | `table-column/check-box` → checkbox 列 |
| 列标题 | `children[0].content` | 文本列的实际标题文字 |
| 列宽度 | `width` | 精确像素值 |
| 列状态 | `enabled` | `false` → 禁用列 |
| 列数量 | `children.length` | 验证单元格数量 = 数据行数 |

#### 步骤 3：验证 checkbox 列

```javascript
// 读取 checkbox 列详情（使用 Read 读取 .pen 文件）
const penData = Read({ filePath: "path/to/design.pen" });
const col = findNodeById(penData, "checkbox-column-id");

// 验证规则：
// - name: components/table-column/check-box → 确认是 checkbox 列
// - children: 包含 N 个 components/table-cell/checkbox → 确认有 N 行
// - enabled: false → 确认整列禁用（前端需设置 disabled）
// - children[每项].checked: true/false → 确认每行选中状态
```

#### 步骤 4：验证特殊列

| 特殊列类型 | 验证字段 | 说明 |
|------------|----------|------|
| 头像列 | `children` 子节点 type | 是否包含 image 或 ref(头像组件) |
| 进度条列 | `children` 子节点 name | 是否包含 progress 组件 |
| 标签列 | `children` 子节点 content | 标签文字内容 |
| 操作列 | `children` 子节点 name | 是否包含 button 组件 |

### 组件状态验证清单

**解析每个组件时必须验证以下状态**：

- [ ] `enabled` 字段：确认是否禁用（.pen schema 通用字段）
- [ ] `opacity` 字段：确认透明度，`0` 表示隐藏
- [ ] `checked` 字段（checkbox）：确认选中状态（可能位于 `metadata` 或组件约定字段中）
- [ ] `variant` / `state` 字段（按钮）：确认按钮状态（如 `primary`、`disabled`、`loading`）
- [ ] `metadata` 对象：确认自定义状态字段

### 禁止行为清单

| 禁止行为 | 正确做法 |
|----------|----------|
| 凭视觉推断组件类型 | 必须读取 `name` 字段确认 |
| 凭经验推断列标题 | 必须读取 `children` 中文本节点 |
| 假设 checkbox 默认启用 | 必须检查 `enabled` 字段 |
| 假设 checkbox 默认未选中 | 必须检查 `checked` 字段 |
| 凭视觉推断层级结构 | 必须使用 `mcp__pencil__execute` 读取 children |
| **在层级结构中显示 `enabled: false` 元素** | **排除禁用元素，只显示可见组件** |

---

## 扫描顺序

**按「从上到下、再从左到右」扫描**：
- 先按 y 坐标排序所有区域
- 再在同一行内按 x 坐标排序

---

## 获取内容清单

### 布局信息

- 整体尺寸（宽度、高度）
- 区域列表（x, y, w, h）
- 区域间间距

### 节点信息

- 文字内容、字体、字号、字重、颜色、行高
- 图片尺寸、位置、比例、圆角
- 布局参数（padding, gap, margin, align-items, justifyContent）
- 层级关系（嵌套、父子、兄弟）

---

## 搜索关键词

| 搜索关键词 | 定位内容 |
|-----------|---------|
| `Pencil\|mcp__pencil` | Pencil MCP 工具 |
| `Figma\|mcp__Framelink` | Figma MCP 工具 |
| `MasterGo\|mcp__mastergo` | MasterGo MCP 工具 |
| `本地图片\|视觉识别` | 本地图片处理 |
| `execute\|节点解析\|关键字段` | .pen 文件节点解析 |
| `name 字段\|children 字段\|enabled 字段` | 字段解析规则 |
| `组件类型\|table-column\|table-cell` | 组件类型识别 |
| `表格专项\|列标题\|checkbox 列` | 表格解析规则 |
| `组件状态\|enabled\|checked\|visible` | 状态验证 |
| `禁止行为\|禁止推断\|必须读取` | 解析约束 |