# Учебный 'trivia bot' на подобие игры "Кто хочет стать миллионером?", для применения полученных знаний на практике
## Запуск бота локально

1. Если у вас запущен бот на `aws-машине` остановите его
1. У вас должен быть `json` файл с вопросами.  Пример файла, можно найти перейдя `bots` -> `trivia-bot` -> `resources` -> `bot_questions_mini.json`
1. Перейдите в репозитории по пути `bots` -> `trivia-bot`-> `resources` в `json` файл `config_client_local.json`. Поменяйте там значения
    1. `questions_filepath` - указываете путь к вашему `json` файлу с вопросами
    1. `game_config` - указываете сколько в игре будет легких, средних и сложных вопросов
1. При запуске файла `mail.py` выставите `Environment variables` (пример `BOT_TOKEN=<telegram token>)`)
    1. Еще один способ ввести токен, перейдите в репозиторий бота `bots` -> `trivia-bot`
		1. Есть файл `bot-sample.env`
			1. Выполните команду `cp bot-sample.env bot.env`
			1. Заполните `bot.env`

1. Перейдите в терминале в репозитории по пути `bots` -> `trivia-bot`. Выполните команду `"python", "./main.py", "-config", "resources/config_client_local.json"`