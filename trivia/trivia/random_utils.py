from abc import ABCMeta, abstractmethod
from typing import List
from random import shuffle
from trivia.question_storage import Question


class Random(metaclass=ABCMeta):
    """
    Интерфейс получения списка вариантов ответа на вопрос и возвращения перемешанного в произвольном порядке списка
    варинтов ответа, и номер правильного ответа.
    """
    @abstractmethod
    def shuffle_one_question(self, question: Question) -> Question:
        """
        Возвращает  вопрос с перешенным в произвольном порядке вариантами ответов и номером правильного ответа
        :param question: вопрос
        :return: вопрос
        """
        pass

    @abstractmethod
    def shuffle_questions(self, questions: List[Question]) -> List[Question]:
        """
        Возвращает список вопросов с перемешенными в произвольном порядке вариантами ответов и номерами правильных
        ответов
        :param questions: список вопросов
        :return: список вопросов
        """


class RandomBot(Random):

    def shuffle_one_question(self, question: Question) -> Question:
        shuffle_ans = list(enumerate(question.answers))
        shuffle(shuffle_ans)
        correct_answer = 0
        answers = []
        for i in range(len(shuffle_ans)):
            if shuffle_ans[i][0] == 0:
                correct_answer = i + 1

        for j in range(len(shuffle_ans)):
            answers.append(shuffle_ans[j][1])

        question.answers = answers
        question.correct_answer = correct_answer
        return question

    def shuffle_questions(self, questions: List[Question]) -> List[Question]:
        for i in range(len(questions)):
            question = questions[i]
            shuffle_ans = list(enumerate(question.answers))
            shuffle(shuffle_ans)
            correct_answer = 0
            answers = []

            for j in range(len(shuffle_ans)):
                if shuffle_ans[j][0] == 0:
                    question.correct_answer = j + 1

            for k in range(len(shuffle_ans)):
               answers.append(shuffle_ans[k][1])

            question.answers = answers
        return questions

