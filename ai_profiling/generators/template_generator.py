import random
from typing import Callable, List, Optional, Set, Tuple
from ai_profiling.datatypes.planning_datatype import AgentInfoUnitModel
from profiler.data_types.agent_info_data_types import AgentInfo
from ai_profiling.helpers.file_helper.file_helper import write_txt_file


def write_planning_source_list_on_file(
    file_path: str,
    prompt_function: Callable[
        [
            List[AgentInfo],
            Set[str],
            List[Tuple[str, str, float]],
            List[Tuple[str, Optional[str]]],
        ],
        str,
    ],
    planning_source_list: List[AgentInfoUnitModel],
) -> str:
    planning_examples: List[str] = []
    for planning_source in planning_source_list:
        planning_examples.append(
            prompt_function(
                available_agents=planning_source.available_agents,
                goal_agent_ids=set(planning_source.goal_agent_ids),
                mappings=planning_source.mappings,
                available_data=planning_source.available_data,
            )
        )

    random.shuffle(planning_examples)

    txt_sources: List[str] = []
    for idx, planning_example in enumerate(planning_examples):
        txt_sources.append(f"Example #{idx + 1}\n" + planning_example[:])

    planning_eamples_text = "\n\n".join(txt_sources)
    write_txt_file(file_path, planning_eamples_text)

    return planning_eamples_text
