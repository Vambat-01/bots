from trivia.question_storage import Question
from typing import Optional, List


SMILE_THUMB_UP = '&#128077'
SMILE_THUMB_DOWN = '&#128078'
SMILE_THUMB_RIGHT = '&#128073'
SMILE_EMPTY = '|&#8195|'


def get_number_of_answers_help(num_of_resp: int) -> str:
    return f"<i>I don't understand you. You can enter a number from 1 to {num_of_resp}</i>"


def get_response_for_valid_answer(correct_answer: int,
                                  answer_id: Optional[int] = None,
                                  next_question: Optional[Question] = None,
                                  game_score: Optional[int] = None) -> str:
    """
    Получает следующий вопрос и в зависимости есть он или нет, возвращает следующий вопрос или что игра закончена.
    :param correct_answer: номер правильного ответа
    :param answer_id: номер ответа, который дал пользователь
    :param next_question: следующий вопрос
    :param game_score: игровые очки пользователя
    :return: текст следующего вопроса или конечная фраза игры
    """

    if next_question is not None:
        return get_text_questions_answers("Next question",
                                          next_question.text,
                                          next_question.answers,
                                          correct_answer,
                                          answer_id
                                          )

    return f"<i>The game is over. Your points: {game_score}</i>"


def get_text_questions_answers(first_text: str,
                               question_text,
                               answers: List[str],
                               correct_answer: Optional[int] = None,
                               answer_id: Optional[int] = None
                               ):
    """
    Возаращает текст вопроса и варианты ответы
    :param first_text: первый текст в сообщение
    :param question_text: текст вопроса
    :param answers: Список вариантоа ответа
    :param correct_answer: номер правильного ответа
    :param answer_id: номер ответа, который дал пользователь
    :return: Возаращает текст вопроса и варианты ответы
    """
    rows = []

    if answer_id is None:
        rows.append(f"<b>&#127891 {first_text}:</b>")
    else:
        if answer_id == correct_answer:
            rows.append(f"<b>&#10004 {first_text}:</b>")

        if answer_id != correct_answer:
            rows.append(f"<b>&#10006 {first_text}:</b>")

    rows.append(f"    <b>{question_text}</b>")
    answers = _get_answers(answers, correct_answer, answer_id)
    rows.extend(answers)
    text = "\n".join(rows)
    return text


def _get_answers(list_answers: List[str], correct_answer: Optional[int], answer_id: Optional[int]):
    possible_answers = []
    for i in range(len(list_answers)):
        if answer_id is not None:
            if answer_id == i + 1:
                if answer_id == correct_answer:
                    possible_answers.append(f"{SMILE_THUMB_UP} {i + 1}: {list_answers[i]}")
                else:
                    possible_answers.append(f"{SMILE_THUMB_DOWN} {i + 1}: {list_answers[i]}")

            if correct_answer == i + 1 and correct_answer != answer_id:
                possible_answers.append(f"{SMILE_THUMB_RIGHT} {i + 1}: {list_answers[i]}")

            if answer_id != i + 1 and correct_answer != i + 1:
                possible_answers.append(f"{SMILE_EMPTY} {i + 1}: {list_answers[i]}")

        else:
            possible_answers.append(f"{SMILE_EMPTY} {i + 1}: {list_answers[i]}")
        return possible_answers

    #     if answer_id is not None:
    #         if correct_answer == answer_id and answer_id == i + 1:
    #             possible_answers.append(f"{SMILE_THUMB_UP} {i + 1}: {list_answers[i]}")
    #
    #         if correct_answer != answer_id and answer_id == i + 1:
    #             possible_answers.append(f"{SMILE_THUMB_DOWN} {i + 1}: {list_answers[i]}")
    #
    #         if correct_answer == i + 1 and correct_answer != answer_id:
    #             possible_answers.append(f"{SMILE_THUMB_RIGHT} {i + 1}: {list_answers[i]}")
    #
    #         if answer_id != i + 1 and correct_answer != i + 1:
    #             possible_answers.append(f"{SMILE_EMPTY} {i + 1}: {list_answers[i]}")
    #
    #     else:
    #         possible_answers.append(f"{SMILE_EMPTY} {i + 1}: {list_answers[i]}")
    # return possible_answers


