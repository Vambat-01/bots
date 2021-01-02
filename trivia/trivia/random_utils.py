from abc import ABCMeta, abstractmethod
from typing import List
from random import shuffle
from trivia.question_storage import Question


class Random(metaclass=ABCMeta):
    """
    Интерфейс получения списка вариантов ответа на вопрос и возвращения перемешанного в произвольном порядке списка
    варинтов ответа, и номер правильного ответа.
    """
    @abstractmethod
    def shuffle(self, data: list) -> None:
        """
        Перемешивает в произвольном порядке переданную последовательность
        :param data: последовательность
        :return: None
        """
        pass


class RandomBot(Random):

    def shuffle(self, data: list) -> None:
        shuffle(data)


