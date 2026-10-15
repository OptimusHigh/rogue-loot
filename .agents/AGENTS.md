# Rogue Loot (Fabric 26.3) — Project Rules & Architecture

## ⚠️ ВЕРСИЯ MINECRAFT: 26.3 (НЕ ОПЕЧАТКА!)

* **Критическое правило для AI:** Проект работает строго на **Minecraft 26.3** (Fabric Loader 0.19.5, Java 25).
* **Это НЕ опечатка 1.20.x, 1.21.x или 1.26.x!** В проекте используется официальная ветка нумерации `26.3`.
* **Запрещено** «исправлять» 26.3 на 1.20/1.21/1.26 в диалогах, документации, коде, конфигах и датапаках.
* Все стандарты сериализации (датапаки, рецепты, компоненты DataComponents, формат Registry) должны строго соответствовать спецификации **26.3** (`pack_format: 48`, DataComponents вместо NBT, современные идентификаторы 26.3).

---

## 🏗️ Архитектура и интеграция

* **Мод:** `roguelike-dungeons-fabric-2.1.2+mc26.3.jar`
* **Назначение:** Полный оверрайд лут-таблиц подземелий `roguelike:chests/*`.
* **Конфиг сервера:** `config/roguelike-dungeons.json` (`"roguelike_loot": false`). При таком значении мод генерирует сундуки с ванильными таблицами лута `data/roguelike/loot_table/chests/*.json`.
* **Система персонального лута:** `slashloot` — перехватывает открытие сундука и генерирует лут индивидуально для каждого игрока на основе этих таблиц.
* **Синхронизация:**
  - Датапак сервера: `d:\GanjaCraft\ganj4craft-vanilla\world\datapacks\roguelike_loot`
  - Ресурсы ядра (фолбэк): `d:\GanjaCraft\ganj4core\src\main\resources\data\roguelike`

---

## 📦 17 Таблиц Лута

| Категория | Этажи 0 (Starter) | Этажи 1-3 (Tier 1) | Этажи 4-5 (Tier 2 / Deep) | Спецкомнаты |
|---|---|---|---|---|
| **Starter** | `starter.json` | — | — | — |
| **Руды / Металлы** | — | `ore1.json` | `ore2.json` | — |
| **Блоки / Декор** | — | `block1.json` | `block2.json` | — |
| **Еда / Припасы** | — | `food1.json` | `food2.json` | — |
| **Расходники** | — | `supply1.json` | `supply2.json` | — |
| **Инструменты** | — | `tool1.json` | `tool2.json` | — |
| **Оружие** | — | `weapon1.json` | `weapon2.json` | — |
| **Броня** | — | `armor1.json` | `armor2.json` | — |
| **Зельеварение** | — | — | — | `brewing.json` |
| **Музыка / Реликвии** | — | — | — | `music.json` |

---

## 🛠️ Скрипты автоматизации

- `python scripts/generate_loot.py` — генерация / пересборка всех JSON-таблиц с валидацией баланса.
- `python scripts/deploy.py` — деплой в мир сервера `ganj4craft-vanilla` и в `ganj4core`.
- `python scripts/validate_loot.py` — проверка целостности JSON, весов, функций и DataComponents.
