from uvicorn import Config, Server  # type: ignore
from core.bot import Bot
from core.live_telegram_api import make_live_telegram_api
from core.telegram_api import TelegramApi
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse
from fastapi import FastAPI, Request
from trivia.telegram_models import Update
import asyncio
import os
from core.live_redis_api import make_live_redis_api, DoNothingRedisApi, LockException
from trivia.bot_config import BotConfig
import json
import logging
from pathlib import Path
from typing import Any, Optional
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from core.bot import BotException
from core.chat_state_storage import DictChatStateStorage, RedisChatStateStorage


async def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-config", type=str, required=True, help="Путь к json файлу с настройками")
    parser.add_argument("-server_url", help="Адрес сервера для регистрации в телеграм")
    parser.add_argument("-out_path", help="Директория для сохранения вывода")
    args = parser.parse_args()

    with open(args.config) as json_file:
        config_json = json.load(json_file)
        config = BotConfig.parse_obj(config_json)

        if args.out_path:
            file_name = get_log_filename(args.out_path)
        elif config.out_path:
            file_name = get_log_filename(config.out_path)
        else:
            file_name = None

        logging.basicConfig(filename=file_name,
                            format='%(asctime)s - %(message)s',
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
            if config.is_server:
                await run_server(config,
                                 telegram_api,
                                 state_factory,
                                 bot_state_to_dict_bijection,
                                 args.server_url
                                 )
            else:
                await run_client(telegram_api,
                                 state_factory,
                                 bot_state_to_dict_bijection,
                                 last_update_id
                                 )


async def run_server(config: BotConfig,
                     telegram_api: TelegramApi,
                     state_factory: BotStateFactory,
                     bot_state_to_dict_bijection: BotStateToDictBijection,
                     server_url: Optional[str]
                     ):
    with make_live_redis_api(config.redis) as redis_api:
        chat_state_storage = RedisChatStateStorage(redis_api, bot_state_to_dict_bijection)
        bot = Bot(telegram_api,
                  redis_api,
                  lambda: GreetingState(state_factory),
                  bot_state_to_dict_bijection,
                  chat_state_storage
                  )

        server_url = next(filter(None, [server_url, os.environ["SERVER_URL"], config.server.url]))
        await telegram_api.set_webhook(server_url)

        app = FastAPI()

        @app.exception_handler(BotException)
        async def on_bot_exception(request: Request, exception: BotException):
            logging.exception(exception)
            return PlainTextResponse(str(exception), status_code=400)

        @app.exception_handler(LockException)
        async def on_lock_chat_exception(request: Request, exception: LockException):
            logging.exception(exception)
            return PlainTextResponse(str(exception), status_code=502)

        @app.exception_handler(RequestValidationError)
        async def on_invalid_request_exception(request: Request, exception: RequestValidationError):
            logging.exception(exception)
            return PlainTextResponse(str(exception), status_code=400)

        @app.post("/")
        async def on_update(update: Update):
            await bot.process_update(update)

        config = Config(app=app,
                        host=config.server.host,
                        port=config.server.port,
                        loop=asyncio.get_running_loop()
                        )
        server = Server(config)
        await server.serve()


async def run_client(telegram_api: Any,
                     state_factory: BotStateFactory,
                     bot_state_to_dict_bijection: BotStateToDictBijection,
                     last_update_id: int
                     ):
    chat_state_storage = DictChatStateStorage()
    bot = Bot(telegram_api,
              DoNothingRedisApi(),
              lambda: GreetingState(state_factory),
              bot_state_to_dict_bijection,
              chat_state_storage
              )
    await telegram_api.delete_webhook(True)
    while True:
        update_response = await telegram_api.get_updates(last_update_id + 1)
        result = update_response.result
        for update in result:
            last_update_id = update.update_id
            try:
                await bot.process_update(update)
            except Exception:
                logging.exception("Failed to process update")


def get_log_filename(directory: str) -> str:
    log_path = Path(directory)
    if not log_path.exists():
        log_path.mkdir()
    return f"{log_path}/trivia_bot.log"


if __name__ == "__main__":
    asyncio.run(main())
