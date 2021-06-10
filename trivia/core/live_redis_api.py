from core.redis_api import RedisApi
import redis
import asyncio
from contextlib import contextmanager
from trivia.bot_config import LiveRedisApiConfig
from typing import Optional


class LockChatException(Exception):
    """
    Класс вызова исключения для Redis
    """
    def __init__(self, key: str, max_attempts: int):
        super().__init__()
        self.key = key
        self.max_attempts = max_attempts

    def __str__(self):
        return f"Failed to lock chat {self.key} after {self.max_attempts} attempts"


class LiveRedisApi(RedisApi):
    def __init__(self, config: LiveRedisApiConfig):
        self._config = config
        self._redis = redis.Redis(host=config.host, port=config.port, db=0)

    def close(self):
        self._redis.close()

    async def lock(self, key: str) -> None:
        for _ in range(self._config.max_attempts):
            was_set = self._redis.set(key, "1", ex=self._config.expire_sec, nx=True)
            if was_set:

                return
            await asyncio.sleep(self._config.delay_ms / 1000)

        raise LockChatException(key, self._config.max_attempts)

    def unlock(self, key: str) -> None:
        self._redis.delete(key)

    def set_key(self, key: str, state: str):
        self._redis.set(key, state)

    def get_key(self, key: str) -> Optional[str]:
        bytes_state: bytes = self._redis.get(key)   # type: ignore
        if bytes_state:
            str_state = bytes_state.decode()
            return str_state

        return None


@contextmanager
def make_live_redis_api(config: LiveRedisApiConfig):
    live_redis = LiveRedisApi(config)
    try:
        yield live_redis
    finally:
        live_redis.close()


class DoNothingRedisApi(RedisApi):
    async def lock(self, key: str) -> None:
        pass

    def unlock(self, key: str) -> None:
        pass

    def set_key(self, key: str, state: str):
        pass

    def get_key(self, key: str) -> Optional[str]:
        return None
