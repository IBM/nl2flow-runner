import os.path as path
from pathlib import Path
import ai_profiling

# Planning example text
planning_example_file_path = path.join(
    path.dirname(path.abspath(ai_profiling.__file__)),
    "data/text_files/planning_examples.txt",
)
PLANNING_EXAMPLES_TEXT = ""
if Path(planning_example_file_path).is_file():
    with open(planning_example_file_path, "r") as f:
        PLANNING_EXAMPLES_TEXT = f.read()

# Concise planning example text
concise_planning_example_file_path = path.join(
    path.dirname(path.abspath(ai_profiling.__file__)),
    "data/text_files/concise_planning_examples.txt",
)
CONCISE_PLANNING_EXAMPLES_TEXT = ""
if Path(concise_planning_example_file_path).is_file():
    with open(concise_planning_example_file_path, "r") as f:
        CONCISE_PLANNING_EXAMPLES_TEXT = f.read()

# json example text
json_example_file_path = path.join(
    path.dirname(path.abspath(ai_profiling.__file__)),
    "data/text_files/json_examples.txt",
)
JSON_EXAMPLES_TEXT = ""
if Path(json_example_file_path).is_file():
    with open(json_example_file_path, "r") as f:
        JSON_EXAMPLES_TEXT = f.read()

INSTRUCTION_TEXT = (
    "Develop a concise plan to achieve the goals. The shorter plan is preferable."
    + " A plan consists of individual actions, each represented by its outputs and an action name followed"
    + " by its parameters in parentheses (e.g., outputs = <action-name>(<parameters>). When it becomes impossible"
    + " to achieve the objectives, the appropriate course of action should be considered as 'no plan'"
)
INSTRUCTION_OBJECT_CREATION_TEXT = "Write a json to describe the context."
EXAMPLE_INTRODUCTION_TEXT = "Here are some examples."
CONTEXT_HEADER = "CONTEXT"
INSTRUCTION_HEADER = "INSTRUCTION"
PLAN_EXPLANATION_FORWARD_HEADER = "PLAN EXPLANATION"
PLAN_HEADER = "PLAN"
JSON_HEADER = "JSON"
PLAN_REQUEST_TEXT = "Now output your plan explanation and plan.\n{plan_explanation_and_plan}"
JSON_REQUEST_TEXT = "Now output your json.\n{json}"
NO_PLAN = "no plan"
