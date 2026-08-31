---
title: 截图交叉验证流程
impact: HIGH
impactDescription: Agent Team 模式验证，确保文档与设计稿一致
tags: screenshot, validation, agent-team, cross-check
---

# 截图交叉验证流程

## 为什么执行截图验证？

**真实错误案例（2026-04-13）**：文档与设计稿不一致

| 问题 | 错误操作 | 正确操作 |
|------|----------|----------|
| 文档记录了虚构元素 | 凭经验推断存在 | 获取截图直观验证 |
| 坐标归属错误 | 只读数据不验证 | 截图+坐标双重验证 |

**后果**：前端开发按文档实现后发现与设计稿不符，需返工修正

---

## Agent Team 模式验证流程

### 1. 创建验证团队

```javascript
// 使用 TeamCreate 创建验证团队
TeamCreate({
  team_name: "design-verification",
  description: "设计稿截图交叉验证团队"
})
```

### 2. 分配验证任务

**根据实际分析结果动态分配验证任务，每个区域分配一个独立的验证 Agent。**

**分配规则：**
- 区域数量 = 文档「区域列表」表格中的区域数量
- Agent 命名：`verify-{区域序号}` 或 `verify-{区域简称}`
- 每个 Agent 负责：截图获取 + 节点数据读取 + 文档对比验证

**示例分配：**

```
区域数量: N = {从区域列表获取}

验证任务分配:
├── verify-01 → 区域1（nodeId: xxx）
├── verify-02 → 区域2（nodeId: xxx）
├── verify-03 → 区域3（nodeId: xxx）
├── ...
└── verify-NN → 区域N（nodeId: xxx）

每个验证 Agent 使用工具（根据设计稿类型）：
- .pen 文件: 优先 `execute` + `Get()` / `TakeScreenshot()`，备选 `Read`
- Figma: mcp__Framelink_Figma_MCP__get_figma_data
- MasterGo: mcp__mastergo-magic-mcp__mcp__getDsl
- 本地图片: Read 工具直接读取图片
```

**⚠️ 注意：区域数量因设计稿而异，根据实际分析结果动态分配！**
**⚠️ 注意：工具选择因设计稿类型而异，使用对应的 MCP 工具！**

### 3. 验证 Agent 执行流程

**每个验证 Agent 执行以下操作（根据设计稿类型选择工具）：**

```
步骤1: 获取区域截图/视觉内容
       → .pen 文件: `execute` + `TakeScreenshot([nodeId])` 或 `Export([nodeId], "png", path)`
       → Figma: mcp__Framelink_Figma_MCP__get_figma_data(fileKey, nodeId)
       → MasterGo: mcp__mastergo-magic-mcp__mcp__getDsl(fileId, layerId)
       → 本地图片: Read(filePath) 直接读取图片

步骤2: 读取区域节点数据
       → .pen 文件: `execute` + `Get(nodeId, { depth: 4 })` 或 `Read` 读取 .pen 文件
       → Figma: mcp__Framelink_Figma_MCP__get_figma_data(fileKey, nodeId)
       → MasterGo: mcp__mastergo-magic-mcp__mcp__getDsl(fileId, layerId)
       → 本地图片: 无节点数据，仅视觉识别

步骤3: 对比文档与截图/数据
       → 检查文字内容是否一致
       → 检查元素位置是否一致
       → 检查层级结构是否一致
       → 检查图表类型是否一致
       → 检查状态字段是否一致

步骤4: 发现错误立即修正
       → 执行异常修正强制流程（5步）
       → 通知其他验证 Agent 同步修正

步骤5: 输出验证报告
       → 发送验证结果给 Team Lead
```

---

## 验证清单（每个区域验证）

| 验证项 | 验证方法 | 通过标准 |
|--------|----------|----------|
| 文字内容一致性 | 对比截图与文档文字 | 文字完全一致 |
| 元素位置一致性 | 对比截图坐标与文档坐标 | 坐标误差 < 5px |
| 层级结构一致性 | 对比截图层级与文档层级树 | 层级嵌套一致 |
| 图表类型一致性 | 读取节点 name 字段 | 类型名称一致 |
| 状态字段一致性 | 检查 enabled/visible 字段 | 状态记录正确 |
| 颜色样式一致性 | 对比截图颜色与文档颜色值 | 色值完全一致 |
| 元素数量一致性 | 统计截图元素与文档记录 | 数量一致 |

---

## 发现错误时的修正流程

**验证过程中发现错误，立即执行以下流程：**

```
步骤1: 记录错误发现位置
       → Agent 名称、验证区域、错误类型

步骤2: 发送错误报告给 Team Lead
       → SendMessage(to: "team-lead", message: "发现错误...")

步骤3: Team Lead 决定修正策略
       → 指定修正 Agent
       → 通知其他 Agent 等待

步骤4: 修正 Agent 执行异常修正流程
       → 执行 5 步修正流程（见 08-error-correction.md）

步骤5: 同步更新所有相关文档位置
       → 使用 Grep 搜索错误元素
       → 确认所有提及处均已修正

步骤6: 通知所有验证 Agent 继续验证
       → SendMessage(to: "team-lead", message: "修正完成，继续验证")
       → Team Lead 广播通知所有成员
```

---

## 验证完成标准

**所有区域验证通过后，文档有效：**

- [ ] 所有区域截图已获取
- [ ] 所有区域文字内容验证通过
- [ ] 所有区域位置坐标验证通过
- [ ] 所有区域层级结构验证通过
- [ ] 所有图表类型验证通过
- [ ] 所有状态字段验证通过
- [ ] 所有颜色样式验证通过
- [ ] 所有元素数量验证通过

---

## 验证报告模板

```markdown
> **截图交叉验证报告**
>
> 验证团队：design-verification
> 验证时间：YYYY-MM-DD HH:MM
> 设计稿类型：{.pen | Figma | MasterGo | 本地图片}
>
> | 区域 | 验证 Agent | 截图状态 | 文字验证 | 位置验证 | 层级验证 | 状态 |
> |------|------------|----------|----------|----------|----------|------|
> | {区域1名称} | verify-01 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | 通过/修正 |
> | {区域2名称} | verify-02 | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | 通过/修正 |
> | ... | ... | ... | ... | ... | ... | ... |
> | {区域N名称} | verify-NN | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | 通过/修正 |
>
> **发现的错误及修正**：
> - {错误1描述} → {修正措施}
> （若无错误则写：无）
>
> **验证结论**：文档与设计稿一致，验证通过 ✅ / 需修正后重新验证 ❌
```

**⚠️ 注意：表格行数取决于实际区域数量，动态生成！**