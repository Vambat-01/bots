from trivia.random_utils import Random
from abc import abstractmethod
from typing import List
from trivia.question_storage import Question


class DoNothingRandom(Random):
    def shuffle_one_question(self, question: Question) -> Question:
        return question

    def shuffle_questions(self, questions: List[Question]) -> List[Question]:
        return questions


class ReversedShuffleRandom(Random):
    def shuffle_one_question(self, question: Question) -> Question:
        question.answers.reverse()
        question.correct_answer = len(question.answers)
        return question

    def shuffle_questions(self, questions: List[Question]) -> List[Question]:
        for i in range(len(questions)):
            questions[i].answers.reverse()
        return questions


