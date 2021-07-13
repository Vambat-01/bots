import textwrap
from typing import Union


JsonDict = dict     # Словарь для хранения данных в Json формате

JsonList = list     # Список для хранения данных в Json формате

Json = Union[JsonDict, JsonList]      # Данные в Json формате


def dedent_and_strip(text: str):
    return textwrap.dedent(text).strip()
