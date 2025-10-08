from typing import List
from profiler.data_types.pddl_generator_datatypes import PddlGeneratorOutput


def get_processed_pddl_generator_outputs(
    pddl_generator_outputs: List[PddlGeneratorOutput],
) -> List[PddlGeneratorOutput]:
    outputs: List[PddlGeneratorOutput] = []
    for pddl_generator_output in pddl_generator_outputs:
        for plan in pddl_generator_output.list_of_plans:
            plan.length = len(plan.plan)
        outputs.append(pddl_generator_output.model_copy(deep=True))
    return outputs
