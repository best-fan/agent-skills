---
name: build-frontend-zip
description: 前端项目打包技能（v1.1.0）。此技能用于前端项目打包。从 package.json 中读取构建命令，经用户确认后执行构建，然后将 dist 目录打包为 zip 格式。当用户请求打包、构建并压缩、或需要分发构建产物时触发。
metadata:
  version: 1.1.0
  updatedAt: 2026-10-09
---

# 前端项目打包

从目标项目的 `package.json` 中读取构建命令，经用户确认后执行构建，并将 `dist` 目录打包为 zip 格式，便于分发。

## 执行流程

### 第一步：检测构建信息（只读，不执行构建）

确定项目路径（优先级：用户指定路径 > `frontend/` 子目录 > 当前目录），然后获取以下信息：

1. 读取 `package.json` 的 `scripts` 字段，按优先级取第一个存在的构建脚本：
   `build` > `build:prod` > `build:production` > `dist`
2. 根据锁文件判断包管理器：
   - `pnpm-lock.yaml` → pnpm
   - `package-lock.json` → npm
   - `yarn.lock` → yarn
   - 无锁文件 → 默认 npm

可手动读取 `package.json`，或运行脚本（位于本技能目录 `scripts/build_zip.py`）完成检测：

```bash
python scripts/build_zip.py [项目路径] --dry-run
```

### 第二步：向用户确认（必须，不可跳过）

将检测结果显示给用户并请求确认，至少包含：

- 项目路径
- 包管理器及判断依据（锁文件名）
- 构建脚本名及 `package.json` 中的原始命令内容
- 最终将执行的完整命令（如 `pnpm run build`）

使用 AskUserQuestion 工具或直接提问进行确认。用户明确同意后方可继续；用户拒绝或未获回应时终止流程。用户要求更换构建脚本（如改用 `build:prod`）时，按用户指定调整并再次确认。

### 第三步：确认后执行打包

用户确认后，追加 `--yes` 参数执行（`--yes` 表示用户已在对话中确认）：

```bash
python scripts/build_zip.py [项目路径] [输出目录] --yes
```

## 脚本参数

| 参数 | 说明 |
|------|------|
| 项目路径 | 可选，默认自动检测 frontend 目录 |
| 输出目录 | 可选，默认输出到项目目录 |
| `--dry-run` | 仅显示检测到的构建信息，不执行 |
| `-y, --yes` | 跳过脚本内交互确认（仅在用户已确认后使用） |

示例：
```bash
python scripts/build_zip.py frontend
python scripts/build_zip.py . ./releases --yes
python scripts/build_zip.py frontend --dry-run
```

## 输出文件命名

zip 文件命名格式：`{项目名}_dist_{时间戳}.zip`

示例：`frontend_dist_20260413_153000.zip`

## 注意事项

- 项目依赖需预先安装，缺失时先提示用户安装
- 构建命令必须来自 `package.json`，禁止臆造构建命令
- 构建失败时不生成 zip 文件，如实报告失败输出
- zip 文件保持 dist 目录结构
- 非交互环境下脚本不会自动确认，必须经对话确认后加 `--yes` 执行
