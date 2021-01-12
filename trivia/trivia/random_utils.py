from random import shuffle
from core.random import Random


class RandomImpl(Random):

    def shuffle(self, data: list) -> None:
        shuffle(data)
