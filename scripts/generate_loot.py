#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор 17 лут-таблиц для Roguelike Dungeons (Minecraft 26.3 / SlashLoot)
"""

import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(REPO_ROOT, "datapacks", "roguelike_loot", "data", "roguelike", "loot_table", "chests")

def write_table(target_dir, filename, rolls_min, rolls_max, entries):
    table = {
        "type": "minecraft:chest",
        "pools": [
            {
                "rolls": {
                    "type": "minecraft:uniform",
                    "min": float(rolls_min),
                    "max": float(rolls_max)
                },
                "entries": entries
            }
        ]
    }
    path = os.path.join(target_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(table, f, indent=2, ensure_ascii=False)
    print(f"  [OK] {filename}")

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
                },
                "options": "#minecraft:on_random_loot"
            }
        ]
    }

def item_potion(name, weight, potion_id):
    return {
        "type": "minecraft:item",
        "name": name,
        "weight": weight,
        "functions": [
            {
                "function": "minecraft:set_potion",
                "id": potion_id
            }
        ]
    }

def generate_all(output_dir=None):
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating loot tables into: {output_dir}")

    # =========================================================================
    # 1. STARTER (Вход в данж, башня на поверхности, 0 этаж)
    # =========================================================================
    write_table(output_dir, "starter.json", 4, 7, [
        item_count("minecraft:torch", 15, 8, 16),
        item_count("minecraft:bread", 12, 4, 8),
        item_count("minecraft:apple", 10, 2, 5),
        item_count("minecraft:arrow", 12, 8, 16),
        item_count("minecraft:string", 10, 2, 5),
        item_count("minecraft:stick", 10, 4, 8),
        item_simple("minecraft:bundle", 5),
        item_simple("minecraft:bow", 6),
        item_simple("minecraft:stone_sword", 8),
        item_simple("minecraft:wooden_sword", 6),
        item_simple("minecraft:stone_pickaxe", 8),
        item_simple("minecraft:wooden_pickaxe", 6),
        item_simple("minecraft:stone_axe", 6),
        item_enchant("minecraft:leather_helmet", 8, 5, 10),
        item_enchant("minecraft:leather_chestplate", 6, 5, 10),
        item_enchant("minecraft:leather_leggings", 6, 5, 10),
        item_enchant("minecraft:leather_boots", 8, 5, 10)
    ])

    # =========================================================================
    # 2. ORE1 (Этажи 1-3) - НИКАКИХ АЛМАЗОВ!
    # =========================================================================
    write_table(output_dir, "ore1.json", 3, 6, [
        item_count("minecraft:coal", 18, 8, 16),
        item_count("minecraft:raw_iron", 15, 4, 10),
        item_count("minecraft:iron_ingot", 14, 2, 6),
        item_count("minecraft:raw_copper", 12, 6, 14),
        item_count("minecraft:copper_ingot", 10, 4, 10),
        item_count("minecraft:lapis_lazuli", 10, 4, 10),
        item_count("minecraft:redstone", 10, 4, 12),
        item_count("minecraft:iron_nugget", 10, 8, 20),
        item_count("minecraft:gold_nugget", 8, 8, 18),
        item_count("minecraft:gold_ingot", 6, 1, 4),
        item_count("minecraft:amethyst_shard", 5, 2, 6)
    ])

    # =========================================================================
    # 3. ORE2 (Этажи 4-5) - АЛМАЗЫ И ЭНДГЕЙМ РЕДКИЕ (вес 5 из ~130)
    # =========================================================================
    write_table(output_dir, "ore2.json", 3, 5, [
        item_count("minecraft:iron_ingot", 20, 6, 14),
        item_count("minecraft:gold_ingot", 18, 4, 10),
        item_count("minecraft:lapis_lazuli", 16, 8, 16),
        item_count("minecraft:redstone", 16, 8, 20),
        item_count("minecraft:emerald", 14, 2, 5),
        item_count("minecraft:amethyst_shard", 12, 4, 10),
        item_count("minecraft:iron_block", 5, 1, 1),
        item_count("minecraft:gold_block", 3, 1, 1),
        item_count("minecraft:diamond", 5, 1, 2),
        item_count("minecraft:ancient_debris", 1, 1, 1),
        item_count("minecraft:netherite_scrap", 1, 1, 1)
    ])

    # =========================================================================
    # 4. BLOCK1 (Этажи 1-3) - БЕЗ МУСОРНОЙ БУЛЫГИ
    # =========================================================================
    write_table(output_dir, "block1.json", 2, 4, [
        item_count("minecraft:lantern", 14, 2, 5),
        item_count("minecraft:iron_chain", 12, 2, 6),
        item_count("minecraft:copper_bulb", 10, 1, 3),
        item_count("minecraft:copper_grate", 10, 2, 6),
        item_count("minecraft:chiseled_stone_bricks", 10, 4, 8),
        item_count("minecraft:bookshelf", 8, 1, 2),
        item_count("minecraft:candle", 8, 2, 6),
        item_count("minecraft:cobweb", 8, 1, 3),
        item_count("minecraft:tinted_glass", 6, 2, 4),
        item_count("minecraft:flower_pot", 6, 1, 2)
    ])

    # =========================================================================
    # 5. BLOCK2 (Этажи 4-5) - АТМОСФЕРНЫЕ И ЦЕННЫЕ БЛОКИ
    # =========================================================================
    write_table(output_dir, "block2.json", 2, 3, [
        item_count("minecraft:crying_obsidian", 14, 2, 4),
        item_count("minecraft:obsidian", 14, 2, 5),
        item_count("minecraft:soul_lantern", 12, 2, 4),
        item_count("minecraft:sea_lantern", 12, 2, 4),
        item_count("minecraft:chiseled_tuff_bricks", 10, 4, 8),
        item_count("minecraft:chiseled_copper", 10, 4, 8),
        item_count("minecraft:magma_block", 8, 2, 6),
        item_count("minecraft:crafter", 3, 1, 1),
        item_count("minecraft:ender_chest", 2, 1, 1),
        item_count("minecraft:lodestone", 1, 1, 1),
        item_count("minecraft:respawn_anchor", 1, 1, 1)
    ])

    # =========================================================================
    # 6. FOOD1 (Этажи 1-3)
    # =========================================================================
    write_table(output_dir, "food1.json", 3, 5, [
        item_count("minecraft:bread", 15, 4, 8),
        item_count("minecraft:baked_potato", 12, 4, 8),
        item_count("minecraft:cooked_beef", 12, 3, 6),
        item_count("minecraft:cooked_porkchop", 12, 3, 6),
        item_count("minecraft:cooked_chicken", 12, 3, 6),
        item_count("minecraft:apple", 10, 3, 6),
        item_count("minecraft:carrot", 10, 4, 8),
        item_count("minecraft:honey_bottle", 6, 1, 2),
        item_count("minecraft:golden_apple", 1, 1, 1)
    ])

    # =========================================================================
    # 7. FOOD2 (Этажи 4-5)
    # =========================================================================
    write_table(output_dir, "food2.json", 3, 5, [
        item_count("minecraft:cooked_beef", 18, 4, 10),
        item_count("minecraft:cooked_porkchop", 18, 4, 10),
        item_count("minecraft:golden_carrot", 14, 3, 6),
        item_count("minecraft:glistering_melon_slice", 10, 2, 5),
        item_count("minecraft:golden_apple", 5, 1, 2),
        item_count("minecraft:enchanted_golden_apple", 1, 1, 1)
    ])

    # =========================================================================
    # 8. SUPPLY1 (Этажи 1-3)
    # =========================================================================
    write_table(output_dir, "supply1.json", 3, 5, [
        item_count("minecraft:torch", 16, 8, 16),
        item_count("minecraft:arrow", 14, 8, 16),
        item_count("minecraft:string", 12, 3, 6),
        item_count("minecraft:bone", 10, 3, 6),
        item_count("minecraft:bone_meal", 10, 4, 8),
        item_count("minecraft:gunpowder", 8, 2, 5),
        item_count("minecraft:paper", 8, 3, 6),
        item_count("minecraft:book", 8, 1, 3),
        item_count("minecraft:glass_bottle", 8, 3, 6),
        item_count("minecraft:feather", 8, 3, 6),
        item_count("minecraft:glow_ink_sac", 6, 1, 3)
    ])

    # =========================================================================
    # 9. SUPPLY2 (Этажи 4-5)
    # =========================================================================
    write_table(output_dir, "supply2.json", 3, 5, [
        item_count("minecraft:experience_bottle", 16, 3, 8),
        item_count("minecraft:glowstone_dust", 14, 4, 10),
        item_count("minecraft:gunpowder", 14, 4, 10),
        item_enchant("minecraft:enchanted_book", 10, 20, 30),
        item_count("minecraft:blaze_rod", 8, 1, 2),
        item_count("minecraft:tnt", 8, 1, 3),
        item_count("minecraft:ghast_tear", 6, 1, 2),
        item_count("minecraft:ender_pearl", 6, 1, 2),
        item_count("minecraft:ominous_bottle", 4, 1, 1),
        item_count("minecraft:echo_shard", 3, 1, 2),
        item_count("minecraft:totem_of_undying", 1, 1, 1)
    ])

    # =========================================================================
    # 10. TOOL1 (Этажи 1-3) - БЕЗ АЛМАЗОВ
    # =========================================================================
    write_table(output_dir, "tool1.json", 2, 3, [
        item_enchant("minecraft:iron_pickaxe", 12, 5, 15),
        item_enchant("minecraft:iron_axe", 10, 5, 15),
        item_enchant("minecraft:iron_shovel", 10, 5, 15),
        item_enchant("minecraft:fishing_rod", 8, 5, 15),
        item_simple("minecraft:flint_and_steel", 8),
        item_simple("minecraft:shears", 8),
        item_simple("minecraft:compass", 6),
        item_simple("minecraft:clock", 6),
        item_count("minecraft:lead", 6, 1, 2),
        item_count("minecraft:name_tag", 5, 1, 1)
    ])

    # =========================================================================
    # 11. TOOL2 (Этажи 4-5) - АЛМАЗНЫЕ ИНСТРУМЕНТЫ РЕДКИЕ
    # =========================================================================
    write_table(output_dir, "tool2.json", 2, 3, [
        item_enchant("minecraft:iron_pickaxe", 10, 20, 30),
        item_enchant("minecraft:diamond_pickaxe", 6, 20, 30),
        item_enchant("minecraft:diamond_axe", 5, 20, 30),
        item_enchant("minecraft:diamond_shovel", 5, 20, 30),
        item_enchant("minecraft:diamond_hoe", 3, 15, 25),
        item_simple("minecraft:spyglass", 8),
        item_count("minecraft:name_tag", 8, 1, 2),
        item_count("minecraft:lead", 8, 1, 2),
        item_simple("minecraft:brush", 6),
        item_simple("minecraft:clock", 6),
        item_simple("minecraft:compass", 6)
    ])

    # =========================================================================
    # 12. WEAPON1 (Этажи 1-3) - БЕЗ АЛМАЗОВ
    # =========================================================================
    write_table(output_dir, "weapon1.json", 2, 4, [
        item_enchant("minecraft:iron_sword", 12, 5, 15),
        item_enchant("minecraft:bow", 10, 5, 15),
        item_enchant("minecraft:crossbow", 8, 5, 15),
        item_simple("minecraft:shield", 10),
        item_enchant("minecraft:stone_sword", 8, 5, 10),
        item_count("minecraft:arrow", 16, 12, 24),
        item_count("minecraft:spectral_arrow", 8, 4, 10)
    ])

    # =========================================================================
    # 13. WEAPON2 (Этажи 4-5) - АЛМАЗНЫЙ МЕЧ И ЭНДГЕЙМ РЕДКИЕ
    # =========================================================================
    write_table(output_dir, "weapon2.json", 2, 4, [
        item_enchant("minecraft:bow", 12, 20, 30),
        item_enchant("minecraft:crossbow", 12, 20, 30),
        item_count("minecraft:spectral_arrow", 12, 8, 16),
        item_count("minecraft:wind_charge", 8, 3, 6),
        item_potion("minecraft:tipped_arrow", 8, "minecraft:strong_healing"),
        item_potion("minecraft:tipped_arrow", 8, "minecraft:long_slowness"),
        item_enchant("minecraft:shield", 8, 15, 25),
        item_enchant("minecraft:diamond_sword", 5, 20, 30),
        item_enchant("minecraft:trident", 2, 15, 25),
        item_count("minecraft:breeze_rod", 2, 1, 1)
    ])

    # =========================================================================
    # 14. ARMOR1 (Этажи 1-3) - КОЛЬЧУГА, ЖЕЛЕЗО, ЗОЛОТО
    # =========================================================================
    write_table(output_dir, "armor1.json", 2, 3, [
        item_enchant("minecraft:chainmail_helmet", 10, 5, 15),
        item_enchant("minecraft:chainmail_chestplate", 8, 5, 15),
        item_enchant("minecraft:chainmail_leggings", 8, 5, 15),
        item_enchant("minecraft:chainmail_boots", 10, 5, 15),
        item_enchant("minecraft:iron_helmet", 8, 5, 15),
        item_enchant("minecraft:iron_chestplate", 6, 5, 15),
        item_enchant("minecraft:iron_leggings", 6, 5, 15),
        item_enchant("minecraft:iron_boots", 8, 5, 15),
        item_enchant("minecraft:golden_helmet", 6, 10, 20),
        item_enchant("minecraft:golden_boots", 6, 10, 20)
    ])

    # =========================================================================
    # 15. ARMOR2 (Этажи 4-5) - АЛМАЗКА + РЕДКИЕ ШАБЛОНЫ ОТДЕЛКИ (TRIMS)
    # =========================================================================
    write_table(output_dir, "armor2.json", 2, 3, [
        item_enchant("minecraft:diamond_helmet", 8, 20, 30),
        item_enchant("minecraft:diamond_chestplate", 6, 20, 30),
        item_enchant("minecraft:diamond_leggings", 6, 20, 30),
        item_enchant("minecraft:diamond_boots", 8, 20, 30),
        item_enchant("minecraft:chainmail_chestplate", 8, 20, 30),
        item_enchant("minecraft:chainmail_leggings", 8, 20, 30),
        item_enchant("minecraft:golden_chestplate", 6, 25, 30),
        item_enchant("minecraft:golden_leggings", 6, 25, 30),
        item_enchant("minecraft:shield", 8, 20, 30),
        item_count("minecraft:sentry_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:dune_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:coast_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:wild_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:vex_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:eye_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:ward_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:rib_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:spire_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:flow_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:bolt_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:silence_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:netherite_upgrade_smithing_template", 1, 1, 1)
    ])

    # =========================================================================
    # 16. BREWING (Спецкомнаты)
    # =========================================================================
    write_table(output_dir, "brewing.json", 3, 5, [
        item_count("minecraft:brewing_stand", 4, 1, 1),
        item_count("minecraft:nether_wart", 12, 3, 7),
        item_count("minecraft:blaze_powder", 10, 2, 4),
        item_count("minecraft:glistering_melon_slice", 10, 2, 4),
        item_count("minecraft:golden_carrot", 10, 2, 4),
        item_count("minecraft:magma_cream", 8, 2, 4),
        item_count("minecraft:fermented_spider_eye", 8, 2, 4),
        item_count("minecraft:glass_bottle", 10, 4, 8),
        item_count("minecraft:ghast_tear", 4, 1, 2),
        item_count("minecraft:phantom_membrane", 4, 1, 2),
        item_potion("minecraft:potion", 8, "minecraft:strong_healing"),
        item_potion("minecraft:potion", 8, "minecraft:long_regeneration"),
        item_potion("minecraft:potion", 8, "minecraft:long_fire_resistance"),
        item_potion("minecraft:potion", 8, "minecraft:strong_strength"),
        item_potion("minecraft:potion", 8, "minecraft:long_speed"),
        item_potion("minecraft:potion", 6, "minecraft:long_night_vision"),
        item_potion("minecraft:splash_potion", 6, "minecraft:strong_healing"),
        item_potion("minecraft:splash_potion", 5, "minecraft:long_slowness"),
        item_potion("minecraft:splash_potion", 5, "minecraft:long_weakness"),
        item_count("minecraft:ominous_bottle", 3, 1, 1)
    ])

    # =========================================================================
    # 17. MUSIC (Спецкомнаты)
    # =========================================================================
    write_table(output_dir, "music.json", 2, 4, [
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
        item_simple("minecraft:music_disc_relic", 2),
        item_simple("minecraft:music_disc_creator", 2),
        item_simple("minecraft:goat_horn", 8),
        item_count("minecraft:echo_shard", 4, 1, 2),
        item_count("minecraft:amethyst_shard", 8, 3, 8),
        item_count("minecraft:nautilus_shell", 4, 1, 1),
        item_count("minecraft:heart_of_the_sea", 1, 1, 1)
    ])

    print("Successfully generated all 17 loot tables!")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    generate_all(out)
