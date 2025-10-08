from typing import List, Optional
from profiler.validators.validator_executer import validate_pddl


def is_valid_plan(pddl_domain: str, pddl_problem, plan: List[str]) -> Optional[bool]:
    return validate_pddl(pddl_domain, pddl_problem, "\n".join(plan))
