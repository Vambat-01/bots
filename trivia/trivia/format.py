from trivia.question_storage import Question
from typing import Optional, List


SMILE_THUMB_UP = '&#128077'
SMILE_THUMB_DOWN = '&#128078'
SMILE_FINGER_RIGHT = '&#128073'
SMILE_EMPTY = '&#8195'
SMILE_HAT = '&#127891'
SMILE_CHECK = '&#10004'
SMILE_CROSS = '&#10006'


def get_number_of_answers_help(num_of_resp: int) -> str:
    return f"<i>I don't understand you. You can enter a number from 1 to {num_of_resp}</i>"


def make_message(correct_answer: int,
                 answer_id: Optional[int] = None,
                 next_question: Optional[Question] = None,
                 game_score: Optional[int] = None) -> str:
    """
    Используется для редактирования предыдущего сообщения бота и для сборки нового ответа пользователю.
    Если "next_question" присутствует, а "game_score" отсутствуют, собирается следующий вопрос.
    Если "game_score" присутствуют, а "next_question" отсутствует, тогда выводится последнее сообщение в игре.
    :param correct_answer: номер правильного ответа
    :param answer_id: опциональный ответ пользователя. Если ответ присутствуеи, редактируется старое сообщение и
    собирается новое. Если ответ отсутствует, предыдущие сообщение пользоватебя не редактируется, собирается новое.
    :param next_question: следующее сообщение
    :param game_score: игровые очки пользователя
    :return: текст следующего вопроса или конечная фраза игры
    """

    if next_question is not None:
        return make_question("Next question",
                             next_question.text,
                             next_question.answers,
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
    Возвращает текст вопроса и варианты ответов. Используется для редактирует старого вопроса и создания нового.
    Если "answer_id" отсутствует, выводится первый текст сообщения со смайлом шляпа.
    Если "answer_id" присутсвует и он верный, выводится первый текст сообщения со смайлом "галочка".
    Если "answer_id" присутсвует и он не верный, выводится первый текст сообщеня со смайлом "крестик"
    :param first_text: первый текст в сообщение
    :param question_text: текст вопроса
    :param answers: Список вариантов ответа
    :param correct_answer: опциональный правильного ответа
    :param answer_id: опциональный ответ пользователя
    :return: Возвращает текст вопроса и варианты ответов
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
                possible_answers.append(f"{SMILE_THUMB_UP} {i + 1}: {list_answers[i]}")
            elif correct_answer != answer_id and answer_id == i + 1:
                possible_answers.append(f"{SMILE_THUMB_DOWN} {i + 1}: {list_answers[i]}")
            elif correct_answer == i + 1 and correct_answer != answer_id:
                possible_answers.append(f"{SMILE_FINGER_RIGHT} {i + 1}: {list_answers[i]}")
            else:
                possible_answers.append(f"|{SMILE_EMPTY}| {i + 1}: {list_answers[i]}")
        else:
            possible_answers.append(f"|{SMILE_EMPTY}| {i + 1}: {list_answers[i]}")

    return possible_answers



