from trivia.question_storage import Question
from typing import Optional, List
import json


def get_number_of_answers_help(num_of_resp: int) -> str:
    return f"<i>I don't understand you. You can enter a number from 1 to {num_of_resp}</i>"


def get_response_for_valid_answer(is_answer_correct: bool,
                                  next_question: Optional[Question] = None,
                                  game_score: Optional[int] = None) -> str:
    if is_answer_correct:
        message_part_1 = "<i>&#127774 Answer is correct!</i>"
    else:
        message_part_1 = "<i>&#127783 Answer is not correct!</i>"

    if next_question is not None:
        string_text = get_text_questions_answers("Next question", next_question.text, next_question.answers)
        message_part_2 = string_text
    else:
        message_part_2 = f"<i>The game is over. Your points: {game_score}</i>"

    return f"{message_part_1} {message_part_2}"


def get_text_questions_answers(first_text: str, question_text, answers: List[str]):
    list_text = []
    list_text.append(f"<b>&#10067{first_text}:</b>")
    list_text.append(f"    <b>{question_text}</b>")
    list_text.append("<i>Choose answer:</i>")
    answers = _get_answers(answers)
    list_text.extend(answers)
    string_text = "\n".join(list_text)
    return string_text


def _get_answers(list_answers: List[str]):
    list_ans = []
    for i in range(len(list_answers)):
        answer = f"{i + 1}: {list_answers[i]}"
        list_ans.append(answer)
    return list_ans


def get_four_buttons():
    array_for_button = [
            [
                {
                    "text": "A",
                    "callback_data": "back_one"
                },
                {
                    "text": "B",
                    "callback_data": "back_two"
                }
            ],
            [
                {
                    "text": "C",
                    "callback_data": "back_three"
                },
                {
                    "text": "D",
                    "callback_data": "back_four"
                    }
            ]
        ]
    string_array = json.dumps(array_for_button)
    return string_array


