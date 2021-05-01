import textwrap


JsonDict = dict     # Словарь для хранения данных в Json формате


def dedent_and_strip(text: str):
    return textwrap.dedent(text).strip()
