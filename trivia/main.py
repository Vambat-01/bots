from core.bot import Bot
from core.live_telegram_api import LiveTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse
from fastapi import FastAPI     # type: ignore
import uvicorn    # type: ignore
from trivia.telegram_models import Update


def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-file",  type=str, help="Путь к json  файлу с вопросами для бота")
    parser.add_argument("-token", type=str, help="Телеграм токен бота")
    parser.add_argument("-server", dest="server", action="store_true", help="Бота запускается, как сервер")
    parser.add_argument("-server_url", help="Адрес подключения сервека к Telegram")
    parser.set_defaults(server=False)
    args = parser.parse_args()

    last_update_id = 0
    storage = JsonQuestionStorage(args.file)
    random = RandomImpl()
    state_factory = BotStateFactory(storage, random)
    telegram_api = LiveTelegramApi(args.token)
    bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
    bot = Bot(telegram_api, lambda: GreetingState(state_factory), bot_state_to_dict_bijection)

    if args.server is False:

        telegram_api.delete_webhook(True)

        while True:
            update_response = telegram_api.get_updates(last_update_id + 1)

            result = update_response.result
            for update in result:
                last_update_id = update.update_id
                bot.process_updates(update)
    else:
        app = FastAPI()
        telegram_api.set_webhook(str(args.server_url))

        @app.post("/")
        async def on_update(update: Update):
            bot.process_updates(update)

        uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
