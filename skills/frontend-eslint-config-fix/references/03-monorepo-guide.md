# Monorepo ESLint 配置指南

## 概述

Monorepo 项目（如使用 lerna、pnpm workspaces、yarn workspaces）中，ESLint 配置需要特别注意：

- 宿主（root）和子包（packages/*）可能有独立的 lint 配置
- 子包可能有独立的发版脚本，lint 串联在发版流程中
- 宿主规则修改不会自动同步到子包

---

## 典型结构

```
project-root/
├── .eslintrc.js              # 宿主 ESLint 配置
├── .eslintignore             # 宿主忽略配置
├── package.json              # 宿主 package.json
├── packages/
│   ├── admin-pages/
│   │   ├── .eslintrc.js      # 子包独立配置
│   │   ├── .eslintignore     # 子包独立忽略
│   │   └── package.json      # 子包 package.json（含 lint:check）
│   ├── shared-components/
│   │   ├── .eslintrc.js
│   │   └── package.json
│   └── utils/
│       └── package.json      # 可能没有独立 lint 配置
└── src/                      # 宿主源码
```

---

## 配置策略

### 策略 1：宿主配置 + 子包继承

宿主定义基础配置，子包通过 `extends` 继承。

**宿主 `.eslintrc.js`**：

```js
module.exports = {
  root: true,  // 重要：阻止向上查找配置
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended'
  ],
  rules: {
    'semi': ['error', 'always'],
    'quotes': ['error', 'single']
  }
}
```

**子包 `packages/admin-pages/.eslintrc.js`**：

```js
module.exports = {
  root: true,
  extends: [
    '../../.eslintrc.js',  // 继承宿主配置
    // 或继承后覆盖
  ],
  rules: {
    // 子包特有规则
    'vue/no-v-html': 'warn'
  }
}
```

**优点**：
- 配置集中管理
- 修改宿主配置自动生效

**缺点**：
- 子包必须使用相对路径
- 子包独立开发时可能缺少上下文

---

### 策略 2：共享配置包

创建共享配置包 `packages/eslint-config-*`。

**`packages/eslint-config-acme/index.js`**：

```js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended'
  ],
  rules: {
    'semi': ['error', 'always'],
    'quotes': ['error', 'single']
  }
}
```

**`packages/eslint-config-acme/package.json`**：

```json
{
  "name": "@acme/eslint-config",
  "version": "1.0.0",
  "main": "index.js"
}
```

**子包使用**：

```js
// packages/admin-pages/.eslintrc.js
module.exports = {
  extends: ['@acme/eslint-config']
}
```

**优点**：
- 配置版本化管理
- 跨项目复用

**缺点**：
- 需要维护配置包版本

---

### 策略 3：独立配置（最常见于存量项目）

宿主和子包各自维护独立配置，规则手动同步。

**适用场景**：
- 存量项目，子包历史配置差异大
- 子包由不同团队维护

**处理方式**：
- 宿主修改规则后，需手动同步到子包
- 建议在文档中记录规则变更

---

## 发版脚本中的 Lint

### 子包独立 lint 脚本

**`packages/admin-pages/package.json`**：

```json
{
  "scripts": {
    "lint:check": "eslint --ext .js,.vue src/",
    "prepublishOnly": "npm run lint:check"
  }
}
```

**风险**：`prepublishOnly` 串联 lint，lint 失败会阻塞发版。

**处理**：

1. **确保子包 lint 配置与宿主一致**：
   ```bash
   # 对比规则差异
   diff <(node -e "console.log(JSON.stringify(require('./.eslintrc.js').rules, null, 2))") \
        <(cd packages/admin-pages && node -e "console.log(JSON.stringify(require('./.eslintrc.js').rules, null, 2))")
   ```

2. **子包 lint 也应 0 error**：
   ```bash
   cd packages/admin-pages
   npm run lint:check; echo "exit=$?"
   ```

---

## 同步检查清单

宿主修改 ESLint 配置后，检查子包是否需要同步：

- [ ] 子包是否有独立 `.eslintrc.js`
- [ ] 子包 lint 脚本是否串联在发版流程（`prepublishOnly`、`lint:check`）
- [ ] 子包 lint 是否 0 error
- [ ] 子包 globals 是否包含特有的构建注入变量

---

## 常见问题

### 问题 1：子包 lint 报错宿主规则

**现象**：宿主 0 error，子包报错。

**原因**：子包配置未同步。

**解决**：
```bash
# 1. 检查子包配置
cd packages/admin-pages
cat .eslintrc.js | grep -A5 'rules:'

# 2. 手动同步规则
# 或修改子包配置继承宿主
```

### 问题 2：子包 lint 阻塞发版

**现象**：`npm publish` 在子包失败。

**原因**：`prepublishOnly` 串联的 lint 有 error。

**解决**：
```bash
# 临时绕过（不推荐）
npm publish --ignore-scripts

# 正确做法：修复子包 lint
cd packages/admin-pages
npm run lint:check
# 按修复流程处理
```

### 问题 3：子包 globals 缺失

**现象**：子包报 `no-undef` 错误。

**原因**：子包有特有的构建注入变量，未声明。

**解决**：
```js
// packages/admin-pages/.eslintrc.js
module.exports = {
  globals: {
    '__ADMIN_CONFIG__': 'readonly'
  }
}
```

---

## 快速参考

```bash
# 检查所有子包 lint 状态
for pkg in packages/*; do
  if [ -f "$pkg/package.json" ] && grep -q "lint:check" "$pkg/package.json"; then
    echo "=== $pkg ==="
    (cd "$pkg" && npm run lint:check; echo "exit=$?")
  fi
done

# 检查子包配置是否继承宿主
grep -r "extends.*\.\." packages/*/\.eslintrc.js
```
