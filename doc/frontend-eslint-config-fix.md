# Fixing ESLint Config 技能文档

## 使用时机

在以下情况使用此技能：

- `npm run lint` 空转或报 "all files matching... are ignored"
- 存量 Vue/JS 项目需要接入或修复 ESLint
- `lintOnSave` overlay 或 CI/发版脚本被 ESLint error 阻塞
- 存量代码与 ESLint 配置风格冲突产生海量报错
- 手动调用 `/frontend-eslint-config-fix` 命令

---

## 核心原则

### 配置适配代码，不是代码适配配置

存量项目的 `.eslintrc.js` 多为脚手架模板默认值，从未真正跑过——它与真实代码风格可能**方向相反**。

修 eslint 时禁止建议 `--fix` 批量改存量代码来迁就配置；先让配置迁就代码。

### 验收线：0 error + exit 0

- **warning** 可留给后续治理
- **error** 必须清零，因为以下消费方会被 error 真实阻塞：
  - `lintOnSave`（dev overlay 只弹 error）
  - CI 流水线
  - 发版脚本（`lint:check && npm publish` 类串联）

修完 exit 1 就交付 = 半成品。

---

## 工作流程

### 步骤 1：诊断 lint 死活（30 秒）

```bash
npm run lint; echo "exit=$?"
```

| 现象 | 诊断 | 处理 |
|------|------|------|
| exit 2 + `all of the files matching... are ignored` | **空转** | 查 `.eslintignore` |
| exit 0 且 0 输出但代码明显有问题 | 也是空转 | 用 `--no-ignore` 复核 |

复核命令：

```bash
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | tail -3
```

**`.eslintignore` 的 gitignore 语义陷阱**：模式不含 `/`（如 `*.js`、`*.vue`）时匹配**任意目录层级**——两条裸 glob 就能吞掉整个 src。

修复方式：

- 按目录精确忽略：`src/assets/`
- 锚定根目录：`/*.js`

---

### 步骤 2：量化基线（不许凭感觉调规则）

```bash
# 按规则统计
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | \
  grep -oE '\[[a-zA-Z@/-]+\]$' | sort | uniq -c | sort -rn | head -30

# 按文件统计（找噪音大户：第三方源码副本/生成文件）
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | \
  grep -E '\.(js|vue):[0-9]+:' | \
  sed -E 's/^(.*)\.(js|vue):[0-9]+:.*$/\1.\2/' | \
  sort | uniq -c | sort -rn | head -15
```

**判定标准**：单个文件贡献 >50% 报错 → 它是第三方副本/生成物，进 `.eslintignore`，不属于规则调参问题。

---

### 步骤 3：配置对齐存量代码（最常见的方向性错误）

**读 10 行真实业务代码，数出事实风格**，再定规则值——不要抄社区惯例（prettier 默认 `semi: never`，但多数国内存量项目带分号）：

| 检查什么 | 怎么判定 | 代码带分号时 |
|----------|----------|--------------|
| `semi` | 数语句尾分号占比 | `['warn'/'error', 'always']` |
| `comma-dangle` | 看多行对象最后一行有没有 `,` | 多行有尾逗号 → 对象形式 `always-multiline`（注意 eslint 7.x 不接受 `'es5'` 字符串简写） |
| `quotes` | 看字符串引号 | 单引号 + `allowTemplateLiterals: true` |
| `eqeqeq` | 搜 `==`（`grep -rn ' == ' src \| wc -l`） | 存量大量 `==` → 降 warn |

**模板值与事实相反时，反转的是配置。** 这一步做对，万级 semi/quotes 假错直接消失。

---

### 步骤 4：归零三件套

1. **globals 补构建注入变量**：`no-undef` 大量同名报错 → grep 报错的变量名，是 DefinePlugin/webpack 注入的（如 `$globalConfig`）就进 `globals: { $globalConfig: 'readonly' }`

2. **噪音大户进 ignore**（第 2 步发现的）

3. **存量修不完的质量规则降 warn**：
   - `eqeqeq`、`prefer-const`、`vue/no-mutating-props`、`no-dupe-keys`、`no-empty`（配 `allowEmptyCatch: true`）等
   - **存量为 0 的规则保持 error**（`no-eval`、`no-dupe-args` 等）——新代码防线不能撤

**其他注意事项**：

- `parserOptions.ecmaVersion: 2020` 支持 script 内 `?.`/`??`（经 babel 转译的项目）
- eslint-plugin-vue 7.x 中 `vue/name-property-casing` 已更名 `vue/component-definition-name-casing`

---

### 步骤 5：验收闭环（REQUIRED，缺一不可）

- [ ] `npm run lint` → **0 errors**，exit 0
- [ ] 剩余 warning 数量已知且已告知用户，其中 `--fix` 可修复的数量已注明
- [ ] 评估过 lint 的**所有消费方**：`lintOnSave`（dev overlay 只弹 error）、CI、package.json 里串联 lint 的脚本（发版闸门）
- [ ] 改动的配置文件通过 `node --check`（连字符规则 key 必须加引号：`'global-require': 0`，裸写是语法错误）
- [ ] 未修改任何业务代码、未执行 `--fix`（除非用户明确要求且有 git/备份保护）

---

## 常见错误

| 错误 | 后果 |
|------|------|
| 把 exit 1（有 error）当"正常完成"交付 | dev overlay 弹错 / 发版被卡，用户返工 |
| 配置与代码冲突时建议 `--fix` 改代码 | 动几百个文件制造无意义 diff，掩盖配置模板才是错的事实 |
| 不量化就调规则 | 该 ignore 的第三方副本（17 万条噪音）被当规则问题反复调参 |
| 忘 `node --check` 校验配置语法 | 连字符 key 丢引号 → `Unexpected token '-'`，lint 直接崩 |

---

## 典型场景案例

### 场景 1：宿主项目修复

- 宿主 `.eslintrc.js` / `.eslintignore` 按此流程修复
- 配置对齐：`semi: always`、`comma-dangle` 对象形式多行尾逗号
- 全局变量：`$globalConfig` 入 globals
- 噪音文件：第三方副本（如 v-region）进 ignore
- 存量规则：降 warn → 结果 0 error / 1.1 万 warn

### 场景 2：lintOnSave 处理

- `vue.config.js` 中 `lintOnSave: NODE_ENV === 'development'`
- error 会触发 dev overlay，必须清零

### 场景 3：Monorepo 多包配置

- 子包（如 `packages/`）有独立 `lint:check` 串联在发版脚本里
- 包内配置是宿主规则的独立副本
- 宿主调规则需手动同步到子包

详见 `skills/frontend-eslint-config-fix/references/03-monorepo-guide.md`。

---

## 快速参考

### 诊断命令

```bash
# 检查 lint 状态
npm run lint; echo "exit=$?"

# 空转复核
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | tail -3

# 按规则统计
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | grep -oE '\[[a-zA-Z@/-]+\]$' | sort | uniq -c | sort -rn | head -30

# 按文件统计
npx eslint --ext .js,.vue src --no-ignore -f unix 2>&1 | grep -E '\.(js|vue):[0-9]+:' | sed -E 's/^(.*)\.(js|vue):[0-9]+:.*$/\1.\2/' | sort | uniq -c | sort -rn | head -15
```

### 配置文件语法校验

```bash
node --check .eslintrc.js
```

---

## 参考文档

| 文件 | 用途 | 读取时机 |
|------|------|----------|
| `skills/frontend-eslint-config-fix/references/01-diagnostic-commands.md` | 诊断命令详解、量化统计方法 | 步骤 1-2 |
| `skills/frontend-eslint-config-fix/references/02-common-rules.md` | 常见规则配置指南、宽松/严格模式模板 | 步骤 3-4 |
| `skills/frontend-eslint-config-fix/references/03-monorepo-guide.md` | Monorepo 配置策略、子包同步 | 步骤 5（Monorepo 项目） |
| `skills/frontend-eslint-config-fix/references/04-verification-checklist.md` | 完整验收清单（校验零到校验十一） | 步骤 5 |

---

## 版本信息

- 当前版本：1.0.0
- 更新日期：2026-10-16
