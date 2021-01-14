from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Bijection(Generic[T, U], metaclass=ABCMeta):
    """
    Переход из одного состояния обьекта в другое
    """
    @abstractmethod
    def forward(self, obj: T) -> U: pass

    @abstractmethod
    def backward(self, obj: U) -> T: pass
