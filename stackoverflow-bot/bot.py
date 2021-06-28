import requests
import os
import datetime


def log(message):
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")


class Bot:
    def __init__(self, token):
        self.token = token
        self.last_update_id = 0

    def handle_updates(self):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        offset = self.last_update_id + 1
        log(f"Listening to telegram. offset = {offset}")
        response = requests.get(url, params={
            "offset": offset,
            "timeout": 5
        })
        data = response.json()
        result = data["result"]
        for update in result:
            chat_id = update["message"]["chat"]["id"]
            message_text = update["message"]["text"]
            log(f"chat_id : {chat_id}. text: {message_text} ")
            self.last_update_id = update["update_id"]
            self.send_message(chat_id, f"I got message: {message_text}")

    def send_message(self, chat_id, text):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.get(url, params={
            "text": text,
            "chat_id": chat_id
        })
        log(f"Send message status code: {response.status_code} ")


token = os.environ["MY_BOT_TOKEN"]
bot = Bot(token)

while True:
    bot.handle_updates()


