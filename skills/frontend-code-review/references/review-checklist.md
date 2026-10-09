# 代码审查清单

## 代码质量

### 命名规范

- [ ] 组件文件使用 PascalCase（如 `UserCard.vue`）
- [ ] 组合式函数使用 camelCase + use 前缀（如 `useAuth`）
- [ ] 普通函数使用 camelCase（如 `getUserInfo`）
- [ ] 常量使用 SCREAMING_SNAKE_CASE（如 `MAX_RETRY_COUNT`）
- [ ] 变量使用 camelCase（如 `isLoading`）
- [ ] 类型/接口使用 PascalCase（如 `UserInfo`）

### 代码复杂度

- [ ] 函数不超过 50 行
- [ ] 嵌套最多 3 层
- [ ] 圈复杂度不超过 10
- [ ] 使用提前返回减少嵌套

### 代码整洁

- [ ] 无未使用的变量
- [ ] 无未使用的函数
- [ ] 无未使用的导入
- [ ] 无重复代码
- [ ] 无 `console.log`（生产代码）

### 错误处理

- [ ] 使用 try-catch 处理异步错误
- [ ] 错误信息对用户友好
- [ ] 错误后状态正确回退

---

## 类型安全

### 类型定义

- [ ] 无 `any` 类型
- [ ] 类型集中在 `src/types/` 管理
- [ ] interface 使用 `I` 前缀（如 `IUserInfo`）
- [ ] type 使用 `T` 前缀（如 `TStatus`）
- [ ] 请求参数使用 `Params` 后缀
- [ ] 响应数据使用 `Data` / `Info` 后缀
- [ ] 列表项使用 `Item` 后缀

### 类型使用

- [ ] 使用 `import type { }` 导入类型
- [ ] 从 `@/types` 统一导入（不导入子路径）
- [ ] 使用 `unknown` 替代 `any`
- [ ] 使用类型守卫进行类型收窄

### 类型安全示例

```typescript
// ✅ 正确
import type { IUserInfo } from '@/types'
function process(data: unknown) {
  if (typeof data === 'string') data.toUpperCase()
}

// ❌ 错误
const user: any = {}
import type { IUserInfo } from '@/types/models/user'
```

---

## Vue 组件

### 组件结构

- [ ] 每个组件单独一个目录
- [ ] 使用 `defineOptions` 声明组件名称
- [ ] 使用 `<script setup>` 语法
- [ ] 样式使用 `<style scoped>`

### 组件文件结构

```
ComponentName/
├── index.vue       # 组件入口
├── index.scss      # 样式文件
└── types.ts        # 类型定义（可选）
```

### Props 定义

- [ ] 使用 TypeScript interface 定义 Props
- [ ] 使用 `withDefaults` 设置默认值
- [ ] 数组/对象默认值使用工厂函数

```typescript
interface Props {
  userId: string       // 必填
  title?: string       // 可选
  items: OrderItem[]   // 数组
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  items: () => []
})
```

### Emits 定义

- [ ] 使用 TypeScript interface 定义 Emits
- [ ] 使用类型安全的 emit 调用

```typescript
interface Emits {
  (e: 'click', id: string): void
  (e: 'update:modelValue', value: string): void
}

const emit = defineEmits<Emits>()
emit('click', props.userId)
```

### 组件规范

- [ ] 不直接修改 props
- [ ] 事件绑定在模板中调用处理函数（如 `@click="handleClick"`）；非事件场景禁止在模板中直接调用函数
- [ ] 使用 computed 缓存计算结果

---

## 样式规范

### 文件结构

- [ ] 样式文件单独存放（`index.scss`）
- [ ] 使用 `<style scoped lang="scss" src="./index.scss">` 引入

### 命名规范

- [ ] 使用 BEM 命名法
- [ ] Block 使用 kebab-case（如 `.user-card`）
- [ ] Element 使用双下划线或嵌套
- [ ] Modifier 使用双横杠或 class 组合

### 样式规则

- [ ] 统一使用 `px` 单位
- [ ] 嵌套最多 3 层
- [ ] 使用 scoped 防止样式污染

---

## npm 安全

### 依赖检查

- [ ] 运行 `pnpm audit` 无高危漏洞
- [ ] 依赖版本不过时
- [ ] 无已知安全风险的包

### 许可证检查

- [ ] 无 GPL 许可证依赖（商业项目）
- [ ] 许可证兼容项目要求

详见 `npm-security-check.md`

---

## 性能优化

### 计算缓存

- [ ] 使用 `computed` 缓存计算结果
- [ ] 避免在模板中直接调用函数（事件除外）

### 防抖节流

- [ ] 搜索输入使用防抖
- [ ] 滚动事件使用节流
- [ ] 高频操作使用防抖/节流

### 懒加载

- [ ] 路由使用懒加载
- [ ] 大组件使用异步组件
- [ ] 图片使用懒加载

---

## 可访问性

- [ ] 图片有 alt 属性
- [ ] 表单有 label 关联
- [ ] 按钮有明确的文字或 aria-label
- [ ] 颜色对比度足够