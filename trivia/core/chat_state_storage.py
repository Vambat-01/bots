import json
from abc import ABCMeta, abstractmethod
from trivia.bijection import BotStateToDictBijection
from typing import Optional, Dict
from core.bot_state import BotState
from core.redis_api import RedisApi
from trivia.question_storage import JSONEncoder, JSONDecoder


class ChatStateStorage(metaclass=ABCMeta):
    """
    Класс для хранения состояний бота
    """

    @abstractmethod
    def set_state(self, chat_id: str, state: BotState):
        """
        Сохраняет состояние бота в словарь
        :param chat_id: Идентификатор чата
        :param state: состояние бота
        """
        pass

    def get_state(self, chat_id: str) -> Optional[BotState]:
        """
        Получает состояние бота из словаря
        :return: опциональное состояние бота
        """
        pass


class DictChatStateStorage(ChatStateStorage):
    """
    Класс для хранения состояний бота в JsonDict
    """
    def __init__(self):
        self.chat_states: Dict[str, BotState] = {}

    def set_state(self, chat_id: str, state: BotState):
        self.chat_states[chat_id] = state

    def get_state(self, chat_id: str) -> Optional[BotState]:
        if chat_id in self.chat_states:
            return self.chat_states[chat_id]
        else:
            return None


class RedisChatStateStorage(ChatStateStorage):
    """
    Класс для хранения состояний бота в Redis
    """
    def __init__(self, redis_api: RedisApi, bot_state_to_dict_bijection: BotStateToDictBijection):
        self.redis_api = redis_api
        self.bot_state_to_dict_bijection = bot_state_to_dict_bijection

    def set_state(self, chat_id: str, state: BotState):
        dict_state = self.bot_state_to_dict_bijection.forward(state)
        str_state = json.dumps(dict_state, cls=JSONEncoder, ensure_ascii=False)
        self.redis_api.set_state(f"state_{chat_id}", str_state)

    def get_state(self, chat_id: str) -> Optional[BotState]:
        str_state = self.redis_api.get_state(f"state_{chat_id}")
        if str_state:
            dict_state = json.loads(str_state, cls=JSONDecoder)
            state = self.bot_state_to_dict_bijection.backward(dict_state)
            return state
        return None
