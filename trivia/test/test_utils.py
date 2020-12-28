from trivia.random_utils import Random
from abc import abstractmethod
from typing import List


class DoNothingRandom(Random):
    @abstractmethod
    def shuffle_answer(self, answers: List[str]) -> (List[str], int):
        pass


class ReversedShuffleRandom(Random):
    @abstractmethod
    def shuffle_answer(self, answers: List[str]) -> (List[str], int):
        answers.reverse()
        return answers, 1
