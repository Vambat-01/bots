from core.bot import Bot
from core.live_telegram_api import LiveTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState, TestState
from trivia.question_storage import JsonQuestionStorage
from core.random import RandomImpl

token = "1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs"
json_file = "resources/questions_for_bot.json"
storage = JsonQuestionStorage(json_file)
random = RandomImpl()
state_factory = BotStateFactory(storage, random)
state = GreetingState(state_factory)
test_state = TestState()
telegram_api = LiveTelegramApi(token)
bot = Bot(telegram_api, lambda: GreetingState(state_factory))

while True:
    bot.process_updates()
