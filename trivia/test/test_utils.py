from core.random import Random
import json
from trivia.bot_config import GameConfig


class DoNothingRandom(Random):
    def shuffle(self, data: list) -> None:
        pass


class ReversedShuffleRandom(Random):
    def shuffle(self, data: list) -> None:
        data.reverse()


def make_game_config(easy: int, medium: int, hard: int) -> GameConfig:
    json_body = {
            "easy_question_count": easy,
            "medium_question_count": medium,
            "hard_question_count": hard
        }
    game_config = GameConfig.parse_obj(json_body)
    return game_config
