import os
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, cast
from ai_profiling.data.planning.planning_sources import get_test_planning_sources
from ai_profiling.datatypes.service_datatype import Seq2SeqEvaluationDataModel
from ai_profiling.generators.llm_data_generator import (
    generate_llm_responses_and_store_at_db,
    validate_llm_json_response_and_store_at_db,
    validate_llm_response_and_store_at_db,
)
from ai_profiling.generators.planning_data_generator import (
    generate_insert_planning_data_to_db,
)
from ai_profiling.generators.planning_data_generator_datatypes import (
    LLMResponsePlanningData,
)
from ai_profiling.generators.template_generator import (
    write_planning_source_list_on_file,
)
from profiler.data_types.generator_data_type import (
    AgentInfoGeneratorInputBatch,
)
from ai_profiling.helpers.file_helper.file_helper import (
    get_base_model_from_json,
    get_base_models_from_jsonl,
    get_file_path,
    get_files_in_folder,
    write_json,
    write_jsonl,
)
from ai_profiling.helpers.prompt_helper.planner_prompt_helper import (
    get_concise_planning_example_prompt,
    get_general_object_creation_example_prompt,
    get_general_planning_example_prompt,
    get_planning_object_prompt,
)
from ai_profiling.helpers.service_helper.language_model_service_datatype import (
    LlmResponse,
)

# from ai_profiling.helpers.stat_helpers.basic_stat_helper import (
#     create_basic_stat_files,
#     get_stat_description_to_json_translation,
# )
from profiler.data_types.pddl_generator_datatypes import PddlGeneratorOutput


def run_llm_plan_validation(
    llm_response_file_path: str,
    file_path_without_extension: str,
    cache_folder_path: Path,
    val_path: Optional[Path],
) -> Path:
    new_output_folder_path = validate_llm_response_and_store_at_db(
        llm_response_file_path=llm_response_file_path,
        output_folder_path=Path(file_path_without_extension),
        cache_folder_path=cache_folder_path,
        val_path=val_path,
    )

    # validation_llm_response_planning_data = retrieve_base_models_from_db(
    #     collection_name=collection_name,
    #     base_model=ValidationLLMResponsePlanningData,
    # )
    # file_path_validation = get_file_path(
    #     file_path_without_extension=file_path_without_extension,
    #     key_words=["plan", "validation"],
    #     extension="jsonl",
    # )
    # write_jsonl(file_path=file_path_validation, base_models=validation_llm_response_planning_data)
    # (
    #     llm_bin,
    #     optimal_histogram,
    #     sound_histogram,
    #     valid_histogram,
    #     file_path_summary,
    #     file_path_optimal,
    #     file_path_sound,
    #     file_path_valid,
    # ) = create_basic_stat_files(
    #     llm_response_planning_evaluation_data=validation_llm_response_planning_data,
    #     file_path_without_extension=file_path_without_extension,
    # )

    return new_output_folder_path


async def retrieve_llm_plans(
    planning_source_file_path: str,
    file_path_without_extension: str,
    api_key: str,
    max_token: int,
    min_new_tokens: int,
    temperature: float,
    time_limit: int,
    num_generations: int,
    llm_model_ids: List[str],
    prompt_function: Callable,
    is_concise: bool,
    start_index: int,
) -> Path:
    new_output_folder_path = await generate_llm_responses_and_store_at_db(
        api_key=api_key,
        max_token=max_token,
        min_new_tokens=min_new_tokens,
        temperature=temperature,
        time_limit=time_limit,
        num_generations=num_generations,
        llm_model_ids=llm_model_ids,
        prompt_function=prompt_function,
        is_concise=is_concise,
        pddl_generator_output_paths=get_files_in_folder(
            folder_path=Path(planning_source_file_path), file_extension="json"
        ),
        output_folder_path=Path(file_path_without_extension),
        is_translation=False,
        start_index=start_index,
    )

    return new_output_folder_path


def join_pytoch_llm_response_with_pddl_output_model(
    file_path_pytorch_seq2seq_output: str,
    file_path_planning_source: str,
    file_path_without_extension: str,
    model_identifier: str = "merged",
) -> str:
    """
    returns jsonl file path for a list of LLMResponsePlanningData
    """
    seq2seq_evaluation_models = get_base_models_from_jsonl(
        file_path=file_path_pytorch_seq2seq_output,
        base_model=Seq2SeqEvaluationDataModel,
    )
    pddl_generator_outputs = get_base_models_from_jsonl(
        file_path=file_path_planning_source, base_model=PddlGeneratorOutput
    )

    sample_hash_pddl_generator_output_dict: Dict[str, PddlGeneratorOutput] = {
        pddl_generator_output.sample_hash: pddl_generator_output for pddl_generator_output in pddl_generator_outputs
    }

    llm_response_planning_data: List[LLMResponsePlanningData] = [
        LLMResponsePlanningData(
            planning_prompt=seq2seq_evaluation_model.text,
            llm_response=LlmResponse(llm_model_id=seq2seq_evaluation_model.llm_model_id),
            pddl_generator_output=sample_hash_pddl_generator_output_dict[
                seq2seq_evaluation_model.sample_hash
            ].model_copy(deep=True),
        )
        for seq2seq_evaluation_model in seq2seq_evaluation_models
        if seq2seq_evaluation_model.sample_hash in sample_hash_pddl_generator_output_dict
    ]

    file_path = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=["plan", "llm", "response", model_identifier],
        extension="jsonl",
    )
    write_jsonl(file_path=file_path, base_models=llm_response_planning_data)

    return file_path


async def retrieve_description_to_json_translation(
    planning_source_file_path: str,
    file_path_without_extension: str,
    api_key: str,
    max_token: int,
    min_new_tokens: int,
    temperature: float,
    time_limit: int,
    num_generations: int,
    llm_model_ids: List[str],
    start_index: int,
) -> Path:
    new_output_folder_path = await generate_llm_responses_and_store_at_db(
        api_key=api_key,
        max_token=max_token,
        min_new_tokens=min_new_tokens,
        temperature=temperature,
        time_limit=time_limit,
        num_generations=num_generations,
        llm_model_ids=llm_model_ids,
        prompt_function=get_planning_object_prompt,
        is_concise=True,
        pddl_generator_output_paths=get_files_in_folder(
            folder_path=Path(planning_source_file_path), file_extension="json"
        ),
        output_folder_path=Path(file_path_without_extension),
        is_translation=True,
        start_index=start_index,
    )

    return new_output_folder_path


def run_validate_description_to_json_translation(llm_response_file_path: str, file_path_without_extension: str) -> Path:
    file_paths = get_files_in_folder(folder_path=Path(llm_response_file_path), file_extension="json")
    llm_response_planning_data: List[LLMResponsePlanningData] = []

    for file_path in file_paths:
        llm_response_planning_data.append(
            cast(
                LLMResponsePlanningData,
                get_base_model_from_json(file_path=str(file_path), base_model=LLMResponsePlanningData),
            )
        )

    output_folder_path = validate_llm_json_response_and_store_at_db(
        llm_response_planning_data=llm_response_planning_data, output_folder_path=Path(file_path_without_extension)
    )

    return output_folder_path


def pipeline_generate_planning_data(
    agent_info_generator_input_batch: AgentInfoGeneratorInputBatch,
    random_seed: int,
    training_prop: float,
    validation_prop: float,
    file_path_without_extension: str,
    should_write_file: bool = False,
) -> Tuple[str, str, str, str, str, Tuple[str, str, str], Tuple[str, str, str], Tuple[str, str, str],]:
    # write a setting file
    file_path_setting = (
        get_file_path(
            file_path_without_extension=file_path_without_extension,
            key_words=["setting"],
            extension="json",
        )
        if should_write_file
        else ""
    )

    if should_write_file:
        write_json(
            file_path=file_path_setting,
            base_model=agent_info_generator_input_batch,
        )

    # generate planning data
    generate_insert_planning_data_to_db(
        agent_info_generator_input_batch=agent_info_generator_input_batch,
        random_seed=random_seed,
        output_folder_path=Path(os.path.join(file_path_without_extension, "planning_data")),
    )

    # print(f"{len(inserted_ids)} data points are inserted to DB.")

    # remove redundant data
    # remove_redundant_planning_data_in_db()

    # if should_write_file:
    #     # retrieve planning data from database
    #     pddl_generator_outputs = retrieve_base_models_from_db(
    #         collection_name=NL2FLOW_MONGODB_COLLECTION, base_model=PddlGeneratorOutput
    #     )

    #     print(f"{len(pddl_generator_outputs)} data points are retrieved.")

    #     # write total data
    #     file_path_total_data = get_file_path(
    #         file_path_without_extension=file_path_without_extension,
    #         key_words=["no", "split"],
    #         extension="jsonl",
    #     )
    #     write_jsonl(file_path=file_path_total_data, base_models=pddl_generator_outputs)

    #     print("Preparing generic output data")
    #     file_path_training, file_path_validation, file_path_test = write_files_data_pipeline(
    #         file_path=file_path_without_extension,
    #         pddl_generator_outputs=pddl_generator_outputs,
    #         training_prop=training_prop,
    #         validation_prop=validation_prop,
    #     )

    #     # data for llm
    #     print("Preparing data to train DNN")
    #     file_paths = [file_path_training, file_path_validation, file_path_test]
    #     output_file_paths = get_set_llm_processing_data(
    #         file_paths=file_paths,
    #         mark_words=["train", "validation", "test"],
    #         file_path_without_extension=file_path_without_extension,
    #     )

    # return (
    #     file_path_setting,
    #     file_path_total_data,
    #     file_path_training,
    #     file_path_validation,
    #     file_path_test,
    #     output_file_paths[0],
    #     output_file_paths[1],
    #     output_file_paths[2],
    # )
    return ("", "", "", "", "", [], [], [])


def create_example_files(folder_path: str) -> Tuple[str, str, str]:
    file_path_planning_examples = os.path.join(folder_path, "planning_examples.txt")
    file_path_concise_planning_examples = os.path.join(folder_path, "concise_planning_examples.txt")
    file_path_json_examples = os.path.join(folder_path, "json_examples.txt")
    write_planning_source_list_on_file(
        file_path=file_path_planning_examples,
        prompt_function=get_general_planning_example_prompt,
        planning_source_list=get_test_planning_sources(),
    )
    write_planning_source_list_on_file(
        file_path=file_path_concise_planning_examples,
        prompt_function=get_concise_planning_example_prompt,
        planning_source_list=get_test_planning_sources(),
    )
    write_planning_source_list_on_file(
        file_path=file_path_json_examples,
        prompt_function=get_general_object_creation_example_prompt,
        planning_source_list=get_test_planning_sources(),
    )

    return (
        file_path_planning_examples,
        file_path_concise_planning_examples,
        file_path_json_examples,
    )
