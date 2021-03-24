from core.bot import Bot
from core.live_telegram_api import LiveTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState, TestState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl
from trivia.bijection import BotStateToDictBijection
import argparse

parser = argparse.ArgumentParser(description="Запуск бота")
parser.add_argument("-file",  type=str, help="Путь к файлу")
parser.add_argument("-token", type=str, help="Уникальный идентификационный номер")
args = parser.parse_args()


storage = JsonQuestionStorage(args.file)
random = RandomImpl()
state_factory = BotStateFactory(storage, random)
state = GreetingState(state_factory)
test_state = TestState()
telegram_api = LiveTelegramApi(args.token)
bot_state_to_dict_bijection = BotStateToDictBijection(state_factory)
bot = Bot(telegram_api, lambda: GreetingState(state_factory), bot_state_to_dict_bijection)

while True:
    bot.process_updates()
