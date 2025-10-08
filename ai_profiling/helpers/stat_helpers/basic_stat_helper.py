from collections import defaultdict
from typing import Dict, List, Tuple
from ai_profiling.datatypes.stat_datatype import LLMResponseHistogram
from ai_profiling.generators.planning_data_generator_datatypes import (
    ValidationLLMResponseJsonData,
    ValidationLLMResponsePlanningData,
)
from ai_profiling.helpers.file_helper.file_helper import (
    get_file_path,
    write_json,
    write_json_from_dict,
)


def create_basic_stat_files(
    llm_response_planning_evaluation_data: List[ValidationLLMResponsePlanningData],
    file_path_without_extension: str,
) -> Tuple[
    Dict[str, Dict[str, int]],
    LLMResponseHistogram,
    LLMResponseHistogram,
    LLMResponseHistogram,
    str,
    str,
    str,
    str,
]:
    optimal_histogram = LLMResponseHistogram()
    sound_histogram = LLMResponseHistogram()
    valid_histogram = LLMResponseHistogram()
    llm_bin: Dict[str, Dict[str, int]] = defaultdict(lambda: {"total": 0, "optimal": 0, "sound": 0, "valid": 0})
    for llm_response_planning_evaluation_unit in llm_response_planning_evaluation_data:
        input = (
            llm_response_planning_evaluation_unit.llm_response_planning_data.pddl_generator_output.agent_info_generator_input  # noqa: E501
        )
        llm_model_id = llm_response_planning_evaluation_unit.llm_response_planning_data.llm_response.llm_model_id
        llm_bin[llm_model_id]["total"] += 1
        # check if translation is intact
        if llm_response_planning_evaluation_unit.report_soundness is not None:
            sound_histogram.update_histogram(
                input=input,
                is_true=llm_response_planning_evaluation_unit.report_soundness.determination,
            )
            if llm_response_planning_evaluation_unit.report_soundness.determination:
                llm_bin[llm_model_id]["sound"] += 1
        if llm_response_planning_evaluation_unit.report_validity is not None:
            valid_histogram.update_histogram(
                input=input,
                is_true=llm_response_planning_evaluation_unit.report_validity.determination,
            )
            if llm_response_planning_evaluation_unit.report_validity.determination:
                llm_bin[llm_model_id]["valid"] += 1
        if llm_response_planning_evaluation_unit.report_optimality is not None:
            optimal_histogram.update_histogram(
                input=input,
                is_true=llm_response_planning_evaluation_unit.report_optimality.determination,
            )
            if llm_response_planning_evaluation_unit.report_optimality.determination:
                llm_bin[llm_model_id]["optimal"] += 1

    file_path_summary = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=["plan", "validation", "summary"],
        extension="json",
    )
    file_path_optimal = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=["plan", "validation", "histogram", "optimal"],
        extension="json",
    )
    file_path_sound = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=["plan", "validation", "histogram", "sound"],
        extension="json",
    )
    file_path_valid = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=["plan", "validation", "histogram", "valid"],
        extension="json",
    )
    write_json_from_dict(file_path=file_path_summary, dic=llm_bin)
    write_json(
        file_path=file_path_optimal,
        base_model=optimal_histogram,
    )
    write_json(
        file_path=file_path_sound,
        base_model=sound_histogram,
    )
    write_json(
        file_path=file_path_valid,
        base_model=valid_histogram,
    )

    return (
        llm_bin,
        optimal_histogram,
        sound_histogram,
        valid_histogram,
        file_path_summary,
        file_path_optimal,
        file_path_sound,
        file_path_valid,
    )


def get_stat_description_to_json_translation(
    llm_response_json_evaluation_data: List[ValidationLLMResponseJsonData],
    file_path_without_extension: str,
) -> Tuple[Dict[str, Dict[str, int]], str]:
    llm_bin: Dict[str, Dict[str, int]] = defaultdict(lambda: {"total": 0, "perfect": 0})
    for llm_response_json_evaluation_unit in llm_response_json_evaluation_data:
        llm_model_id = llm_response_json_evaluation_unit.llm_response_planning_data.llm_response.llm_model_id

        # check if translation is intact
        stat = llm_response_json_evaluation_unit.json_translation_stat
        is_perfect_translation = True
        llm_bin[llm_model_id]["total"] += 1

        if stat is None:
            continue

        for field in stat.model_fields_set:
            field_obj = getattr(stat, field)
            if field_obj.num_correct != field_obj.total:
                is_perfect_translation = False

        if is_perfect_translation:
            llm_bin[llm_model_id]["perfect"] += 1

    file_path = get_file_path(
        file_path_without_extension=file_path_without_extension,
        key_words=["d2json", "stat", "summary"],
        extension="json",
    )
    write_json_from_dict(file_path=file_path, dic=llm_bin)

    return llm_bin, file_path
