# -*- coding: utf-8 -*-
"""
run_all.py —— 全流程一键脚本
清洗 → 质量评分 → 分析 → 输出报告
运行：python run_all.py
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from src import clean_data, data_quality, analysis  # noqa: E402


def main():
    print("=" * 50)
    print("煤矿数据质量平台 · 全流程执行")
    print("=" * 50)

    print("\n[1/3] 数据清洗")
    df, report = clean_data.clean()

    print("\n[2/3] 数据质量评分")
    dq = data_quality.dq_score(df)
    for k, v in dq.items():
        print(f"  {k}: {v}")

    print("\n[3/3] 产量分析")
    analysis.by_mine(df)
    print()
    print("全流程完成。结果文件：data/coal_cleaned.csv, data/dq_report.csv")


if __name__ == "__main__":
    main()
