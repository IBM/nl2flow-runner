from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel
from ai_profiling.data.prompt_templates import (
    CONCISE_PLANNING_EXAMPLES_TEXT,
    CONTEXT_HEADER,
    EXAMPLE_INTRODUCTION_TEXT,
    INSTRUCTION_HEADER,
    INSTRUCTION_OBJECT_CREATION_TEXT,
    INSTRUCTION_TEXT,
    JSON_EXAMPLES_TEXT,
    JSON_HEADER,
    JSON_REQUEST_TEXT,
    NO_PLAN,
    PLAN_EXPLANATION_FORWARD_HEADER,
    PLAN_HEADER,
    PLAN_REQUEST_TEXT,
    PLANNING_EXAMPLES_TEXT,
)
from ai_profiling.datatypes.planning_datatype import AgentInfoUnitModel
from ai_profiling.datatypes.service_datatype import LLM_SERVICELlmTrainingDataModel
from ai_profiling.helpers.file_helper.file_helper import (
    get_base_models_from_jsonl,
    get_file_path,
    write_datasetdict_file_from_jsonls,
    write_jsonl,
)
from ai_profiling.helpers.prompt_helper.planner_prompt_helper_variable import (
    description_to_pddl_instruction_prompt,
    description_plan_prompt,
    tarski_description,
    description_to_tarski_Conversion_instruction,
    plan_instruction_prompt,
    pddl_domain_problem_introduction_prompt,
    description_to_pddl_introduction_prompt,
)
from profiler.converters.info_2_flow_converter import get_flow_from_agent_infos
from profiler.generators.description_generator.description_generator import (
    get_sample_description,
)
from profiler.generators.description_generator.description_generator_helper import (
    get_concise_description,
)
from profiler.data_types.agent_info_data_types import AgentInfo
from profiler.data_types.generator_data_type import (
    PlanningInputDescriptionMode,
)
from nl2flow.plan.planners.kstar import Kstar
from profiler.data_types.pddl_generator_datatypes import PddlGeneratorOutput
from nl2flow.printers.codelike import CodeLikePrint
from nl2flow.printers.verbalize import VerbalizePrint


def get_prompt_description_to_plan(description: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return "Text description:\n" + description + "\n" + description_plan_prompt
    if model == "gpt-3":
        return "Text description:\n" + description + "\n" + description_plan_prompt
    return "Text description:\n" + description + "\n" + description_plan_prompt


def get_prompt_description_to_tarski(description: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return ""
    if model == "gpt-3":
        return ""
    return (
        tarski_description
        + description_to_tarski_Conversion_instruction
        + "\n\n"
        + "Text description:\n"
        + description
        + "\n"
        + "Python code:\n"
    )


def get_prompt_description_to_code(description: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return ""
    if model == "gpt-3":
        return ""
    return "Text description:\n" + description + "\n" + "Write the description in Python.\n"


def get_prompt_description_to_pddl(description: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return ""
    if model == "gpt-3":
        return ""
    return (
        description_to_pddl_introduction_prompt
        + "\n\n"
        + "Text description:\n"
        + description
        + "\n"
        + description_to_pddl_instruction_prompt
    )


def get_prompt_description_paraphrasing(description: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return ""
    if model == "gpt-3":
        return ""
    return "Text description:\n" + description + "\n" + "Paraphrase this text.\n"


def get_prompt_python_to_pddl(code: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return ""
    if model == "gpt-3":
        return ""
    return "Python:\n" + code + "\n" + "Convert the flow from Python to Planning Domain Definition Language (PDDL).\n"


def get_prompt_python_to_plan(code: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return ""
    if model == "gpt-3":
        return ""
    return (
        "Python:\n"
        + code
        + "\n"
        + "Use information described in the python code to Come up with a plan made of action names and parameters."
        + " Give only action names and parameters as <action-name>(<paramaters>) and nothing else.\n"
    )


def get_prompt_pddl_to_plan(pddl_domain: str, pddl_problem: str, model: str = "gpt-4") -> str:
    if model == "gpt-3.5-turbo":
        return ""
    if model == "gpt-3":
        return ""
    return (
        pddl_domain_problem_introduction_prompt
        + "\n\n"
        + "PDDL Domain:\n"
        + pddl_domain
        + "\n\nPDDL Problem:\n"
        + pddl_problem
        + "\n"
        + plan_instruction_prompt
    )


def get_general_planning_example_prompt(
    available_agents: List[AgentInfo],
    goal_agent_ids: Set[str],
    mappings: List[Tuple[str, str, float]],
    available_data: List[Tuple[str, Optional[str]]],
) -> str:
    flow_obj = get_flow_from_agent_infos(
        available_agents=available_agents,
        mappings=mappings,
        goals=goal_agent_ids,
        available_data=available_data,
    )

    PLANNER = Kstar()
    planner_response = flow_obj.plan_it(PLANNER)

    prompt: List[str] = []

    # planning problem
    prompt.append(CONTEXT_HEADER)
    prompt.append(
        get_sample_description(
            available_agents=available_agents,
            goal_agent_ids=goal_agent_ids,
            mappings=mappings,
            available_data=available_data,
        )
    )
    # planning instruction
    prompt.append(INSTRUCTION_HEADER)
    prompt.append(INSTRUCTION_TEXT)
    # plan explanation (forward)
    prompt.append(PLAN_EXPLANATION_FORWARD_HEADER)
    plan_explanation_forward_text = (
        VerbalizePrint.pretty_print_plan(
            planner_response.list_of_plans[0],
            flow_object=flow_obj,
            lookahead=True,
        )
        if len(planner_response.list_of_plans) > 0
        else NO_PLAN
    )
    prompt.append(plan_explanation_forward_text)
    # plan
    prompt.append(PLAN_HEADER)
    plan_text = (
        CodeLikePrint.pretty_print_plan(planner_response.list_of_plans[0])
        if len(planner_response.list_of_plans) > 0
        else NO_PLAN
    )
    prompt.append(plan_text)

    return "\n".join(prompt)


def get_general_object_creation_example_prompt(
    available_agents: List[AgentInfo],
    goal_agent_ids: List[str],
    mappings: List[Tuple[str, str, float]],
    available_data: List[Tuple[str, Optional[str]]],
) -> str:
    prompt: List[str] = []

    # planning problem
    prompt.append(CONTEXT_HEADER)
    prompt.append(
        get_sample_description(
            available_agents=available_agents,
            goal_agent_ids=goal_agent_ids,
            mappings=mappings,
            available_data=available_data,
        )
    )
    # planning instruction
    prompt.append(INSTRUCTION_HEADER)
    prompt.append(INSTRUCTION_OBJECT_CREATION_TEXT)
    # json
    prompt.append(JSON_HEADER)
    agent_info_unit_model = AgentInfoUnitModel(
        available_agents=available_agents,
        goal_agent_ids=goal_agent_ids,
        mappings=mappings,
        available_data=available_data,
    )
    prompt.append(agent_info_unit_model.get_simple_planning_model_json_str())

    return "\n".join(prompt)


def get_concise_planning_example_prompt(
    available_agents: List[AgentInfo],
    goal_agent_ids: Set[str],
    mappings: List[Tuple[str, str, float]],
    available_data: List[Tuple[str, Optional[str]]],
) -> str:
    flow_obj = get_flow_from_agent_infos(
        available_agents=available_agents,
        mappings=mappings,
        goals=goal_agent_ids,
        available_data=available_data,
    )

    PLANNER = Kstar()
    planner_response = flow_obj.plan_it(PLANNER)

    prompt: List[str] = []

    # planning problem
    prompt.append(CONTEXT_HEADER)
    # concise planning problem description
    agent_info_unit_model = AgentInfoUnitModel(
        available_agents=available_agents,
        goal_agent_ids=goal_agent_ids,
        mappings=mappings,
        available_data=available_data,
    )
    prompt.append(get_concise_description(simple_planning_model=agent_info_unit_model.get_simple_planning_model()))
    # planning instruction
    prompt.append(INSTRUCTION_HEADER)
    prompt.append(INSTRUCTION_TEXT)
    # plan explanation (forward)
    prompt.append(PLAN_EXPLANATION_FORWARD_HEADER)
    plan_explanation_forward_text = (
        VerbalizePrint.pretty_print_plan(
            planner_response.list_of_plans[0],
            flow_object=flow_obj,
            lookahead=True,
        )
        if len(planner_response.list_of_plans) > 0
        else NO_PLAN
    )
    prompt.append(plan_explanation_forward_text)
    # plan
    prompt.append(PLAN_HEADER)
    plan_text = (
        CodeLikePrint.pretty_print_plan(planner_response.list_of_plans[0])
        if len(planner_response.list_of_plans) > 0
        else NO_PLAN
    )
    prompt.append(plan_text)

    return "\n".join(prompt)


def get_planning_prompt(planning_problem: str) -> str:
    prompt: List[str] = []
    prompt.append(CONTEXT_HEADER)
    prompt.append(planning_problem)
    prompt.append(INSTRUCTION_HEADER)
    prompt.append(INSTRUCTION_TEXT)
    prompt.append("\n")
    prompt.append(EXAMPLE_INTRODUCTION_TEXT)
    prompt.append("\n")
    prompt.append(PLANNING_EXAMPLES_TEXT)
    prompt.append("\n")
    prompt.append(PLAN_REQUEST_TEXT)

    return "\n".join(prompt)


def get_planning_prompt_for_training(planning_problem: str, instruction_txt: str) -> str:
    prompt: List[str] = []
    prompt.append(CONTEXT_HEADER)
    prompt.append(planning_problem)
    prompt.append(INSTRUCTION_HEADER)
    prompt.append(instruction_txt)

    return "\n".join(prompt)


def get_concise_planning_prompt(planning_problem: str) -> str:
    prompt: List[str] = []
    prompt.append(CONTEXT_HEADER)
    prompt.append(planning_problem)
    prompt.append(INSTRUCTION_HEADER)
    prompt.append(INSTRUCTION_TEXT)
    prompt.append("\n")
    prompt.append(EXAMPLE_INTRODUCTION_TEXT)
    prompt.append("\n")
    prompt.append(CONCISE_PLANNING_EXAMPLES_TEXT)
    prompt.append("\n")
    prompt.append(PLAN_REQUEST_TEXT)

    return "\n".join(prompt)


# def get_planning_prompt_for_training(planning_problem: str) -> str:
#     prompt: List[str] = []
#     prompt.append(CONTEXT_HEADER)
#     prompt.append(planning_problem)
#     prompt.append(INSTRUCTION_HEADER)
#     prompt.append(INSTRUCTION_OBJECT_CREATION_TEXT)

#     return "\n".join(prompt)


def get_planning_object_prompt(planning_problem: str) -> str:
    prompt: List[str] = []
    prompt.append(CONTEXT_HEADER)
    prompt.append(planning_problem)
    prompt.append(INSTRUCTION_HEADER)
    prompt.append(INSTRUCTION_OBJECT_CREATION_TEXT)
    prompt.append("\n")
    prompt.append(EXAMPLE_INTRODUCTION_TEXT)
    prompt.append("\n")
    prompt.append(JSON_EXAMPLES_TEXT)
    prompt.append("\n")
    prompt.append(JSON_REQUEST_TEXT)

    return "\n".join(prompt)


def get_optimal_plan_str_from_prretified_plan_str(prettified_plan_str: str) -> str:
    # ignore lines not starting with [
    # stop when the number within [] descrease
    response_str_list: List[str] = []
    max_action_sequence = -1
    action_sequence = -1
    for line in prettified_plan_str.splitlines():
        if len(line) > 0 and line.startswith("["):
            close_bracket_index = line.index("]")
            if close_bracket_index <= 1:
                continue
            try:
                action_sequence = int(line[1:close_bracket_index])
            except Exception as e:
                print(e)
                action_sequence = -1
            if action_sequence <= max_action_sequence:
                break

            response_str_list.append(line[:])
            max_action_sequence = action_sequence

    return "\n".join(response_str_list)


def get_llm_response_example_plan(pddl_generator_output: PddlGeneratorOutput) -> str:
    response_str_list: List[str] = []
    response_str_list.append(PLAN_EXPLANATION_FORWARD_HEADER)
    response_str_list.append(
        NO_PLAN
        if len(pddl_generator_output.list_of_plans) == 0
        else pddl_generator_output.prettified_optimal_plan_forward
    )
    response_str_list.append(PLAN_HEADER)
    response_str_list.append(
        NO_PLAN
        if len(pddl_generator_output.list_of_plans) == 0
        else get_optimal_plan_str_from_prretified_plan_str(pddl_generator_output.prettified_plans)
    )

    return "\n".join(response_str_list)


def get_llm_response_example_json_translation(
    pddl_generator_output: PddlGeneratorOutput,
) -> str:
    response_str_list: List[str] = []
    response_str_list.append(JSON_HEADER)
    response_str_list.append(
        pddl_generator_output.agent_info_generator_output_item.describe(
            planning_input_description_mode=PlanningInputDescriptionMode.JSON
        )
    )

    return "\n".join(response_str_list)


def get_LLM_SERVICE_llm_training_model_from_pddl_generator_output_description_to_plan(
    pddl_generator_output: PddlGeneratorOutput,
    planning_input_description_mode: PlanningInputDescriptionMode,
) -> LLM_SERVICELlmTrainingDataModel:
    return LLM_SERVICELlmTrainingDataModel(
        input=get_planning_prompt_for_training(
            planning_problem=pddl_generator_output.agent_info_generator_output_item.describe(
                planning_input_description_mode=planning_input_description_mode
            ),
            instruction_txt=INSTRUCTION_TEXT,
        ),
        output=get_llm_response_example_plan(pddl_generator_output=pddl_generator_output),
        sample_hash=pddl_generator_output.sample_hash,
    )


def get_LLM_SERVICE_llm_training_model_from_pddl_generator_output_description_to_json(
    pddl_generator_output: PddlGeneratorOutput,
    planning_input_description_mode: PlanningInputDescriptionMode,
) -> LLM_SERVICELlmTrainingDataModel:
    return LLM_SERVICELlmTrainingDataModel(
        input=get_planning_prompt_for_training(
            planning_problem=pddl_generator_output.agent_info_generator_output_item.describe(
                planning_input_description_mode=planning_input_description_mode
            ),
            instruction_txt=INSTRUCTION_OBJECT_CREATION_TEXT,
        ),
        output=get_llm_response_example_json_translation(pddl_generator_output=pddl_generator_output),
        sample_hash=pddl_generator_output.sample_hash,
    )


def get_LLM_SERVICE_training_data_planning_from_pddl_generator_outputs(
    pddl_generator_outputs: List[PddlGeneratorOutput],
    planning_input_description_mode: PlanningInputDescriptionMode,
    file_path_without_extension: str,
    mark_word: str,
) -> str:
    # convert to LLM_SERVICE training data format
    LLM_SERVICE_training_models: List[LLM_SERVICELlmTrainingDataModel] = list(
        map(
            lambda model: get_LLM_SERVICE_llm_training_model_from_pddl_generator_output_description_to_plan(
                model, planning_input_description_mode
            ),
            pddl_generator_outputs,
        )
    )
    # write jsonl file
    file_path_LLM_SERVICE_training = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=[mark_word, "llm", "planning", planning_input_description_mode],
        extension="jsonl",
    )
    write_jsonl(file_path=file_path_LLM_SERVICE_training, base_models=LLM_SERVICE_training_models)

    return file_path_LLM_SERVICE_training


def get_LLM_SERVICE_training_data_translation_from_pddl_generator_outputs(
    pddl_generator_outputs: List[PddlGeneratorOutput],
    planning_input_description_mode: PlanningInputDescriptionMode,
    file_path_without_extension: str,
    mark_word: str,
) -> str:
    # convert to LLM_SERVICE training data format
    LLM_SERVICE_training_models: List[LLM_SERVICELlmTrainingDataModel] = list(
        map(
            lambda model: get_LLM_SERVICE_llm_training_model_from_pddl_generator_output_description_to_json(
                model, planning_input_description_mode
            ),
            pddl_generator_outputs,
        )
    )
    # write jsonl file
    file_path_LLM_SERVICE_training = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=[
            mark_word,
            "LLM_SERVICE",
            "translation",
            planning_input_description_mode,
        ],
        extension="jsonl",
    )
    write_jsonl(file_path=file_path_LLM_SERVICE_training, base_models=LLM_SERVICE_training_models)

    return file_path_LLM_SERVICE_training


def parse_llm_planner_response(response: str, available_agents: List[AgentInfo]) -> Optional[List[str]]:
    if NO_PLAN in response:
        return []

    split_text = PLAN_HEADER + "\n"
    plan_start_idx = response.rfind(split_text)
    if plan_start_idx == -1:
        return None

    if (plan_start_idx + len(split_text)) > (len(response) - 1):
        return []

    plan_response = response[(plan_start_idx + len(split_text)) :]  # noqa: E203

    if len(plan_response) == 0:
        return []

    plan: List[str] = []
    action_name_input_parameters_dict: Dict[str, List[str]] = {}

    for available_agent in available_agents:
        action_name_input_parameters_dict[available_agent.agent_id.strip()] = list(
            map(lambda signature: signature.name.strip(), available_agent.actuator_signature.in_sig_full)
        )

    for action_str in plan_response.split("\n"):
        if len(action_str) > 0:
            if "]" in action_str:
                action_str = action_str.split("]")[1].strip()
                if ")" in action_str:
                    idx = action_str.find(")")
                    action_str = action_str[: idx + 1].strip()
                    try:
                        # edit action string here
                        pre_action_string = ""
                        tmp_action_str = action_str[:]
                        if "=" in action_str:
                            action_parts = action_str.split("=")
                            pre_action_string = action_parts[0].strip()
                            tmp_action_str = action_parts[1].strip()
                        if "(" in tmp_action_str and ")" in tmp_action_str:
                            idx_start = tmp_action_str.find("(")
                            idx_end = tmp_action_str.find(")")
                            if idx_end > (idx_start + 1):  # parameter exists
                                action_name = tmp_action_str[:idx_start].strip()
                                if (
                                    action_name != "ask"
                                    and action_name != "map"
                                    and action_name in action_name_input_parameters_dict
                                ):
                                    generated_parameters_set = set(
                                        filter(
                                            lambda ele: len(ele) > 0,
                                            map(
                                                lambda param: param.strip(),
                                                tmp_action_str[idx_start + 1 : idx_end].split(","),  # noqa: E203
                                            ),
                                        )
                                    )

                                    if len(generated_parameters_set) > 0:
                                        sorted_parameters = []
                                        true_parameters = action_name_input_parameters_dict[action_name]
                                        for true_parameter in true_parameters:
                                            if true_parameter in generated_parameters_set:
                                                sorted_parameters.append(true_parameter[:])
                                                generated_parameters_set.remove(true_parameter)

                                        sorted_parameters += list(
                                            generated_parameters_set
                                        )  # append hallucinated parameters

                                        action_str = action_name + "(" + ", ".join(sorted_parameters) + ")"

                        if len(pre_action_string) > 0:
                            action_str = pre_action_string.strip() + " = " + action_str.strip()
                    except Exception as e:
                        print(e)
                plan.append(action_str)

    return plan


def parse_llm_json_response(response: str, base_model: BaseModel) -> Tuple[Optional[BaseModel], str]:
    start_character = "{"
    end_character = "}"
    if start_character not in response or end_character not in response:
        return base_model(), "Invalid Json. No curly brackets. Json Parsing failed"

    start_index = response.index(start_character)
    end_index = response.rfind(end_character)
    json_str = response[start_index : (end_index + 1)]  # noqa: E203
    model: Optional[BaseModel] = None
    error_message = ""
    try:
        model = base_model.model_validate_json(json_str)
    except Exception as e:
        error_message = str(e)

    return model, error_message


def get_llm_processing_data(
    pddl_generator_outputs: List[PddlGeneratorOutput],
    file_path_without_extension: str,
    mark_word: str,
) -> Tuple[str, str, str]:
    # long description to plan data for LLM_SERVICE
    file_path_LLM_SERVICE_training_long_description_to_plan = (
        get_LLM_SERVICE_training_data_planning_from_pddl_generator_outputs(
            pddl_generator_outputs=pddl_generator_outputs,
            planning_input_description_mode=PlanningInputDescriptionMode.VERBOSE,
            file_path_without_extension=file_path_without_extension,
            mark_word=mark_word,
        )
    )

    file_path_LLM_SERVICE_training_short_description_to_plan = (
        get_LLM_SERVICE_training_data_planning_from_pddl_generator_outputs(
            pddl_generator_outputs=pddl_generator_outputs,
            planning_input_description_mode=PlanningInputDescriptionMode.CONCISE,
            file_path_without_extension=file_path_without_extension,
            mark_word=mark_word,
        )
    )

    file_path_LLM_SERVICE_training_long_description_to_json = (
        get_LLM_SERVICE_training_data_translation_from_pddl_generator_outputs(
            pddl_generator_outputs=pddl_generator_outputs,
            planning_input_description_mode=PlanningInputDescriptionMode.VERBOSE,
            file_path_without_extension=file_path_without_extension,
            mark_word=mark_word,
        )
    )

    return (
        file_path_LLM_SERVICE_training_long_description_to_plan,
        file_path_LLM_SERVICE_training_short_description_to_plan,
        file_path_LLM_SERVICE_training_long_description_to_json,
    )


def get_set_llm_processing_data(
    file_paths: List[str], mark_words: List[str], file_path_without_extension: str
) -> List[Tuple[str, str, str]]:
    output_file_paths: List[Tuple[str, str, str]] = []

    for i in range(len(file_paths)):
        output_file_paths.append(
            get_llm_processing_data(
                pddl_generator_outputs=get_base_models_from_jsonl(
                    file_path=file_paths[i], base_model=PddlGeneratorOutput
                ),
                file_path_without_extension=file_path_without_extension,
                mark_word=mark_words[i],
            )
        )

    # group file paths by datasetdict
    file_paths_by_datasetdict: List[List[str]] = [[] for _ in range(len(file_paths))]

    for output_file_path_set in output_file_paths:
        for i in range(len(file_paths)):
            file_paths_by_datasetdict[i].append(output_file_path_set[i])

    data_type_names = ["planning_verbose", "planning_concise", "translation_json"]
    for i, file_paths_training_validation_test in enumerate(file_paths_by_datasetdict):
        write_datasetdict_file_from_jsonls(
            file_paths=file_paths_training_validation_test,
            base_model=LLM_SERVICELlmTrainingDataModel,
            output_file_path=file_path_without_extension + "_" + data_type_names[i] + "_" + "datasetdict",
        )

    return output_file_paths
