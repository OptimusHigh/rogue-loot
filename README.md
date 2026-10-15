# Rogue Loot (Minecraft 26.3) — GanjaCraft

Централизованный репозиторий разработки и балансировки кастомных лут-таблиц для мода **Roguelike Dungeons** на сервере **GanjaCraft Vanilla (Minecraft 26.3 / Fabric)**.

---

## 🧭 Архитектурный контекст

* **Minecraft 26.3** (`pack_format: 48`, DataComponents вместо NBT).
* **Мод подземелий:** `roguelike-dungeons-fabric-2.1.2+mc26.3.jar`
* **Конфигурация:** `config/roguelike-dungeons.json` (`"roguelike_loot": false`). Мод вместо жестко закодированных Java-таблиц обращается к стандартным `data/roguelike/loot_table/chests/*.json`.
* **Персональный лут:** `slashloot` — перехватывает открытие каждого контейнера и рассчитывает персональный лут для игрока без грифа и воровства.

---

## 📁 Структура проекта

```
rogue-loot/
├── .agents/
│   └── AGENTS.md                  # Правила проекта и спецификации 26.3
├── datapacks/
│   └── roguelike_loot/            # Датапак для сервера
│       ├── pack.mcmeta            # pack_format 48
│       └── data/roguelike/loot_table/chests/
│           ├── starter.json       # Башня / вход (уровень 0)
│           ├── ore1.json / ore2.json
│           ├── block1.json / block2.json
│           ├── food1.json / food2.json
│           ├── supply1.json / supply2.json
│           ├── tool1.json / tool2.json
│           ├── weapon1.json / weapon2.json
│           ├── armor1.json / armor2.json
│           ├── brewing.json       # Зельеварение (спецкомната)
│           └── music.json         # Музыка / реликвии (спецкомната)
├── scripts/
│   ├── generate_loot.py           # Программный генератор всех 17 таблиц
│   ├── deploy.py                  # Деплой в мир ganj4craft-vanilla и ganj4core
│   └── validate_loot.py           # Валидация JSON, весов и компонентов
├── EXPANSION_PLAN.md              # Подробный план расширения и синергии
└── README.md
```

---

## ⚡ Быстрый старт

### 1. Перегенерация таблиц
```bash
python scripts/generate_loot.py
```

### 2. Валидация
```bash
python scripts/validate_loot.py
```

### 3. Деплой на сервер
```bash
python scripts/deploy.py
```
*(Копирует датапак в `d:\GanjaCraft\ganj4craft-vanilla\world\datapacks\roguelike_loot` и ресурсы в `d:\GanjaCraft\ganj4core\src\main\resources\data\roguelike`)*.
