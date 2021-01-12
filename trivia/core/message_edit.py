from typing import Optional
from dataclasses import dataclass


@dataclass
class MessageEdit:
    """
        Обновление сообщений. Позволяет изменить существующее сообщение в истории сообщений, вместо отправки нового
        сообщения. Это наиболее удобно для сообщений со втроенной клавиатурой, это помогает уменьшить бесопрядок в чате.
        Telegram Api documentation ( https://core.telegram.org/bots/api#editmessagetext )
        chat_id: идентификатор чата
        message_id: идентификатор сообщения для редактирования
        text: новый текст редактируемого сообщения
        parse_mode: режим форматирования текста сообщения
    """
    chat_id: int
    message_id: int
    text: str
    parse_mode: Optional[str] = None
