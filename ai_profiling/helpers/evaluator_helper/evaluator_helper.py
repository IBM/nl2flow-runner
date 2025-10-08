from pathlib import Path
import subprocess
from typing import List

from ai_profiling.generators.planning_data_generator_datatypes import ValOutputModel


def convert_nl2flow_plan_to_pddl_plan(plan_nl2flow_txt: str) -> str:
    action_line: List[str] = []
    for line in plan_nl2flow_txt.split("\n"):
        idx = line.find("=")
        if idx == -1:
            idx = 0
        elif idx < (len(line) - 1):
            idx = idx + 1
        action_str = line[idx:]
        action_str = action_str.replace("(", " ").replace(")", " ").replace(",", " ")
        token_list: List[str] = []
        for token in action_str.split(" "):
            token = token.strip()
            if len(token) > 0:
                token_list.append(token)

        if len(token_list) > 0:
            token_str = " ".join(token_list)
            action_line.append("(" + token_str + ")")

    return "\n".join(action_line)


def get_cost_form_val_output_txt(val_txt: str) -> int:
    cost = -1
    lines = val_txt.split("\n")
    for line in lines:
        if "final value:" in line:
            idx = line.find(":")
            try:
                cost = int(line[idx + 1 :].strip())  # noqa: E203
            except Exception as e:
                print(e)
                print("Val cost parsing failied")
    return cost


def parse_val_txt(val_txt: str, optimal_cost: int) -> ValOutputModel:
    if len(val_txt) == 0:
        return ValOutputModel()

    is_executable = "executed successfully" in val_txt
    reach_goals = "plan valid" in val_txt
    cost = get_cost_form_val_output_txt(val_txt=val_txt)

    return ValOutputModel(
        is_optimal=(is_executable and reach_goals and cost == optimal_cost),
        is_valid=(is_executable and reach_goals),
        is_executable=is_executable,
        reach_goals=reach_goals,
        cost=cost,
        output_txt=val_txt,
    )


def validate_pddl_plan(
    val_path: Path, domain_file: Path, problem_file: Path, plan_file: Path, cost: int
) -> ValOutputModel:
    """Validates a PDDL plan using VAL."""

    command = [str(val_path), str(domain_file), str(problem_file), str(plan_file), "-v"]
    output_txt: str = ""
    error_message: str = ""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output_txt = result.stdout.lower()
    except subprocess.CalledProcessError as e:
        error_message = str(e.stderr)

    val_output_model = parse_val_txt(val_txt=output_txt, optimal_cost=cost)
    val_output_model.error_message = error_message

    return val_output_model
