from pathlib import Path
from trivia.question_storage import SqliteQuestionStorage, JsonQuestionStorage
import argparse


def main():
    parser = argparse.ArgumentParser(description="Указатель пути")
    parser.add_argument("-file", type=str, help="Путь к файлу")
    parser.add_argument("-db", type=str, help="Путь к базе данных")
    args = parser.parse_args()

    storage = JsonQuestionStorage(Path(args.file))
    questions = storage.load_questions()

    storage = SqliteQuestionStorage.create_in_file(Path(args.db))
    storage.add_questions(questions)


if __name__ == "__main__":
    main()
