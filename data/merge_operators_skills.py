#!/usr/bin/env python3
"""
合并 operators_by_rarity.json 与 base_skills.json，生成 operators_with_skills.json。

逻辑：
  - 遍历 operators_by_rarity.json 中按星级(TIER_1~TIER_6)分组的干员
  - 以干员 name 为 key，从 base_skills.json 查找对应技能列表
  - 合并到干员对象的 "skills" 字段（找不到则为空数组 []）
  - 保持按星级分组的顶层结构不变
"""

import json
import os
from collections import OrderedDict

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

OPERATORS_PATH = os.path.join(SCRIPT_DIR, "operators_by_rarity.json")
SKILLS_PATH = os.path.join(SCRIPT_DIR, "base_skills.json")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "operators_with_skills.json")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    operators_data = load_json(OPERATORS_PATH)
    skills_data = load_json(SKILLS_PATH)

    # ----- 统计变量 -----
    total_operators = 0
    operators_with_skills = 0
    operators_without_skills = []  # (name, rarity)
    tier_stats = {}  # rarity_label -> {"total": int, "with_skills": int}

    # ----- 合并 -----
    result = OrderedDict()

    for tier, op_list in operators_data.items():
        merged_list = []
        tier_total = 0
        tier_with = 0
        rarity_label = ""

        for operator in op_list:
            name = operator.get("name", "")
            tier_total += 1
            total_operators += 1
            rarity_label = operator.get("rarity_label", tier)

            # 复制原始字段
            merged_obj = dict(operator)
            # 查找技能
            if name in skills_data:
                merged_obj["skills"] = skills_data[name]
                operators_with_skills += 1
                tier_with += 1
            else:
                merged_obj["skills"] = []
                operators_without_skills.append((name, rarity_label))

            merged_list.append(merged_obj)

        result[tier] = merged_list

        if rarity_label:
            if rarity_label not in tier_stats:
                tier_stats[rarity_label] = {"total": 0, "with_skills": 0}
            tier_stats[rarity_label]["total"] += tier_total
            tier_stats[rarity_label]["with_skills"] += tier_with

    # ----- 写入结果 -----
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # ----- 统计报告 -----
    print(f"=" * 60)
    print(f"合并完成！已生成: {OUTPUT_PATH}")
    print(f"=" * 60)
    print(f"  总干员数:         {total_operators}")
    print(f"  有技能数据的干员: {operators_with_skills}")
    print(f"  缺失技能数据的:   {len(operators_without_skills)}")
    print(f"")

    # 各星级覆盖率
    print(f"各星级技能覆盖率:")
    print(f"{'星级':<8} {'总数':>6} {'有技能':>8} {'覆盖率':>10}")
    print(f"-" * 35)
    for label in sorted(tier_stats.keys(), key=lambda x: int(x[0]) if x[0].isdigit() else 99):
        s = tier_stats[label]
        pct = (s["with_skills"] / s["total"] * 100) if s["total"] > 0 else 0
        print(f"{label:<8} {s['total']:>6} {s['with_skills']:>8} {pct:>9.1f}%")

    # 缺失技能干员列表
    if operators_without_skills:
        print(f"")
        print(f"缺失技能数据的干员列表 ({len(operators_without_skills)} 人):")
        for name, rarity in operators_without_skills:
            print(f"  - [{rarity}] {name}")

    print(f"=" * 60)


if __name__ == "__main__":
    main()