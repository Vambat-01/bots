from pathlib import Path
import json
from typing import List
from trivia.question_storage import Question, SqliteQuestionStorage
import argparse


def get_questions_from_file(file_path: Path) -> List[Question]:
    """
    Получить список вопросов из json файла, обработать их и вернуть список вопросов
    """
    with open(file_path) as json_file:
        data = json.load(json_file)

    all_questions = []
    for question in data:
        text = question["question"]
        answers = question["answers"]
        difficulty = question["difficulty"]
        all_questions.append(Question(text, answers, difficulty + 1, difficulty, 0))
    return all_questions


def main():
    parser = argparse.ArgumentParser(description="Указатель пути")
    parser.add_argument("-file", type=str, help="Путь к файлу")
    parser.add_argument("-db", type=str, help="Путь к базе данных")
    args = parser.parse_args()

    all_questions = get_questions_from_file(Path(args.file))
    storage = SqliteQuestionStorage.create_in_file(Path(args.db))
    storage.add_questions(all_questions)


# Запускать только при выполнение, как скрипт
if __name__ == "__main__":
    main()
