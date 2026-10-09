# Build Frontend Zip 技能文档

## 使用时机

在以下情况使用此技能：

- 前端项目需要打包构建并生成可分发的 zip 文件
- 需要将构建产物（dist 目录）压缩打包用于部署或分发
- 快速生成带有时间戳的构建产物包

---

## 核心功能

- 自动检测项目路径（支持 frontend 目录自动识别）
- 动态读取 `package.json` 的构建命令
- 自动识别包管理器（pnpm/npm/yarn）
- 将 dist 目录打包为 zip 格式
- 输出构建汇总信息（分支、耗时、文件数量等）

---

## 执行步骤

1. **检测项目路径** - 自动识别 frontend 目录或使用指定路径
2. **读取构建命令** - 从 `package.json` 的 `scripts.build` 获取构建方式
3. **运行构建** - 根据项目锁文件判断包管理器并执行构建
4. **打包 dist** - 将构建产物压缩为 zip 格式
5. **输出汇总** - 显示 git 分支、耗时、文件数量、文件大小等信息

---

## 构建命令检测

构建命令动态从 `package.json` 中读取：

| 锁文件 | 包管理器 | 构建命令 |
|--------|----------|----------|
| `pnpm-lock.yaml` | pnpm | `pnpm build` |
| `package-lock.json` | npm | `npm run build` |
| `yarn.lock` | yarn | `yarn build` |

---

## 执行脚本

```bash
python scripts/build_zip.py [项目路径] [输出目录]
```

**参数说明：**

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 项目路径 | 前端项目目录 | 自动检测 frontend 目录 |
| 输出目录 | zip 文件输出位置 | 项目目录 |

**使用示例：**

```bash
# 自动检测 frontend 目录
python scripts/build_zip.py

# 指定项目路径
python scripts/build_zip.py frontend

# 指定项目和输出目录
python scripts/build_zip.py . ./releases
```

---

## 输出文件命名

zip 文件命名格式：`{项目名}_dist_{时间戳}.zip`

示例：`frontend_dist_20260413_153000.zip`

---

## 输出汇总信息

构建完成后输出以下信息：

| 信息项 | 说明 |
|--------|------|
| 项目路径 | 构建项目的绝对路径 |
| Git 分支 | 当前 git 分支名称 |
| Git Commit | 最新 commit 的第一行信息 |
| 构建耗时 | 构建命令执行时间 |
| 打包耗时 | zip 打包时间 |
| 总耗时 | 整个流程总时间 |
| 文件数量 | zip 中包含的文件数 |
| 文件大小 | zip 文件大小（MB） |
| 输出文件 | zip 文件的完整路径 |

---

## 注意事项

| 注意点 | 说明 |
|--------|------|
| 依赖安装 | 项目依赖需预先安装 |
| 构建失败 | 构建失败时不生成 zip 文件 |
| 目录结构 | zip 文件保持 dist 目录结构 |
| 项目名 | 从 `package.json` 的 `name` 字段读取 |

---

## 前置条件

- Python 3.x 环境
- 项目已安装依赖（已执行 `pnpm install` / `npm install` / `yarn`）
- 项目有有效的 `scripts.build` 配置

---

## 技能文件结构

```
skills/build-frontend-zip/
├── SKILL.md              # 技能入口定义
└── scripts/
    └── build_zip.py      # 构建打包脚本
```

---

## 版本信息

- 当前版本：1.1.0
- 更新日期：2026-10-09