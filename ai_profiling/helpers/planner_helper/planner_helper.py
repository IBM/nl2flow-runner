from copy import deepcopy
import json
from nl2flow.plan.planner import Planner
from nl2flow.compile.schemas import PDDL
from typing import Dict, List, Optional, Tuple
from ai_profiling.helpers.str_helper.str_helper import get_idxs_list_str
from ai_profiling.helpers.planner_helper.planner_helper_variables import (
    pretty_plan_start_key,
    round_removal_pattern,
    round_removal_group_pattern,
)
import re


def get_pddl_name(input: str) -> str:
    return input.replace(",", "").strip().replace(" ", "_")


def remove_type_information_in_pretty_plan(input: str) -> str:
    result = re.sub(round_removal_pattern, round_removal_group_pattern, input)
    return result.strip()


def transform_pretty_plan_action_to_pddl_action(action_str: str) -> Optional[str]:
    if "Step" not in action_str or "Inputs:" not in action_str or "Outputs:" not in action_str:
        return None
    idx_inputs = action_str.index("Inputs:")
    idx_outputs = action_str.index("Outputs:")
    action_elements: List[str] = list()
    # action name
    action_name_segment = action_str[0:idx_inputs].strip()
    action_elements.append(get_pddl_name(action_name_segment.split(":")[1]))
    # input parameters
    input_names_segment = remove_type_information_in_pretty_plan(action_str[idx_inputs:idx_outputs].strip())
    input_names = list(
        filter(
            lambda name: len(name) > 0,
            map(lambda variable: get_pddl_name(variable), input_names_segment.split(":")[1].split(",")),
        )
    )
    if not (len(input_names) == 1 and input_names[0] == "None"):
        action_elements.extend(input_names)

    return "(" + " ".join(action_elements) + ")"


def transform_pretty_plan_to_raw_plan(pretty_plan: str) -> List[List[str]]:
    """
    return a list of plans with actions
    """
    lines = pretty_plan.splitlines()
    plan_start_idxs = get_idxs_list_str(lines, pretty_plan_start_key)
    plans: List[List[str]] = list()
    if len(plan_start_idxs) == 0:
        return []
    for i, plan_start_idx in enumerate(plan_start_idxs):
        end_idx = len(lines) if i == len(plan_start_idxs) - 1 else plan_start_idxs[i + 1]
        plan_lines = lines[plan_start_idx:end_idx]
        plans.append([])
        for plan_line in plan_lines:
            action_str = transform_pretty_plan_action_to_pddl_action(plan_line)
            if action_str is not None:
                plans[-1].append(action_str)
    return plans


def transform_llm_action_to_pddl_action(llm_action_str: str) -> str:
    segments = llm_action_str.split(". ")
    action_str = segments[1]
    action_str = action_str.replace("(", " ")
    action_str = action_str.replace(",", "")
    action_str = "(" + action_str
    return action_str if action_str[-1] == ")" else action_str + ")"


def transform_LLM_plan_to_raw_plan(llm_plan: str) -> Tuple[List[str], List[str]]:
    """
    return a list of actions and a list of debugger messages
    """
    lines = llm_plan.splitlines()
    actions: List[str] = list()
    debug_messages: List[str] = list()
    for line in lines:
        if len(line) > 0 and line[0].isnumeric():
            if "No plan for Action" in line:  # handle a debug message
                debug_messages.append(line)
            else:  # handle an action
                actions.append(transform_llm_action_to_pddl_action(line))
    return actions, debug_messages


def trim_actions(plans_input: List[Dict]) -> List[Dict]:
    plans = deepcopy(plans_input)
    for idx, plan_input in enumerate(plans):
        if "actions" in plan_input:
            actions: List[str] = list()
            for action in plan_input["actions"]:
                actions.append(action.strip())
            plan_input["actions"] = actions
    return plans


def get_plans(pddl_domain: str, pddl_problem: str, planner: Planner) -> Optional[List[Dict]]:
    """
    returns plans in str
    """
    pddl = PDDL(domain=pddl_domain, problem=pddl_problem)
    response = planner.plan(pddl=pddl)
    if response.status_code == 200:
        response_dict = json.loads(response.text)
        return trim_actions(response_dict["plans"])
    return None
