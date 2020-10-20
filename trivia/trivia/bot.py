import requests
import datetime
from trivia.bot_state import EchoState, Message, Command, BotState, GreetingState, BotStateFactory
from trivia.question_storage import JsonQuestionStorage
import os


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
        json_file = "resources/questions_for_bot.json"
        storage = JsonQuestionStorage(json_file)
        state_factory = BotStateFactory(storage)
        self.token = token
        self.last_update_id = 0
        self.state: BotState = GreetingState(state_factory)

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
            if message_text.startswith("/"):
                user_command = Command(chat_id, message_text)
                bot_response = self.state.process_command(user_command)
            else:
                user_message = Message(chat_id, message_text)
                bot_response = self.state.process_message(user_message)
            self.last_update_id = update["update_id"]
            self.send_message(bot_response.message.chat_id, bot_response.message.text)

            if bot_response.new_state is not None:
                new_state: BotState = bot_response.new_state
                self.state = new_state
                first_message = self.state.on_enter(chat_id)
                if first_message is not None:
                    self.send_message(first_message.chat_id, first_message.text)

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
            "chat_id": str(chat_id)
        })
        log(f"Send message status code: {response.status_code} ")



