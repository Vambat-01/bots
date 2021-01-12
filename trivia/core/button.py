from typing import Dict


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
