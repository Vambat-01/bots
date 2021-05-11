import textwrap
from typing import Any


JsonDict = dict     # Словарь для хранения данных в Json формате

Json = Any      # Данные в Json формате


def dedent_and_strip(text: str):
    return textwrap.dedent(text).strip()
