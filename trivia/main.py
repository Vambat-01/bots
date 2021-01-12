from core.bot import Bot
from core.real_telegram_api import RealTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState, TestState
from trivia.question_storage import JsonQuestionStorage
from trivia.random_utils import RandomImpl

token = "1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs"
json_file = "resources/questions_for_bot.json"
storage = JsonQuestionStorage(json_file)
random = RandomImpl()
state_factory = BotStateFactory(storage, random)
state = GreetingState(state_factory)
test_state = TestState()
telegram_api = RealTelegramApi(token)
bot = Bot(telegram_api, lambda: GreetingState(state_factory))

while True:
    bot.process_updates()



