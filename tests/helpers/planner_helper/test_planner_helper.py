import unittest
from tests.test_helpers.file_helper import read_str_from_file
from ai_profiling.helpers.str_helper.str_helper import get_pddl_strs
from ai_profiling.helpers.planner_helper.planner_helper import (
    get_plans,
    transform_LLM_plan_to_raw_plan,
    transform_pretty_plan_to_raw_plan,
    transform_pretty_plan_action_to_pddl_action,
)
from nl2flow.plan.planners.kstar import Kstar


PLANNER = Kstar()


class TestPlannerHelper(unittest.TestCase):
    @unittest.skip("deprecated")
    def test_get_plans(self):
        response = read_str_from_file("./tests/data/responses/description_to_pddl_translation_response.txt")
        pddl_domain_str, pddl_problem_str = get_pddl_strs(response)
        plans = get_plans(pddl_domain_str, pddl_problem_str, PLANNER)
        self.assertEqual(1, len(plans))

    def test_transform_pretty_plan_action_to_pddl_action(self):
        action_str = "Step 0: Fix errors, Inputs: v__1 (generic), v__2(generic), Outputs: None"
        res = transform_pretty_plan_action_to_pddl_action(action_str)
        self.assertEqual("(Fix_errors v__1 v__2)", res)

    def test_transform_pretty_plan_to_raw_plan(self):
        pretty_plan = read_str_from_file("./tests/data/pddl/pretty_plan.txt")
        plans = transform_pretty_plan_to_raw_plan(pretty_plan)
        self.assertEqual(1, len(plans))
        self.assertEqual("(ask list_of_errors)", plans[0][0])
        self.assertEqual("(Fix_Errors list_of_errors)", plans[0][1])

    @unittest.skip("deprecated")
    def test_transform_LLM_plan_to_raw_plan(self):
        llm_plan_str = read_str_from_file("./tests/data/responses/description_plan_response.txt")
        actions, debug_messages = transform_LLM_plan_to_raw_plan(llm_plan_str)
        self.assertEqual(6, len(actions))
        self.assertEqual("(ask v__0)", actions[0])
        self.assertEqual("(a__20 v__4 v__0)", actions[5])
        self.assertEqual(1, len(debug_messages))
        self.assertEqual(
            "7. No plan for Action a__7, as Variable v__6 cannot be acquired by asking the user.",
            debug_messages[0],
        )
