# Учебный 'trivia bot' для применения полученных знаний на практике
## Запуск бота локально

1. У вас должен быть `json` файл с вопросами.  Пример файла, можно найти перейдя `bots` -> `trivia-bot` -> `resources` -> `bot_questions_mini.json`
1. Перейдите в репозитории по пути `bots` -> `trivia-bot`-> `resources` в `json` файл `config_client_local.json`. Поменяйте там значения.
    1. `questions_filepath` - указываете путь к вашему `json` файлу с вопросами.
    1. `game_config` - указываете сколько в игре будет легких, средних и сложных вопросов.
1. В файле `mail.py` заполняете
    1. Parameters `-config resources/config_client_local.json`
    1. Enviroment variables `BOT_TOKEN=<ваш телеграм токен>`

1. Запускаете бота (файл `mail.py`)