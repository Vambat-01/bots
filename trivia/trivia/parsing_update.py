from dataclasses import dataclass, field
from typing import Optional, List
from dataclasses_json import dataclass_json, config, Undefined

"""
Входящее обновление из Telegram: Update documentation ( https://core.telegram.org/bots/api#getting-updates )
"""


@dataclass
class From:
    id: int
    is_bot: bool
    first_name: str
    username: str


@dataclass
class Chat:
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


@dataclass_json
@dataclass
class Message:
    message_id: int
    from_: From = field(metadata=config(field_name="from"))
    chat: Chat
    date: int
    text: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CallBackQuery:
    id: str
    from_: From = field(metadata=config(field_name="from"))
    message: Message
    data: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Update:
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallBackQuery] = None

    def get_chat_id(self, update: "Update") -> int:
        chat_id = 0

        if update.callback_query:
            chat_id = update.callback_query.message.chat.id
        elif update.message:
            chat_id = update.message.chat.id
        return chat_id


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class UpdateData:
    ok: bool
    result: List[Update]
