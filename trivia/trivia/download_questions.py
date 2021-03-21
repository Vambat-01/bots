import requests
from typing import List, Dict
import json
from pathlib import Path
from itertools import chain
from core.utils import log
from time import sleep


all_questions: List[Dict] = []
file_path = Path("/home/vambat/projects/bots/trivia/resources/database_questions_for_bot.json")


def get_questions(q_type: int, q_count: int, delay: int) -> List[Dict]:
    """
    Получает вопросы для заполнения SQLite базы данных
    :param q_type: тип сложности получаемого вопрос
    :param q_count: количество полученных вопросов
    :param delay: задержка между вызовами
    """

    url = "https://engine.lifeis.porn/api/millionaire.php"
    response = requests.get(url, params={
                            "difficulty": q_type,
                            "count": q_count
                            })

    log(f"Send message status code: {response.status_code} ")

    if response.status_code == 200:
        questions_json = response.json()
        data = questions_json["data"]

        for question in data:
            question["difficulty"] = q_type
        delay = 1
        return data

    elif response.status_code == 429:
        sleep(delay)
        log(f"Time is sleepiing {delay} sec")
        delay = min(delay * 2, 300)
        return get_questions(q_type, q_count, delay)

    else:
        return []


def fixed_text_question(questions: List[Dict]) -> List[Dict]:
    """
    Исправляет текст вопроса
    :param questions: список вопросов
    :return: список вопросов и справленным текстом
    """
    for question in questions:
        text = question["question"]
        fix_text = text.replace("\u2063", "")
        question["question"] = fix_text

    return questions


def save_to_file(questions: List[Dict], file_path: Path):
    """
    Записывает вопросы в файл в формате json
    :param questions: список вопросов
    :param file_path: путь к файлу
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=4)


while len(all_questions) < 250:
    easy = get_questions(1, 5, 1)
    medium = get_questions(2, 5, 1)
    hard = get_questions(3, 5, 1)

    for question in chain(easy, medium, hard):
        all_questions.append(question)

fixed_text_question(all_questions)
save_to_file(all_questions, file_path)
