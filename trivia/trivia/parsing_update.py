from dataclasses import dataclass, field
from typing import Optional, List
from dataclasses_json import dataclass_json, config, Undefined


@dataclass
class From:
    """
     https://core.telegram.org/bots/api#getting-updates
    """

    id: int
    is_bot: bool
    first_name: str
    username: str


@dataclass
class Chat:
    """
     https://core.telegram.org/bots/api#getting-updates
    """
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


@dataclass_json
@dataclass
class Message:
    """
     https://core.telegram.org/bots/api#getting-updates
    """
    message_id: int
    from_: From = field(metadata=config(field_name="from"))
    chat: Chat
    date: int
    text: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class CallBackQuery:
    """
     https://core.telegram.org/bots/api#getting-updates
    """
    id: str
    from_: From = field(metadata=config(field_name="from"))
    message: Message
    data: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Update:
    """
     https://core.telegram.org/bots/api#getting-updates
    """
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
    """
     https://core.telegram.org/bots/api#getting-updates
    """
    ok: bool
    result: List[Update]
