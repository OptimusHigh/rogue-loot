#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенный генератор 17 лут-таблиц для Roguelike Dungeons (Minecraft 26.3 / SlashLoot)
Особенности:
- Мультипуловая архитектура: каждый сундук щедро наполнен (8-16 слотов)
- Фонари, факела, цепи, стрелы, мешки (bundle) в каждом типе сундуков
- Богатый дроп со всех мобов (порох, кости, нитки, слизь, глаза, перья, стержни ифрита/бриза, смола)
- Гарантированно зачарованная броня и оружие с высокими чарами
- Полное соблюдение ограничений: НИКАКИХ шалкеров, незеритовых доспехов/инструментов, дерева и кожи
- Все 18 кузнечных шаблонов (Trims), Trial Chambers 26.3, Pale Garden 26.3, пластинки, реликвии
"""

import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(REPO_ROOT, "datapacks", "roguelike_loot", "data", "roguelike", "loot_table", "chests")

def make_pool(rolls_min, rolls_max, entries):
    return {
        "rolls": {
            "type": "minecraft:uniform",
            "min": float(rolls_min),
            "max": float(rolls_max)
        },
        "entries": entries
    }

def write_table(target_dir, filename, pools):
    table = {
        "type": "minecraft:chest",
        "pools": pools
    }
    path = os.path.join(target_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(table, f, indent=2, ensure_ascii=False)
    print(f"  [OK] {filename} ({len(pools)} pools)")

def item_count(name, weight, min_c, max_c):
    entry = {
        "type": "minecraft:item",
        "name": name,
        "weight": weight
    }
    if min_c == max_c == 1:
        entry["functions"] = [{
            "function": "minecraft:set_count",
            "count": 1.0,
            "add": False
        }]
    else:
        entry["functions"] = [{
            "function": "minecraft:set_count",
            "count": {
                "type": "minecraft:uniform",
                "min": float(min_c),
                "max": float(max_c)
            },
            "add": False
        }]
    return entry

def item_simple(name, weight):
    return {
        "type": "minecraft:item",
        "name": name,
        "weight": weight
    }

def item_enchant(name, weight, min_lvl, max_lvl):
    return {
        "type": "minecraft:item",
        "name": name,
        "weight": weight,
        "functions": [
            {
                "function": "minecraft:enchant_with_levels",
                "levels": {
                    "type": "minecraft:uniform",
                    "min": float(min_lvl),
                    "max": float(max_lvl)
                }
            }
        ]
    }

def item_enchant_random(weight, options):
    return {
        "type": "minecraft:item",
        "name": "minecraft:book",
        "weight": weight,
        "functions": [
            {
                "function": "minecraft:enchant_randomly",
                "options": options
            }
        ]
    }

def item_potion(name, weight, potion_id, min_c=1, max_c=1):
    funcs = [
        {
            "function": "minecraft:set_potion",
            "id": potion_id
        }
    ]
    if min_c == max_c == 1:
        pass
    else:
        funcs.append({
            "function": "minecraft:set_count",
            "count": {
                "type": "minecraft:uniform",
                "min": float(min_c),
                "max": float(max_c)
            },
            "add": False
        })
    return {
        "type": "minecraft:item",
        "name": name,
        "weight": weight,
        "functions": funcs
    }

def item_ominous_bottle(weight, min_amp=1, max_amp=5, min_c=1, max_c=3):
    funcs = []
    if min_c == max_c == 1:
        funcs.append({
            "function": "minecraft:set_count",
            "count": 1.0,
            "add": False
        })
    else:
        funcs.append({
            "function": "minecraft:set_count",
            "count": {
                "type": "minecraft:uniform",
                "min": float(min_c),
                "max": float(max_c)
            },
            "add": False
        })
    funcs.append({
        "function": "minecraft:set_ominous_bottle_amplifier",
        "amplifier": {
            "type": "minecraft:uniform",
            "min": float(min_amp),
            "max": float(max_amp)
        }
    })
    return {
        "type": "minecraft:item",
        "name": "minecraft:ominous_bottle",
        "weight": weight,
        "functions": funcs
    }

def item_goat_horn(weight):
    return {
        "type": "minecraft:item",
        "name": "minecraft:goat_horn",
        "weight": weight,
        "functions": [
            {
                "function": "minecraft:set_instrument",
                "options": "#minecraft:goat_horns"
            }
        ]
    }

def item_sealed_relic(item_name, relic_id, cit_id, model_data, name_text, lore_lines, enchants_dict):
    funcs = [
        {
            "function": "minecraft:set_components",
            "components": {
                "minecraft:custom_data": {
                    "bounty_relic": relic_id,
                    "relic_id": relic_id,
                    "cit_id": cit_id,
                    "relic_sealed": True,
                    "CustomModelData": model_data
                },
                "minecraft:repair_cost": 1000,
                "minecraft:custom_name": json.dumps({"text": name_text, "color": "dark_purple", "bold": True, "italic": False}),
                "minecraft:lore": [
                    json.dumps({"text": line, "italic": False}) for line in lore_lines
                ]
            }
        }
    ]
    if enchants_dict:
        funcs.append({
            "function": "minecraft:set_enchantments",
            "enchantments": enchants_dict
        })
    return {
        "type": "minecraft:item",
        "name": item_name,
        "weight": 1,
        "functions": funcs
    }

# =============================================================================
# ОБЩИЕ ПУЛЫ НАПОЛНЕНИЯ (Свет, Расходники, Дроп мобов, Металлы)
# =============================================================================

def pool_common_gear_t1(rolls_min=2, rolls_max=4):
    """Походный свет, расходники и снаряжение (Этажи 0-3)"""
    return make_pool(rolls_min, rolls_max, [
        item_count("minecraft:torch", 16, 16, 32),
        item_count("minecraft:lantern", 12, 2, 6),
        item_count("minecraft:copper_bulb", 8, 2, 6),
        item_count("minecraft:iron_chain", 10, 3, 8),
        item_count("minecraft:bread", 12, 4, 10),
        item_count("minecraft:baked_potato", 10, 4, 10),
        item_count("minecraft:arrow", 14, 16, 32),
        item_count("minecraft:spectral_arrow", 6, 4, 10),
        item_count("minecraft:snowball", 6, 8, 16),
        item_count("minecraft:egg", 6, 4, 12),
        item_count("minecraft:bundle", 8, 1, 1),
        item_count("minecraft:flint_and_steel", 6, 1, 1)
    ])

def pool_common_gear_t2(rolls_min=3, rolls_max=5):
    """Освещение глубин, редкие расходники и мобильность (Этажи 4-5)"""
    return make_pool(rolls_min, rolls_max, [
        item_count("minecraft:torch", 14, 20, 40),
        item_count("minecraft:lantern", 12, 3, 8),
        item_count("minecraft:soul_lantern", 12, 2, 6),
        item_count("minecraft:copper_bulb", 10, 2, 5),
        item_count("minecraft:iron_chain", 10, 6, 14),
        item_count("minecraft:golden_carrot", 10, 4, 10),
        item_count("minecraft:golden_apple", 4, 2, 5),
        item_count("minecraft:wind_charge", 10, 6, 16),
        item_count("minecraft:spectral_arrow", 12, 8, 18),
        item_count("minecraft:arrow", 12, 16, 32),
        item_count("minecraft:snowball", 6, 8, 16),
        item_count("minecraft:bundle", 8, 1, 1)
    ])

def pool_common_mob_drops_t1(rolls_min=2, rolls_max=4):
    """Богатый дроп с мобов всех мастей (Этажи 0-3)"""
    return make_pool(rolls_min, rolls_max, [
        item_count("minecraft:gunpowder", 14, 4, 14),
        item_count("minecraft:bone", 15, 6, 18),
        item_count("minecraft:string", 14, 6, 16),
        item_count("minecraft:spider_eye", 12, 3, 8),
        item_count("minecraft:slime_ball", 10, 2, 6),
        item_count("minecraft:feather", 12, 6, 16),
        item_count("minecraft:leather", 10, 3, 8),
        item_count("minecraft:rabbit_hide", 8, 3, 8),
        item_count("minecraft:rabbit_foot", 4, 2, 5),
        item_count("minecraft:glow_ink_sac", 8, 2, 6),
        item_count("minecraft:ink_sac", 8, 4, 10),
        item_count("minecraft:honeycomb", 6, 2, 6),
        item_count("minecraft:sugar", 8, 4, 12),
        item_count("minecraft:clay_ball", 8, 6, 16)
    ])

def pool_common_mob_drops_t2(rolls_min=3, rolls_max=5):
    """Дроп опасных мобов, алхимия и эндгейм-компоненты (Этажи 4-5)"""
    return make_pool(rolls_min, rolls_max, [
        item_count("minecraft:gunpowder", 14, 8, 20),
        item_count("minecraft:bone", 12, 8, 20),
        item_count("minecraft:string", 12, 8, 20),
        item_count("minecraft:slime_ball", 10, 4, 12),
        item_count("minecraft:breeze_rod", 8, 2, 5),
        item_count("minecraft:blaze_rod", 10, 3, 8),
        item_count("minecraft:blaze_powder", 12, 4, 10),
        item_count("minecraft:magma_cream", 10, 3, 8),
        item_count("minecraft:ghast_tear", 6, 2, 5),
        item_count("minecraft:resin_clump", 10, 3, 8),
        item_count("minecraft:phantom_membrane", 8, 2, 5),
        item_count("minecraft:glow_ink_sac", 8, 3, 8),
        item_count("minecraft:prismarine_shard", 8, 4, 10),
        item_count("minecraft:prismarine_crystals", 6, 3, 8),
        item_count("minecraft:glowstone_dust", 10, 6, 16),
        item_count("minecraft:echo_shard", 4, 2, 5)
    ])

def pool_common_minerals_t1(rolls_min=2, rolls_max=4):
    """Металлы, самородки и базовые минералы (Этажи 0-3, БЕЗ АЛМАЗОВ)"""
    return make_pool(rolls_min, rolls_max, [
        item_count("minecraft:iron_nugget", 14, 12, 28),
        item_count("minecraft:gold_nugget", 12, 8, 20),
        item_count("minecraft:copper_ingot", 14, 4, 12),
        item_count("minecraft:iron_ingot", 12, 2, 6),
        item_count("minecraft:gold_ingot", 8, 2, 6),
        item_count("minecraft:lapis_lazuli", 10, 6, 16),
        item_count("minecraft:redstone", 10, 6, 18),
        item_count("minecraft:coal", 14, 10, 24),
        item_count("minecraft:amethyst_shard", 8, 3, 8),
        item_count("minecraft:quartz", 8, 4, 10),
        item_count("minecraft:flint", 8, 4, 10)
    ])

def pool_common_minerals_t2(rolls_min=2, rolls_max=4):
    """Драгоценные металлы, алмазы и самоцветы глубин (Этажи 4-5)"""
    return make_pool(rolls_min, rolls_max, [
        item_count("minecraft:diamond", 6, 2, 5),
        item_count("minecraft:emerald", 10, 2, 6),
        item_count("minecraft:gold_ingot", 12, 4, 12),
        item_count("minecraft:iron_ingot", 12, 6, 14),
        item_count("minecraft:copper_ingot", 10, 8, 20),
        item_count("minecraft:gold_nugget", 14, 16, 36),
        item_count("minecraft:iron_nugget", 14, 16, 36),
        item_count("minecraft:lapis_lazuli", 12, 12, 28),
        item_count("minecraft:redstone", 12, 12, 28),
        item_count("minecraft:amethyst_shard", 8, 6, 14),
        item_count("minecraft:quartz", 8, 8, 18)
    ])


def generate_all(output_dir=None):
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating expanded multi-pool loot tables into: {output_dir}")

    # =========================================================================
    # 1. STARTER (Вход в данж, башня на поверхности, 0 этаж)
    # =========================================================================
    write_table(output_dir, "starter.json", [
        make_pool(2, 3, [
            item_enchant("minecraft:iron_sword", 10, 10, 18),
            item_enchant("minecraft:stone_sword", 8, 8, 14),
            item_enchant("minecraft:chainmail_helmet", 8, 10, 18),
            item_enchant("minecraft:chainmail_chestplate", 6, 10, 18),
            item_enchant("minecraft:chainmail_leggings", 6, 10, 18),
            item_enchant("minecraft:chainmail_boots", 8, 10, 18),
            item_enchant("minecraft:iron_helmet", 6, 10, 18),
            item_enchant("minecraft:iron_chestplate", 4, 10, 18),
            item_enchant("minecraft:iron_leggings", 4, 10, 18),
            item_enchant("minecraft:iron_boots", 6, 10, 18),
            item_enchant("minecraft:bow", 8, 10, 18),
            item_enchant("minecraft:iron_pickaxe", 8, 10, 18),
            item_simple("minecraft:shield", 10),
            item_simple("minecraft:brush", 6),
            item_count("minecraft:compass", 6, 1, 3),
            item_count("minecraft:clock", 6, 1, 3)
        ]),
        pool_common_gear_t1(3, 5),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(2, 4)
    ])

    # =========================================================================
    # 2. ORE1 (Этажи 1-3) - БЕЗ АЛМАЗОВ
    # =========================================================================
    write_table(output_dir, "ore1.json", [
        make_pool(3, 5, [
            item_count("minecraft:raw_iron", 16, 6, 16),
            item_count("minecraft:raw_copper", 14, 8, 20),
            item_count("minecraft:raw_gold", 10, 4, 10),
            item_count("minecraft:iron_ingot", 14, 4, 10),
            item_count("minecraft:copper_ingot", 12, 6, 16),
            item_count("minecraft:gold_ingot", 8, 2, 6),
            item_count("minecraft:lapis_lazuli", 12, 8, 20),
            item_count("minecraft:redstone", 12, 8, 20),
            item_count("minecraft:amethyst_shard", 8, 4, 10),
            item_count("minecraft:quartz", 8, 6, 14),
            item_count("minecraft:coal", 16, 12, 28)
        ]),
        pool_common_gear_t1(2, 4),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(3, 5)
    ])

    # =========================================================================
    # 3. ORE2 (Этажи 4-5) - АЛМАЗЫ, СМОЛА 26.3, ЭНДГЕЙМ
    # =========================================================================
    write_table(output_dir, "ore2.json", [
        make_pool(3, 5, [
            item_count("minecraft:diamond", 8, 2, 6),
            item_count("minecraft:emerald", 12, 4, 10),
            item_count("minecraft:gold_ingot", 14, 6, 16),
            item_count("minecraft:iron_ingot", 16, 8, 20),
            item_count("minecraft:lapis_lazuli", 14, 12, 28),
            item_count("minecraft:redstone", 14, 12, 28),
            item_count("minecraft:amethyst_shard", 10, 6, 16),
            item_count("minecraft:resin_clump", 10, 4, 10),
            item_count("minecraft:iron_block", 5, 1, 3),
            item_count("minecraft:gold_block", 4, 1, 3),
            item_count("minecraft:emerald_block", 3, 1, 3),
            item_count("minecraft:echo_shard", 4, 2, 5)
        ]),
        pool_common_gear_t2(3, 5),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(3, 5)
    ])

    # =========================================================================
    # 4. BLOCK1 (Этажи 1-3) - ДЕКОР, АРХЕОЛОГИЯ И МЕДЬ 26.3
    # =========================================================================
    write_table(output_dir, "block1.json", [
        make_pool(3, 5, [
            item_count("minecraft:lantern", 14, 4, 10),
            item_count("minecraft:iron_chain", 14, 6, 14),
            item_count("minecraft:copper_bulb", 12, 2, 6),
            item_count("minecraft:copper_grate", 12, 4, 12),
            item_count("minecraft:chiseled_stone_bricks", 10, 6, 14),
            item_count("minecraft:chiseled_tuff", 10, 6, 14),
            item_count("minecraft:bookshelf", 8, 2, 5),
            item_count("minecraft:candle", 10, 4, 12),
            item_count("minecraft:cobweb", 8, 2, 6),
            item_count("minecraft:tinted_glass", 6, 3, 8),
            item_count("minecraft:flower_pot", 6, 2, 4),
            item_count("minecraft:pale_oak_sapling", 6, 2, 5),
            item_count("minecraft:decorated_pot", 4, 1, 3),
            item_count("minecraft:burn_pottery_sherd", 3, 1, 4),
            item_count("minecraft:danger_pottery_sherd", 3, 1, 4),
            item_count("minecraft:friend_pottery_sherd", 3, 1, 4),
            item_count("minecraft:heart_pottery_sherd", 3, 1, 4),
            item_count("minecraft:heartbreak_pottery_sherd", 3, 1, 4),
            item_count("minecraft:sheaf_pottery_sherd", 3, 1, 4)
        ]),
        pool_common_gear_t1(2, 4),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(2, 4)
    ])

    # =========================================================================
    # 5. BLOCK2 (Этажи 4-5) - СЕРДЦЕ СКРИПУНА, СКАЛК, CRAFTER 26.3
    # =========================================================================
    write_table(output_dir, "block2.json", [
        make_pool(3, 5, [
            item_count("minecraft:crying_obsidian", 14, 3, 8),
            item_count("minecraft:obsidian", 14, 4, 10),
            item_count("minecraft:soul_lantern", 12, 3, 8),
            item_count("minecraft:sea_lantern", 12, 3, 8),
            item_count("minecraft:chiseled_tuff_bricks", 10, 6, 16),
            item_count("minecraft:chiseled_copper", 10, 6, 16),
            item_count("minecraft:magma_block", 8, 4, 10),
            item_count("minecraft:resin_bricks", 8, 6, 16),
            item_count("minecraft:chiseled_resin_bricks", 6, 4, 10),
            item_count("minecraft:sculk_catalyst", 4, 1, 3),
            item_count("minecraft:sculk_sensor", 4, 1, 3),
            item_count("minecraft:crafter", 4, 1, 3),
            item_count("minecraft:ender_chest", 3, 1, 3),
            item_count("minecraft:lodestone", 2, 1, 2),
            item_count("minecraft:respawn_anchor", 2, 1, 2),
            item_count("minecraft:creaking_heart", 2, 1, 2)
        ]),
        pool_common_gear_t2(3, 5),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(2, 4)
    ])

    # =========================================================================
    # 6. FOOD1 (Этажи 1-3)
    # =========================================================================
    write_table(output_dir, "food1.json", [
        make_pool(3, 5, [
            item_count("minecraft:bread", 16, 8, 18),
            item_count("minecraft:cooked_beef", 14, 6, 14),
            item_count("minecraft:cooked_porkchop", 14, 6, 14),
            item_count("minecraft:cooked_chicken", 14, 6, 14),
            item_count("minecraft:baked_potato", 14, 8, 16),
            item_count("minecraft:apple", 12, 6, 14),
            item_count("minecraft:carrot", 12, 8, 18),
            item_count("minecraft:cookie", 10, 8, 20),
            item_count("minecraft:pumpkin_pie", 8, 2, 6),
            item_count("minecraft:sweet_berries", 10, 6, 16),
            item_count("minecraft:honey_bottle", 8, 2, 5),
            item_count("minecraft:melon_seeds", 6, 4, 10),
            item_count("minecraft:pumpkin_seeds", 6, 4, 10),
            item_count("minecraft:golden_apple", 3, 1, 3),
            item_count("minecraft:egg", 10, 6, 16)
        ]),
        pool_common_gear_t1(2, 4),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(2, 4)
    ])

    # =========================================================================
    # 7. FOOD2 (Этажи 4-5) - ДРЕВНЯЯ ФЛОРА И ЗОЛОТАЯ ЕДА
    # =========================================================================
    write_table(output_dir, "food2.json", [
        make_pool(3, 5, [
            item_count("minecraft:golden_carrot", 16, 6, 16),
            item_count("minecraft:golden_apple", 8, 2, 6),
            item_count("minecraft:cooked_beef", 14, 8, 18),
            item_count("minecraft:cooked_porkchop", 14, 8, 18),
            item_count("minecraft:glistering_melon_slice", 10, 4, 10),
            item_count("minecraft:honey_bottle", 10, 4, 8),
            item_count("minecraft:sniffer_egg", 3, 1, 3),
            item_count("minecraft:turtle_egg", 4, 2, 6),
            item_count("minecraft:torchflower_seeds", 4, 2, 6),
            item_count("minecraft:pitcher_pod", 4, 2, 6),
            item_count("minecraft:popped_chorus_fruit", 8, 6, 14),
            item_count("minecraft:enchanted_golden_apple", 1, 1, 2)
        ]),
        pool_common_gear_t2(3, 5),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(2, 4)
    ])

    # =========================================================================
    # 8. SUPPLY1 (Этажи 1-3)
    # =========================================================================
    write_table(output_dir, "supply1.json", [
        make_pool(3, 5, [
            item_count("minecraft:saddle", 8, 1, 1),
            item_count("minecraft:minecart", 8, 1, 1),
            item_count("minecraft:bundle", 10, 1, 1),
            item_count("minecraft:lead", 8, 2, 6),
            item_count("minecraft:name_tag", 8, 2, 6),
            item_count("minecraft:compass", 6, 1, 3),
            item_count("minecraft:clock", 6, 1, 3),
            item_simple("minecraft:spyglass", 6),
            item_count("minecraft:flint_and_steel", 8, 1, 1),
            item_count("minecraft:shears", 8, 1, 1),
            item_count("minecraft:brush", 8, 1, 1),
            item_count("minecraft:snowball", 10, 12, 24)
        ]),
        pool_common_gear_t1(3, 5),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(2, 4)
    ])

    # =========================================================================
    # 9. SUPPLY2 (Этажи 4-5) - КЛЮЧИ ИСПЫТАНИЙ, КНИГИ, ТОТЕМ
    # =========================================================================
    write_table(output_dir, "supply2.json", [
        make_pool(3, 5, [
            item_count("minecraft:trial_key", 8, 2, 5),
            item_count("minecraft:ominous_trial_key", 4, 1, 3),
            item_ominous_bottle(6, 1, 4, 1, 3),
            item_count("minecraft:totem_of_undying", 2, 1, 1),
            item_count("minecraft:saddle", 6, 1, 1),
            item_count("minecraft:bundle", 8, 1, 1),
            item_count("minecraft:wind_charge", 12, 8, 20),
            item_count("minecraft:spectral_arrow", 12, 12, 24),
            item_count("minecraft:echo_shard", 5, 2, 5),
            item_enchant_random(4, "veinminer_enchantment:veinminer"),
            item_enchant_random(4, "minecraft:swift_sneak"),
            item_enchant_random(4, "minecraft:mending"),
            item_enchant_random(4, "minecraft:unbreaking"),
            item_enchant_random(4, "minecraft:fortune"),
            item_enchant_random(4, "minecraft:looting"),
            item_enchant_random(3, "minecraft:density"),
            item_enchant_random(3, "minecraft:breach"),
            item_enchant_random(3, "minecraft:wind_burst")
        ]),
        pool_common_gear_t2(3, 5),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(3, 5)
    ])

    # =========================================================================
    # 10. TOOL1 (Этажи 1-3) - ИНСТРУМЕНТЫ С ГАРАНТИРОВАННЫМИ ЧАРАМИ
    # =========================================================================
    write_table(output_dir, "tool1.json", [
        make_pool(2, 4, [
            item_enchant("minecraft:iron_pickaxe", 12, 15, 25),
            item_enchant("minecraft:iron_axe", 10, 15, 25),
            item_enchant("minecraft:iron_shovel", 10, 15, 25),
            item_enchant("minecraft:iron_hoe", 6, 15, 25),
            item_enchant("minecraft:fishing_rod", 8, 15, 25),
            item_simple("minecraft:flint_and_steel", 8),
            item_simple("minecraft:shears", 8),
            item_simple("minecraft:brush", 8),
            item_count("minecraft:compass", 6, 1, 3),
            item_count("minecraft:clock", 6, 1, 3),
            item_count("minecraft:lead", 6, 2, 6),
            item_count("minecraft:name_tag", 6, 2, 6)
        ]),
        pool_common_gear_t1(2, 4),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(2, 4)
    ])

    # =========================================================================
    # 11. TOOL2 (Этажи 4-5) - АЛМАЗНЫЕ ИНСТРУМЕНТЫ, RECOVERY COMPASS, РЕЛИКВИИ
    # =========================================================================
    write_table(output_dir, "tool2.json", [
        make_pool(2, 4, [
            item_enchant("minecraft:diamond_pickaxe", 10, 25, 35),
            item_enchant("minecraft:diamond_axe", 8, 25, 35),
            item_enchant("minecraft:diamond_shovel", 8, 25, 35),
            item_enchant("minecraft:diamond_hoe", 5, 20, 30),
            item_enchant("minecraft:iron_pickaxe", 8, 25, 35),
            item_count("minecraft:recovery_compass", 4, 1, 2),
            item_simple("minecraft:spyglass", 6),
            item_count("minecraft:name_tag", 8, 2, 6),
            item_count("minecraft:lead", 8, 2, 6),
            item_enchant_random(4, "veinminer_enchantment:veinminer"),
            # Запечатанные реликвии GanjaCraftCore (Алмазная основа)
            item_sealed_relic(
                "minecraft:diamond_pickaxe", "soulcatcher_pickaxe", "sealed_soulcatcher_pickaxe", 7701,
                "★ Запечатанный Шуруповёрт 'Макита'",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Украден со стройки элитного ЖК, так и не донесён до скупщика.",
                    "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                    " ",
                    "§e✦ Свойство: §fСкручивает спавнеры монстров в инвентарь",
                ],
                {"minecraft:efficiency": 6, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:diamond_pickaxe", "autosmelt_pickaxe", "sealed_autosmelt_pickaxe", 7726,
                "★ Запечатанная Горелка-Автоплавилка",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Промышленный резак с высокотемпературным пламенем.",
                    "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                    " ",
                    "§e✦ Свойство: §fМгновенная плавка руд прямо в забое",
                    "§e✦ Бонус: §fУмножает выплавленные слитки с учётом Удачи IV",
                ],
                {"minecraft:efficiency": 6, "minecraft:fortune": 4, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:diamond_pickaxe", "excavator_pickaxe", "sealed_excavator_pickaxe", 7728,
                "★ Запечатанный Шахтный Бур 3х3",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Тяжёлая буровая коронка с алмазным напылением.",
                    "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                    " ",
                    "§e✦ Свойство: §fМгновенная проходка тоннелей 3х3 блока",
                ],
                {"minecraft:efficiency": 6, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:diamond_shovel", "excavator_shovel", "sealed_excavator_shovel", 7712,
                "★ Запечатанный Экскаваторный Ковш",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Гидравлический ковш со стройки метрополитена.",
                    "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                    " ",
                    "§e✦ Свойство: §fВыемка грунта 3х3 блока",
                ],
                {"minecraft:efficiency": 6, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:fishing_rod", "poacher_harpoon", "sealed_poacher_harpoon", 7714,
                "★ Запечатанный Титановый Гарпун",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Китобойный трос с усиленной электролебёдкой.",
                    "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                    " ",
                    "§b✦ Свойство: §fМагнитная тяга лута со дна и земли",
                    "§b✦ Спецэффект: §fПодтягивает мобов в упор и сбивает щиты",
                ],
                {"minecraft:unbreaking": 5, "minecraft:lure": 3}
            )
        ]),
        pool_common_gear_t2(3, 5),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(3, 5)
    ])

    # =========================================================================
    # 12. WEAPON1 (Этажи 1-3) - ОРУЖИЕ С ГАРАНТИРОВАННЫМИ ЧАРАМИ (БЕЗ ДЕРЕВА И АЛМАЗОВ)
    # =========================================================================
    write_table(output_dir, "weapon1.json", [
        make_pool(2, 4, [
            item_enchant("minecraft:iron_sword", 14, 15, 25),
            item_enchant("minecraft:iron_axe", 10, 15, 25),
            item_enchant("minecraft:golden_sword", 6, 20, 30),
            item_enchant("minecraft:bow", 12, 15, 25),
            item_enchant("minecraft:crossbow", 10, 15, 25),
            item_enchant("minecraft:shield", 8, 15, 25),
            item_count("minecraft:spectral_arrow", 10, 6, 16),
            item_potion("minecraft:tipped_arrow", 8, "minecraft:poison", 3, 8),
            item_potion("minecraft:tipped_arrow", 8, "minecraft:weakness", 3, 8),
            item_potion("minecraft:tipped_arrow", 8, "minecraft:slowness", 3, 8)
        ]),
        pool_common_gear_t1(3, 5),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(2, 4)
    ])

    # =========================================================================
    # 13. WEAPON2 (Этажи 4-5) - HEAVY CORE, РЕЛИКВИИ, АЛМАЗЫ (БУЛАВА ИСКЛЮЧЕНА)
    # =========================================================================
    write_table(output_dir, "weapon2.json", [
        make_pool(2, 4, [
            item_enchant("minecraft:diamond_sword", 10, 25, 35),
            item_enchant("minecraft:diamond_axe", 8, 25, 35),
            item_enchant("minecraft:bow", 10, 25, 35),
            item_enchant("minecraft:crossbow", 10, 25, 35),
            item_enchant("minecraft:trident", 3, 25, 35),
            item_enchant("minecraft:shield", 8, 20, 30),
            item_count("minecraft:heavy_core", 1, 1, 2),
            item_count("minecraft:totem_of_undying", 2, 1, 1),
            item_potion("minecraft:tipped_arrow", 8, "minecraft:strong_healing", 3, 8),
            item_potion("minecraft:tipped_arrow", 8, "minecraft:strong_harming", 3, 8),
            item_potion("minecraft:tipped_arrow", 8, "minecraft:long_slowness", 3, 8),
            # Запечатанные реликвии GanjaCraftCore (Алмазная / специальная основа)
            item_sealed_relic(
                "minecraft:diamond_sword", "executioner_blade", "sealed_executioner_blade", 7702,
                "★ Запечатанная Бандитская Заточка",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Выкована из рессоры грузовика в подпольном гараже.",
                    "§8Кровавая гравировка: невозможно изменить на наковальне.",
                    " ",
                    "§c✦ Свойство: §fУбойная сила и повышенный отжим лута",
                ],
                {"minecraft:sharpness": 6, "minecraft:looting": 4, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:diamond_sword", "vampire_blade", "sealed_vampire_blade", 7706,
                "★ Запечатанная Заточка с Кровотоком",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Лезвие впитало слишком много криминальных разборок.",
                    "§8Кровавая гравировка: невозможно изменить на наковальне.",
                    " ",
                    "§c✦ Свойство: §fВампиризм 35% и глубокое кровотечение",
                ],
                {"minecraft:sharpness": 6, "minecraft:looting": 4, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:golden_sword", "thief_dagger", "sealed_thief_dagger", 7710,
                "★ Запечатанная Заточка Вора-Авторитета",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Именное перо криминального авторитета из чистейшего золота.",
                    "§8Воровская метка: невозможно изменить на наковальне.",
                    " ",
                    "§e✦ Свойство: §fУдар в спину: x2.5 урона по мобам, кража 50-500 EMC у игроков",
                ],
                {"minecraft:sharpness": 6, "minecraft:looting": 4, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:crossbow", "pipe_shotgun", "sealed_pipe_shotgun", 7724,
                "★ Запечатанный Кустарный Дробовик 12К",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Тяжёлый гладкоствольный обрез с расточенным патронником.",
                    "§8Сварной шов: невозможно изменить на наковальне.",
                    " ",
                    "§c✦ Свойство: §fЗалп из 7 стрел веером за 1 патрон",
                    "§c✦ Убойная сила: §fКолоссальный урон картечью в упор",
                ],
                {"minecraft:quick_charge": 3, "minecraft:piercing": 4, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:bow", "ancestral_bow", "sealed_ancestral_bow", 7703,
                "★ Запечатанный Самопал из Трубы",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Собран на коленке из водопроводных труб и натяжного троса.",
                    "§8Кустарная резьба: невозможно изменить на наковальне.",
                    " ",
                    "§b✦ Свойство: §fБесконечные зажигательные залпы",
                ],
                {"minecraft:power": 6, "minecraft:flame": 1, "minecraft:infinity": 1, "minecraft:unbreaking": 4}
            ),
            item_sealed_relic(
                "minecraft:shield", "titan_shield", "sealed_titan_shield", 7704,
                "★ Запечатанный Люк от Теплотрассы",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Тяжеленный чугунный люк с клеймом советского ГОСТа.",
                    "§8Заварен наглухо: невозможно изменить на наковальне.",
                    " ",
                    "§6✦ Свойство: §fНепробиваемая чугунная защита",
                ],
                {"minecraft:unbreaking": 5}
            )
        ]),
        pool_common_gear_t2(3, 5),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(3, 5)
    ])

    # =========================================================================
    # 14. ARMOR1 (Этажи 1-3) - КОЛЬЧУГА, ЖЕЛЕЗО, ЗОЛОТО, ТРИМЫ (БЕЗ КОЖИ!)
    # =========================================================================
    write_table(output_dir, "armor1.json", [
        make_pool(2, 4, [
            item_enchant("minecraft:chainmail_helmet", 10, 15, 25),
            item_enchant("minecraft:chainmail_chestplate", 8, 15, 25),
            item_enchant("minecraft:chainmail_leggings", 8, 15, 25),
            item_enchant("minecraft:chainmail_boots", 10, 15, 25),
            item_enchant("minecraft:iron_helmet", 8, 15, 25),
            item_enchant("minecraft:iron_chestplate", 6, 15, 25),
            item_enchant("minecraft:iron_leggings", 6, 15, 25),
            item_enchant("minecraft:iron_boots", 8, 15, 25),
            item_enchant("minecraft:golden_helmet", 6, 20, 30),
            item_enchant("minecraft:golden_chestplate", 6, 20, 30),
            item_enchant("minecraft:golden_boots", 6, 20, 30),
            # Шаблоны отделки брони 1-3 этажей
            item_count("minecraft:sentry_armor_trim_smithing_template", 3, 1, 3),
            item_count("minecraft:dune_armor_trim_smithing_template", 3, 1, 3),
            item_count("minecraft:coast_armor_trim_smithing_template", 3, 1, 3),
            item_count("minecraft:wild_armor_trim_smithing_template", 3, 1, 3),
            item_count("minecraft:wayfinder_armor_trim_smithing_template", 3, 1, 3),
            item_count("minecraft:raiser_armor_trim_smithing_template", 3, 1, 3)
        ]),
        pool_common_gear_t1(3, 5),
        pool_common_mob_drops_t1(2, 4),
        pool_common_minerals_t1(2, 4)
    ])

    # =========================================================================
    # 15. ARMOR2 (Этажи 4-5) - АЛМАЗКА, 18 ТРИМОВ, ТОТЕМ, РЕЛИКВИИ
    # =========================================================================
    write_table(output_dir, "armor2.json", [
        make_pool(2, 4, [
            item_enchant("minecraft:diamond_helmet", 8, 25, 35),
            item_enchant("minecraft:diamond_chestplate", 6, 25, 35),
            item_enchant("minecraft:diamond_leggings", 6, 25, 35),
            item_enchant("minecraft:diamond_boots", 8, 25, 35),
            item_enchant("minecraft:chainmail_chestplate", 8, 25, 35),
            item_enchant("minecraft:golden_chestplate", 6, 25, 35),
            item_enchant("minecraft:shield", 8, 20, 30),
            item_count("minecraft:totem_of_undying", 2, 1, 1),
            # ПОЛНЫЙ НАБОР 18 ШАБЛОНОВ ОТДЕЛКИ (TRIMS)
            item_count("minecraft:sentry_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:dune_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:coast_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:wild_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:wayfinder_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:raiser_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:shaper_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:host_armor_trim_smithing_template", 2, 1, 3),
            item_count("minecraft:vex_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:eye_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:ward_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:rib_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:spire_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:snout_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:tide_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:flow_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:bolt_armor_trim_smithing_template", 1, 1, 3),
            item_count("minecraft:silence_armor_trim_smithing_template", 1, 1, 2),
            item_count("minecraft:netherite_upgrade_smithing_template", 1, 1, 2),
            # Узоры флагов
            item_count("minecraft:flow_banner_pattern", 1, 1, 2),
            item_count("minecraft:guster_banner_pattern", 1, 1, 2),
            item_count("minecraft:piglin_banner_pattern", 1, 1, 2),
            # Запечатанные реликвии GanjaCraftCore (Алмазная основа)
            item_sealed_relic(
                "minecraft:turtle_helmet", "welding_mask", "sealed_welding_mask", 7716,
                "★ Запечатанный Тепловизор Спецназа",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Армейский прибор ночного видения с инфракрасным сканером.",
                    "§8Военная приёмка: невозможно изменить на наковальне.",
                    " ",
                    "§e✦ Свойство: §fНочное зрение и иммунитет к темноте",
                    "§e✦ Тепловизор: §fПодсвечивает монстров вокруг сквозь стены",
                ],
                {"minecraft:protection": 5, "minecraft:unbreaking": 5, "minecraft:respiration": 3}
            ),
            item_sealed_relic(
                "minecraft:diamond_chestplate", "collector_vest", "sealed_collector_vest", 7718,
                "★ Запечатанный Инкассаторский Жилет",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Бронежилет высшего класса защиты с титановыми пластинами.",
                    "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                    " ",
                    "§a✦ Свойство: §fКолоссальная броня (+10) и анти-отдача",
                ],
                {"minecraft:protection": 5, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:diamond_leggings", "abibas_pants", "sealed_abibas_pants", 7720,
                "★ Запечатанные Штаны 'Абибас Три Полоски'",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Оригинальный винтажный костюм в идеальном сохране.",
                    "§8Шелкография 90-х: невозможно изменить на наковальне.",
                    " ",
                    "§a✦ Свойство: §fБег в горку без прыжков (+0.5 блока шага)",
                    "§a✦ Второе дыхание: §fПри HP < 30% даёт Спешку II и Скорость III",
                ],
                {"minecraft:protection": 5, "minecraft:unbreaking": 5}
            ),
            item_sealed_relic(
                "minecraft:diamond_boots", "roofer_sneakers", "sealed_roofer_sneakers", 7722,
                "★ Запечатанные Грави-Кроссы Контрабандиста",
                [
                    "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                    "§7Экспериментальная обувь на магнитной воздушной подушке.",
                    "§8Герметичная прошивка: невозможно изменить на наковальне.",
                    " ",
                    "§b✦ Свойство: §fНулевой урон от падений с любой высоты",
                    "§b✦ Мобильность: §fСвободный бег в воде и по рыхлому снегу",
                ],
                {"minecraft:feather_falling": 5, "minecraft:depth_strider": 3, "minecraft:unbreaking": 5}
            )
        ]),
        pool_common_gear_t2(3, 5),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(3, 5)
    ])

    # =========================================================================
    # 16. BREWING (Спецкомнаты алхимии)
    # =========================================================================
    write_table(output_dir, "brewing.json", [
        make_pool(3, 5, [
            item_count("minecraft:brewing_stand", 6, 1, 2),
            item_count("minecraft:nether_wart", 14, 6, 16),
            item_count("minecraft:blaze_powder", 12, 4, 12),
            item_count("minecraft:blaze_rod", 10, 2, 6),
            item_count("minecraft:glistering_melon_slice", 12, 4, 10),
            item_count("minecraft:golden_carrot", 12, 4, 10),
            item_count("minecraft:magma_cream", 10, 4, 10),
            item_count("minecraft:fermented_spider_eye", 10, 3, 8),
            item_count("minecraft:glass_bottle", 12, 8, 20),
            item_count("minecraft:ghast_tear", 6, 2, 5),
            item_count("minecraft:phantom_membrane", 6, 2, 6),
            item_count("minecraft:dragon_breath", 5, 2, 5),
            item_count("minecraft:rabbit_foot", 6, 2, 5),
            item_count("minecraft:spider_eye", 12, 4, 12),
            item_count("minecraft:sugar", 12, 8, 20),
            item_count("minecraft:glowstone_dust", 12, 8, 20),
            item_count("minecraft:redstone", 12, 8, 20),
            item_ominous_bottle(6, 1, 5, 1, 3),
            # Готовые зелья
            item_potion("minecraft:potion", 8, "minecraft:strong_healing"),
            item_potion("minecraft:potion", 8, "minecraft:long_regeneration"),
            item_potion("minecraft:potion", 8, "minecraft:long_fire_resistance"),
            item_potion("minecraft:potion", 8, "minecraft:strong_strength"),
            item_potion("minecraft:potion", 8, "minecraft:long_speed"),
            item_potion("minecraft:potion", 6, "minecraft:long_night_vision"),
            item_potion("minecraft:potion", 4, "minecraft:long_turtle_master"),
            item_potion("minecraft:potion", 5, "minecraft:weaving"),
            item_potion("minecraft:potion", 5, "minecraft:wind_charged"),
            item_potion("minecraft:potion", 5, "minecraft:oozing"),
            item_potion("minecraft:potion", 5, "minecraft:infested"),
            item_potion("minecraft:splash_potion", 6, "minecraft:strong_healing"),
            item_potion("minecraft:splash_potion", 6, "minecraft:long_slowness"),
            item_potion("minecraft:splash_potion", 6, "minecraft:long_weakness")
        ]),
        pool_common_gear_t2(2, 4),
        pool_common_mob_drops_t2(2, 4),
        pool_common_minerals_t2(2, 4)
    ])

    # =========================================================================
    # 17. MUSIC (Спецкомнаты музыки, сокровищницы и реликвий)
    # =========================================================================
    write_table(output_dir, "music.json", [
        make_pool(3, 5, [
            item_simple("minecraft:music_disc_cat", 3),
            item_simple("minecraft:music_disc_blocks", 3),
            item_simple("minecraft:music_disc_chirp", 3),
            item_simple("minecraft:music_disc_far", 3),
            item_simple("minecraft:music_disc_mall", 3),
            item_simple("minecraft:music_disc_mellohi", 3),
            item_simple("minecraft:music_disc_stal", 3),
            item_simple("minecraft:music_disc_strad", 3),
            item_simple("minecraft:music_disc_ward", 3),
            item_simple("minecraft:music_disc_11", 2),
            item_simple("minecraft:music_disc_wait", 3),
            item_simple("minecraft:music_disc_pigstep", 2),
            item_simple("minecraft:music_disc_otherside", 2),
            item_simple("minecraft:music_disc_5", 2),
            item_count("minecraft:disc_fragment_5", 6, 2, 5),
            item_simple("minecraft:music_disc_relic", 2),
            item_simple("minecraft:music_disc_creator", 2),
            item_simple("minecraft:music_disc_precipice", 2),
            item_goat_horn(8),
            item_count("minecraft:echo_shard", 6, 2, 5),
            item_count("minecraft:amethyst_shard", 10, 6, 16),
            item_count("minecraft:nautilus_shell", 6, 2, 5),
            item_count("minecraft:heart_of_the_sea", 2, 1, 2),
            item_count("minecraft:totem_of_undying", 2, 1, 1),
            item_count("minecraft:nether_star", 1, 1, 2) # Ультраредкий джекпот
        ]),
        pool_common_gear_t2(2, 4),
        pool_common_mob_drops_t2(3, 5),
        pool_common_minerals_t2(3, 5)
    ])

    print("\nSuccessfully generated all 17 expanded multi-pool loot tables!")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    generate_all(out)
