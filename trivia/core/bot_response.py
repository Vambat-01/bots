from core.message import Message
from core.message_edit import MessageEdit
from typing import Optional
from dataclasses import dataclass
from core.bot_state import BotState


@dataclass
class BotResponse:
    """
        Ответ бота
    """
    message: Optional[Message] = None
    message_edit: Optional[MessageEdit] = None
    new_state: Optional["BotState"] = None
