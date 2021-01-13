from core.bijection import Bijection
from core.bot_state import BotState
from trivia.bot_state import GreetingState, IdleState, InGameState, BotStateFactory


class BotStateToDictBijection(Bijection[BotState, dict]):
    def __init__(self, bot_state_factory: BotStateFactory):
        self.bot_state_factory = bot_state_factory

    def forward(self, obj: BotState) -> dict:
        bot_state_data = obj.save()
        if isinstance(obj, GreetingState):
            bot_state_type = "GreetingState"
        elif isinstance(obj, IdleState):
            bot_state_type = "IdleState"
        elif isinstance(obj, InGameState):
            bot_state_type = "InGameState"
        else:
            raise Exception(f"Unknown BotState type")

        return {
            "bot_state_type": bot_state_type,
            "bot_state_data": bot_state_data
        }

    def backward(self, obj: dict) -> BotState:
        bot_state_type = obj["bot_state_type"]
        bot_state_data = obj["bot_state_data"]

        if bot_state_type == "GreetingState":
            bot_state = GreetingState(self.bot_state_factory)
        elif bot_state_type == "IdleState":
            bot_state = self.bot_state_factory.create_idle_state()
        elif bot_state_type == "InGameState":
            bot_state = self.bot_state_factory.create_in_game_state()
        else:
            raise Exception(f"Unknown bot_state type: {bot_state_type}")

        bot_state.load(bot_state_data)
        return bot_state
