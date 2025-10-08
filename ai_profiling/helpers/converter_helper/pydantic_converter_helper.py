from typing import List

from pydantic import BaseModel


def convert_basemodels_to_dicts(lst: List[BaseModel]) -> List:
    return list(map(lambda model: model.model_dump(), lst))
