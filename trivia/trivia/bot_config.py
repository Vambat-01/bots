from pydantic import BaseModel
from pathlib import Path


class ServerConfig(BaseModel):
    """
    Класс для натсроек Server
    """
    host: str
    port: int
    url: str


class LiveRedisApiConfig(BaseModel):
    """
    Класс для настроек Redis
    """
    host: str
    port: int
    expire_sec: int
    max_attempts: int
    delay: int


class BotConfig(BaseModel):
    """
    Класс, чтбы распарсить json файла для запуска Бота
    """
    questions_filepath: Path
    is_server: bool
    server: ServerConfig
    redis: LiveRedisApiConfig
