from typing import List, Any
from core.button import Button


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
