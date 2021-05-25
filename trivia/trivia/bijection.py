from core.bot_state_to_dict_bijection import Bijection
from core.bot_state import BotState
from trivia.bot_state import GreetingState, IdleState, InGameState, BotStateFactory
from core.utils import JsonDict
from core.bot_state_logging_wrapper import BotStateLoggingWrapper


class StateSaveException(Exception):
    """
    Ошибка сохранения или загрузки состояния бота
    """
    pass


class BotStateToDictBijection(Bijection[BotState, JsonDict]):
    """
    Биекция для сохранения состояния бота в словарь
    """
    def __init__(self, bot_state_factory: BotStateFactory):
        self.bot_state_factory = bot_state_factory

    def forward(self, obj: BotState) -> JsonDict:
        bot_state_data = obj.save()
        if isinstance(obj, GreetingState):
            bot_state_type = "GreetingState"
        elif isinstance(obj, IdleState):
            bot_state_type = "IdleState"
        elif isinstance(obj, InGameState):
            bot_state_type = "InGameState"
        elif isinstance(obj, BotStateLoggingWrapper):
            inner_dict = self.forward(obj.inner)
            inner_dict["is_logging_wrapper"] = True
            return inner_dict
        else:
            raise StateSaveException(f"Unknown BotState type")

        return {
            "is_logging_wrapper": False,
            "bot_state_type": bot_state_type,
            "bot_state_data": bot_state_data
        }

    def backward(self, obj: JsonDict) -> BotState:
        bot_state_type = obj["bot_state_type"]
        bot_state_data = obj["bot_state_data"]
        is_logging_wrapper = obj["is_logging_wrapper"]

        if bot_state_type == "GreetingState":
            bot_state = GreetingState(self.bot_state_factory)
        elif bot_state_type == "IdleState":
            bot_state = self.bot_state_factory.create_idle_state()
        elif bot_state_type == "InGameState":
            bot_state = self.bot_state_factory.create_in_game_state()
        else:
            raise StateSaveException(f"Unknown bot_state type: {bot_state_type}")

        bot_state.load(bot_state_data)
        if is_logging_wrapper:
            return BotStateLoggingWrapper(bot_state)

        return bot_state
