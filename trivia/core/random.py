from abc import ABCMeta, abstractmethod
from random import shuffle


class Random(metaclass=ABCMeta):
    """
    Интерфейс для работы с random. Все операции с random должны производиться через него для возможности контролировать
    поведение системы в тестах.
    """
    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

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
