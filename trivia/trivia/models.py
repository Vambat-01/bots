from typing import List, Dict, Any
from typing import Optional
from dataclasses import dataclass


class Button:
    """
        Представляет собой одну кнопку встроенной клавиатуры.
        Telegram Api documentation ( https://core.telegram.org/bots/api#inlinekeyboardbutton ).
    """

    def __init__(self, text: str, callback_data: str):
        """
        :param text: текст, который отображается на кнопке
        :param callback_data: данные для отправки боту в ответном запроси при нажатии кнопки, 1-64 байта
        """
        self.text = text
        self.callback_data = callback_data

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return f"""
                    Button:
                    text: {self.text}
                    callback_data: {self.callback_data}

                """

    def as_json(self) -> Dict[str, str]:
        """
            Возвращает JSON представление кнопки для отправки в Telegram API
        :return: Dict[str, str]
        """
        return {
            "text": self.text,
            "callback_data": self.callback_data
        }


class Keyboard:
    """
        Встроенная клавиатура, которая появляется рядом с сообщением, которому она принадлежит и может быть добавлена к
        любому сообщению. Чтобы пользователь имел возможность воспользоваться кнопками для ответа, вместо печати.
        Telegram Api documentation ( https://core.telegram.org/bots/api#inlinekeyboardmarkup ).
    """
    def __init__(self, buttons: List[List[Button]]):
        """
        :param buttons: Двумерный массив
        """
        self.buttons = buttons

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"""
                    Keyboard:
                    buttons: {self.buttons}
                """

    def as_json(self) -> List[Any]:
        """
            Возаращает JSON представление клавиаутры для оптравки в Telegram API
        :return: List[Any]
        """
        result_row = []
        for row in self.buttons:
            array_row = []
            for button in row:
                array_row.append(button.as_json())
            result_row.append(array_row)
        return result_row


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


class Command:
    """
        Телеграм команда
    """

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False


@dataclass
class CallbackQuery:
    """
        Входящий запрос обратного вызова. Когда пользователю отправляется сообщение с прикрепленной встроенной
        клавиатурой, как только пользователь нажимает кнопку на клавиатуре, мы получаем CallbackQuery обновление.
        Telegram Api documentation ( https://core.telegram.org/bots/api/#callbackquery ).
        data: Данные связанные с кнопкой обратного вызова
    """
    data: str
    message: Message


@dataclass
class MessageEdit:
    """
       Обновление сообщений. Позволяет изменить существующее сообщение в истории сообщений, вместо отправки нового
       сообщения. Это наиболее удобно для сообщений со втроенной клавиатурой, это помогает уменьшить бесопрядок в чате.
       Telegram Api documentation ( https://core.telegram.org/bots/api#editmessagetext )
       chat_id: идентификатор чата
       message_id: идентификатор сообщения для редактирования
       text: новый текст редактируемого сообщения
    """
    chat_id: int
    message_id: int
    text: str

