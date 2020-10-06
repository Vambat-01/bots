import requests
import datetime


def log(message: str) -> None:
    """
        Выводит текущее время и сообщение
    :param message: полученное сообщение
    :return: None
    """
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")


class Bot:
    def __init__(self, token: str):
        self.token = token
        self.last_update_id = 0

    def process_updates(self) -> None:
        """
            Получает входящее обновление
        :return: None
        """
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        offset = self.last_update_id + 1
        log(f"Listen to telegram. offset: {offset}")
        response = requests.get(url, params={
            "offset": offset,
            "timeout": 10
        })
        data = response.json()
        result = data["result"]
        for update in result:
            chat_id = update["message"]["chat"]["id"]
            message_text = update["message"]["text"]
            log(f"chat_id : {chat_id}. text: {message_text} ")
            self.last_update_id = update["update_id"]
            self.send_message(chat_id, f"I got message: {message_text}")

    def send_message(self, chat_id: int, text: str ) -> None:
        """
            Отправляет текстовое сообщение
        :param chat_id: идентификатор чата
        :param text: текст сообщения
        :return:None
        """
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        response = requests.get(url, params={
            "text": text,
            "chat_id": chat_id
        })
        log(f"Send message status code: {response.status_code} ")


token = "1162468954:AAEk6dzuhBqfgRm0WO_3QRbZWe0WnYv0_Qs"
bot = Bot(token)

while True:
    bot.process_updates()
