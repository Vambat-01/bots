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
from core.live_redis_api import make_live_redis_api, DoNothingRedisApi
from trivia.bot_config import BotConfig, LiveRedisApiConfig
import json


async def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-config", type=str, required=True, help="Путь к json файлу с настройками")
    args = parser.parse_args()

    with open(args.config) as json_file:
        config_json = json.load(json_file)
        config = BotConfig.parse_obj(config_json)

        token = os.environ["BOT_TOKEN"]
        last_update_id = 0
        storage = JsonQuestionStorage(config.questions_filepath)
        random = RandomImpl()
        state_factory = BotStateFactory(storage, random)
        bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
        async with make_live_telegram_api(token) as telegram_api:
            if not config.is_server:
                bot = Bot(telegram_api,
                          DoNothingRedisApi(),
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
                with make_live_redis_api(config.redis) as redis_api:
                    bot = Bot(telegram_api, redis_api, lambda: GreetingState(state_factory),
                              bot_state_to_dict_bijection)
                    app = FastAPI()
                    await telegram_api.set_webhook(str(config.server.url))

                @app.post("/")
                async def on_update(update: Update):
                    await bot.process_update(update)

                config = Config(app=app,
                                host=int(config.server.host),
                                port=config.server.port,
                                loop=asyncio.get_running_loop()
                                )
                server = Server(config)
                await server.serve()


if __name__ == "__main__":
    log("Starting bot")
    asyncio.run(main())
