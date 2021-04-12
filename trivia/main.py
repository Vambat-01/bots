from core.bot import Bot
from core.live_telegram_api import LiveTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse
from fastapi import FastAPI
import uvicorn
from trivia.telegram_models import Update

# app = FastAPI()


def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-file",  type=str, help="Путь к json  файлу с вопросами для бота")
    parser.add_argument("-token", type=str, help="Телеграм токен бота")
    parser.add_argument("-tel", type=str, help="Как запустить бота сервер(server) или клиент")
    args = parser.parse_args()

    last_update_id: int = 0
    storage = JsonQuestionStorage(args.file)
    random = RandomImpl()
    state_factory = BotStateFactory(storage, random)
    telegram_api = LiveTelegramApi(args.token)
    bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
    bot = Bot(telegram_api, lambda: GreetingState(state_factory), bot_state_to_dict_bijection)

    while True:
        update_response = telegram_api.get_updates(last_update_id + 1)
        if update_response:
            result = update_response.result
            for update in result:
                last_update_id = update.update_id
                bot.process_updates(update)

    # if args.tel == "server":
    #     @app.post("/")
    #     async def on_update(update: Update):
    #         bot.process_updates(update)

    # else:
    #     while True:
    #         update_response = telegram_api.get_updates(last_update_id + 1)
    #         update = update_response.result
    #         last_update_id = update.update_id
    #         bot.process_updates(update)


if __name__ == "__main__":
    main()



# def main():
#     parser = argparse.ArgumentParser(description="Запуск бота")
#     parser.add_argument("-file",  type=str, help="Путь к json  файлу с вопросами для бота")
#     parser.add_argument("-token", type=str, help="Телеграм токен бота")
#     args = parser.parse_args()
#
#     storage = JsonQuestionStorage(args.file)
#     random = RandomImpl()
#     state_factory = BotStateFactory(storage, random)
#     telegram_api = LiveTelegramApi(args.token)
#     bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
#     bot = Bot(telegram_api, lambda: GreetingState(state_factory), bot_state_to_dict_bijection)
#
#     while True:
#         bot.process_updates()
#
#
# if __name__ == "__main__":
#     main()
