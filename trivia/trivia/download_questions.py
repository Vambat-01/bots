import requests
from typing import List, Dict
import json
from pathlib import Path
from itertools import chain
from core.utils import log
from time import sleep
from trivia.question_storage import Question, SqliteQuestionStorage
import argparse


INITIAL_RETRY_DELAY = 1
MAX_DELAY = 300


def get_questions(q_type: int, q_count: int, delay: int) -> List[Dict]:
    """
    Загружает вопросы для заполнения SQLite базы данных
    :param q_type: тип сложности получаемого вопроса
    :param q_count: количество полученных вопросов
    :param delay: начальная задержка перед повторной попыткой запроса. Если изначальная попытка не удалась,
                  то время задержки возростает экспоненциально. Если попытка удачная, то задержка становится
                  снова равной начальной задержке. Максимальное время задержки 5 минут. Если в базе данных
                  закончились вопросы, то при запросе возвращается пустой список.
    """
    url = "https://engine.lifeis.porn/api/millionaire.php"
    response = requests.get(url, params={
                            "qType": q_type,
                            "count": q_count
                            })

    log(f"Request status code: {response.status_code} ")

    if response.status_code == 200:
        data = response.json()["data"]

        for question in data:
            question["difficulty"] = q_type
        delay = INITIAL_RETRY_DELAY
        return data

    elif response.status_code == 429:
        log(f"Got 429. Sleeping {delay} sec before next attempt")
        sleep(delay)
        delay = min(delay * 2, MAX_DELAY)
        return get_questions(q_type, q_count, delay)

    else:
        return []


def fix_text_question(question: Dict):
    """
    Исправляет текст в переданном вопросе
    """
    text = question["question"]
    fixed_text = text.replace("\u2063", "")
    question["question"] = fixed_text


def get_all_questions(max_questions: int) -> List[Dict]:
    """
    Получает нужное количество вопросов для SQLite базы данных и возвращает список вопросов
    :param max_questions: максимальное количество вопросов
    """
    all_questions: List[Dict] = []
    while len(all_questions) < max_questions:
        easy = get_questions(1, 5, 1)
        medium = get_questions(2, 5, 1)
        hard = get_questions(3, 5, 1)

        for question in chain(easy, medium, hard):
            all_questions.append(question)

    return all_questions


def to_question(question: Dict) -> Question:
    text = question["question"]
    answers = question["answers"]
    dif = question["difficulty"]
    difficulty, points = [
        (Question.Difficulty.EASY, 1),
        (Question.Difficulty.MEDIUM, 2),
        (Question.Difficulty.HARD, 3)
    ][dif - 1]

    return Question(text, answers, points, difficulty, 0)


def main():
    parser = argparse.ArgumentParser(
        description="Получает список вопросов по API запросу, обрабатывает их и записывает в json фойл ")
    parser.add_argument("-file", type=str, help="Путь, куда будет записал json файл ")
    parser.add_argument("-count", type=int, help="Количество вопросов, полученных по API запросу")
    args = parser.parse_args()

    questions_for_file = []
    all_questions = get_all_questions(args.count)

    for question in all_questions:
        fix_text_question(question)
        questions_for_file.append(to_question(question))

    q_json = Question.schema().dump(questions_for_file, many=True)
    q_str = json.dumps(q_json, ensure_ascii=False, indent=4)

    SqliteQuestionStorage.save_to_file(q_str, Path(args.file))


if __name__ == "__main__":
    main()
