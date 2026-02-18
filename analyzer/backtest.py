"""
研报分析系统 - 回溯验证脚本

用法: uv run python backtest.py TSLA --metric="Q1交付量" --actual="423000" --accurate

功能:
  1. 查找标的所有研报中匹配指标的预测
  2. 标记预测的验证结果
  3. 更新机构准确率和记分板
  4. 更新催化剂日历验证状态
"""

import sys
import os
import argparse
from pathlib import Path

# Windows环境下强制使用UTF-8编码输出
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 将analyzer目录加入路径
sys.path.insert(0, str(Path(__file__).parent))

from lib.backtest_engine import verify_prediction, get_unverified_predictions


def run_backtest(ticker: str, metric: str, actual: str, accurate: bool, deviation: float = None) -> None:
    """执行回溯验证"""

    print(f"\n{'='*60}")
    print(f"  🎯 回溯验证: {ticker}")
    print(f"     指标: {metric}")
    print(f"     实际值: {actual}")
    print(f"     判定: {'✅ 准确' if accurate else '❌ 不准确'}")
    if deviation is not None:
        print(f"     偏差: {deviation:.1f}%")
    print(f"{'='*60}\n")

    result = verify_prediction(
        ticker=ticker,
        metric=metric,
        actual_value=actual,
        accurate=accurate,
        deviation_pct=deviation
    )

    print(f"\n📊 验证结果:")
    print(f"   匹配预测数: {result['verified_count']}")
    for detail in result["details"]:
        status = "✅" if detail["accurate"] else "❌"
        print(f"   {status} {detail['institution']}: 预测{detail['predicted']} → 实际{detail['actual']}")

    print(f"\n{'='*60}")
    print(f"  ✅ 回溯验证完成")
    print(f"{'='*60}\n")


def show_unverified(ticker: str) -> None:
    """显示标的所有待验证的预测"""
    print(f"\n⏳ {ticker} 待验证的预测:")
    unverified = get_unverified_predictions(ticker)
    if not unverified:
        print("   无待验证预测")
        return

    for uv in unverified:
        print(f"   [{uv['date']}] {uv['institution']}: {uv['metric']} = {uv['predicted_value']} (截止{uv['deadline']})")


def main():
    parser = argparse.ArgumentParser(description="回溯验证研报预测")
    parser.add_argument("ticker", type=str, help="标的代码，如 TSLA")
    parser.add_argument("--metric", "-m", type=str, help="预测指标名")
    parser.add_argument("--actual", "-a", type=str, help="实际值")
    parser.add_argument("--accurate", action="store_true", help="预测是否准确")
    parser.add_argument("--inaccurate", action="store_true", help="预测不准确")
    parser.add_argument("--deviation", "-d", type=float, default=None, help="偏差百分比")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有待验证预测")

    args = parser.parse_args()
    ticker = args.ticker.upper()

    if args.list:
        show_unverified(ticker)
        return

    if not args.metric or not args.actual:
        print("❌ 需要指定 --metric 和 --actual 参数")
        print("   示例: uv run python backtest.py TSLA --metric='Q1交付量' --actual='423000' --accurate")
        print("   列出待验证: uv run python backtest.py TSLA --list")
        sys.exit(1)

    accurate = args.accurate or (not args.inaccurate)
    if args.inaccurate:
        accurate = False

    run_backtest(ticker, args.metric, args.actual, accurate, args.deviation)


if __name__ == "__main__":
    main()
