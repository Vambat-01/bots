from typing import Optional, List
from pydantic import BaseModel, Field


class User(BaseModel):
    """
     https://core.telegram.org/bots/api#user
    """

    id: int
    is_bot: bool
    first_name: str
    username: Optional[str]


class Chat(BaseModel):
    """
     https://core.telegram.org/bots/api#chat
    """
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    type: str


class Message(BaseModel):
    """
     https://core.telegram.org/bots/api#message
    """
    message_id: int
    from_: Optional[User] = Field(alias="from")
    chat: Chat
    date: int
    text: str


class CallBackQuery(BaseModel):
    """
     https://core.telegram.org/bots/api#callbackquery
    """
    id: str
    from_: User = Field(alias="from")
    message: Optional[Message]
    data: str


class Update(BaseModel):
    """
     https://core.telegram.org/bots/api#getting-updates
    """
    update_id: int
    message: Optional[Message] = None
    callback_query: Optional[CallBackQuery] = None

    def get_chat_id(self, update: "Update") -> int:
        chat_id = 0
        if update.callback_query and update.callback_query.message:
            chat_id = update.callback_query.message.chat.id
        elif update.message:
            chat_id = update.message.chat.id
        return chat_id


class UpdatesResponse(BaseModel):
    """
     https://core.telegram.org/bots/api#getting-updates
    """
    ok: bool
    result: List[Update]
