from pathlib import Path
import json
from typing import List, Dict
from trivia.question_storage import Question, SqliteQuestionStorage


file_path = Path("/home/vambat/projects/bots/trivia/resources/database_questions_for_bot.json")
file_path_db = Path("/home/vambat/Desktop/questions_and_answers.db")


def get_questions_from_file(file_path: Path) ->List[Dict]:
    """
    Получить список вопросов из json файла
    :param file_path: пусть к файлу
    :return: список вопросов
    """
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def get_all_questions(questions: List[Dict]) -> List[Question]:
    """
    Заполняет таблицы в SQLite базе данных
    :param questions: список вопросов из json файла
    :return: список вопросов
    """
    all_questions = []
    for question in questions:
        text = question["question"]
        answers = question["answers"]
        difficulty = question["difficulty"]
        all_questions.append(Question(text, answers, difficulty + 1, difficulty, 0))
    return all_questions


data = get_questions_from_file(file_path)
all_questions = get_all_questions(data)
SqliteQuestionStorage.create_database(file_path_db)
storage = SqliteQuestionStorage.create_in_file(file_path_db)
storage.add_questions(all_questions)


