from copy import deepcopy
from typing import List
from profiler.data_types.agent_info_data_types import (
    AgentInfo,
    AgentInfoSignature,
    AgentInfoSignatureItem,
)

from ai_profiling.datatypes.planning_datatype import AgentInfoUnitModel


SAMPLE_AGENT_INFOS: List[AgentInfo] = [
    AgentInfo(
        agent_id="C",
        actuator_signature=AgentInfoSignature(
            in_sig_full=[AgentInfoSignatureItem(name="bb", slot_fillable=True)],
            out_sig_full=[],
        ),
    ),
    AgentInfo(
        agent_id="A",
        actuator_signature=AgentInfoSignature(
            in_sig_full=[AgentInfoSignatureItem(name="aa", slot_fillable=False)],
            out_sig_full=[AgentInfoSignatureItem(name="bb", slot_fillable=True)],
        ),
    ),
    AgentInfo(
        agent_id="D",
        actuator_signature=AgentInfoSignature(
            in_sig_full=[AgentInfoSignatureItem(name="z", slot_fillable=False)],
            out_sig_full=[AgentInfoSignatureItem(name="aa", slot_fillable=False)],
        ),
    ),
    AgentInfo(
        agent_id="E",
        actuator_signature=AgentInfoSignature(
            in_sig_full=[
                AgentInfoSignatureItem(name="x", slot_fillable=True),
                AgentInfoSignatureItem(name="y", slot_fillable=True),
            ],
            out_sig_full=[AgentInfoSignatureItem(name="bb", slot_fillable=True)],
        ),
    ),
    AgentInfo(
        agent_id="B",
        actuator_signature=AgentInfoSignature(
            in_sig_full=[],
            out_sig_full=[AgentInfoSignatureItem(name="aa", slot_fillable=False)],
        ),
    ),
]

SAMPLE_MAPPINGS = [("cc", "bb", 1.0)]
SAMPLE_AVAILABLE_DATA = [("cc", None)]


def get_test_planning_sources() -> List[AgentInfoUnitModel]:
    planning_source_list: List[AgentInfoUnitModel] = []
    default_planning_source = AgentInfoUnitModel(
        available_agents=list(map(lambda model: model.model_copy(deep=True), SAMPLE_AGENT_INFOS)),
        goal_agent_ids=[SAMPLE_AGENT_INFOS[0].agent_id[:]],
        mappings=deepcopy(SAMPLE_MAPPINGS),
        available_data=deepcopy(SAMPLE_AVAILABLE_DATA),
    )

    # example 1
    planning_source_0 = default_planning_source.model_copy(deep=True)
    planning_source_0.shuffle_information()
    planning_source_list.append(planning_source_0)

    # example 1.1
    planning_source_0_0 = default_planning_source.model_copy(deep=True)
    planning_source_0_0.available_agents[1] = AgentInfo(
        agent_id="A",
        actuator_signature=AgentInfoSignature(
            in_sig_full=[
                AgentInfoSignatureItem(name="aa", slot_fillable=False),
                AgentInfoSignatureItem(name="cc", slot_fillable=True),
            ],
            out_sig_full=[AgentInfoSignatureItem(name="bb", slot_fillable=True)],
        ),
    )
    planning_source_0_0.available_agents[2] = AgentInfo(
        agent_id="D",
        actuator_signature=AgentInfoSignature(
            in_sig_full=[AgentInfoSignatureItem(name="z", slot_fillable=False)],
            out_sig_full=[
                AgentInfoSignatureItem(name="aa", slot_fillable=False),
                AgentInfoSignatureItem(name="u", slot_fillable=False),
            ],
        ),
    )
    planning_source_0_0.goal_agent_ids = [
        planning_source_0_0.available_agents[-2].agent_id,
        planning_source_0_0.available_agents[0].agent_id,
    ]
    planning_source_0_0.shuffle_information()
    planning_source_list.append(planning_source_0_0)

    # example 2
    planning_source_1 = default_planning_source.model_copy(deep=True)
    planning_source_1.goal_agent_ids = [
        planning_source_1.available_agents[0].agent_id,
        planning_source_1.available_agents[1].agent_id,
    ]
    planning_source_1.shuffle_information()
    planning_source_list.append(planning_source_1)

    # example 3
    planning_source_2 = default_planning_source.model_copy(deep=True)
    planning_source_2.goal_agent_ids = [
        planning_source_2.available_agents[2].agent_id,
    ]
    planning_source_2.mappings = []
    planning_source_2.shuffle_information()
    planning_source_list.append(planning_source_2)

    # example 4
    planning_source_3 = default_planning_source.model_copy(deep=True)
    planning_source_3.available_agents = planning_source_3.available_agents[-3:]
    planning_source_3.goal_agent_ids = [
        planning_source_3.available_agents[0].agent_id,
    ]
    planning_source_3.mappings = []
    planning_source_3.available_data = [("bb", None), ("z", None)]
    planning_source_3.shuffle_information()
    planning_source_list.append(planning_source_3)

    # example 5
    planning_source_4 = default_planning_source.model_copy(deep=True)
    planning_source_4.available_agents = [planning_source_4.available_agents[0]] + planning_source_4.available_agents[
        -2:
    ]
    planning_source_4.goal_agent_ids = [
        planning_source_4.available_agents[-1].agent_id,
    ]
    planning_source_4.shuffle_information()
    planning_source_list.append(planning_source_4)

    return planning_source_list
