from core.random import Random


class DoNothingRandom(Random):
    def shuffle(self, data: list) -> None:
        pass


class ReversedShuffleRandom(Random):
    def shuffle(self, data: list) -> None:
        data.reverse()
