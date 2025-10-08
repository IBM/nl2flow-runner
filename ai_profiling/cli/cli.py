import argparse
import asyncio
import os
from pathlib import Path
import pprint
import sys
from ai_profiling.helpers.database_helper.mongodb_helper.mongodb_manager_variables import (
    DB_TASK_DELETE,
    DB_TASK_RETRIEVE,
    # DESCRIPTION_PDDL_MONGODB_COLLECTION,
    # DESCRIPTION_PDDL_MONGODB_FAILED_COLLECTION,
    # DESCRIPTION_PLAN_MONGODB_COLLECTION,
    # DESCRIPTION_PLAN_MONGODB_FAILED_COLLECTION,
    # NL2FLOW_CONCISE_LLM_MONGODB_COLLECTION,
    # NL2FLOW_CONCISE_VALIDATION_MONGODB_COLLECTION,
    # NL2FLOW_JSON_LLM_MONGODB_COLLECTION,
    # NL2FLOW_JSON_VALIDATION_MONGODB_COLLECTION,
    # NL2FLOW_LLM_MONGODB_COLLECTION,
    # NL2FLOW_MONGODB_COLLECTION,
    # NL2FLOW_MONGODB_FAILED_COLLECTION,
    # NL2FLOW_VALIDATION_MONGODB_COLLECTION,
    # PDDL_PLAN_MONGODB_COLLECTION,
    # PDDL_PLAN_MONGODB_FAILED_COLLECTION,
    # PDDL_SYM_PLAN_MONGODB_COLLECTION,
    # PDDL_SYM_PLAN_MONGODB_FAILED_COLLECTION,
)
from ai_profiling.helpers.file_helper.file_helper import get_base_model_from_json
from profiler.data_types.generator_data_type import AgentInfoGeneratorInputBatch

from ai_profiling.helpers.prompt_helper.planner_prompt_helper import get_concise_planning_prompt, get_planning_prompt
from ai_profiling.pipeline.llm_planning_pipeline import (
    pipeline_generate_planning_data,
    retrieve_description_to_json_translation,
    retrieve_llm_plans,
    run_llm_plan_validation,
    run_validate_description_to_json_translation,
)


def generator(args) -> None:
    output_file_paths = pipeline_generate_planning_data(
        agent_info_generator_input_batch=get_base_model_from_json(
            file_path=args.generator_config_file_path, base_model=AgentInfoGeneratorInputBatch
        ),
        random_seed=args.random_seed,
        training_prop=args.training_proportion,
        validation_prop=args.validation_proportion,
        file_path_without_extension=os.path.join(args.output_directory_path, "planning_source"),
        should_write_file=args.should_write_file,
    )
    print()
    print("Generated files are")
    pprint.pp(output_file_paths)


def collector(args) -> None:
    is_concise = False if args.style_planning_problem_description == "long" else True
    prompt_function = (
        get_planning_prompt if args.style_planning_problem_description == "long" else get_concise_planning_prompt
    )

    llm_plan_file_path = asyncio.run(
        retrieve_llm_plans(
            planning_source_file_path=args.planning_source_file_path,
            file_path_without_extension=args.output_directory_path,
            api_key=args.api_key,
            max_token=args.max_tokens,
            min_new_tokens=args.min_new_tokens,
            temperature=args.language_model_temperature,
            time_limit=args.time_limit,
            num_generations=args.num_retrievals,
            llm_model_ids=args.model_id,
            prompt_function=prompt_function,
            is_concise=is_concise,
            start_index=args.start_index,
        )
    )
    print()
    pprint.pp(llm_plan_file_path)

    # output_file_path = run_llm_plan_validation(
    #     llm_response_file_path=llm_plan_file_path,
    #     file_path_without_extension=file_path_without_extension,
    # )

    # print()
    # pprint.pp(output_file_path)


def collector_translation(args) -> None:
    new_output_folder_path = asyncio.run(
        retrieve_description_to_json_translation(
            planning_source_file_path=args.planning_source_file_path,
            file_path_without_extension=args.output_directory_path,
            api_key=args.api_key,
            max_token=args.max_tokens,
            min_new_tokens=args.min_new_tokens,
            temperature=args.language_model_temperature,
            time_limit=args.time_limit,
            num_generations=args.num_retrievals,
            llm_model_ids=args.model_id,
            start_index=args.start_index,
        )
    )

    pprint.pp(new_output_folder_path)

    output_file_path = run_validate_description_to_json_translation(
        llm_response_file_path=new_output_folder_path,
        file_path_without_extension=args.output_directory_path,
    )

    pprint.pp(output_file_path)


def evaluator(args) -> None:
    # file_path_without_extension = os.path.join(args.output_directory_path, "planning")
    # llm_plan_file_path = join_pytoch_llm_response_with_pddl_output_model(
    #     file_path_pytorch_seq2seq_output=args.model_output_file_path,
    #     file_path_planning_source=args.planning_source_file_path,
    #     file_path_without_extension=file_path_without_extension,
    #     model_identifier=args.model_identifier,
    # )

    # pprint.pp(llm_plan_file_path)

    output_file_paths = run_llm_plan_validation(
        llm_response_file_path=args.model_output_file_path,
        file_path_without_extension=args.output_directory_path,
        cache_folder_path=Path(args.cache_folder_path),
        val_path=Path(args.val_path) if len(args.val_path) > 0 else None,
    )

    pprint.pp(output_file_paths)


def evaluator_translation(args) -> None:
    # file_path_without_extension = os.path.join(args.output_directory_path, "planning")
    # translation_file_path = join_pytoch_llm_response_with_pddl_output_model(
    #     file_path_pytorch_seq2seq_output=args.model_output_file_path,
    #     file_path_planning_source=args.planning_source_file_path,
    #     file_path_without_extension=file_path_without_extension,
    #     model_identifier=args.model_identifier,
    # )

    # pprint.pp(translation_file_path)

    output_file_path = run_validate_description_to_json_translation(
        llm_response_file_path=args.model_output_file_path,
        file_path_without_extension=args.output_directory_path,
    )

    pprint.pp(output_file_path)


def cli():
    # Create an ArgumentParser object with a description
    parser = argparse.ArgumentParser(description="Conversational AI Benchmark Tool")

    # Define command-line arguments
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        help="NL2FLOW Runner tool mode",
        choices=["generator", "collector", "evaluator", "manager"],
        default="generator",
    )

    parser.add_argument(
        "-tm",
        "--task_mode",
        type=str,
        help="NL2FLOW Runner task mode",
        choices=["planning", "translation"],
        default="planning",
    )
    # parser.add_argument(
    #     "-vb",
    #     "--verbose",
    #     action=argparse.BooleanOptionalAction,
    #     help="Verbose CLI Mode",
    #     default=False,
    # )

    parser.add_argument(
        "-od",
        "--output_directory_path",
        type=str,
        help="Absolute path for an output directory",
    )

    parser.add_argument(
        "-ak",
        "--api_key",
        type=str,
        help="API key",
    )

    parser.add_argument("-si", "--start_index", type=int, help="Index to start an operation", default=0)

    parser.add_argument(
        "-mt", "--max_tokens", type=int, help="The maximum number of tokens to retrieve from a model", default=400
    )

    parser.add_argument(
        "-nt",
        "--min_new_tokens",
        type=int,
        help="The minimum number of new tokens to retrieve from a model",
        default=20,
    )

    parser.add_argument(
        "-lmt",
        "--language_model_temperature",
        type=float,
        help="Language model temperature",
        default=0.0,
    )

    parser.add_argument(
        "-tl",
        "--time_limit",
        type=int,
        help="Time limit in second",
        default=300,
    )

    parser.add_argument(
        "-nr",
        "--num_retrievals",
        type=int,
        help="The number of response retrievals per sample",
        default=1,
    )

    # Generator
    parser.add_argument(
        "-gf",
        "--generator_config_file_path",
        type=str,
        help="Absolute path for the json file containing a generator configuration",
    )

    parser.add_argument(
        "-sd",
        "--random_seed",
        type=int,
        help="Random seed for generating data",
    )

    parser.add_argument(
        "-tp", "--training_proportion", type=float, help="The proportion of data for training", default=0.9
    )

    parser.add_argument(
        "-vp", "--validation_proportion", type=float, help="The proportion of data for validation", default=0.05
    )

    # Collector
    parser.add_argument(
        "-mid",
        "--model_id",
        nargs="*",
        type=str,
        help="Model IDs. Currently, they are model ids for LLM_SERVICE",
        default=["meta-llama/llama-3-3-70b-instruct"],
    )

    # python my_app.py --listb 5 6 7 8 --lista  1 2 3 4
    # lista: [1, 2, 3, 4]
    # listb: [5.0, 6.0, 7.0, 8.0]

    parser.add_argument(
        "-psf",
        "--planning_source_file_path",
        type=str,
        help="Absolute path for a planning source file",
    )

    parser.add_argument(
        "-sppd",
        "--style_planning_problem_description",
        type=str,
        help="Style of planning problem description",
        choices=["long", "short"],
        default="long",
    )

    # Evaluator
    parser.add_argument(
        "-mofp",
        "--model_output_file_path",
        type=str,
        help="Absolute path for an output file from a model",
    )
    parser.add_argument(
        "-cf",
        "--cache_folder_path",
        type=str,
        default="",
        help="Absolute path for a cache folder",
    )
    parser.add_argument(
        "-vfp",
        "--val_path",
        type=str,
        default="",
        help="Absolute path for VAL file for validating plans",
    )

    parser.add_argument(
        "-sf",
        "--should_write_file",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Should write outputs in file",
    )

    parser.add_argument("-mi", "--model_identifier", type=str, help="Model identifier", default="merged")

    # Data Manager
    # parser.add_argument(
    #     "-cn",
    #     "--db_collection_name",
    #     type=str,
    #     help="Collection name at MongoDB",
    #     choices=[
    #         NL2FLOW_MONGODB_COLLECTION,
    #         NL2FLOW_LLM_MONGODB_COLLECTION,
    #         NL2FLOW_CONCISE_LLM_MONGODB_COLLECTION,
    #         NL2FLOW_JSON_LLM_MONGODB_COLLECTION,
    #         NL2FLOW_VALIDATION_MONGODB_COLLECTION,
    #         NL2FLOW_CONCISE_VALIDATION_MONGODB_COLLECTION,
    #         NL2FLOW_JSON_VALIDATION_MONGODB_COLLECTION,
    #         NL2FLOW_MONGODB_FAILED_COLLECTION,
    #         DESCRIPTION_PLAN_MONGODB_COLLECTION,
    #         DESCRIPTION_PLAN_MONGODB_FAILED_COLLECTION,
    #         DESCRIPTION_PDDL_MONGODB_COLLECTION,
    #         DESCRIPTION_PDDL_MONGODB_FAILED_COLLECTION,
    #         PDDL_PLAN_MONGODB_COLLECTION,
    #         PDDL_PLAN_MONGODB_FAILED_COLLECTION,
    #         PDDL_SYM_PLAN_MONGODB_COLLECTION,
    #         PDDL_SYM_PLAN_MONGODB_FAILED_COLLECTION,
    #     ],
    #     default=NL2FLOW_MONGODB_COLLECTION,
    # )
    parser.add_argument(
        "-mtm",
        "--manager_task_mode",
        type=str,
        help="Database Manager task mode",
        choices=[DB_TASK_DELETE, DB_TASK_RETRIEVE],
        default=DB_TASK_RETRIEVE,
    )
    # Parse the command-line arguments
    args = parser.parse_args()

    if not len(sys.argv) > 1:
        print("No argument is provided to NL2FLOW Runner.")
        return

    print()
    print(f"{args.mode.capitalize()} starts.")

    if args.mode.lower() == "generator":
        generator(args)

    if args.mode.lower() == "collector":
        if args.task_mode.lower() == "planning":
            collector(args)
        elif args.task_mode.lower() == "translation":
            collector_translation(args)

    if args.mode.lower() == "evaluator":
        if args.task_mode.lower() == "planning":
            evaluator(args)
        elif args.task_mode.lower() == "translation":
            evaluator_translation(args)

    print()
    print(f"{args.mode.capitalize()} ends.")
