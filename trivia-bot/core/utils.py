import textwrap
from typing import Union
import hashlib


JsonDict = dict     # Словарь для хранения данных в Json формате

JsonList = list     # Список для хранения данных в Json формате

Json = Union[JsonDict, JsonList]      # Данные в Json формате


def dedent_and_strip(text: str):
    return textwrap.dedent(text).strip()


def get_sha256_hash(obj: str) -> str:
    """
    Шифрует данные преобразуя их в цифровой отпечаток длинны 256 бит
    :param obj: обьект который будет зашифрован
    """
    sha = hashlib.sha256()
    tok = obj.encode()
    sha.update(tok)
    sha_token = sha.hexdigest()
    return sha_token
