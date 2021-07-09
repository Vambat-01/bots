from typing import Optional
from core.keyboard import Keyboard


class Message:
    """
        Телеграм сообщение
    """

    def __init__(self, chat_id: int, text: str, parse_mode: Optional[str] = None, keyboard: Optional[Keyboard] = None):
        """
        :param chat_id: идентификатор чата
        :param text: текст сообщения
        :param parse_mode: режим форматирования текста сообщения
        :param keyboard: опциональная встроенная клавиатура, которая будет отображаться пользователю
        """
        self.chat_id = chat_id
        self.text = text
        self.parse_mode = parse_mode
        self.keyboard = keyboard

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return f"""
                    Message:
                    text: {self.text}
                    chat_id: {self.chat_id}
                    parse_mode: {self.parse_mode} 
                    keyboard: {self.keyboard}
                 """

    def __str__(self):
        return self.__repr__()
