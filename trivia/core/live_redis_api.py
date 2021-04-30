from core.redis_api import RedisApi
import redis
import asyncio
from contextlib import contextmanager
from trivia.bot_config import LiveRedisApiConfig


class LockChatException(Exception):
    def __init__(self, chat_id: int, max_attempts):
        super().__init__()
        self.chat_id = chat_id
        self.max_attempts = max_attempts

    def __str__(self):
        return f"Failed to lock chat {self.chat_id} after {self.max_attempts} attempts"


class LiveRedisApi(RedisApi):
    def __init__(self, config: LiveRedisApiConfig):
        self.config = config
        self._redis = redis.Redis(host=config.host, port=config.port, db=0)

    def close(self):
        self._redis.close()

    async def lock_chat(self, chat_id: int) -> None:
        for _ in range(self.config.max_attempts):
            was_set = self._redis.set(str(chat_id), "1", ex=self.config.expire_sec, nx=True)
            if was_set:
                return
            await asyncio.sleep(self.config.delay_ms / 1000)

        raise LockChatException(chat_id, self.config.max_attempts)

    def unlock_chat(self, chat_id: int) -> None:
        self._redis.delete(str(chat_id))


@contextmanager
def make_live_redis_api(config: LiveRedisApiConfig):
    live_redis = LiveRedisApi(config)
    try:
        yield live_redis
    finally:
        live_redis.close()


class DoNothingRedisApi(RedisApi):
    async def lock_chat(self, chat_id: int) -> None:
        pass

    def unlock_chat(self, chat_id: int) -> None:
        pass
