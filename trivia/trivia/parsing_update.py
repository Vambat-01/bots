from dataclasses import dataclass


@dataclass
class From:
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str


@dataclass
class Chat:
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


@dataclass
class Message:
    message_id: int
    from_: From
    chat: Chat
    date: int
    text: str


@dataclass
class Result:
    update_id: int
    message: Message
