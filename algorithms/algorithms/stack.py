from typing import TypeVar, Generic, List, Optional
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod

T = TypeVar("T")


class Stack(Generic[T], metaclass=ABCMeta):
    """
    Интерфейс абстрактных типов данных, которые представляют собой список, организованных
    по принципу LIFO (англ. last in — first out, «последним пришёл — первым вышел»).
    """

    @abstractmethod
    def push(self, item: T) -> None:
        """
        Добавляет элемент в стек
        :param item: добавляемый элемент
        :return: None
        """
        pass

    @abstractmethod
    def pop(self) -> T:
        """
        Удаляет элемент из стека
        :return: удаленный элемент
        """
        return T

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Проверяет пустой стек
        :return: True or False
        """
        pass


class ListBasedStack(Stack):
    """
    Абстрактный тип данных, представляющий собой список элементов, организованных
    по принципу LIFO (англ. last in — first out, «последним пришёл — первым вышел»).
    """

    def __init__(self):
        self._list: List[T] = []

    def push(self, item: T) -> None:
        self._list.append(item)

    def pop(self) -> T:
        return self._list.pop()

    def is_empty(self) -> bool:
        return not self._list


class LinkedListBasedStack(Stack):
    """
    Абстрактный тип данных, представляющий собой список элементов, организованных
    по принципу LIFO (англ. last in — first out, «последним пришёл — первым вышел»)
    """

    @dataclass
    class Node(Generic[T]):
        val: T
        next: Optional["Node"] = None

    def __init__(self):
        self._head = None

    def push(self, item: T) -> None:
        self._head = LinkedListBasedStack.Node(item, self._head)

    def pop(self) -> T:
        val = self._head.val
        self._head = self._head.next
        return val

    def is_empty(self) -> bool:
        return not self._head
