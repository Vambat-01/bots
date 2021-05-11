from uvicorn import Config, Server  # type: ignore
from core.bot import Bot
from core.live_telegram_api import make_live_telegram_api
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse
from fastapi import FastAPI, Request
from trivia.telegram_models import Update
import asyncio
import os
from core.live_redis_api import make_live_redis_api, DoNothingRedisApi, LockChatException
from trivia.bot_config import BotConfig
import json
import logging
from pathlib import Path
from typing import Any, Optional
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from core.bot import BotException


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
                await run_server(config, telegram_api, state_factory, bot_state_to_dict_bijection, args.server_url)
            elif config.is_client:
                await run_client(telegram_api, state_factory, bot_state_to_dict_bijection, last_update_id)


async def run_server(config: BotConfig,
                     telegram_api: Any,
                     state_factory: BotStateFactory,
                     bot_state_to_dict_bijection: BotStateToDictBijection,
                     arg_server: Optional[str]):
    with make_live_redis_api(config.redis) as redis_api:
        bot = Bot(telegram_api, redis_api, lambda: GreetingState(state_factory),
                  bot_state_to_dict_bijection)

        app = FastAPI()
        if arg_server:
            server_url = arg_server
        elif os.environ["SERVER_URL"]:
            server_url = os.environ["SERVER_URL"]
        else:
            server_url = str(config.server.url)

        await telegram_api.set_webhook(server_url)

        @app.exception_handler(BotException)
        async def bot_exception(request, ext):
            print("ЗАШЕЛ в BotException")
            logging.exception(ext)
            return PlainTextResponse(str(ext), status_code=400)

        @app.exception_handler(LockChatException)
        async def lock_chat_exception(request, ex):
            print("ЗАШЕЛ в LockChatException")
            logging.exception(ex)
            return PlainTextResponse(str(ex), status_code=502)

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request, exc):
            print("ЗАШЕЛ в RequestValidationError")
            logging.exception(exc)
            return PlainTextResponse(str(exc), status_code=400)

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

        @app.post("/test")
        async def on_update_test(request: Request):
            json_body = await request.json()
            print(json_body)


async def run_client(telegram_api: Any,
                     state_factory: BotStateFactory,
                     bot_state_to_dict_bijection: BotStateToDictBijection,
                     last_update_id: int):
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
            except Exception:
                logging.exception("Failed to process update")


def get_log_filename(directory: str) -> str:
    log_path = Path(directory)
    if not log_path.exists():
        log_path.mkdir()
    return f"{log_path}/trivia_bot.log"


if __name__ == "__main__":
    asyncio.run(main())
