# mapper_prompt = 'When one variable can be used for another variable, express it by using an action whose name is "map"' # noqa: E501
plan_formatting_prompt = (
    "Make sure that actions to execute are defined properly as actions in PDDL." + ' Remove "execute-" in action names.'
)  # + mapper_prompt

description_plan_prompt = (
    "How can it achieve it? Give only action names and parameters as (<action-name> <paramaters>) and nothing else."
    + " Ensure the order of input and output variables matches the original action description."
    + " Show only one action per line.\n"
)
# + mapper_prompt
description_plan_prompt += 'If there is no way to achieve goals, say "no plan"\n'

tarski_description = "Tarski is a python library to generate Planning Domain Definition Language (PDDL) files."

description_to_tarski_Conversion_instruction = (
    "Convert the text description of domain and problem into python code with tarski"
)

# + mapper_prompt
plan_instruction_prompt = (
    "Come up with a plan to solve the problem. Give only action names"
    + " and parameters as (<action-name> <paramaters>) and nothing else."
    + "  Ensure the order of input and output variables matches the original action description.\n"
)

pddl_domain_problem_introduction_prompt = (
    "The following paragraphs are a domain and a problem described in Planning Domain Definition Language (PDDL)"
)
description_to_pddl_introduction_prompt = (
    "The following paragraph contains the text descriptions of a domain and a problem."
)
description_to_pddl_instruction_prompt = (
    "Write a domain and a problem described in the text in Planning Domain Definition Language (PDDL).\n"
    + plan_formatting_prompt
)
