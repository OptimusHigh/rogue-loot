#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Деплой датапака rogue-loot в мир сервера ganj4craft-vanilla и ganj4core.
"""

import shutil
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DATAPACK = os.path.join(REPO_ROOT, "datapacks", "roguelike_loot")

TARGET_WORLD_DATAPACK = r"d:\GanjaCraft\ganj4craft-vanilla\world\datapacks\roguelike_loot"
TARGET_CORE_DATA = r"d:\GanjaCraft\ganj4core\src\main\resources\data\roguelike"

def deploy():
    print(f"Deploying from: {SRC_DATAPACK}")
    
    # 1. World datapack deploy
    if os.path.exists(TARGET_WORLD_DATAPACK):
        shutil.rmtree(TARGET_WORLD_DATAPACK)
    shutil.copytree(SRC_DATAPACK, TARGET_WORLD_DATAPACK)
    print(f"  -> World Datapack: OK ({TARGET_WORLD_DATAPACK})")
    
    # 2. Ganja4Core resources deploy
    core_loot_src = os.path.join(SRC_DATAPACK, "data", "roguelike")
    if os.path.exists(TARGET_CORE_DATA):
        shutil.rmtree(TARGET_CORE_DATA)
    shutil.copytree(core_loot_src, TARGET_CORE_DATA)
    print(f"  -> Ganja4Core Resources: OK ({TARGET_CORE_DATA})")

    print("\nDeployment completed successfully!")

if __name__ == "__main__":
    deploy()
