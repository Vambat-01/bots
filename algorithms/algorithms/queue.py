from typing import TypeVar, Generic, List, Optional
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
import time
from algorithms.utils import elapsed_time

T = TypeVar("T")


class Queue(Generic[T], metaclass=ABCMeta):
    """
    Интерфейс абстрактных типов данных, которые представляют собой список, организованных
    по принципу FIFO (англ. first in - first out, <<первый пришел - первый вышел>>).
    """

    @abstractmethod
    def push(self, item: T) -> None:
        """
        Добавляет элемент в очередь
        :param item: добавляемый элемент
        :return: None
        """
        pass

    @abstractmethod
    def pop(self) -> T:
        """
        Удаляет элемент из очереди
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


class ListBasedQueue(Queue):
    """
    В качестве базовой структуры использован питонный список
    """
    def __init__(self):
        self._list: List[T] = []

    def push(self, item: T) -> None:
        self._list.insert(0, item)

    def pop(self) -> T:
        return self._list.pop()

    def is_empty(self) -> bool:
        return not self._list


class LinkedListBasedQueue(Queue):
    """
    В качестве базовой структуры использован двунаправленный связный список
    """
    @dataclass
    class Node(Generic[T]):
        val: T
        prev: Optional["Node"] = None
        next: Optional["Node"] = None

    def __init__(self):
        self.head = None
        self.tail = None

    def push(self, item: T) -> None:
        new_node = LinkedListBasedQueue.Node(item)
        if self.head is None and self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def pop(self) -> T:
        val = self.head.val
        new_node = self.head.next
        if new_node is None:
            self.tail = None
        else:
            new_node.prev = None
        self.head = new_node
        return val

    def is_empty(self) -> bool:
        return not self.head


@elapsed_time
def _elapsed_time_for_queue(q: Queue):
    t = time.process_time()
    for _ in range(100):
        for _ in range(100000):
            q.push(1)
        for _ in range(100000):
            q.pop()
    elapsed_time = time.process_time() - t
    print(elapsed_time)


queue_list_based = ListBasedQueue()
_elapsed_time_for_queue(queue_list_based)

queue_linked_list_based = LinkedListBasedQueue()
_elapsed_time_for_queue(queue_linked_list_based)
