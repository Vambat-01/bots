from core.redis_api import RedisApi
import redis
import asyncio
from contextlib import contextmanager


class LiveRedisApi(RedisApi):
    def __init__(self, host: str, port: int, db: int):
        self.host = host
        self.port = port
        self.db = db
        self._redis = redis.Redis(host=self.host, port=self.port, )

    def close(self):
        self._redis.close()

    async def lock_chat(self, chat_id: int) -> None:
        while True:
            was_set = self._redis.set(str(chat_id), "1", ex=5, nx=True)
            if was_set:
                return
            await asyncio.sleep(1)

    def delete_key(self, chat_id: int) -> None:
        self._redis.delete(str(chat_id))


@contextmanager
def make_live_redis_api(host: str, port: int, db: int):
    live_redis = LiveRedisApi(host, port, db)
    try:
        yield live_redis
    finally:
        live_redis.close()
