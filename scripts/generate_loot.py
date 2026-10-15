#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Расширенный генератор 17 лут-таблиц для Roguelike Dungeons (Minecraft 26.3 / SlashLoot)
Включает:
- Полную палитру ванильных данжей (Trial Chambers, Ancient City, Bastions, Trail Ruins, Pale Garden)
- Синергию с сервером (VeinMiner, 18 шаблонов отделки брони, запечатанные реликвии GanjaCraftCore)
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

def item_ominous_bottle(weight, min_amp=1, max_amp=4):
    return {
        "type": "minecraft:item",
        "name": "minecraft:ominous_bottle",
        "weight": weight,
        "functions": [
            {
                "function": "minecraft:set_count",
                "count": 1.0,
                "add": False
            },
            {
                "function": "minecraft:set_ominous_bottle_amplifier",
                "amplifier": {
                    "type": "minecraft:uniform",
                    "min": float(min_amp),
                    "max": float(max_amp)
                }
            }
        ]
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


def generate_all(output_dir=None):
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating expanded loot tables into: {output_dir}")

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
        item_simple("minecraft:bundle", 6),
        item_simple("minecraft:shield", 8),
        item_simple("minecraft:bow", 6),
        item_simple("minecraft:brush", 5),
        item_simple("minecraft:stone_sword", 8),
        item_simple("minecraft:wooden_sword", 6),
        item_simple("minecraft:stone_pickaxe", 8),
        item_simple("minecraft:wooden_pickaxe", 6),
        item_simple("minecraft:stone_axe", 6),
        item_count("minecraft:wheat_seeds", 6, 4, 8),
        item_count("minecraft:carrot", 6, 2, 4),
        item_simple("minecraft:miner_pottery_sherd", 3),
        item_simple("minecraft:shelter_pottery_sherd", 3),
        item_simple("minecraft:howl_pottery_sherd", 3),
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
        item_count("minecraft:amethyst_shard", 5, 2, 6),
        item_count("minecraft:flint", 8, 4, 8),
        item_count("minecraft:quartz", 6, 4, 8)
    ])

    # =========================================================================
    # 3. ORE2 (Этажи 4-5) - АЛМАЗЫ, СМОЛА 26.3, ЭНДГЕЙМ
    # =========================================================================
    write_table(output_dir, "ore2.json", 3, 5, [
        item_count("minecraft:iron_ingot", 18, 6, 14),
        item_count("minecraft:gold_ingot", 16, 4, 10),
        item_count("minecraft:lapis_lazuli", 14, 8, 16),
        item_count("minecraft:redstone", 14, 8, 20),
        item_count("minecraft:emerald", 12, 2, 5),
        item_count("minecraft:amethyst_shard", 10, 4, 10),
        item_count("minecraft:resin_clump", 8, 2, 6),     # Смола 26.3
        item_count("minecraft:iron_block", 4, 1, 1),
        item_count("minecraft:gold_block", 3, 1, 1),
        item_count("minecraft:emerald_block", 2, 1, 1),
        item_count("minecraft:diamond", 5, 1, 2),        # Редкие алмазы
        item_count("minecraft:ancient_debris", 1, 1, 1), # Супер-редкий эндгейм
        item_count("minecraft:netherite_scrap", 1, 1, 1) # Супер-редкий эндгейм
    ])

    # =========================================================================
    # 4. BLOCK1 (Этажи 1-3) - ДЕКОР, АРХЕОЛОГИЯ И МЕДЬ 26.3
    # =========================================================================
    write_table(output_dir, "block1.json", 2, 4, [
        item_count("minecraft:lantern", 14, 2, 5),
        item_count("minecraft:iron_chain", 12, 2, 6),
        item_count("minecraft:copper_bulb", 10, 1, 3),
        item_count("minecraft:copper_grate", 10, 2, 6),
        item_count("minecraft:chiseled_stone_bricks", 10, 4, 8),
        item_count("minecraft:chiseled_tuff", 8, 4, 8),
        item_count("minecraft:bookshelf", 8, 1, 2),
        item_count("minecraft:candle", 8, 2, 6),
        item_count("minecraft:cobweb", 8, 1, 3),
        item_count("minecraft:tinted_glass", 6, 2, 4),
        item_count("minecraft:flower_pot", 6, 1, 2),
        item_count("minecraft:pale_oak_sapling", 4, 1, 2), # 26.3
        item_simple("minecraft:decorated_pot", 4),
        item_simple("minecraft:burn_pottery_sherd", 2),
        item_simple("minecraft:danger_pottery_sherd", 2),
        item_simple("minecraft:friend_pottery_sherd", 2),
        item_simple("minecraft:heart_pottery_sherd", 2),
        item_simple("minecraft:heartbreak_pottery_sherd", 2),
        item_simple("minecraft:sheaf_pottery_sherd", 2)
    ])

    # =========================================================================
    # 5. BLOCK2 (Этажи 4-5) - СЕРДЦЕ СКРИПУНА, СКАЛК, CRAFTER 26.3
    # =========================================================================
    write_table(output_dir, "block2.json", 2, 3, [
        item_count("minecraft:crying_obsidian", 14, 2, 4),
        item_count("minecraft:obsidian", 14, 2, 5),
        item_count("minecraft:soul_lantern", 12, 2, 4),
        item_count("minecraft:sea_lantern", 12, 2, 4),
        item_count("minecraft:chiseled_tuff_bricks", 10, 4, 8),
        item_count("minecraft:chiseled_copper", 10, 4, 8),
        item_count("minecraft:magma_block", 8, 2, 6),
        item_count("minecraft:resin_bricks", 6, 2, 6),           # Смоляные кирпичи 26.3
        item_count("minecraft:chiseled_resin_bricks", 5, 2, 4),   # Резные смоляные кирпичи 26.3
        item_count("minecraft:sculk_catalyst", 4, 1, 2),         # Ancient city
        item_count("minecraft:sculk_sensor", 4, 1, 2),
        item_count("minecraft:crafter", 3, 1, 1),                # 26.3 автоверстак
        item_count("minecraft:ender_chest", 2, 1, 1),            # Эндер-сундук
        item_count("minecraft:lodestone", 1, 1, 1),              # Магнетит
        item_count("minecraft:respawn_anchor", 1, 1, 1),          # Якорь возрождения
        item_count("minecraft:creaking_heart", 1, 1, 1)          # 26.3 Сердце Скрипуна (джекпот)
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
        item_count("minecraft:cookie", 8, 4, 8),
        item_count("minecraft:pumpkin_pie", 6, 1, 3),
        item_count("minecraft:sweet_berries", 8, 4, 8),
        item_count("minecraft:honey_bottle", 6, 1, 2),
        item_count("minecraft:melon_seeds", 6, 2, 4),
        item_count("minecraft:pumpkin_seeds", 6, 2, 4),
        item_count("minecraft:golden_apple", 1, 1, 1)
    ])

    # =========================================================================
    # 7. FOOD2 (Этажи 4-5) - ДРЕВНЯЯ ФЛОРА И ЗОЛОТАЯ ЕДА
    # =========================================================================
    write_table(output_dir, "food2.json", 3, 5, [
        item_count("minecraft:cooked_beef", 16, 4, 10),
        item_count("minecraft:cooked_porkchop", 16, 4, 10),
        item_count("minecraft:golden_carrot", 14, 3, 6),
        item_count("minecraft:glistering_melon_slice", 10, 2, 5),
        item_count("minecraft:golden_apple", 5, 1, 2),
        item_count("minecraft:sniffer_egg", 2, 1, 1),         # Яйцо нюхача!
        item_count("minecraft:torchflower_seeds", 3, 1, 2),
        item_count("minecraft:pitcher_pod", 3, 1, 2),
        item_count("minecraft:enchanted_golden_apple", 1, 1, 1) # Супер-редко
    ])

    # =========================================================================
    # 8. SUPPLY1 (Этажи 1-3)
    # =========================================================================
    write_table(output_dir, "supply1.json", 3, 5, [
        item_count("minecraft:torch", 16, 8, 16),
        item_count("minecraft:arrow", 14, 8, 16),
        item_count("minecraft:string", 12, 3, 6),
        item_count("minecraft:leather", 10, 2, 5),
        item_count("minecraft:bone", 10, 3, 6),
        item_count("minecraft:bone_meal", 10, 4, 8),
        item_count("minecraft:gunpowder", 8, 2, 5),
        item_count("minecraft:slime_ball", 8, 2, 4),
        item_count("minecraft:paper", 8, 3, 6),
        item_count("minecraft:book", 8, 1, 3),
        item_count("minecraft:glass_bottle", 8, 3, 6),
        item_count("minecraft:feather", 8, 3, 6),
        item_count("minecraft:glow_ink_sac", 6, 1, 3)
    ])

    # =========================================================================
    # 9. SUPPLY2 (Этажи 4-5) - TRIAL KEYS, VEINMINER, КНИГИ ЧАР
    # =========================================================================
    write_table(output_dir, "supply2.json", 3, 5, [
        item_count("minecraft:experience_bottle", 16, 4, 10),
        item_count("minecraft:glowstone_dust", 14, 4, 10),
        item_count("minecraft:gunpowder", 14, 4, 10),
        item_count("minecraft:wind_charge", 10, 4, 8),        # 26.3
        item_count("minecraft:breeze_rod", 8, 1, 2),          # 26.3
        item_count("minecraft:blaze_rod", 8, 1, 2),
        item_count("minecraft:tnt", 8, 1, 3),
        item_count("minecraft:ghast_tear", 6, 1, 2),
        item_count("minecraft:ender_pearl", 6, 1, 2),
        item_count("minecraft:trial_key", 8, 1, 2),           # 26.3 Ключ испытаний
        item_count("minecraft:ominous_trial_key", 3, 1, 1),   # 26.3 Зловещий ключ
        item_count("minecraft:echo_shard", 4, 1, 2),          # Ancient city
        item_ominous_bottle(4, 1, 4),                         # 26.3 Ominous Bottle II-V
        item_enchant("minecraft:enchanted_book", 8, 20, 30),
        item_enchant_random(2, "minecraft:swift_sneak"),      # Ancient city swift sneak
        item_enchant_random(2, ["minecraft:density", "minecraft:breach", "minecraft:wind_burst"]), # 26.3 Mace enchants
        item_enchant_random(2, "veinminer_enchantment:veinminer"), # VeinMiner книга!
        item_count("minecraft:totem_of_undying", 1, 1, 1)      # Тотем бессмертия
    ])

    # =========================================================================
    # 10. TOOL1 (Этажи 1-3) - БЕЗ АЛМАЗОВ
    # =========================================================================
    write_table(output_dir, "tool1.json", 2, 3, [
        item_enchant("minecraft:iron_pickaxe", 12, 5, 15),
        item_enchant("minecraft:iron_axe", 10, 5, 15),
        item_enchant("minecraft:iron_shovel", 10, 5, 15),
        item_enchant("minecraft:iron_hoe", 6, 5, 15),
        item_enchant("minecraft:fishing_rod", 8, 5, 15),
        item_simple("minecraft:flint_and_steel", 8),
        item_simple("minecraft:shears", 8),
        item_simple("minecraft:brush", 6),
        item_simple("minecraft:compass", 6),
        item_simple("minecraft:clock", 6),
        item_count("minecraft:lead", 6, 1, 2),
        item_count("minecraft:name_tag", 5, 1, 1)
    ])

    # =========================================================================
    # 11. TOOL2 (Этажи 4-5) - АЛМАЗНЫЕ ИНСТРУМЕНТЫ, RECOVERY COMPASS, РЕЛИКВИИ
    # =========================================================================
    write_table(output_dir, "tool2.json", 2, 3, [
        item_enchant("minecraft:iron_pickaxe", 10, 20, 30),
        item_enchant("minecraft:diamond_pickaxe", 6, 20, 30),
        item_enchant("minecraft:diamond_axe", 5, 20, 30),
        item_enchant("minecraft:diamond_shovel", 5, 20, 30),
        item_enchant("minecraft:diamond_hoe", 4, 15, 25),
        item_simple("minecraft:recovery_compass", 3),         # Ancient city
        item_simple("minecraft:spyglass", 8),
        item_count("minecraft:name_tag", 8, 1, 2),
        item_count("minecraft:lead", 8, 1, 2),
        item_simple("minecraft:brush", 6),
        item_simple("minecraft:clock", 6),
        item_enchant_random(2, "veinminer_enchantment:veinminer"), # VeinMiner
        # Запечатанные реликвии GanjaCraftCore
        item_sealed_relic(
            "minecraft:netherite_pickaxe", "soulcatcher_pickaxe", "sealed_soulcatcher_pickaxe", 7701,
            "★ Запечатанный Шуруповёрт 'Макита'",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Украден со стройки элитного ЖК, так и не донесён до скупщика.",
                "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                " ",
                "§e✦ Свойство: §fСкручивает спавнеры монстров в инвентарь",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:efficiency": 6, "minecraft:unbreaking": 5}
        ),
        item_sealed_relic(
            "minecraft:netherite_pickaxe", "autosmelt_pickaxe", "sealed_autosmelt_pickaxe", 7726,
            "★ Запечатанная Горелка-Автоплавилка",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Промышленный резак с высокотемпературным пламенем.",
                "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                " ",
                "§e✦ Свойство: §fМгновенная плавка руд прямо в забое",
                "§e✦ Бонус: §fУмножает выплавленные слитки с учётом Удачи IV",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:efficiency": 6, "minecraft:fortune": 4, "minecraft:unbreaking": 5}
        ),
        item_sealed_relic(
            "minecraft:netherite_pickaxe", "excavator_pickaxe", "sealed_excavator_pickaxe", 7728,
            "★ Запечатанный Шахтный Бур 3х3",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Тяжёлая буровая коронка с алмазным напылением.",
                "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                " ",
                "§e✦ Свойство: §fМгновенная проходка тоннелей 3х3 блока",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:efficiency": 6, "minecraft:unbreaking": 5}
        )
    ])

    # =========================================================================
    # 12. WEAPON1 (Этажи 1-3) - БЕЗ АЛМАЗОВ
    # =========================================================================
    write_table(output_dir, "weapon1.json", 2, 4, [
        item_enchant("minecraft:iron_sword", 12, 5, 15),
        item_enchant("minecraft:iron_axe", 8, 5, 15),
        item_enchant("minecraft:bow", 10, 5, 15),
        item_enchant("minecraft:crossbow", 8, 5, 15),
        item_simple("minecraft:shield", 10),
        item_enchant("minecraft:stone_sword", 6, 5, 10),
        item_count("minecraft:arrow", 16, 12, 24),
        item_count("minecraft:spectral_arrow", 8, 4, 10),
        item_potion("minecraft:tipped_arrow", 6, "minecraft:poison"),
        item_potion("minecraft:tipped_arrow", 6, "minecraft:weakness")
    ])

    # =========================================================================
    # 13. WEAPON2 (Этажи 4-5) - HEAVY CORE, MACE, РЕЛИКВИИ БОССОВ
    # =========================================================================
    write_table(output_dir, "weapon2.json", 2, 4, [
        item_enchant("minecraft:bow", 12, 20, 30),
        item_enchant("minecraft:crossbow", 12, 20, 30),
        item_count("minecraft:spectral_arrow", 12, 8, 16),
        item_count("minecraft:wind_charge", 10, 4, 8),
        item_potion("minecraft:tipped_arrow", 8, "minecraft:strong_healing"),
        item_potion("minecraft:tipped_arrow", 8, "minecraft:long_slowness"),
        item_enchant("minecraft:shield", 8, 15, 25),
        item_enchant("minecraft:diamond_sword", 5, 20, 30),
        item_enchant("minecraft:trident", 2, 15, 25),
        item_count("minecraft:breeze_rod", 3, 1, 2),
        item_enchant("minecraft:mace", 2, 20, 30),           # 26.3 Булава с чарами
        item_count("minecraft:heavy_core", 1, 1, 1),         # 26.3 Тяжелое ядро (джекпот!)
        # Запечатанные реликвии GanjaCraftCore
        item_sealed_relic(
            "minecraft:netherite_sword", "executioner_sword", "sealed_executioner_blade", 7702,
            "★ Запечатанная Бандитская Заточка",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Выкована из рессоры грузовика в подпольном гараже.",
                "§8Кровавая гравировка: невозможно изменить на наковальне.",
                " ",
                "§c✦ Свойство: §fУбойная сила и повышенный отжим лута",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:sharpness": 6, "minecraft:looting": 4, "minecraft:unbreaking": 5}
        ),
        item_sealed_relic(
            "minecraft:mace", "demolition_mace", "sealed_demolition_mace", 7708,
            "★ Запечатанный Отбойный Молот Сноса",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Инструмент бригады сноса аварийных многоэтажек.",
                "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                " ",
                "§e✦ Свойство: §fУдар с прыжка раскидывает врагов волной ветра",
                "§e✦ Спецэффект: §fОглушение, слабость и замедление в радиусе 5 блоков",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:unbreaking": 5, "minecraft:density": 5, "minecraft:breach": 4}
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
                "§d★ Легендарный Ломбардный Хабар"
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
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:unbreaking": 5}
        )
    ])

    # =========================================================================
    # 14. ARMOR1 (Этажи 1-3) - КОЛЬЧУГА, ЖЕЛЕЗО, НАЧАЛЬНЫЕ ШАБЛОНЫ ОТДЕЛКИ
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
        item_enchant("minecraft:golden_boots", 6, 10, 20),
        # Начальные шаблоны отделки брони
        item_count("minecraft:sentry_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:dune_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:coast_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:wild_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:wayfinder_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:raiser_armor_trim_smithing_template", 2, 1, 1)
    ])

    # =========================================================================
    # 15. ARMOR2 (Этажи 4-5) - АЛМАЗКА, ПОЛНЫЙ НАБОР 18 ТРИМОВ, РЕЛИКВИИ
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
        # ПОЛНЫЙ НАБОР 18 ШАБЛОНОВ ОТДЕЛКИ (TRIMS)
        item_count("minecraft:sentry_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:dune_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:coast_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:wild_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:wayfinder_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:raiser_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:shaper_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:host_armor_trim_smithing_template", 2, 1, 1),
        item_count("minecraft:vex_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:eye_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:ward_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:rib_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:spire_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:snout_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:tide_armor_trim_smithing_template", 1, 1, 1),
        item_count("minecraft:flow_armor_trim_smithing_template", 1, 1, 1),    # 26.3
        item_count("minecraft:bolt_armor_trim_smithing_template", 1, 1, 1),    # 26.3
        item_count("minecraft:silence_armor_trim_smithing_template", 1, 1, 1), # Джекпот
        item_count("minecraft:netherite_upgrade_smithing_template", 1, 1, 1),  # Незерит
        # Узоры флагов
        item_simple("minecraft:flow_banner_pattern", 1),
        item_simple("minecraft:guster_banner_pattern", 1),
        item_simple("minecraft:piglin_banner_pattern", 1),
        # Запечатанные реликвии GanjaCraftCore (Броня)
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
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:protection": 5, "minecraft:unbreaking": 5, "minecraft:respiration": 3}
        ),
        item_sealed_relic(
            "minecraft:netherite_chestplate", "collector_vest", "sealed_collector_vest", 7718,
            "★ Запечатанный Инкассаторский Жилет",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Бронежилет высшего класса защиты с титановыми пластинами.",
                "§8Заводская пломба на месте: невозможно изменить на наковальне.",
                " ",
                "§a✦ Свойство: §fКолоссальная броня (+10) и анти-отдача",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:protection": 5, "minecraft:unbreaking": 5}
        ),
        item_sealed_relic(
            "minecraft:netherite_leggings", "abibas_pants", "sealed_abibas_pants", 7720,
            "★ Запечатанные Штаны 'Абибас Три Полоски'",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Оригинальный винтажный костюм в идеальном сохране.",
                "§8Шелкография 90-х: невозможно изменить на наковальне.",
                " ",
                "§a✦ Свойство: §fБег в горку без прыжков (+0.5 блока шага)",
                "§a✦ Второе дыхание: §fПри HP < 30% даёт Спешку II и Скорость III",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:protection": 5, "minecraft:unbreaking": 5}
        ),
        item_sealed_relic(
            "minecraft:netherite_boots", "roofer_sneakers", "sealed_roofer_sneakers", 7722,
            "★ Запечатанные Грави-Кроссы Контрабандиста",
            [
                "§5§l✦ ЗАПЕЧАТАННЫЙ ЛОМБАРДНЫЙ КУШ",
                "§7Экспериментальная обувь на магнитной воздушной подушке.",
                "§8Герметичная прошивка: невозможно изменить на наковальне.",
                " ",
                "§b✦ Свойство: §fНулевой урон от падений с любой высоты",
                "§b✦ Мобильность: §fСвободный бег в воде и по рыхлому снегу",
                "§d★ Легендарный Ломбардный Хабар"
            ],
            {"minecraft:feather_falling": 5, "minecraft:depth_strider": 3, "minecraft:unbreaking": 5}
        )
    ])

    # =========================================================================
    # 16. BREWING (Спецкомнаты) - АЛХИМИЯ 26.3 И ОМНИ-БУТЫЛКИ
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
        item_count("minecraft:dragon_breath", 3, 1, 2),
        # Стандартные зелья
        item_potion("minecraft:potion", 8, "minecraft:strong_healing"),
        item_potion("minecraft:potion", 8, "minecraft:long_regeneration"),
        item_potion("minecraft:potion", 8, "minecraft:long_fire_resistance"),
        item_potion("minecraft:potion", 8, "minecraft:strong_strength"),
        item_potion("minecraft:potion", 8, "minecraft:long_speed"),
        item_potion("minecraft:potion", 6, "minecraft:long_night_vision"),
        item_potion("minecraft:potion", 4, "minecraft:long_turtle_master"),
        # Новые зелья 26.3
        item_potion("minecraft:potion", 4, "minecraft:weaving"),
        item_potion("minecraft:potion", 4, "minecraft:wind_charged"),
        item_potion("minecraft:potion", 4, "minecraft:oozing"),
        item_potion("minecraft:potion", 4, "minecraft:infested"),
        # Взрывные зелья
        item_potion("minecraft:splash_potion", 6, "minecraft:strong_healing"),
        item_potion("minecraft:splash_potion", 5, "minecraft:long_slowness"),
        item_potion("minecraft:splash_potion", 5, "minecraft:long_weakness"),
        item_ominous_bottle(4, 1, 4) # 26.3 Зловещие флаконы
    ])

    # =========================================================================
    # 17. MUSIC (Спецкомнаты) - ПОЛНЫЙ НАБОР ПЛАСТИНОК И РЕЛИКВИЙ ГЛУБИН
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
        item_simple("minecraft:music_disc_5", 2),
        item_count("minecraft:disc_fragment_5", 4, 1, 3),   # Осколки диска 5
        item_simple("minecraft:music_disc_relic", 2),
        item_simple("minecraft:music_disc_creator", 2),     # 26.3 Lena Raine
        item_simple("minecraft:music_disc_precipice", 2),   # 26.3 Aaron Cherof
        item_goat_horn(8),                                  # Козьи рога
        item_count("minecraft:echo_shard", 5, 1, 2),
        item_count("minecraft:amethyst_shard", 8, 3, 8),
        item_count("minecraft:nautilus_shell", 4, 1, 1),
        item_count("minecraft:heart_of_the_sea", 1, 1, 1)   # Сердце моря
    ])

    print("\nSuccessfully generated all 17 expanded loot tables!")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    generate_all(out)
