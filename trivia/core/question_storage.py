from typing import List
from abc import ABCMeta, abstractmethod
from trivia.question_storage import Question


class QuestionStorage(metaclass=ABCMeta):
    """
        Интерфейс для доступа к вопросам
    """

    @abstractmethod
    def load_questions(self) -> List[Question]:
        """
            Считывает список вопросов
        :return: список вопросов
        """
        pass

