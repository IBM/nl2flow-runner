import hashlib
from typing import Any, List


def get_hash(data: Any) -> str:
    dhash = hashlib.md5()
    dhash.update(data)
    return dhash.hexdigest()


def get_list_hash(lst: List) -> str:
    return get_hash(bytearray(str(tuple(lst)), "utf-8"))


def format_plan(actions: List[str]) -> List[str]:
    """
    returns formatted plan and a hash
    """
    formatted_actions: List[str] = list()
    for action in actions:
        action_str = action[1:-1]
        terms = action_str.split(" ")
        # handle slot filler here
        if len(terms) > 1:
            parameters = terms[1:]
            parameters.sort()  # sort parameter names
            formatted_action_str = "(" + " ".join([terms[0][:]] + parameters) + ")"
            formatted_actions.append(formatted_action_str)
        else:
            formatted_actions.append(action[:])
    return formatted_actions


def get_plan_hash(plan: List[str]) -> str:
    return get_list_hash(format_plan(plan))
