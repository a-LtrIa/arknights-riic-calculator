#!/usr/bin/env python3
"""
从 ArknightsGameData 获取所有干员，按星级分类。
数据来源: https://github.com/Kengxxiao/ArknightsGameData
"""
import requests
import json
import os

# 配置
CHAR_TABLE_URL = "https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/excel/character_table.json"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

RARITY_MAP = {
    "TIER_1": "1星",
    "TIER_2": "2星",
    "TIER_3": "3星",
    "TIER_4": "4星",
    "TIER_5": "5星",
    "TIER_6": "6星",
}

PROFESSION_MAP = {
    "PIONEER": "先锋",
    "WARRIOR": "近卫",
    "TANK": "重装",
    "SNIPER": "狙击",
    "CASTER": "术师",
    "MEDIC": "医疗",
    "SUPPORT": "辅助",
    "SPECIAL": "特种",
}


def fetch_operators():
    headers = {"User-Agent": "Mozilla/5.0"}

    print(f"正在获取干员数据: {CHAR_TABLE_URL}")
    resp = requests.get(CHAR_TABLE_URL, headers=headers, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # 按星级分类，排除无 potentialItemId 的非干员角色
    operators_by_rarity = {tier: [] for tier in RARITY_MAP}

    for char_id, char in data.items():
        if char.get("potentialItemId") is None:
            continue
        rarity = char["rarity"]
        if rarity in operators_by_rarity:
            operators_by_rarity[rarity].append(
                {
                    "name": char["name"],
                    "rarity": rarity,
                    "rarity_label": RARITY_MAP.get(rarity, rarity),
                    "profession": char["profession"],
                    "profession_label": PROFESSION_MAP.get(
                        char["profession"], char["profession"]
                    ),
                    "subProfessionId": char.get("subProfessionId"),
                    "nationId": char.get("nationId"),
                    "isNotObtainable": char.get("isNotObtainable", False),
                    "displayNumber": char.get("displayNumber"),
                }
            )

    # 每个星级按名称排序
    for tier in operators_by_rarity:
        operators_by_rarity[tier].sort(key=lambda x: x["name"])

    return operators_by_rarity


def main():
    operators = fetch_operators()

    total = 0
    for tier in ["TIER_1", "TIER_2", "TIER_3", "TIER_4", "TIER_5", "TIER_6"]:
        count = len(operators[tier])
        total += count
        label = RARITY_MAP[tier]
        print(f"\n{'='*50}")
        print(f"  {label} ({count}人)")
        print(f"{'='*50}")
        for op in operators[tier]:
            flag = " [不可获取]" if op["isNotObtainable"] else ""
            print(f"  {op['name']:<12} {op['profession_label']:<6}{flag}")

    print(f"\n总计: {total} 名干员")

    # 保存 JSON
    output_path = os.path.join(OUTPUT_DIR, "operators_by_rarity.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(operators, f, ensure_ascii=False, indent=2)
    print(f"\n数据已保存到: {output_path}")

    # 保存按星级分组的摘要
    summary = {}
    for tier, ops in operators.items():
        summary[RARITY_MAP[tier]] = {
            "count": len(ops),
            "operators": [op["name"] for op in ops],
        }
    summary_path = os.path.join(OUTPUT_DIR, "operators_by_rarity_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"摘要已保存到: {summary_path}")


if __name__ == "__main__":
    main()