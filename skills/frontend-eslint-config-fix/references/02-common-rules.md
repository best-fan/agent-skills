# 常见 ESLint 规则配置指南

## 代码风格类规则

### semi - 分号

控制语句末尾是否使用分号。

```js
// .eslintrc.js
rules: {
  'semi': ['error', 'always'],    // 强制使用分号
  // 'semi': ['error', 'never'],  // 强制不使用分号
}
```

**采样判定**：

```bash
# 检查代码中分号使用比例
head -100 src/views/Home.vue | grep -c ';\s*$'
```

| 场景 | 配置 |
|------|------|
| 多数语句有分号 | `['error', 'always']` |
| 多数语句无分号 | `['error', 'never']` |

---

### quotes - 引号

控制字符串使用的引号类型。

```js
rules: {
  'quotes': ['error', 'single', {
    'avoidEscape': true,          // 允许字符串包含需要转义的引号
    'allowTemplateLiterals': true // 允许使用模板字符串
  }]
}
```

| 场景 | 配置 |
|------|------|
| 代码使用单引号 | `['error', 'single']` |
| 代码使用双引号 | `['error', 'double']` |

---

### comma-dangle - 尾逗号

控制对象、数组等最后一项后是否有逗号。

```js
rules: {
  // 多行时要求尾逗号，单行时禁止
  'comma-dangle': ['error', {
    'arrays': 'always-multiline',
    'objects': 'always-multiline',
    'imports': 'always-multiline',
    'exports': 'always-multiline',
    'functions': 'never'
  }]
  
  // 简写形式（ESLint 7.x+）
  // 'comma-dangle': ['error', 'always-multiline']
}
```

**注意**：ESLint 7.x 不接受 `'es5'` 字符串简写，需使用对象形式。

---

### indent - 缩进

控制缩进风格。

```js
rules: {
  'indent': ['error', 2, {        // 2 空格缩进
    'SwitchCase': 1,              // switch case 缩进级别
    'flatTernaryExpressions': true // 三元表达式不额外缩进
  }]
}
```

---

## 质量类规则

### eqeqeq - 相等比较

控制是否使用 `===` 和 `!==`。

```js
rules: {
  'eqeqeq': ['warn', 'always', {  // 存量项目建议 warn
    'null': 'ignore'              // 允许 == null
  }]
}
```

**判定**：

```bash
grep -rn ' == ' src/ | wc -l  # 统计 == 使用量
```

| 场景 | 配置 |
|------|------|
| 存量大量 `==` | `['warn', 'always']` |
| 新代码 / 少量 `==` | `['error', 'always']` |

---

### no-unused-vars - 未使用变量

检测声明但未使用的变量。

```js
rules: {
  'no-unused-vars': ['error', {
    'args': 'none',               // 不检查函数参数
    'ignoreRestSiblings': true,   // 忽略解构剩余
    'caughtErrors': 'none'        // 不检查 catch 参数
  }]
}
```

---

### no-undef - 未定义变量

检测未声明的变量引用。

```js
rules: {
  'no-undef': 'error'
}

// 构建注入变量需要在 globals 中声明
globals: {
  '$globalConfig': 'readonly',
  '__webpack_public_path__': 'writable'
}
```

---

### prefer-const - 优先使用 const

检测可以声明为 `const` 的 `let` 变量。

```js
rules: {
  'prefer-const': ['warn', {      // 存量项目建议 warn
    'destructuring': 'any',
    'ignoreReadBeforeAssign': true
  }]
}
```

---

## Vue 专用规则

### vue/no-mutating-props - 禁止修改 props

```js
rules: {
  'vue/no-mutating-props': ['warn']  // 存量项目建议 warn
}
```

---

### vue/component-definition-name-casing - 组件命名风格

ESLint-plugin-vue 7.x+ 使用，替代已废弃的 `vue/name-property-casing`。

```js
rules: {
  'vue/component-definition-name-casing': ['error', 'PascalCase']
  // 或 'kebab-case'
}
```

---

### vue/html-indent - 模板缩进

```js
rules: {
  'vue/html-indent': ['error', 2, {
    'attribute': 1,
    'closeBracket': 0,
    'alignAttributesVertically': true
  }]
}
```

---

## 通用配置模式

### 宽松模式（存量项目）

适用于从未运行过 lint 的老项目，优先清零 error。

```js
module.exports = {
  rules: {
    // 风格类：按代码实际风格配置
    'semi': ['error', 'always'],
    'quotes': ['error', 'single', { allowTemplateLiterals: true }],
    'comma-dangle': ['error', 'always-multiline'],
    
    // 质量类：降为 warn
    'eqeqeq': 'warn',
    'prefer-const': 'warn',
    'no-unused-vars': 'warn',
    'vue/no-mutating-props': 'warn',
    
    // 底线规则：保持 error
    'no-eval': 'error',
    'no-dupe-args': 'error',
    'no-dupe-keys': 'error',
    'no-undef': 'error'
  }
}
```

### 严格模式（新项目）

适用于新项目或有代码规范的项目。

```js
module.exports = {
  rules: {
    // 风格类
    'semi': 'error',
    'quotes': ['error', 'single'],
    'comma-dangle': ['error', 'always-multiline'],
    'indent': ['error', 2],
    
    // 质量类
    'eqeqeq': 'error',
    'prefer-const': 'error',
    'no-unused-vars': 'error',
    'vue/no-mutating-props': 'error',
    
    // 最佳实践
    'no-var': 'error',
    'prefer-template': 'error',
    'object-shorthand': 'error'
  }
}
```

---

## 常见陷阱

### 连字符规则名必须加引号

```js
// 错误 - 语法错误
'global-require': 0

// 正确
'global-require': 0
```

### eslint-plugin-vue 版本兼容

| 规则 | 旧版 (< 7.x) | 新版 (>= 7.x) |
|------|--------------|---------------|
| 组件命名 | `vue/name-property-casing` | `vue/component-definition-name-casing` |

### parserOptions 配置

```js
module.exports = {
  parserOptions: {
    ecmaVersion: 2020,        // 支持 ?. ?? 等新语法
    sourceType: 'module'      // ES Module
  }
}
```
