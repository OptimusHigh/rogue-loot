#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Валидатор таблиц лута Roguelike Dungeons (JSON, типы, веса, синтаксис 26.3)
"""

import json
import os
import glob
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES_DIR = os.path.join(REPO_ROOT, "datapacks", "roguelike_loot", "data", "roguelike", "loot_table", "chests")

EXPECTED_TABLES = [
    "armor1.json", "armor2.json", "block1.json", "block2.json",
    "brewing.json", "food1.json", "food2.json", "music.json",
    "ore1.json", "ore2.json", "starter.json", "supply1.json",
    "supply2.json", "tool1.json", "tool2.json", "weapon1.json", "weapon2.json"
]

def validate():
    print(f"Validating tables in: {TABLES_DIR}")
    errors = 0
    checked = 0

    files = glob.glob(os.path.join(TABLES_DIR, "*.json"))
    found_names = set(os.path.basename(f) for f in files)

    # Check for missing expected tables
    for exp in EXPECTED_TABLES:
        if exp not in found_names:
            print(f"  [ERROR] Missing expected table: {exp}")
            errors += 1

    for fpath in files:
        fname = os.path.basename(fpath)
        checked += 1
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if data.get("type") != "minecraft:chest":
                print(f"  [WARN] {fname}: type is not 'minecraft:chest' (got {data.get('type')})")

            pools = data.get("pools", [])
            if not pools:
                print(f"  [ERROR] {fname}: has 0 pools!")
                errors += 1
                continue

            for p_idx, pool in enumerate(pools):
                rolls = pool.get("rolls")
                if not rolls:
                    print(f"  [ERROR] {fname} (pool {p_idx}): missing rolls")
                    errors += 1
                entries = pool.get("entries", [])
                if not entries:
                    print(f"  [ERROR] {fname} (pool {p_idx}): empty entries")
                    errors += 1
                total_weight = 0
                for e in entries:
                    w = e.get("weight", 1)
                    total_weight += w
                    item_type = e.get("type")
                    if item_type == "minecraft:item":
                        name = e.get("name")
                        if not name or ":" not in name:
                            print(f"  [ERROR] {fname}: invalid item name '{name}'")
                            errors += 1
                    elif item_type == "minecraft:loot_table":
                        pass
                # Print summary
                print(f"  [OK] {fname:14} | Pools: {len(pools)} | Entries: {len(entries):2} | Total Weight: {total_weight:3}")

        except Exception as e:
            print(f"  [ERROR] {fname}: Failed to parse JSON: {e}")
            errors += 1

    print("-" * 50)
    if errors == 0:
        print(f"ALL {checked} TABLES VALIDATED SUCCESSFULLY! NO ERRORS.")
        return 0
    else:
        print(f"VALIDATION FINISHED WITH {errors} ERROR(S).")
        return 1

if __name__ == "__main__":
    sys.exit(validate())
