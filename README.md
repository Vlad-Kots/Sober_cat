# Sober Bot 🐈

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.7-5865F2?logo=discord&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-in%20development-yellow)

Discord бот на Python (discord.py), написаний як навчальний pet-проект.

## Функціонал

### Система рівнів (XP)
Бот нараховує досвід за активність у чаті (з кулдауном, щоб уникнути спаму) і відстежує прогрес учасників.

| Команда | Опис |
|---|---|
| `!rank [@user]` | Показує рівень і XP (свій або вказаного користувача) |
| `!leaderboard` | Топ-10 учасників сервера за XP |

## Технології

- **Python 3.14**
- **discord.py 2.7** — основна бібліотека для взаємодії з Discord API
- **python-dotenv** — безпечне зберігання токена бота
- **JSON** — легковаге сховище даних (рівні/XP)

## Структура проекту
discord-bot/
├── main.py # точка входу, автозавантаження cogs
├── cogs/
│ ├── leveling.py # система рівнів і XP
│ └── responder.py # автовідповіді бота
├── data/ # JSON-сховище (генерується автоматично)
└── .env # токен бота (не в репозиторії)


## Запуск локально

1. Клонуй репозиторій і встанови залежності:
```bash
pip install discord.py python-dotenv deep-translator
```

2. Створи `.env` файл у корені проекту:

DISCORD_TOKEN=твій_токен_бота


3. Увімкни на [Discord Developer Portal](https://discord.com/developers/applications) для свого бота:
   - Message Content Intent
   - Server Members Intent

4. Запусти:
```bash
python main.py
```

## Плани на майбутнє

- Модерація (кік/бан/очищення повідомлень)
- Перекладач повідомлень за реакцією
- Система привітання нових учасників