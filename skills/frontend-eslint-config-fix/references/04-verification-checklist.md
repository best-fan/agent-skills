# 验收清单

## 概述

ESLint 配置修复完成后，必须逐项通过以下验收清单。任一项目未通过，视为未完成。

---

## 核心验收

### 校验零：0 error 验证

- [ ] `npm run lint` 退出码为 0
- [ ] 输出中无 `error` 级别问题
- [ ] 如有 error，继续修复

```bash
npm run lint; echo "exit=$?"
# 预期：exit=0
```

---

### 校验一：warning 统计

- [ ] 统计剩余 warning 数量
- [ ] 告知用户 warning 数量
- [ ] 说明哪些 warning 可通过 `--fix` 自动修复

```bash
# 统计 warning 数量
npm run lint 2>&1 | grep -c "warning"

# 统计可自动修复的数量
npx eslint --ext .js,.vue src --fix-dry-run 2>&1 | tail -1
```

---

### 校验二：配置文件语法

- [ ] `.eslintrc.js` 通过 `node --check`
- [ ] 连字符规则 key 已加引号（如 `'global-require': 0`）

```bash
node --check .eslintrc.js
# 无输出即通过
```

---

## 消费方验收

### 校验三：lintOnSave

- [ ] 检查 `vue.config.js` 或 `vite.config.js` 的 `lintOnSave` 配置
- [ ] 确认 `lintOnSave` 行为（是否只在 development 环境启用）
- [ ] 启动开发服务器，确认无 overlay 弹出

```bash
# 检查 lintOnSave 配置
grep -n "lintOnSave" vue.config.js vite.config.js 2>/dev/null

# 启动开发服务器验证
npm run dev  # 或 npm run serve
```

**lintOnSave 行为**：

| 配置 | 行为 |
|------|------|
| `true` | 每次保存都 lint |
| `false` | 不 lint |
| `'warning'` | 只警告，不弹 overlay |
| `NODE_ENV === 'development'` | 仅开发环境 lint |

**注意**：`lintOnSave` 只弹 error，warning 不会阻塞开发。

---

### 校验四：CI 流水线

- [ ] 检查 CI 配置文件（`.github/workflows/*`、`.gitlab-ci.yml`、`Jenkinsfile` 等）
- [ ] 确认 CI 中的 lint 命令
- [ ] 本地模拟 CI lint 命令，确认通过

```bash
# 查找 CI 配置
find . -name ".github" -o -name ".gitlab-ci.yml" -o -name "Jenkinsfile" | head -5

# 模拟 CI lint 命令
npm run lint
# 或
npx eslint --ext .js,.vue src/
```

---

### 校验五：发版脚本

- [ ] 检查 `package.json` 中串联 lint 的脚本
- [ ] 确认发版流程（`prepublishOnly`、`publish`、`lint:check && npm publish`）
- [ ] 本地模拟发版脚本，确认通过

```bash
# 检查 package.json 脚本
grep -E "(prepublish|publish|lint:check)" package.json

# 常见串联模式
# "prepublishOnly": "npm run lint:check"
# "publish": "npm run lint:check && npm publish"
# "release": "npm run build && npm run lint:check && npm publish"
```

---

## 安全验收

### 校验六：未修改业务代码

- [ ] 未使用 `--fix` 修改业务代码
- [ ] 未手动修改业务代码来适配配置
- [ ] 如有修改，确认用户明确要求且有备份

```bash
# 检查 git 状态
git status

# 应只有配置文件变更：
# modified: .eslintrc.js
# modified: .eslintignore
# 不应有业务代码变更
```

---

### 校验七：git 备份

- [ ] 修复前有 git commit 或备份
- [ ] 可回滚到修复前状态

```bash
# 检查最近提交
git log --oneline -5

# 如需回滚
git stash  # 暂存当前修改
# 或
git checkout .eslintrc.js .eslintignore  # 恢复配置文件
```

---

## 完整性验收

### 校验八：空转检查

- [ ] 确认 lint 实际检查了文件
- [ ] 无 "all files matching... are ignored" 警告
- [ ] 输出文件数量 > 0

```bash
# 检查 lint 检查的文件数
npx eslint --ext .js,.vue src/ --debug 2>&1 | grep "Linting" | wc -l
```

---

### 校验九：ignore 配置检查

- [ ] `.eslintignore` 语法正确
- [ ] 无裸 glob（如 `*.js`、`*.vue`）误忽略所有文件
- [ ] 第三方副本/生成文件已忽略

```bash
# 检查 .eslintignore
cat .eslintignore

# 正确示例：
# src/assets/        # 按目录精确忽略
# /*.js              # 锚定根目录
# src/vendor/        # 第三方副本
```

---

### 校验十：globals 检查

- [ ] 构建注入变量已声明在 globals
- [ ] 无 `no-undef` 误报

```bash
# 检查 globals
grep -A5 "globals:" .eslintrc.js

# 验证 no-undef 是否清零
npm run lint 2>&1 | grep "no-undef" | wc -l
# 预期：0
```

---

## Monorepo 专项

### 校验十一：子包 lint 同步

- [ ] 检查子包是否有独立 lint 配置
- [ ] 子包 lint 是否 0 error
- [ ] 子包 lint 是否串联在发版脚本

```bash
# 检查子包 lint 状态
for pkg in packages/*; do
  if [ -f "$pkg/package.json" ] && grep -q "lint:check" "$pkg/package.json"; then
    echo "=== $pkg ==="
    (cd "$pkg" && npm run lint:check 2>&1 | tail -3)
  fi
done
```

---

## 验收结果模板

```markdown
## 验收结果

### 核心验收
- [x] 校验零：0 error - exit=0 ✓
- [x] 校验一：warning 统计 - 11,234 个 warning，0 个可 --fix 修复
- [x] 校验二：配置文件语法 - node --check 通过 ✓

### 消费方验收
- [x] 校验三：lintOnSave - vue.config.js 配置为 NODE_ENV === 'development' ✓
- [x] 校验四：CI 流水线 - .github/workflows/ci.yml 中 npm run lint 通过 ✓
- [x] 校验五：发版脚本 - prepublishOnly 串联 lint:check 通过 ✓

### 安全验收
- [x] 校验六：未修改业务代码 - git status 仅显示配置文件变更 ✓
- [x] 校验七：git 备份 - 修复前已 commit (commit hash: abc123) ✓

### 完整性验收
- [x] 校验八：空转检查 - 实际检查 234 个文件 ✓
- [x] 校验九：ignore 配置 - 无裸 glob 误忽略 ✓
- [x] 校验十：globals 检查 - $globalConfig 已声明，no-undef 为 0 ✓

### Monorepo 专项（如适用）
- [x] 校验十一：子包 lint 同步 - packages/admin-pages 0 error ✓
```
