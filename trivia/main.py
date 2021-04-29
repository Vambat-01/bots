from uvicorn import Config, Server  # type: ignore
from core.bot import Bot
from core.live_telegram_api import make_live_telegram_api
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse
from fastapi import FastAPI
from trivia.telegram_models import Update
import asyncio
from core.utils import log
import os
from core.live_redis_api import make_live_redis_api, FakeRedisApi
from trivia.start_bot_model import StartBot
import json


async def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-start_file", type=str, required=True, help="Путь к json файлу для запуска бота")
    args = parser.parse_args()

    with open(args.start_file) as json_file:
        start_bot = json.load(json_file)
        start = StartBot.parse_obj(start_bot)

        token = os.environ["BOT_TOKEN"]
        last_update_id = 0
        storage = JsonQuestionStorage(start.file)
        random = RandomImpl()
        state_factory = BotStateFactory(storage, random)
        bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
        async with make_live_telegram_api(token) as telegram_api:
            if not start.server:
                bot = Bot(telegram_api,
                          FakeRedisApi(),
                          lambda: GreetingState(state_factory),
                          bot_state_to_dict_bijection
                          )
                await telegram_api.delete_webhook(True)
                while True:
                    update_response = await telegram_api.get_updates(last_update_id + 1)
                    upd_resp = update_response
                    result = upd_resp.result
                    for update in result:
                        last_update_id = update.update_id
                        await bot.process_update(update)
            else:
                with make_live_redis_api(start.redis_host, start.redis_port, start.redis_db) as redis_api:
                    bot = Bot(telegram_api, redis_api, lambda: GreetingState(state_factory),
                              bot_state_to_dict_bijection)
                    app = FastAPI()
                    await telegram_api.set_webhook(str(start.server_url))

                @app.post("/")
                async def on_update(update: Update):
                    await bot.process_update(update)

                config = Config(app=app,
                                host=int(start.server_host),
                                port=start.server_port,
                                loop=asyncio.get_running_loop()
                                )
                server = Server(config)
                await server.serve()


if __name__ == "__main__":
    log("Starting bot")
    asyncio.run(main())
