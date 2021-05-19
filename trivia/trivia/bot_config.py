from pydantic import BaseModel
from pathlib import Path
from typing import Optional


class ServerConfig(BaseModel):
    """
    Настройки работы бота в режиме сервера.
    """
    host: str
    port: int
    url: Optional[str]


class LiveRedisApiConfig(BaseModel):
    """
    Настройки Redis клиента
    """
    host: str
    port: int
    expire_sec: int
    max_attempts: int
    delay_ms: int


class GameConfig(BaseModel):
    """
    Настройки количествао вопросов разной сложности
    """
    easy_question_count: int
    medium_question_count: int
    hard_question_count: int


class BotConfig(BaseModel):
    """
    Настройки бота
    """
    questions_filepath: Path
    question_difficulties: GameConfig
    is_server: bool
    server: ServerConfig
    redis: LiveRedisApiConfig
    out_path: Optional[str]
