from uvicorn import Config, Server  # type: ignore
from core.bot import Bot
from core.live_telegram_api import make_live_telegram_api
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse
from fastapi import FastAPI, HTTPException
from trivia.telegram_models import Update
import asyncio
import os
from core.live_redis_api import make_live_redis_api, DoNothingRedisApi, LockChatException
from trivia.bot_config import BotConfig
import json
import logging
from pathlib import Path


async def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-config", type=str, required=True, help="Путь к json файлу с настройками")
    parser.add_argument("-server_url", help="Адрес сервера для регистрации в телеграм")
    parser.add_argument("-log_path", help="Путь к логу для бота")
    args = parser.parse_args()

    with open(args.config) as json_file:
        config_json = json.load(json_file)
        config = BotConfig.parse_obj(config_json)

        if config.log_path:
            log_path = Path(config.log_path)
            if not log_path.exists():
                log_path.mkdir()

        elif args.log_path:
            log_path = Path(args.log_path)
            if not log_path.exists():
                log_path.mkdir()

            logging.basicConfig(filename=f"{log_path}/trivia_bot.log",
                                format='%(asctime)s - %(message)s',
                                datefmt='%d-%b-%y %H:%M:%S',
                                level=logging.INFO
                                )
        else:
            logging.basicConfig(format='%(asctime)s - %(message)s',
                                datefmt='%d-%b-%y %H:%M:%S',
                                level=logging.INFO
                                )

        logging.info("Starting bot")

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
                        try:
                            await bot.process_update(update)
                        except Exception as ex:
                            logging.info(ex)
            else:
                with make_live_redis_api(config.redis) as redis_api:
                    bot = Bot(telegram_api, redis_api, lambda: GreetingState(state_factory),
                              bot_state_to_dict_bijection)

                    app = FastAPI()
                    if args.server_url:
                        await telegram_api.set_webhook(args.server_url)
                    else:
                        await telegram_api.set_webhook(str(config.server.url))

                @app.post("/")
                async def on_update(update: Update):
                    try:
                        await bot.process_update(update)

                    except LockChatException as exlc:
                        raise HTTPException(status_code=505, detail="Bad Gatawey")

                    except Exception as ex:
                        logging.info(ex)
                        raise HTTPException(status_code=500, detail="Something went wrong")

                config = Config(app=app,
                                host=int(config.server.host),
                                port=config.server.port,
                                loop=asyncio.get_running_loop()
                                )
                server = Server(config)
                await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
