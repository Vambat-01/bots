from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Bijection(Generic[T, U], metaclass=ABCMeta):
    @abstractmethod
    def forward(self, obj: T) -> U: pass

    @abstractmethod
    def backward(self, obj: U) -> T: pass
