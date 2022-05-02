from pathlib import Path
from typing import Union

import yaml


def read_config(path: Union[Path, str], encoding: str="utf-8") -> dict:
    if isinstance(path, str):
        path = Path(path)
    if not path.exist():
        raise FileNotFoundError

    with open(path, mode='r', encoding=encoding) as file:
        return yaml.safe_load(file)


def write_config(path: Union[Path, str], data: dict, encoding: str="utf-8"):
    if isinstance(path, str):
        path = Path(path)

    with open(path, mode='w', encoding=encoding) as file:
        yaml.safe_dump(data, file)
