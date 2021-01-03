from abc import ABCMeta, abstractmethod
from random import shuffle


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


class RandomImpl(Random):

    def shuffle(self, data: list) -> None:
        shuffle(data)


