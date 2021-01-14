from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Bijection(Generic[T, U], metaclass=ABCMeta):
    """
    Биекция определяет обратимую трансформацию между типами T и U
    """
    @abstractmethod
    def forward(self, obj: T) -> U:
        """
        Трансформирует тип T в U
        :param obj: T
        :return: U
        """
        pass

    @abstractmethod
    def backward(self, obj: U) -> T:
        """
        Обратно трансформирует тип U в T
        :param obj: U
        :return: T
        """
        pass
