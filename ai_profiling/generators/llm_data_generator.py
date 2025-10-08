import asyncio
import os
from pathlib import Path
from typing import Callable, List, Optional, cast
from nl2flow.debug.debug import BasicDebugger
from nl2flow.debug.schemas import SolutionQuality, DebugFlag
from profiler.data_types.pddl_generator_datatypes import PddlGeneratorOutput
from profiler.converters.info_2_flow_converter import get_flow_from_agent_infos
from ai_profiling.datatypes.planning_datatype import (
    AgentInfoUnitModel,
    SimplePlanningModel,
)
from ai_profiling.datatypes.stat_datatype import CheckPointModel
from ai_profiling.generators.planning_data_generator_datatypes import (
    LLMResponsePlanningData,
    TemporalFailureModel,
    ValOutputModel,
    ValidationLLMResponseJsonData,
    ValidationLLMResponsePlanningData,
)
from ai_profiling.helpers.evaluator_helper.evaluator_helper import convert_nl2flow_plan_to_pddl_plan, validate_pddl_plan
from ai_profiling.helpers.file_helper.file_helper import (
    delete_file,
    get_base_model_from_json,
    get_date_time_str,
    get_files_in_folder,
    write_json,
    write_json_record,
    write_txt_file,
)
from ai_profiling.helpers.prompt_helper.planner_prompt_helper import (
    parse_llm_json_response,
    parse_llm_planner_response,
)
from ai_profiling.helpers.service_helper.language_model_service_datatype import LlmResponse
from ai_profiling.helpers.service_helper.language_model_service_helper import (
    get_multiple_responses_from_LLM_SERVICE,
)
from profiler.generators.description_generator.description_generator_helper import (
    get_concise_description,
)


def convert_to_llm_responses_planning_data_batch(
    responses: List[LlmResponse], planning_prompt: str, pddl_generator_output: PddlGeneratorOutput, is_concise: bool
) -> List[LLMResponsePlanningData]:
    llm_responses_planning_data_batch: List[LLMResponsePlanningData] = []
    for response in responses:
        if response is not None:
            for llm_response in response:
                llm_responses_planning_data_batch.append(
                    LLMResponsePlanningData(
                        planning_prompt=planning_prompt,
                        llm_response=llm_response.model_copy(deep=True),
                        pddl_generator_output=pddl_generator_output.model_copy(deep=True),
                        is_concise=is_concise,
                    )
                )

    return llm_responses_planning_data_batch


async def get_llm_planning_responses(
    pddl_generator_output: PddlGeneratorOutput,
    api_key: str,
    planning_prompt: str,
    max_token: int,
    min_new_tokens: int,
    temperature: float,
    time_limit: int,
    num_generations: int,
    llm_model_ids: List[str],
    is_concise: bool,
) -> List[LLMResponsePlanningData]:
    tasks = [
        get_multiple_responses_from_LLM_SERVICE(
            id_model=llm_model_id[:],
            api_key=api_key[:],
            content=planning_prompt[:],
            temperature=temperature,
            max_tokens=max_token,
            min_tokens=min_new_tokens,
            num_generations=num_generations,
            verbose=True,
            timeout=time_limit,
        )
        for llm_model_id in llm_model_ids
    ]
    responses = await asyncio.gather(*tasks)
    return convert_to_llm_responses_planning_data_batch(
        responses=responses,
        planning_prompt=planning_prompt,
        pddl_generator_output=pddl_generator_output,
        is_concise=is_concise,
    )


# def get_llm_planning_responses_local(
#     pddl_generator_output: PddlGeneratorOutput,
#     api_key: str,
#     planning_prompt: str,
#     max_token: int,
#     min_new_tokens: int,
#     temperature: float,
#     time_limit: int,
#     num_generations: int,
#     llm_model_ids: List[str],
#     is_concise: bool,
# ) -> List[LLMResponsePlanningData]:
#     tasks = [
#         get_multiple_responses_from_LLM_SERVICE(
#             id_model=llm_model_id[:],
#             api_key=api_key[:],
#             content=planning_prompt[:],
#             temperature=temperature,
#             max_tokens=max_token,
#             min_tokens=min_new_tokens,
#             num_generations=num_generations,
#             verbose=True,
#             timeout=time_limit,
#         )
#         for llm_model_id in llm_model_ids
#     ]
#     responses = await asyncio.gather(*tasks)
#     return convert_to_llm_responses_planning_data_batch(
#         responses=responses,
#         planning_prompt=planning_prompt,
#         pddl_generator_output=pddl_generator_output,
#         is_concise=is_concise,
#     )


def get_description(pddl_generator_output: PddlGeneratorOutput, is_concise: bool) -> str:
    if not is_concise:
        return pddl_generator_output.agent_info_generator_output_item.describe()

    output_item = pddl_generator_output.agent_info_generator_output_item
    # concise planning problem description
    agent_info_unit_model = AgentInfoUnitModel(
        available_agents=output_item.available_agents,
        goal_agent_ids=output_item.goal_agent_ids,
        mappings=output_item.mappings,
        available_data=output_item.available_data,
    )

    return get_concise_description(
        simple_planning_model=agent_info_unit_model.get_simple_planning_model(), should_objects_known_in_memory=True
    )


async def generate_llm_responses_and_store_at_db(
    api_key: str,
    max_token: int,
    min_new_tokens: int,
    temperature: float,
    time_limit: int,
    num_generations: int,
    llm_model_ids: List[str],
    prompt_function: Callable[[str], str],
    is_concise: bool = False,
    pddl_generator_output_paths: List[Path] = [],
    output_folder_path: Optional[Path] = None,
    is_translation: bool = False,
    start_index: int = 0,
) -> Path:
    folder_name = "llm_translation_collector" if is_translation else "llm_plan_collector"
    file_prefix = "llm_response"
    file_extension = ".json"
    concise_str = "short" if is_concise else "long"
    index_file_name = get_date_time_str() + ".ckpt"
    new_output_folder_path = os.path.join(output_folder_path, folder_name, concise_str)
    for idx, pddl_generator_output_path in enumerate(pddl_generator_output_paths):
        if idx < start_index:
            continue
        pddl_generator_output = get_base_model_from_json(
            file_path=str(pddl_generator_output_path), base_model=PddlGeneratorOutput
        )
        # parse pddl_generator_output here
        planning_prompt = prompt_function(
            get_description(
                pddl_generator_output=pddl_generator_output, is_concise=False if is_translation else is_concise
            )
        )
        llm_response_planning_data_batch = await get_llm_planning_responses(
            pddl_generator_output=pddl_generator_output,
            api_key=api_key,
            planning_prompt=planning_prompt,
            max_token=max_token,
            min_new_tokens=min_new_tokens,
            temperature=temperature,
            time_limit=time_limit,
            num_generations=num_generations,
            llm_model_ids=llm_model_ids,
            is_concise=is_concise,
        )
        write_json_record(
            file_path=Path(os.path.join(new_output_folder_path, index_file_name)),
            base_model=CheckPointModel(idx=idx),
        )

        if len(llm_response_planning_data_batch) > 0 and output_folder_path is not None:
            for llm_response_planning_data in llm_response_planning_data_batch:
                llm_response_planning_data.llm_response.llm_model_id
                file_name = (
                    file_prefix
                    + "_"
                    + concise_str
                    + "_"
                    + llm_response_planning_data.pddl_generator_output.sample_hash
                    + file_extension
                )
                output_path = os.path.join(
                    new_output_folder_path, llm_response_planning_data.llm_response.llm_model_id, file_name
                )
                write_json(file_path=output_path, base_model=llm_response_planning_data)

    return Path(new_output_folder_path)


def get_validation_result_from_val(
    val_path: Path, cache_folder_path: Path, plan_txt: str, domain_txt: str, problem_txt: str, cost: int
) -> ValOutputModel:
    plan_file_path = Path(os.path.join(cache_folder_path, "evaluator", "plan.pddl"))
    domain_file_path = Path(os.path.join(cache_folder_path, "evaluator", "domain.pddl"))
    problem_file_path = Path(os.path.join(cache_folder_path, "evaluator", "problem.pddl"))

    pddl_plan_txt = convert_nl2flow_plan_to_pddl_plan(plan_nl2flow_txt=plan_txt)

    write_txt_file(file_path=str(plan_file_path), text=pddl_plan_txt)
    write_txt_file(file_path=str(domain_file_path), text=domain_txt)
    write_txt_file(file_path=str(problem_file_path), text=problem_txt)

    val_output_model = validate_pddl_plan(
        val_path=val_path,
        domain_file=domain_file_path,
        problem_file=problem_file_path,
        plan_file=plan_file_path,
        cost=cost,
    )

    delete_file(file_path=plan_file_path)
    delete_file(file_path=domain_file_path)
    delete_file(file_path=problem_file_path)

    return val_output_model


def validate_llm_response_and_store_at_db(
    llm_response_file_path: Path,
    output_folder_path: Path,
    cache_folder_path: Path,
    val_path: Optional[Path],
) -> Path:
    file_paths = get_files_in_folder(folder_path=Path(llm_response_file_path), file_extension="json")
    llm_response_planning_data: List[LLMResponsePlanningData] = []

    for file_path in file_paths:
        llm_response_planning_data.append(
            cast(
                LLMResponsePlanningData,
                get_base_model_from_json(file_path=str(file_path), base_model=LLMResponsePlanningData),
            )
        )

    file_prefix = "llm_plan_evaluation"
    new_folder_path = os.path.join(output_folder_path, file_prefix)
    for datum in llm_response_planning_data:
        action_str_list = parse_llm_planner_response(
            response=datum.llm_response.generated_text,
            available_agents=datum.pddl_generator_output.agent_info_generator_output_item.available_agents,
        )
        validation_llm_response_planning_data = ValidationLLMResponsePlanningData(
            llm_response_planning_data=datum, llm_plan=action_str_list
        )

        validation_llm_response_planning_data.val_output_model = ValOutputModel()

        if action_str_list is not None:
            if val_path is not None:
                if len(datum.pddl_generator_output.list_of_plans) == 0 and len(action_str_list) == 0:  # no plan match
                    validation_llm_response_planning_data.val_output_model = ValOutputModel(
                        is_optimal=True, is_executable=True, is_valid=True, reach_goals=True, cost=-1
                    )
                else:
                    validation_llm_response_planning_data.val_output_model = get_validation_result_from_val(
                        val_path=val_path,
                        cache_folder_path=cache_folder_path,
                        plan_txt=("\n".join(action_str_list)),
                        domain_txt=datum.pddl_generator_output.pddl_domain,
                        problem_txt=datum.pddl_generator_output.pddl_problem,
                        cost=(
                            int(datum.pddl_generator_output.list_of_plans[0].cost)
                            if len(datum.pddl_generator_output.list_of_plans) > 0
                            else -2
                        ),
                    )
            else:
                flow = get_flow_from_agent_infos(
                    available_agents=datum.pddl_generator_output.agent_info_generator_output_item.available_agents,
                    mappings=datum.pddl_generator_output.agent_info_generator_output_item.mappings,
                    goals=set(datum.pddl_generator_output.agent_info_generator_output_item.goal_agent_ids),
                    available_data=datum.pddl_generator_output.agent_info_generator_output_item.available_data,
                )
                debugger = BasicDebugger(flow)

                try:
                    validation_llm_response_planning_data.report_soundness = debugger.debug(
                        list_of_tokens=action_str_list,
                        report_type=SolutionQuality.SOUND,
                        debug_flag=DebugFlag.TOKENIZE,
                        timeout=15,
                        show_output=None,
                    )
                except KeyboardInterrupt as e:
                    print(e)

                try:
                    validation_llm_response_planning_data.report_validity = debugger.debug(
                        list_of_tokens=action_str_list,
                        report_type=SolutionQuality.VALID,
                        debug_flag=DebugFlag.TOKENIZE,
                        timeout=15,
                        show_output=None,
                    )
                except KeyboardInterrupt as e:
                    print(e)

                try:
                    validation_llm_response_planning_data.report_optimality = debugger.debug(
                        list_of_tokens=action_str_list,
                        report_type=SolutionQuality.OPTIMAL,
                        debug_flag=DebugFlag.TOKENIZE,
                        timeout=15,
                        show_output=None,
                    )
                except KeyboardInterrupt as e:
                    print(e)

        new_file_name = file_prefix + datum.pddl_generator_output.sample_hash + ".json"
        concise_str = "short" if datum.is_concise else "long"
        file_path = os.path.join(new_folder_path, concise_str, datum.llm_response.llm_model_id, new_file_name)
        write_json(file_path=file_path, base_model=validation_llm_response_planning_data)

    return new_folder_path


def validate_llm_json_response_and_store_at_db(
    llm_response_planning_data: List[LLMResponsePlanningData], output_folder_path: Path
) -> Path:
    file_name_prefix = "llm_json_response_validation"
    new_output_folder_path = os.path.join(output_folder_path, file_name_prefix)

    for datum in llm_response_planning_data:
        output_file_name = file_name_prefix + datum.pddl_generator_output.sample_hash + ".json"
        datum.llm_response.llm_model_id

        simple_planning_model, error_message = parse_llm_json_response(
            datum.llm_response.generated_text, SimplePlanningModel
        )

        model = ValidationLLMResponseJsonData(llm_response_planning_data=datum)
        model.update_error_message(error_message)

        if len(model.error_messages) > 0:
            model.temporal_failure = TemporalFailureModel.JSON_PARSING
        else:
            generator_output_model = datum.pddl_generator_output.agent_info_generator_output_item
            agent_info_unit_model = AgentInfoUnitModel(
                available_agents=generator_output_model.available_agents,
                goal_agent_ids=generator_output_model.goal_agent_ids,
                mappings=generator_output_model.mappings,
                available_data=generator_output_model.available_data,
            )
            model.planning_input_from_llm = agent_info_unit_model.model_copy(deep=True)
            model.json_translation_stat = simple_planning_model.get_stat(
                true_model=agent_info_unit_model.get_simple_planning_model()
            )

        concise_str = "short" if datum.is_concise else "long"
        write_json(
            file_path=os.path.join(
                new_output_folder_path, concise_str, datum.llm_response.llm_model_id, output_file_name
            ),
            base_model=model,
        )

    return Path(new_output_folder_path)
