from pydantic import BaseModel
from pathlib import Path
from typing import Optional


class ServerConfig(BaseModel):
    """
    Настройки работы бота в режиме сервера.
    """
    host: str
    port: int
    url: str


class LiveRedisApiConfig(BaseModel):
    """
    Настройки Redis клиента
    """
    host: str
    port: int
    expire_sec: int
    max_attempts: int
    delay_ms: int


class BotConfig(BaseModel):
    """
    Настройки бота
    """
    questions_filepath: Path
    is_server: bool
    server: ServerConfig
    redis: LiveRedisApiConfig
    out_path: Optional[str]
