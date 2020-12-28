from abc import ABCMeta, abstractmethod
from typing import List
from random import shuffle


class Random(metaclass=ABCMeta):
    """
    Интерфейс получения списка вариантов ответа на вопрос и возвращения перемешанного в произвольном порядке списка
    варинтов ответа, и номер правильного ответа.
    """
    @abstractmethod
    def shuffle_answer(self, answers: List[str]) -> (List[str], int):
        """
        Возвращает список перешанных в происзвольном порядке вариантов ответа и новер правильного ответа
        :param answers:
        :return: список ответов и номер правильного ответа
        """
        pass


class RandomBot(Random):
    @abstractmethod
    def shuffle_answer(self, answers: List[str]) -> (List[str], int):
        shuffle_ans = list(enumerate(answers))
        shuffle(shuffle_ans)
        correct_answer = 0
        for i in range(len(shuffle_ans) - 1):
            if shuffle_ans[i][i] == 0:
                correct_answer = i + 1
        return shuffle_ans, correct_answer


