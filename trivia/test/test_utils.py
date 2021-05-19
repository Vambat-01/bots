from core.random import Random
import json
from pathlib import Path
from trivia.bot_config import BotConfig


class DoNothingRandom(Random):
    def shuffle(self, data: list) -> None:
        pass


class ReversedShuffleRandom(Random):
    def shuffle(self, data: list) -> None:
        data.reverse()


def make_bot_config(config_path: Path) -> BotConfig:
    with open(config_path) as json_file:
        config_json = json.load(json_file)
        config = BotConfig.parse_obj(config_json)
        return config
