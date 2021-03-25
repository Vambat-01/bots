from pathlib import Path
import json
from typing import List, Dict
from trivia.question_storage import SqliteQuestionStorage
from trivia.download_questions import get_normalize_questions
import argparse


def get_questions_from_file(file_path: Path) -> List[Dict]:
    """
    Получить список вопросов из json файла, обработать их и вернуть список вопросов
    """
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


def main():
    parser = argparse.ArgumentParser(description="Указатель пути")
    parser.add_argument("-file", type=str, help="Путь к файлу")
    parser.add_argument("-db", type=str, help="Путь к базе данных")
    args = parser.parse_args()

    questions = get_questions_from_file(Path(args.file))
    all_questions = get_normalize_questions(questions)
    storage = SqliteQuestionStorage.create_in_file(Path(args.db))
    storage.add_questions(all_questions)


# Запускать только при выполнение, как скрипт
if __name__ == "__main__":
    main()
