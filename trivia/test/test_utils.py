from trivia.random_utils import Random
from abc import abstractmethod
from typing import List
from trivia.question_storage import Question


class DoNothingRandom(Random):
    def shuffle(self, data: list) -> None:
        pass


class ReversedShuffleRandom(Random):
    def shuffle(self, data: list) -> None:
        data.reverse()




