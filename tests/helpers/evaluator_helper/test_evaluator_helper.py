import os
from pathlib import Path
import unittest

from ai_profiling.helpers.evaluator_helper.evaluator_helper import convert_nl2flow_plan_to_pddl_plan, validate_pddl_plan


test_folder_path = Path(__file__).parent.parent.parent.resolve()


class TestEvaluatorHelper(unittest.TestCase):
    @unittest.skip("provide an absolute path of Validate from Val")
    def test_validate_pddl_with_valid_plan(self):
        val_path = Path("/Users/jungkookang/Documents/projects/VAL/bin/Validate")
        domain_file = Path(os.path.join(test_folder_path, "data", "pddl", "domain.pddl"))
        problem_file = Path(os.path.join(test_folder_path, "data", "pddl", "problem.pddl"))
        plan_file = Path(os.path.join(test_folder_path, "data", "pddl", "plan.pddl"))
        output_model = validate_pddl_plan(
            val_path=val_path, domain_file=domain_file, problem_file=problem_file, plan_file=plan_file, cost=7
        )
        self.assertTrue(output_model.is_valid)
        self.assertTrue(output_model.is_executable)
        self.assertTrue(output_model.reach_goals)
        self.assertEqual(output_model.cost, 7)

    @unittest.skip("provide an absolute path of Validate from Val")
    def test_validate_pddl_with_invalid_plan(self):
        val_path = Path("/Users/jungkookang/Documents/projects/VAL/bin/Validate")
        domain_file = Path(os.path.join(test_folder_path, "data", "pddl", "domain.pddl"))
        problem_file = Path(os.path.join(test_folder_path, "data", "pddl", "problem.pddl"))
        plan_file = Path(os.path.join(test_folder_path, "data", "pddl", "invalid_plan.pddl"))
        output_model = validate_pddl_plan(
            val_path=val_path, domain_file=domain_file, problem_file=problem_file, plan_file=plan_file, cost=7
        )
        self.assertFalse(output_model.is_valid)
        self.assertFalse(output_model.is_executable)
        self.assertFalse(output_model.reach_goals)
        self.assertEqual(output_model.cost, -1)

    def test_convert_nl2flow_plan_to_pddl_plan(self):
        plan_nl2flow_txt = "a()\na1, b2 = data-mapper(job_id occupation_id)\nb()"
        pddl_plan_txt = convert_nl2flow_plan_to_pddl_plan(plan_nl2flow_txt=plan_nl2flow_txt)
        self.assertEqual(len(pddl_plan_txt), 42)
