from abc import ABCMeta, abstractmethod


class Random(metaclass=ABCMeta):
    """
    Интерфейс для работы с random. Все операции с random должны производиться через него для возможности контролировать
    поведение системы в тестах.
    """
    @abstractmethod
    def shuffle(self, data: list) -> None:
        """
        Перемешивает в произвольном порядке переданную последовательность
        :param data: последовательность
        :return: None
        """
        pass