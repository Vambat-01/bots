import textwrap
import datetime


def dedent_and_strip(text: str):
    return textwrap.dedent(text).strip()


def log(message: str) -> None:
    """
        Выводит текущее время и сообщение
    :param message: полученное сообщение
    :return: None
    """
    time_now = datetime.datetime.now()
    print(f"{time_now} {message}")


