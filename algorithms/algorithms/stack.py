from typing import TypeVar, Generic, List

T = TypeVar("T")


class StackList(Generic[T]):
    """
    Абстрактный тип данных, представляющий собой список элементов, организованных
    по принципу LIFO (англ. last in — first out, «последним пришёл — первым вышел»).
    """

    def __init__(self):
        self.list: List[T] = []

    def push(self, item: T):
        """
        Добавляет элемент в конец списка
        :param item: добавляемый элемент
        """
        self.list.append(item)

    def pop(self) -> T:
        """
        Удаляет последний элемент из списка
        :return: возвращает удаленный элемент
        """
        return self.list.pop()

    def is_empty(self) -> bool:
        """
        Проверяет пустой список или нет
        :return: True or False
        """
        return not self.list


class StackLinkedList(Generic[T]):
    """
    Абстрактный тип данных, представляющий собой список элементов, организованных
    по принципу LIFO (англ. last in — first out, «последним пришёл — первым вышел»)
    """

    class Node(Generic[T]):
        """
        Класс узел
        :param val: значение хранящиеся в узле
        :param next: ссылка на следующий узел
        """
        def __init__(self, val: T, next):
            self.val = val
            self.next = next

    def __init__(self):
        self._head = None

    def push(self, item: T):
        """
        Добавляет элемент в конец списка
        :param item: добавляемый элемент
        """
        self._head = StackLinkedList.Node(item, self._head)

    def pop(self) -> T:
        """
        Удаляет последний элемент из списка
        :return: возвращает удаленный элемент
        """
        val = self._head.val
        self._head = self._head.next
        return val

    def is_empty(self) -> bool:
        """
        Проверяет пустой список или нет
        :return: True or False
        """
        return not self._head
