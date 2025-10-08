from collections import defaultdict
from typing import Dict
from pydantic import BaseModel
from profiler.data_types.generator_data_type import (
    AgentInfoGeneratorInput,
)


class BooleanCounter(BaseModel):
    true: int = 0
    false: int = 0

    def update_counter(self, is_true: bool) -> None:
        if is_true:
            self.true += 1
        else:
            self.false += 1


class CheckPointModel(BaseModel):
    idx: int


class LLMResponseHistogram(BaseModel):
    # The number of available agents
    # # of True & # of False
    num_agents: Dict[str, BooleanCounter] = defaultdict(lambda: BooleanCounter())
    # The number of variables
    num_var: Dict[str, BooleanCounter] = defaultdict(lambda: BooleanCounter())
    # The number of input parameters for an agent (action)
    # The number of output parameters for an agent is equal to The number of input parameters for an agent
    num_input_parameters: Dict[str, BooleanCounter] = defaultdict(lambda: BooleanCounter())
    # The number of goal agents in available agents
    num_goal_agents: Dict[str, BooleanCounter] = defaultdict(lambda: BooleanCounter())
    # The proportion of coupled agents
    proportion_coupled_agents: Dict[str, BooleanCounter] = defaultdict(lambda: BooleanCounter())
    # The proportion of slot-fillable variables
    proportion_slot_fillable_variables: Dict[str, BooleanCounter] = defaultdict(lambda: BooleanCounter())
    # The proportion of mappable variables
    proportion_mappable_variables: Dict[str, BooleanCounter] = defaultdict(lambda: BooleanCounter())

    def update_histogram(self, input: AgentInfoGeneratorInput, is_true: bool) -> None:
        self.num_agents[str(input.num_agents)].update_counter(is_true=is_true)
        self.num_var[str(input.num_var)].update_counter(is_true=is_true)
        self.num_input_parameters[str(input.num_input_parameters)].update_counter(is_true=is_true)
        self.num_goal_agents[str(input.num_goal_agents)].update_counter(is_true=is_true)
        self.proportion_coupled_agents[str(input.proportion_coupled_agents)].update_counter(is_true=is_true)
        self.proportion_slot_fillable_variables[str(input.proportion_slot_fillable_variables)].update_counter(
            is_true=is_true
        )
        self.proportion_mappable_variables[str(input.proportion_mappable_variables)].update_counter(is_true=is_true)
