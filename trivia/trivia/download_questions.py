import requests
from typing import List, Dict
import json
from pathlib import Path
from itertools import chain
from core.utils import log
from time import sleep
import argparse


INITIAL_RETRY_DELAY = 1
MAX_DELAY = 300


def get_questions(q_type: int, q_count: int, delay: int) -> List[Dict]:
    """
    Получает вопросы для заполнения SQLite базы данных
    :param q_type: тип сложности получаемого вопроса
    :param q_count: количество полученных вопросов
    :param delay: начальная задержка перед повторной попыткой запроса, если изначальная попытка не удалась,
                  то время задержки возростает экспоненциально, если попытка удачная, то задержка становится
                  снова равной начальной задержке. Максимальное время задержки 5 минут. Если в базе данных
                  закончились вопросы, то при запросе возвращается пустой список.
    """
    url = "https://engine.lifeis.porn/api/millionaire.php"
    response = requests.get(url, params={
                            "difficulty": q_type,
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
        log(f"Time is sleeping {delay} sec")
        sleep(delay)
        delay = min(delay * 2, MAX_DELAY)
        return get_questions(q_type, q_count, delay)

    else:
        return []


def fix_text_question(questions: List[Dict]) -> List[Dict]:
    """
    Исправляет текст в переданных вопросах
    """
    for question in questions:
        text = question["question"]
        fix_text = text.replace("\u2063", "")
        question["question"] = fix_text

    return questions


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


def main():
    parser = argparse.ArgumentParser(description="Указатель пути")
    parser.add_argument("-file", type=str, help="Путь к файлу")
    args = parser.parse_args()

    all_questions = get_all_questions(250)
    fix_text_question(all_questions)
    save_to_file(all_questions, Path(args.file))


# Запускать только при выполнение, как скрипт
if __name__ == "__main__":
    main()
