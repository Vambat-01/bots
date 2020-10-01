from typing import List


class Question:
    def __init__(self, text: str, answers: List[str], points: int):
        self.text = text
        self.answers = answers
        self.points = points


def add_one(x: int) -> int:
    return x + 2
