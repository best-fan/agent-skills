# npm 安全检查执行规范

> 每次执行 npm 安全检查时，必须读取此规范并按流程执行。

## 检查命令

```bash
cd frontend

# 1. 漏洞检查（必须使用官方 registry）
pnpm audit --registry https://registry.npmjs.org/ --json 2>&1

# 2. 过时依赖检查
pnpm outdated 2>&1

# 3. 许可证检查
pnpm licenses list 2>&1
```

---

## 重要说明：registry 问题

### 为什么必须指定官方 registry？

项目可能配置了阿里云或其他私有 npm registry，这些 registry：
- 可能不支持 `/-/npm/v1/security/advisories` 接口
- 可能返回非标准 JSON 格式
- 导致 `pnpm audit` 执行失败（如 "Unexpected end of JSON input"）

### 解决方案

**始终使用官方 registry 执行漏洞检查**：

```bash
# 正确方式：指定官方 registry
pnpm audit --registry https://registry.npmjs.org/ --json 2>&1

# 错误方式：使用默认 registry（可能失败）
pnpm audit --json 2>&1
```

---

## 漏洞等级映射

| npm audit 级别 | 报告等级 | 处理要求 |
|---------------|---------|---------|
| critical | 🔴 严重 | 必须立即修复 |
| high | 🔴 严重 | 必须在合并前修复 |
| moderate | 🟡 中等 | 建议在本次迭代修复 |
| low | 🟢 轻微 | 可后续优化 |

---

## 许可证风险等级

| 许可证 | 风险等级 | 说明 |
|--------|---------|------|
| GPL-2.0、GPL-3.0 | 🔴 严重 | 传染性许可证，商业项目慎用 |
| AGPL-3.0 | 🔴 严重 | 网络传染性，SaaS 项目需开源 |
| LGPL | 🟡 中等 | 动态链接可商用 |
| MPL-2.0 | 🟡 中等 | 文件级传染 |
| MIT、Apache-2.0、BSD、ISC | ✅ 安全 | 宽松许可证，可商用 |

---

## 输出格式

### 漏洞统计表格

```markdown
| 等级 | 数量 |
|------|------|
| 严重 | X |
| 高危 | X |
| 中危 | X |
| 低危 | X |
```

### 漏洞详情表格

```markdown
| 包名 | 当前版本 | 风险等级 | 漏洞描述 | 建议版本 | 修复命令 |
|------|---------|---------|---------|---------|---------|
| {name} | {version} | {level} | {desc} | {safe} | `pnpm update {name}@{safe}` |
```

### 过时依赖表格

```markdown
| 包名 | 当前版本 | 最新版本 | 差距等级 | 升级建议 |
|------|---------|---------|---------|---------|
| {name} | {current} | {latest} | {level} | {suggestion} |
```

### 许可证风险表格

```markdown
| 包名 | 许可证 | 风险等级 | 说明 |
|------|--------|---------|------|
| {name} | {license} | {level} | {note} |
```

---

## 检查流程

1. **执行漏洞检查**：使用官方 registry 执行 `pnpm audit`
2. **执行过时依赖检查**：执行 `pnpm outdated`
3. **执行许可证检查**：执行 `pnpm licenses list`，检查是否存在高风险许可证
4. **解析结果**：将输出转换为结构化数据
5. **等级映射**：按漏洞等级映射表分类
6. **生成报告**：按输出格式生成表格

---

## 常见问题处理

### 非零退出码

`pnpm audit` 与 `pnpm outdated` 在「有发现」时退出码非 0，属正常结果而非命令失败：

- `pnpm audit`：存在漏洞（critical/high）时退出码非 0
- `pnpm outdated`：存在过时依赖时退出码为 1

此时直接解析输出内容生成报告；仅当输出为空或无法解析出有效数据时，才视为执行失败。

### pnpm audit 仍失败

如果指定官方 registry 后仍失败：
1. 检查网络连接
2. 尝试使用 `npm audit` 代替
3. 报告中标注：「漏洞检查执行失败，建议手动检查」

### JSON 解析错误

错误信息如 "Unexpected end of JSON input"：
- 原因：registry 返回空响应或非标准格式
- 解决：确认使用了 `--registry https://registry.npmjs.org/` 参数

### 无漏洞

- 报告中标注：「未发现已知安全漏洞」

### 开发依赖漏洞

- 通常不影响生产环境
- 仍需记录到报告中
- 可降低处理优先级

### 间接依赖漏洞

当漏洞存在于间接依赖（如 `vite > esbuild`）：
- 查找依赖路径
- 说明需要通过父依赖升级间接修复
- 在报告中标注依赖路径