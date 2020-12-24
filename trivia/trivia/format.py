from trivia.question_storage import Question
from typing import Optional, List


def get_number_of_answers_help(num_of_resp: int) -> str:
    return f"<i>I don't understand you. You can enter a number from 1 to {num_of_resp}</i>"


def get_response_for_valid_answer(answer_correct: int,
                                  answer_id: Optional[int] = None,
                                  next_question: Optional[Question] = None,
                                  game_score: Optional[int] = None) -> str:

    if next_question is not None:
        string_text = get_text_questions_answers("Next question",
                                                 next_question.text,
                                                 next_question.answers,
                                                 answer_correct,
                                                 answer_id
                                                 )
        text_message = string_text
    else:
        text_message = f"<i>The game is over. Your points: {game_score}</i>"
    return text_message


def get_text_questions_answers(first_text: str,
                               question_text,
                               answers: List[str],
                               correct_answer: Optional[int],
                               answer_id: Optional[int]):
    list_text = []
    list_text.append(f"<b>&#127891 {first_text}:</b>")
    if answer_id is not None:

        if answer_id == correct_answer:
            list_text[0] = f"<b>&#10004 {first_text}:</b>"
        else:
            list_text[0] = f"<b>&#10006 {first_text}:</b>"

    list_text.append(f"    <b>{question_text}</b>")
    answers = _get_answers(answers, correct_answer, answer_id)
    list_text.extend(answers)
    string_text = "\n".join(list_text)
    return string_text


def _get_answers(list_answers: List[str], correct_answer: Optional[int], answer_id: Optional[int]):
    list_ans = []
    for i in range(len(list_answers)):
        answer = f"|&#8195| {i + 1}: {list_answers[i]}"
        list_ans.append(answer)

    if answer_id is not None:
        if correct_answer == answer_id:
            list_ans[answer_id - 1] = f"&#128077 {answer_id}: {list_answers[answer_id - 1]}"
        else:
            list_ans[0] = f"&#128073 {1}: {list_answers[0]}"
            list_ans[answer_id - 1] = f"&#128078 {answer_id }: {list_answers[answer_id - 1]}"

    return list_ans


