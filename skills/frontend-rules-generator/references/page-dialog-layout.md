# 页面、弹窗、布局使用规范模板

此模板用于生成项目的 `page-dialog-layout.md` 规则文件，约束三类高频结构的使用方式：页面（pages/views）、弹窗（dialog/modal）、布局（layout）。

生成时必须先分析项目实际代码，将模板中的占位内容（`{...}`）替换为项目真实约定，删除项目不存在的部分。

## YAML Frontmatter

```yaml
---
paths:
  - "src/pages/**/*.vue"
  - "src/views/**/*.vue"
  - "src/layout/**/*"
  - "src/layouts/**/*"
  - "src/components/**/Dialog*.vue"
  - "src/components/**/Modal*.vue"
---
```

React 项目对应替换为 `.tsx` 扩展名与实际目录。

## 完整模板示例

```markdown
---
paths:
  - "src/pages/**/*.vue"
  - "src/layout/**/*"
---
# 页面、弹窗、布局使用规范

## 一、页面（Page）使用规范

### 开发前检查流程

**新建页面前，必须按以下顺序检查：**

### 1. 检查是否已存在类似页面

```bash
# 搜索现有页面
ls src/pages/
grep -r "功能关键词" src/pages/
```

**页面复用判断**：

| 条件 | 处理方式 |
|------|----------|
| 已有页面完全满足需求 | 直接配置路由指向现有页面 |
| 已有页面可扩展（加 tab / 加分支） | 扩展现有页面 |
| 需求完全不同 | 新建页面 |

### 2. 页面归属与命名

| 规范项 | 约定 | 示例 |
|--------|------|------|
| 目录位置 | `src/pages/{模块名}/` | `src/pages/order/` |
| 文件命名 | PascalCase | `OrderList.vue`、`OrderDetail.vue` |
| 路由 name | 与页面用途一致的驼峰命名 | `orderList`、`orderDetail` |
| 路由 path | kebab-case | `/order-list`、`/order-detail` |

### 3. 页面代码模板示例

```vue
<!-- ✅ 标准页面结构 -->
<!-- src/pages/order/OrderList.vue -->
<template>
  <div class="page order-list-page">
    <!-- 搜索区 -->
    <!-- 表格区 -->
    <!-- 弹窗区 -->
  </div>
</template>

<script setup lang="ts">
// 1. 类型导入
// 2. 组件导入
// 3. composable 导入
// 4. 状态定义
// 5. 数据请求
// 6. 方法定义
</script>

<style scoped lang="scss">
.order-list-page {
  // 页面级样式
}
</style>
```

```vue
<!-- ❌ 错误：页面写成一坨，无分区注释 -->
```

### 4. 页面禁止事项

1. ❌ 禁止在页面中定义会被其他页面复用的组件——提取到 `src/components/`
2. ❌ 禁止页面之间直接相互 import——共用逻辑提取到 composable / utils
3. ❌ 禁止绕过路由直接渲染另一个页面组件
4. ❌ 禁止在页面内硬编码其他页面的路由路径——使用路由 name 跳转

## 二、弹窗（Dialog / Modal）使用规范

### 开发前检查流程

**新建弹窗前，必须按以下顺序检查：**

### 1. 检查全局已有哪些弹窗能力

**必须先搜索，确认使用方式**：

```bash
# 搜索 UI 库弹窗组件
grep -r "ElDialog\|el-dialog" src/
grep -r "a-modal" src/

# 搜索项目封装的弹窗组件
ls src/components/ | grep -i "dialog\|modal"
```

**弹窗能力清单**（按项目实际填写）：

| 能力 | 来源 | 使用场景 |
|------|------|----------|
| {ElDialog} | UI 库 | 通用信息展示 |
| {ConfirmDialog} | `src/components/` | 确认操作 |
| {FormDialog} | `src/components/` | 表单提交 |

### 2. 弹窗实现方式选择

| 条件 | 实现方式 | 示例 |
|------|----------|------|
| 简单确认/提示 | UI 库原生气泡/确认框 | 删除确认 |
| 通用交互（确认、表单提交） | 全局封装弹窗组件 | `FormDialog` |
| 页面专属复杂弹窗 | 页面内定义，命令式或声明式 | 订单详情抽屉 |

### 3. 弹窗代码模板示例

```vue
<!-- ✅ 声明式弹窗：页面内使用，状态收在页面 -->
<template>
  <FormDialog
    v-model="visible"
    :title="isEdit ? '编辑订单' : '新建订单'"
    :loading="submitting"
    @confirm="handleSubmit"
  >
    <OrderForm ref="formRef" :initial-data="currentOrder" />
  </FormDialog>
</template>

<script setup lang="ts">
const visible = ref(false)
const isEdit = computed(() => !!currentOrder.value?.id)

function openCreate() {
  currentOrder.value = null
  visible.value = true
}

function openEdit(row: Order) {
  currentOrder.value = row
  visible.value = true
}
</script>
```

```vue
<!-- ❌ 错误：弹窗内部自己管理打开状态，外部无法控制 -->
<!-- ❌ 错误：每个弹窗都从零写一个 dialog 壳，不用全局封装 -->
```

### 4. 弹窗禁止事项

1. ❌ 禁止重复封装弹窗壳——已有 `FormDialog`/`ConfirmDialog` 时必须复用
2. ❌ 禁止弹窗内部自行决定打开/关闭——打开状态由调用方（页面）持有
3. ❌ 禁止在弹窗关闭后不重置表单和内部状态
4. ❌ 禁止弹窗内直接操作路由（跳转走页面逻辑）
5. ❌ 禁止同步多个弹窗状态混乱——同时只应有一个主弹窗，嵌套弹窗需明确层级

## 三、布局（Layout）使用规范

### 开发前检查流程

**新建布局或往布局加东西前，必须按以下顺序检查：**

### 1. 检查现有布局结构

```bash
# 搜索现有布局
ls src/layout/
grep -r "router-view\|RouterView" src/layout/
```

**现有布局清单**（按项目实际填写）：

| 布局 | 文件 | 适用场景 |
|------|------|----------|
| {DefaultLayout} | `src/layout/DefaultLayout.vue` | 带侧边栏的主布局 |
| {BlankLayout} | `src/layout/BlankLayout.vue` | 登录页等无框架页面 |

### 2. 布局选择判断

| 条件 | 处理方式 |
|------|----------|
| 页面需要侧边栏/顶栏 | 使用 {DefaultLayout}，配置路由即可 |
| 登录、全屏预览等 | 使用 {BlankLayout} |
| 新的页面骨架结构（如分栏后台） | 评估后新建布局组件 |

### 3. 布局代码模板示例

```vue
<!-- ✅ 布局只管骨架，不含业务 -->
<!-- src/layout/DefaultLayout.vue -->
<template>
  <div class="layout">
    <AppHeader />
    <div class="layout-body">
      <AppSidebar />
      <main class="layout-main">
        <router-view />
      </main>
    </div>
  </div>
</template>
```

```javascript
// ✅ 路由层指定布局
{
  path: '/order',
  component: DefaultLayout,
  children: [
    { path: 'list', name: 'orderList', component: () => import('@/pages/order/OrderList.vue') }
  ]
}

// ❌ 错误：页面内部再包一层布局
```

### 4. 布局禁止事项

1. ❌ 禁止在布局组件中写业务逻辑或请求特定业务数据
2. ❌ 禁止页面内重复实现侧边栏/顶栏——应通过路由配置切换布局
3. ❌ 禁止绕过布局体系直接写全屏页面（除 BlankLayout 场景）
4. ❌ 禁止频繁新建布局——同骨架页面必须共用同一布局

## 通用约束

1. **先查后建**：页面、弹窗、布局三类都必须先搜索现有实现，再决定新建
2. **状态归属明确**：弹窗开关状态在页面，页面数据在页面，布局不持有业务状态
3. **命名可检索**：弹窗组件名必须含 Dialog/Modal/Drawer 后缀，布局必须含 Layout 后缀
```

## 生成时提取项目信息的检查点

生成 `page-dialog-layout.md` 前必须从项目代码中确认：

| 检查项 | 检查方式 | 填入位置 |
|--------|----------|----------|
| 页面目录是 `pages` 还是 `views` | `ls src/` | frontmatter paths、页面规范 |
| UI 库及弹窗组件名 | `grep "element-plus\|ant-design" package.json` | 弹窗能力清单 |
| 全局封装的弹窗组件 | `ls src/components/` 找 Dialog/Modal 命名 | 弹窗能力清单 |
| 现有布局组件 | `ls src/layout/` 或 `ls src/layouts/` | 布局清单 |
| 布局与路由的绑定方式 | 读取 `src/router/` 配置 | 布局模板示例 |
| 页面命名实际风格 | `ls src/pages/` 或 `ls src/views/` | 命名规范表 |
