"""
研报分析系统 - 自动Git推送脚本

用法: uv run python auto_push.py "更新TSLA高盛研报分析"

功能: 自动执行 git add, commit, push
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def auto_push(message: str = "更新研报分析数据") -> None:
    """自动执行git add, commit, push"""

    print(f"\n🚀 自动推送到GitHub...")
    print(f"   提交信息: {message}\n")

    try:
        # git add
        result = subprocess.run(
            ["git", "add", "."],
            cwd=str(PROJECT_ROOT),
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"❌ git add 失败: {result.stderr}")
            return

        # 检查是否有变更
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(PROJECT_ROOT),
            capture_output=True, text=True
        )
        if not result.stdout.strip():
            print("ℹ️ 没有需要提交的变更")
            return

        print(f"   变更文件:")
        for line in result.stdout.strip().split("\n"):
            print(f"     {line}")

        # git commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(PROJECT_ROOT),
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"❌ git commit 失败: {result.stderr}")
            return
        print(f"\n   ✅ 已提交")

        # git push
        result = subprocess.run(
            ["git", "push"],
            cwd=str(PROJECT_ROOT),
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"⚠️ git push 失败（可能尚未配置远程仓库）: {result.stderr}")
            return
        print(f"   ✅ 已推送到远程仓库")

        print(f"\n🎉 推送完成! Vercel将自动重新构建。")

    except FileNotFoundError:
        print("❌ git未安装或不在PATH中")
    except Exception as e:
        print(f"❌ 推送失败: {e}")


if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "更新研报分析数据"
    auto_push(msg)
