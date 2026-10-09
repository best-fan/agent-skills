#!/usr/bin/env python3
"""
前端项目打包脚本
- 从 package.json 的 scripts 中读取构建命令
- 根据锁文件自动判断包管理器（pnpm/npm/yarn）
- 展示检测信息，确认后执行（--yes 跳过确认，--dry-run 仅查看）
- 将 dist 目录打包为 zip 格式
- 输出 git 分支、耗时等信息
"""

import argparse
import json
import os
import subprocess
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path

# 构建脚本候选名，按优先级排列
BUILD_SCRIPT_CANDIDATES = ["build", "build:prod", "build:production", "dist"]

# 锁文件与包管理器的对应关系
LOCK_FILE_MAP = {
    "pnpm-lock.yaml": "pnpm",
    "package-lock.json": "npm",
    "yarn.lock": "yarn",
}


def setup_stdout_utf8():
    """Windows 管道环境下强制 UTF-8 输出，避免中文乱码"""
    for stream in (sys.stdout, sys.stderr):
        if stream and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def detect_project_path() -> str:
    """自动检测项目路径：优先 frontend 子目录，否则当前目录"""
    frontend_path = os.path.join(os.getcwd(), "frontend")
    if os.path.exists(frontend_path):
        return frontend_path
    return os.getcwd()


def detect_package_manager(project_path: str) -> tuple[str, str]:
    """根据锁文件判断包管理器，返回 (包管理器, 依据的锁文件名)"""
    for lock_file, pm in LOCK_FILE_MAP.items():
        if (Path(project_path) / lock_file).exists():
            return pm, lock_file
    return "npm", ""


def read_build_script(project_path: str) -> tuple[str, str]:
    """
    从 package.json 读取构建脚本
    返回 (脚本名, 脚本内容)；找不到时抛出 RuntimeError
    """
    pkg_path = Path(project_path) / "package.json"
    if not pkg_path.exists():
        raise RuntimeError(f"未找到 package.json: {pkg_path}")

    try:
        with open(pkg_path, "r", encoding="utf-8") as f:
            pkg = json.load(f)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"package.json 解析失败: {e}")

    scripts = pkg.get("scripts") or {}
    for name in BUILD_SCRIPT_CANDIDATES:
        if scripts.get(name):
            return name, scripts[name]

    available = ", ".join(scripts.keys()) or "（无）"
    raise RuntimeError(
        f"package.json 中未找到构建脚本（已尝试: {', '.join(BUILD_SCRIPT_CANDIDATES)}），"
        f"可用 scripts: {available}"
    )


def get_git_branch(project_path: str) -> str:
    """获取当前 git 分支"""
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=project_path
    )
    if result.returncode == 0:
        return result.stdout.strip() or "unknown"
    return "unknown"


def get_git_commit_info(project_path: str) -> str:
    """获取当前 commit 的第一行信息"""
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=format:%s"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=project_path
    )
    if result.returncode == 0:
        return result.stdout.strip() or "unknown"
    return "unknown"


def print_build_info(info: dict):
    """打印检测到的构建信息"""
    lock_note = info["lock_file"] if info["lock_file"] else "未找到锁文件，默认使用 npm"
    print("=" * 50)
    print("构建信息")
    print("=" * 50)
    print(f"项目路径: {info['project_path']}")
    print(f"包管理器: {info['package_manager']}（依据: {lock_note}）")
    print(f"构建脚本: {info['script_name']}")
    print(f"脚本内容: {info['script_command']}")
    print(f"执行命令: {info['full_command']}")
    print(f"输出目录: {info['output_dir']}")
    print("=" * 50)


def confirm_execution(info: dict, auto_yes: bool) -> bool:
    """打印构建信息并请求用户确认"""
    print_build_info(info)

    if auto_yes:
        print("已通过 --yes 跳过脚本内确认\n")
        return True

    # 非交互环境（如被其他程序调用）无法交互确认
    if not sys.stdin.isatty():
        print("非交互环境无法确认。请核对以上信息后，追加 --yes 参数执行。")
        return False

    try:
        answer = input("确认执行以上构建命令? [y/N]: ")
    except (EOFError, KeyboardInterrupt):
        print()
        return False
    return answer.strip().lower() in ("y", "yes")


def run_build(project_path: str, command: str) -> tuple[bool, float]:
    """运行构建命令，返回 (是否成功, 耗时秒数)"""
    print(f"正在执行构建: {command}")

    start_time = time.time()

    # 使用 subprocess 的 cwd 参数，不改变当前工作目录
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=project_path
    )

    elapsed_time = time.time() - start_time

    if result.returncode != 0:
        # 构建工具（vite/vue-tsc 等）的错误常输出在 stdout，一并展示
        print(f"构建失败:\n{result.stdout}\n{result.stderr}")
        return False, elapsed_time

    print(f"构建成功 (耗时 {elapsed_time:.1f}s)")
    return True, elapsed_time


def create_zip(project_path: str, output_dir: str = None) -> tuple[str, int, float]:
    """将 dist 目录打包为 zip，返回 (zip路径, 文件数量, 耗时秒数)"""
    dist_path = Path(project_path) / "dist"

    if not dist_path.exists():
        print(f"dist 目录不存在: {dist_path}")
        return None, 0, 0

    # 生成 zip 文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_name = Path(project_path).name
    zip_name = f"{project_name}_dist_{timestamp}.zip"

    # 输出目录
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = Path(project_path)

    output_path.mkdir(parents=True, exist_ok=True)
    zip_path = output_path / zip_name

    print(f"正在打包: {zip_path}")

    start_time = time.time()
    file_count = 0

    # 创建 zip 文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in dist_path.rglob('*'):
            if file_path.is_file():
                # 保持相对路径结构
                arc_name = file_path.relative_to(dist_path)
                zf.write(file_path, arc_name)
                file_count += 1

    elapsed_time = time.time() - start_time

    print(f"打包完成: {zip_path} (耗时 {elapsed_time:.1f}s)")

    return str(zip_path), file_count, elapsed_time


def format_time(seconds: float) -> str:
    """格式化时间为 HH:MM:SS 或 MM:SS"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs:.1f}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m {secs:.1f}s"


def main():
    """主函数"""
    setup_stdout_utf8()

    parser = argparse.ArgumentParser(
        description="前端项目构建打包工具：读取 package.json 构建命令，确认后执行并打包 dist 为 zip"
    )
    parser.add_argument("project_path", nargs="?", help="项目路径，默认自动检测 frontend 目录")
    parser.add_argument("output_dir", nargs="?", help="zip 输出目录，默认输出到项目目录")
    parser.add_argument("-y", "--yes", action="store_true",
                        help="跳过确认直接执行（仅在已获得用户确认后使用）")
    parser.add_argument("--dry-run", action="store_true",
                        help="仅显示检测到的构建信息，不执行构建")
    args = parser.parse_args()

    total_start_time = time.time()

    # 解析项目路径与输出目录
    project_path = os.path.abspath(args.project_path or detect_project_path())
    output_dir = os.path.abspath(args.output_dir) if args.output_dir else None

    # 从 package.json 检测构建命令与包管理器
    try:
        package_manager, lock_file = detect_package_manager(project_path)
        script_name, script_command = read_build_script(project_path)
    except RuntimeError as e:
        print(f"错误: {e}")
        sys.exit(1)

    full_command = f"{package_manager} run {script_name}"

    info = {
        "project_path": project_path,
        "package_manager": package_manager,
        "lock_file": lock_file,
        "script_name": script_name,
        "script_command": script_command,
        "full_command": full_command,
        "output_dir": output_dir or project_path,
    }

    if args.dry_run:
        print_build_info(info)
        print("\n[dry-run] 以上为检测到的构建信息，未执行任何命令")
        sys.exit(0)

    # 确认后执行
    if not confirm_execution(info, args.yes):
        print("已取消，未执行构建")
        sys.exit(1)

    # 获取 git 信息
    git_branch = get_git_branch(project_path)
    git_commit = get_git_commit_info(project_path)

    # 1. 运行构建
    build_success, build_time = run_build(project_path, full_command)
    if not build_success:
        sys.exit(1)

    # 2. 打包 dist
    zip_path, file_count, pack_time = create_zip(project_path, output_dir)

    total_time = time.time() - total_start_time

    if zip_path:
        # 获取 zip 文件大小
        zip_size = Path(zip_path).stat().st_size
        size_mb = zip_size / (1024 * 1024)

        # 输出汇总信息
        print("\n" + "=" * 50)
        print("打包完成")
        print("=" * 50)
        print(f"项目路径: {project_path}")
        print(f"执行命令: {full_command}")
        print(f"Git 分支: {git_branch}")
        print(f"Git Commit: {git_commit}")
        print(f"构建耗时: {format_time(build_time)}")
        print(f"打包耗时: {format_time(pack_time)}")
        print(f"总耗时:   {format_time(total_time)}")
        print(f"文件数量: {file_count}")
        print(f"文件大小: {size_mb:.2f} MB")
        print(f"输出文件: {zip_path}")
        print("=" * 50)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
