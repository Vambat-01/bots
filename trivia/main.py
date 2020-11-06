from trivia.bot import Bot, RealTelegramApi
from trivia.bot_state import BotStateFactory, GreetingState, TestState
from trivia.question_storage import JsonQuestionStorage

token = "1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs"
json_file = "resources/questions_for_bot.json"
storage = JsonQuestionStorage(json_file)
state_factory = BotStateFactory(storage)
state = GreetingState(state_factory)
test_state = TestState()
telegram_api = RealTelegramApi(token)
bot = Bot(telegram_api, state)

while True:
    bot.process_updates()



