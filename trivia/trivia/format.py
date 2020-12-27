from trivia.question_storage import Question
from typing import Optional, List


def get_number_of_answers_help(num_of_resp: int) -> str:
    return f"<i>I don't understand you. You can enter a number from 1 to {num_of_resp}</i>"


def get_response_for_valid_answer(correct_answer: int,
                                  answer_id: Optional[int] = None,
                                  next_question: Optional[Question] = None,
                                  game_score: Optional[int] = None) -> str:

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
    rows = []

    if answer_id is None:
        rows.append(f"<b>&#127891 {first_text}:</b>")
    else:
        if answer_id == correct_answer:
            rows.append(f"<b>&#10004 {first_text}:</b>")
        else:
            rows.append(f"<b>&#10006 {first_text}:</b>")

    rows.append(f"    <b>{question_text}</b>")
    answers = _get_answers(answers, correct_answer, answer_id)
    rows.extend(answers)
    string_text = "\n".join(rows)
    return string_text


def _get_answers(list_answers: List[str], correct_answer: Optional[int], answer_id: Optional[int]):
    possible_answers = []
    for i in range(len(list_answers)):
        if answer_id is not None:
            if correct_answer == answer_id and answer_id == i + 1:
                possible_answers.append(f"&#128077 {i + 1}: {list_answers[i]}")

            if correct_answer != answer_id and answer_id == i + 1:
                possible_answers.append(f"&#128078 {i + 1}: {list_answers[i]}")

            if correct_answer == i + 1 and correct_answer != answer_id:
                possible_answers.append(f"&#128073 {i + 1}: {list_answers[i]}")

            if answer_id != i + 1 and correct_answer != i + 1:
                possible_answers.append(f"|&#8195| {i + 1}: {list_answers[i]}")

        else:
            possible_answers.append(f"|&#8195| {i + 1}: {list_answers[i]}")
    return possible_answers


