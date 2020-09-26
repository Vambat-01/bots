import requests

import datetime


def log(message):
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")

class Bot:
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0

    def receive_update(self):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        offset = self.last_update_id + 1
        log(f"Sending request. offset = {offset}")
        response= requests.get(url, params={
            "offset": offset,
            "timeout": 5
        })
        data = response.json()
        result = data["result"]
        for update in result:
            chat_id = update["message"]["chat"]["id"]
            text_message = update["message"]["text"]
            self.last_update_id = update["update_id"]
            self.send_message(chat_id, f"I got your message. Message: {text_message}")

    def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.get(url, params={
            "chat_id": chat_id,
            "text": text
        })


token = "1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs"
bot = Bot(token)

while True:
    bot.receive_update()

