import asyncio
import time


# q = [Question("tedt", ["1", "2"], 2, Question.Difficulty.MEDIUM, 1)]
# q_json = Question.schema().dump(q, many=True)
# q_str = JSONEncoder().encode(q_json)
# # you can save q_str to a file and load later
# q_restored_json = JSONDecoder().decode(q_str)
# q_restored = Question.schema().load(q_restored_json, many=True)
# print(q == q_restored)


def count():
    print("One")
    time.sleep(3)
    print("Two")


def main():
    for _ in range(3):
        count()


if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")