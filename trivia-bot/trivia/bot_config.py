from pydantic import BaseModel
from pathlib import Path
from typing import Optional


class ServerConfig(BaseModel):
    """
    Настройки работы бота в режиме сервера.
    Url можно передать в бота разными способами, поэтому он опциональный. Бота можно запустить в режиме сервера
    локально без парамметров key и cert, поэтому они тоже опциональны
    """
    host: str
    port: int
    url: Optional[str]
    key: Optional[str]
    cert: Optional[Path]


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

    @staticmethod
    def make(easy_question_count: int,
             medium_question_count: int,
             hard_question_count: int
             ) -> "GameConfig":

        return GameConfig(easy_question_count=easy_question_count,
                          medium_question_count=medium_question_count,
                          hard_question_count=hard_question_count
                          )


class BotConfig(BaseModel):
    """
    Настройки бота
    """
    questions_filepath: Path
    game_config: GameConfig
    is_server: bool
    server: ServerConfig
    redis: LiveRedisApiConfig
    out_path: Optional[str]
