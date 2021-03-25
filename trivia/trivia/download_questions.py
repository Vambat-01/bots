import requests
from typing import List, Dict
import json
from pathlib import Path
from itertools import chain
from core.utils import log
from time import sleep
from trivia.question_storage import Question
import argparse


INITIAL_RETRY_DELAY = 1
MAX_DELAY = 300


def get_questions(q_type: int, q_count: int, delay: int) -> List[Dict]:
    """
    Получает вопросы для заполнения SQLite базы данных
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
    Исправляет текст в переданных вопросах
    """
    text = question["question"]
    fixed_text = text.replace("\u2063", "")
    question["question"] = fixed_text


def save_to_file(questions: List[Dict], file_path: Path):
    """
    Записывает переданные вопросы в файл в json формате
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)


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


def get_normalize_questions(questions: List[Dict]) -> List[Question]:
    all_questions = []
    for question in questions:
        text = question["question"]
        answers = question["answers"]
        dif = question["difficulty"]
        difficulty = Question.Difficulty.EASY
        points = 0
        if dif == 1:
            difficulty = Question.Difficulty.EASY
            points = 1
        elif dif == 2:
            difficulty = Question.Difficulty.MEDIUM
            points = 2
        elif dif == 3:
            difficulty = Question.Difficulty.HARD
            points = 3

        all_questions.append(Question(text, answers, points, difficulty, 0))
    return all_questions


def main():
    parser = argparse.ArgumentParser(
        description="Получает список вопросов по API запросу, обрабатывает их и записывает в json фойл ")
    parser.add_argument("-file", type=str, help="Путь, куда будет записал json файл ")
    parser.add_argument("-count", type=int, help="Количество вопросов, полученных по API запросу")
    args = parser.parse_args()

    all_questions = get_all_questions(args.count)

    for question in all_questions:
        fix_text_question(question)

    save_to_file(all_questions, Path(args.file))


# Запускать только при выполнение, как скрипт
if __name__ == "__main__":
    main()
