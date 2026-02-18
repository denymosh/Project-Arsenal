"""
研报分析系统 - 分析结果保存脚本

用法: uv run python save_analysis.py TSLA --input=tmp_analysis.json

功能:
  1. 读取Antigravity输出的分析JSON
  2. 生成分析MD报告
  3. 更新标的JSON数据（追加研报 + 重算共识 + 更新交叉对比）
  4. 更新催化剂日历
  5. 更新记分板（新机构注册）
  6. 重新生成标的汇总MD
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Windows环境下强制使用UTF-8编码输出
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# 将analyzer目录加入路径
sys.path.insert(0, str(Path(__file__).parent))

from lib.models import AnalysisInput
from lib.data_manager import (
    add_report_to_ticker,
    ensure_institution_in_scorecard,
    add_catalysts_from_report,
    PROJECT_ROOT
)
from lib.consensus import update_consensus, update_consensus_matrix
from lib.cross_validator import find_divergences
from lib.report_generator import generate_analysis_md, generate_summary_md


def save_analysis(ticker: str, input_path: str) -> None:
    """执行完整的分析保存流程"""

    print(f"\n{'='*60}")
    print(f"  💾 保存 {ticker} 研报分析结果")
    print(f"{'='*60}\n")

    # 1. 读取分析JSON
    filepath = Path(input_path)
    if not filepath.is_absolute():
        filepath = PROJECT_ROOT / filepath

    if not filepath.exists():
        print(f"❌ 输入文件不存在: {filepath}")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    # 2. 验证数据格式
    try:
        analysis = AnalysisInput.model_validate(raw_data)
    except Exception as e:
        print(f"❌ 数据格式验证失败: {e}")
        sys.exit(1)

    print(f"  📄 研报: {analysis.report.institution} ({analysis.report.date})")
    print(f"     评级: {analysis.report.rating} | 目标价: ${analysis.report.target_price}")

    # 3. 添加研报到标的数据
    print(f"\n  [1/6] 添加研报记录...")
    stored_report = add_report_to_ticker(ticker, analysis)

    # 4. 确保机构在记分板中
    print(f"  [2/6] 更新记分板...")
    ensure_institution_in_scorecard(
        analysis.report.institution,
        analysis.report.institution_en
    )

    # 5. 重新计算共识
    print(f"  [3/6] 重新计算共识...")
    update_consensus(ticker)
    update_consensus_matrix(ticker)

    # 6. 交叉验证
    print(f"  [4/6] 执行交叉验证...")
    find_divergences(ticker)

    # 7. 更新催化剂日历
    if analysis.report.catalysts:
        print(f"  [5/6] 更新催化剂日历...")
        catalysts_data = [cat.model_dump() for cat in analysis.report.catalysts]
        add_catalysts_from_report(
            ticker, stored_report.id,
            analysis.report.institution,
            catalysts_data
        )
    else:
        print(f"  [5/6] 无新催化剂事件")

    # 8. 生成分析MD报告
    print(f"  [6/6] 生成报告文件...")
    generate_analysis_md(ticker, stored_report)
    generate_summary_md(ticker)

    print(f"\n{'='*60}")
    print(f"  ✅ 保存完成!")
    print(f"     分析文件: {stored_report.analysis_file}")
    print(f"     数据文件: data/{ticker}.json")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="保存研报分析结果")
    parser.add_argument("ticker", type=str, help="标的代码，如 TSLA")
    parser.add_argument("--input", "-i", type=str, required=True, help="分析JSON文件路径")
    args = parser.parse_args()

    save_analysis(args.ticker.upper(), args.input)


if __name__ == "__main__":
    main()
