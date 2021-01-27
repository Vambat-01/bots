from typing import TypeVar, Generic, List
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

    def pop(self) -> T:
        """
        Удаляет элемент из стека
        :return: удаленный элемент
        """
        return T

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
        """
        Добавляет элемент в стек
        :param item: добавляемый элемент
        """
        self._list.append(item)

    def pop(self) -> T:
        """
        Удаляет последний элемент из стека
        :return: возвращает удаленный элемент
        """
        return self._list.pop()

    def is_empty(self) -> bool:
        """
        Проверяет пустой стек
        :return: True or False
        """
        return not self._list


class LinkedListBasedStack(Stack):
    """
    Абстрактный тип данных, представляющий собой список элементов, организованных
    по принципу LIFO (англ. last in — first out, «последним пришёл — первым вышел»)
    """

    @dataclass
    class Node(Generic[T]):
        """
        Узел списка
        :param val: значение хранящиеся в узле
        :param next: ссылка на следующий узел
        """
        val: T
        next: "Node"

    def __init__(self):
        self._head = None

    def push(self, item: T):
        """
        Добавляет элемент в конец стека
        :param item: добавляемый элемент
        """
        self._head = LinkedListBasedStack.Node(item, self._head)

    def pop(self) -> T:
        """
        Удаляет последний элемент из стека
        :return: возвращает удаленный элемент
        """
        val = self._head.val
        self._head = self._head.next
        return val

    def is_empty(self) -> bool:
        """
        Проверяет пустой стек или нет
        :return: True or False
        """
        return not self._head
