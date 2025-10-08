from typing import List
from ai_profiling.helpers.hash_helper.hash_helper import get_plan_hash


def are_optimal_plans(plans_not_validated: List[List[str]], plans_optimal: List[List[str]]) -> List[bool]:
    """
    return a list of a status for optimal plan
    """
    hashs_not_validated_plans = list(map(lambda plan: get_plan_hash(plan), plans_not_validated))
    hashs_optimal_plans = set(map(lambda plan: get_plan_hash(plan), plans_optimal))
    return list(
        map(lambda hash_not_validated_plan: hash_not_validated_plan in hashs_optimal_plans, hashs_not_validated_plans)
    )
