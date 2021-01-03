from abc import ABCMeta, abstractmethod
from random import shuffle


class Random(metaclass=ABCMeta):
    """
    Интерфейс перемешивания в произвольном порядке последовательнсти
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


