from trivia.question_storage import Question
from typing import Optional, List


SMILE_GREEN_CIRCLE = '&#128994'
SMILE_RED_CIRCLE = '&#128308'
SMILE_WHITE_CIRCLE = '&#9898'
SMILE_HAT = '&#127891'
SMILE_CHECK = '&#10004'
SMILE_CROSS = '&#10006'


def get_number_of_answers_help(num_of_resp: int) -> str:
    return f"<i>I don't understand you. You can enter a number from 1 to {num_of_resp}</i>"


def make_message(correct_answer: int,
                 answer_id: Optional[int] = None,
                 question: Optional[Question] = None,
                 game_score: Optional[int] = None) -> str:
    """
    Используется для редактирования предыдущего сообщения бота и для сборки нового.
    Наличие "question" и отсутствие "game_score" - собирает следующий вопрос.
    Наличие "game_score" и отсутствие "question" - выводит последнее сообщение в игре.
    :param correct_answer: правильный ответ
    :param answer_id: опциональный ответ пользователя. Наличие "answer_id" означает редактирование.
    Отсутствие - создание нового вопроса.
    :param question: опциональный вопрос
    :param game_score: опциональные очки пользователя
    :return: текст следующего вопроса или конечная фраза игры
    """

    if question is not None:
        return make_question("Next question",
                             question.text,
                             question.answers,
                             correct_answer,
                             answer_id
                             )

    return f"<i>The game is over. Your points: {game_score}</i>"


def make_question(first_text: str,
                  question_text,
                  answers: List[str],
                  correct_answer: Optional[int] = None,
                  answer_id: Optional[int] = None
                  ):
    """
    Возвращает текст вопроса и варианты ответов. Используется для редактирования старого вопроса и создания нового.
    Наличие `answer_id` означает редактирование. Отсутствие - создание нового вопроса.
    :param first_text: первый текст в сообщение
    :param question_text: текст вопроса
    :param answers: список вариантов ответа
    :param correct_answer: опциональный правильный ответ
    :param answer_id: опциональный ответ пользователя
    :return: возвращает текст вопроса и варианты ответов
    """
    rows = []

    if answer_id is None:
        rows.append(f"<b>{SMILE_HAT} {first_text}:</b>")
    elif answer_id == correct_answer:
        rows.append(f"<b>{SMILE_CHECK} {first_text}:</b>")
    else:
        rows.append(f"<b>{SMILE_CROSS} {first_text}:</b>")

    rows.append(f"    <b>{question_text}</b>")
    answers = _get_answers(answers, correct_answer, answer_id)
    rows.extend(answers)
    text = "\n".join(rows)
    return text


def _get_answers(list_answers: List[str], correct_answer: Optional[int], answer_id: Optional[int]):
    possible_answers = []
    for i in range(len(list_answers)):
        if answer_id is not None:
            if correct_answer == answer_id and answer_id == i + 1:
                possible_answers.append(f"{SMILE_GREEN_CIRCLE} {i + 1}: {list_answers[i]}")
            elif correct_answer != answer_id and answer_id == i + 1:
                possible_answers.append(f"{SMILE_RED_CIRCLE} {i + 1}: {list_answers[i]}")
            elif correct_answer == i + 1 and correct_answer != answer_id:
                possible_answers.append(f"{SMILE_GREEN_CIRCLE} {i + 1}: {list_answers[i]}")
            else:
                possible_answers.append(f"{SMILE_WHITE_CIRCLE} {i + 1}: {list_answers[i]}")
        else:
            possible_answers.append(f"{SMILE_WHITE_CIRCLE} {i + 1}: {list_answers[i]}")

    return possible_answers
