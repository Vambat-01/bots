from pydantic import BaseModel
from pathlib import Path


class StartBot(BaseModel):
    """
    Класс, чтбы распарсить json файла для запуска Бота
    """
    file: Path
    server_host: str
    server_port: int
    server: bool
    server_url: str
    redis_host: str
    redis_port: int
    redis_db: int
