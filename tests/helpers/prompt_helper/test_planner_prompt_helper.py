import unittest

from ai_profiling.helpers.prompt_helper.planner_prompt_helper import (
    parse_llm_planner_response,
    get_optimal_plan_str_from_prretified_plan_str,
)


class TestPlannerPromptHelper(unittest.TestCase):
    @unittest.skip("deprecated")
    def test_parse_llm_planner_response(self) -> None:
        response = (
            " \n\nPLAN EXPLANATION\n0. Execute action a__0. This will result in acquiring v__1.\n1."
            + " Execute action a__1 with v__1 as input. This will result in acquiring v__2.\n2."
            + "Execute action ask with v__4 as input. This will result in acquiring v__4.\n3."
            + " Execute action a__2 with v__3 as input. Since a__2 was a goal of this plan,"
            + " return the results of a__2(v__3) to the user.\n4. Execute action a__0 with v__4 as input."
            + " Since a__0 was a goal of this plan, return the results of a__0(v__4)"
            + " to the user.\n\nPLAN\n[0] v__1 = a__0(v__0)\n[1] v__2 = a__1(v__1)\n[2] v__4"
            + " = ask(v__4)\n[3] a__2(v__3)\n[4] a__0(v__4)"
        )
        plan = parse_llm_planner_response(response)
        self.assertEqual(len(plan), 5)

    def test_get_llm_response_example(self) -> None:
        prettified_plan_str = (
            "\n\n---- Plan #0 ----\nCost: 100010.0, Length: 2\n\n[0] ask(v__0)\n" + "[1] v__1 = a__0(v__0)"
        )
        optimal_plan_str = get_optimal_plan_str_from_prretified_plan_str(prettified_plan_str)
        self.assertEqual(optimal_plan_str, "[0] ask(v__0)\n[1] v__1 = a__0(v__0)")
