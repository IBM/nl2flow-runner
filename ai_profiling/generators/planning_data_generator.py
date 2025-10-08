import os
from pathlib import Path
from typing import List
from profiler.generators.batch_data_generator.batch_data_generator import (
    get_pddl_generator_output_batch,
)
from profiler.data_types.generator_data_type import (
    AgentInfoGeneratorInputBatch,
)
from nl2flow.plan.planners.kstar import Kstar
import random
from ai_profiling.datatypes.stat_datatype import CheckPointModel
from profiler.data_types.pddl_generator_datatypes import PddlGeneratorOutput

from ai_profiling.helpers.file_helper.file_helper import get_date_time_str, write_json_record


PLANNER = Kstar()


def generate_planning_data(
    agent_info_generator_input_batch: AgentInfoGeneratorInputBatch, random_seed: int
) -> List[PddlGeneratorOutput]:
    random.seed(random_seed)
    pddl_generator_output_aggregate: List[PddlGeneratorOutput] = []
    for pddl_generator_output_batch in get_pddl_generator_output_batch(
        batch_input=agent_info_generator_input_batch,
        planner=PLANNER,
        random=random,
    ):
        if pddl_generator_output_batch is not None:
            pddl_generator_output_aggregate.extend(pddl_generator_output_batch)

    return pddl_generator_output_aggregate


def generate_insert_planning_data_to_db(
    agent_info_generator_input_batch: AgentInfoGeneratorInputBatch,
    random_seed: int,
    output_folder_path: Path,
) -> None:
    random.seed(random_seed)
    output_file_prefix = "planning_data"
    cnt = 0
    index_file_name = get_date_time_str() + ".ckpt"
    for idx_generation_batch, pddl_generator_output_batch in enumerate(
        get_pddl_generator_output_batch(
            batch_input=agent_info_generator_input_batch,
            planner=PLANNER,
            random=random,
        )
    ):
        write_json_record(
            file_path=Path(os.path.join(output_folder_path, index_file_name)),
            base_model=CheckPointModel(idx=idx_generation_batch),
        )
        if len(pddl_generator_output_batch) > 0:
            for pddl_generator_output in pddl_generator_output_batch:
                file_name = output_file_prefix + "_" + pddl_generator_output.sample_hash + ".json"
                write_json_record(
                    file_path=Path(os.path.join(output_folder_path, file_name)), base_model=pddl_generator_output
                )
                cnt += 1
