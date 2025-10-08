from typing import List, Tuple
from ai_profiling.helpers.str_helper.str_helper_variables import pddl_domain_start_key, pddl_problem_start_key


def get_idx_list_str(lines: List[str], str_to_match: str) -> int:
    for idx, line in enumerate(lines):
        if str_to_match in line:
            return idx
    return len(lines)


def get_idxs_list_str(lines: List[str], str_to_match: str) -> List[int]:
    idxs: List[int] = list()
    for idx, line in enumerate(lines):
        if str_to_match in line:
            idxs.append(idx)
    return idxs


def get_pddl_strs(response: str) -> Tuple[str, str]:
    lines = response.split("\n")
    idx_pddl_domain_start = get_idx_list_str(lines, pddl_domain_start_key)
    idx_pddl_problem_start = get_idx_list_str(lines, pddl_problem_start_key)
    pddl_doamin_str = "\n".join(lines[idx_pddl_domain_start:idx_pddl_problem_start])
    pddl_problem_str = "\n".join(lines[idx_pddl_problem_start:])
    return pddl_doamin_str, pddl_problem_str
