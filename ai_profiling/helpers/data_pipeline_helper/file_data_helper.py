import random
from typing import List, Tuple
from profiler.data_types.pddl_generator_datatypes import PddlGeneratorOutput

from ai_profiling.helpers.file_helper.file_helper import get_file_path, write_jsonl


def write_files_data_pipeline(
    file_path: str,
    pddl_generator_outputs: List[PddlGeneratorOutput],
    training_prop: float,
    validation_prop: float,
) -> Tuple[str, str, str]:
    total_length = len(pddl_generator_outputs)
    len_training = int(total_length * training_prop)
    len_validation = int(total_length * validation_prop)

    pddl_generator_outputs_shuffled = list(map(lambda model: model.model_copy(deep=True), pddl_generator_outputs))
    random.shuffle(pddl_generator_outputs_shuffled)

    training_dataset = pddl_generator_outputs_shuffled[:len_training]
    validation_dataset = pddl_generator_outputs_shuffled[len_training : len_training + len_validation]  # noqa: E203
    test_dataset = pddl_generator_outputs_shuffled[len_training + len_validation :]  # noqa: E203

    file_extension = "jsonl"
    training_file_path = get_file_path(
        file_path_without_extension=file_path,
        key_words=["training"],
        extension=file_extension,
    )
    validation_file_path = get_file_path(
        file_path_without_extension=file_path,
        key_words=["validation"],
        extension=file_extension,
    )
    test_file_path = get_file_path(
        file_path_without_extension=file_path,
        key_words=["test"],
        extension=file_extension,
    )

    write_jsonl(file_path=training_file_path, base_models=training_dataset)
    write_jsonl(file_path=validation_file_path, base_models=validation_dataset)
    write_jsonl(file_path=test_file_path, base_models=test_dataset)

    return training_file_path, validation_file_path, test_file_path
