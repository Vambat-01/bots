from trivia.bot import Bot

token = "1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs"
bot = Bot(token)

while True:
    bot.process_updates()