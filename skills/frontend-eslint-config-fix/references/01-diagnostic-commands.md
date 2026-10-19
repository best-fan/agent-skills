# 诊断命令参考

## 基础诊断

### 检查 lint 状态

```bash
npm run lint; echo "exit=$?"
```

**退出码含义**：

| 退出码 | 含义 |
|--------|------|
| 0 | 正常完成，无错误 |
| 1 | 发现错误 |
| 2 | 参数错误或文件被忽略（空转） |

### 空转复核

当 `npm run lint` 返回 0 但实际未检查文件时：

```bash
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | tail -3
```

- `--no-ignore`：忽略 `.eslintignore` 配置，强制检查所有文件
- `-f unix`：Unix 风格输出，便于 grep 处理

---

## 量化统计

### 按规则统计

统计各规则产生的错误数量：

```bash
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | \
  grep -oE '\[[a-zA-Z@/-]+\]$' | \
  sort | uniq -c | sort -rn | head -30
```

**输出示例**：

```
  12456 [semi]
   8923 [quotes]
   3456 [no-unused-vars]
   1234 [eqeqeq]
    567 [comma-dangle]
```

**判定**：

- 某规则报错 > 5000：优先考虑调整规则而非修改代码
- 某规则报错 < 100：可以考虑修复代码

### 按文件统计

找出报错最多的文件（噪音大户）：

```bash
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | \
  grep -E '\.(js|vue):[0-9]+:' | \
  sed -E 's/^(.*)\.(js|vue):[0-9]+:.*$/\1.\2/' | \
  sort | uniq -c | sort -rn | head -15
```

**输出示例**：

```
  178234 src/vendor/v-region/index.js
   12345 src/components/LegacyForm.vue
    8901 src/utils/old-helper.js
```

**判定**：

- 单文件贡献 > 50% 报错：第三方副本或生成文件，进 `.eslintignore`
- 前 3 文件贡献 > 80% 报错：优先处理这些文件的 ignore 或规则调整

---

## 代码风格采样

### 分号使用

```bash
# 采样前 50 行代码
head -50 src/views/Home.vue | grep -E '^\s*[^/].*;\s*$' | wc -l
```

### 引号使用

```bash
# 单引号 vs 双引号
grep -roE "['\"]" src/ | sort | uniq -c
```

### 尾逗号使用

```bash
# 多行对象/数组最后一项是否有逗号
grep -B1 '^\s*}' src/views/Home.vue | head -20
```

### 等号使用

```bash
# == vs ===
grep -rn ' == ' src/ | wc -l
grep -rn ' === ' src/ | wc -l
```

---

## 配置文件校验

### ESLint 配置语法检查

```bash
node --check .eslintrc.js
```

**常见错误**：

- 连字符 key 未加引号：`'global-require': 0`（正确）vs `global-require: 0`（错误）
- 字符串引号不匹配

### ESLint 配置内容验证

```bash
# 打印最终合并后的配置
npx eslint --print-config src/index.js | head -50
```

---

## 快速诊断流程

```bash
# 1. 检查 lint 状态
npm run lint; echo "exit=$?"

# 2. 如 exit 0 但怀疑空转，复核
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | tail -3

# 3. 量化错误分布
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | \
  grep -oE '\[[a-zA-Z@/-]+\]$' | sort | uniq -c | sort -rn | head -10

# 4. 定位噪音文件
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | \
  grep -E '\.(js|vue):[0-9]+:' | \
  sed -E 's/^(.*)\.(js|vue):[0-9]+:.*$/\1.\2/' | sort | uniq -c | sort -rn | head -5

# 5. 校验配置语法
node --check .eslintrc.js
```
