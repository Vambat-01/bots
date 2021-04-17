from uvicorn import Config, Server  # type: ignore
from core.bot import Bot
from core.live_telegram_api import LiveTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse
from fastapi import FastAPI
import uvicorn    # type: ignore
from trivia.telegram_models import Update
import asyncio


async def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-file", type=str, required=True, help="Путь к json  файлу с вопросами для бота")
    parser.add_argument("-token", type=str, required=True, help="Телеграм токен бота")
    parser.add_argument("-server", dest="server", action="store_true", help="Бот запускается, как сервер")
    parser.add_argument("-server_url", help="Адрес сервера для регистрации в Telegram")
    parser.set_defaults(server=False)
    args = parser.parse_args()

    last_update_id = 0
    storage = JsonQuestionStorage(args.file)
    random = RandomImpl()
    state_factory = BotStateFactory(storage, random)
    telegram_api = LiveTelegramApi(args.token)
    bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
    bot = Bot(telegram_api, lambda: GreetingState(state_factory), bot_state_to_dict_bijection)

    if not args.server:

        await telegram_api.delete_webhook(True)

        while True:
            update_response = telegram_api.get_updates(last_update_id + 1)
            upd_resp = await update_response
            result = upd_resp.result
            for update in result:
                last_update_id = update.update_id
                await bot.process_update(update)
    else:
        app = FastAPI()
        await telegram_api.set_webhook(str(args.server_url))

        @app.post("/")
        async def on_update(update: Update):
            await bot.process_update(update)

        config = Config(app=app, host="127.0.0.1", port=8000, loop=asyncio.get_running_loop())
        server = Server(config)
        await server.serve()
        uvicorn.run(app, host="127.0.0.1", port=8000, loop=asyncio.get_event_loop())


if __name__ == "__main__":
    asyncio.run(main())
