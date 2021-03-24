from core.bot import Bot
from core.live_telegram_api import LiveTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse


def main():
    parser = argparse.ArgumentParser(description="Запуск бота")
    parser.add_argument("-file",  type=str, help="Путь к json  файлу с вопросами для бота")
    parser.add_argument("-token", type=str, help="Уникальный идентификационный номер телеграм токен бота")
    args = parser.parse_args()

    storage = JsonQuestionStorage(args.file)
    random = RandomImpl()
    state_factory = BotStateFactory(storage, random)
    telegram_api = LiveTelegramApi(args.token)
    bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
    bot = Bot(telegram_api, lambda: GreetingState(state_factory), bot_state_to_dict_bijection)

    while True:
        bot.process_updates()


if __name__ == "__main__":
    main()
