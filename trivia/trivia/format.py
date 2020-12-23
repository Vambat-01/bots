from trivia.question_storage import Question
from typing import Optional, List


def get_number_of_answers_help(num_of_resp: int) -> str:
    return f"<i>I don't understand you. You can enter a number from 1 to {num_of_resp}</i>"


def get_response_for_valid_answer(answer_correct: int,
                                  answer_id: Optional[int],
                                  next_question: Optional[Question] = None,
                                  game_score: Optional[int] = None) -> str:
    if answer_correct == answer_id:
        message_part_1 = "<i>&#127774 Answer is correct!</i>"
    else:
        message_part_1 = "<i>&#127783 Answer is not correct!</i>"

    if next_question is not None:
        string_text = get_text_questions_answers("Next question",
                                                 next_question.text,
                                                 next_question.answers,
                                                 answer_correct,
                                                 answer_id
                                                 )
        message_part_2 = string_text
    else:
        message_part_2 = f"<i>The game is over. Your points: {game_score}</i>"

    return f"{message_part_1} {message_part_2}"


def get_text_questions_answers(first_text: str,
                               question_text,
                               answers: List[str],
                               correct_answer: Optional[int],
                               answer_id: Optional[int]):
    list_text = []
    list_text.append(f"<b>&#10067{first_text}:</b>")
    list_text.append(f"    <b>{question_text}</b>")
    list_text.append("<i>Choose answer:</i>")
    answers = _get_answers(answers, correct_answer, answer_id)
    list_text.extend(answers)
    string_text = "\n".join(list_text)
    return string_text


def _get_answers(list_answers: List[str], correct_answer: Optional[int], answer_id: Optional[int]):
    list_ans = []
    for i in range(len(list_answers)):
        answer = f"{i + 1}: {list_answers[i]}"
        list_ans.append(answer)

    if answer_id is not None:
        if correct_answer == answer_id:
            list_ans[answer_id] = f"{answer_id - 1}: {list_answers[answer_id - 1]} U+2714"
        else:
            list_ans[0] = f"{1}: {list_answers[0]} U+26A0"
            list_ans[int(answer_id) - 1] = f"{answer_id}: {list_answers[int(answer_id) - 1]} U+274C"
    return list_ans


