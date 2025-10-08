from typing import List, Tuple
from ai_profiling.helpers.planner_helper.planner_helper_datatypes import PlanQuality
from ai_profiling.helpers.planner_helper.plan_comparison_helper import are_optimal_plans
from ai_profiling.helpers.planner_helper.plan_validation_helper import is_valid_plan


def get_plan_quality(
    plans_not_validated: List[List[str]], plans_optimal: List[List[str]], pddl_domain: str, pddl_problem: str
) -> List[PlanQuality]:
    optimal_plan_statuses = are_optimal_plans(plans_not_validated, plans_optimal)
    plan_validation_results: List[Tuple[bool, bool]] = list(
        map(lambda plan: is_valid_plan(pddl_domain, pddl_problem, plan))
    )
    plan_qualities: List[PlanQuality] = list()
    for i in range(len(optimal_plan_statuses)):
        plan_qualities.append(
            PlanQuality(
                is_optimal_plan=optimal_plan_statuses[i],
                is_executable_plan=plan_validation_results[i][0],
                is_valid_plan=plan_validation_results[i][1],
            )
        )
    return plan_qualities
