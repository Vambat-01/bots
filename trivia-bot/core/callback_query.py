from dataclasses import dataclass
from core.message import Message


@dataclass
class CallbackQuery:
    """
        Входящий запрос обратного вызова. Когда пользователю отправляется сообщение с прикрепленной встроенной
        клавиатурой, как только пользователь нажимает кнопку на клавиатуре, мы получаем CallbackQuery обновление.
        Telegram Api documentation ( https://core.telegram.org/bots/api/#callbackquery ).
        data: Данные связанные с кнопкой обратного вызова
        message: сообщение с кнопкой, которая инициировала callback query
        message_id: идентификатор сообщения для редактирования
    """
    data: str
    message: Message
    message_id: int
