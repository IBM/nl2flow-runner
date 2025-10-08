import os
from pathlib import Path
import unittest

from ai_profiling.pipeline.llm_planning_pipeline import run_llm_plan_validation

current_file_path = Path(__file__).parent.resolve()


class TestEvaluator(unittest.TestCase):
    @unittest.skip("provide an absolute path of Validate from Val")
    def test_evaluator_val(self):
        output_file_paths = run_llm_plan_validation(
            llm_response_file_path=Path(os.path.join(current_file_path.parent, "data", "collector", "plan", "long")),
            file_path_without_extension=Path(os.path.join(current_file_path.parent.parent, "output")),
            cache_folder_path=Path(os.path.join(current_file_path.parent.parent, "cache")),
            val_path=Path("/Users/jungkookang/Documents/projects/VAL/bin/Validate"),
        )

        self.assertIsNotNone(output_file_paths)

    def test_evaluator_nl2flow(self):
        output_file_paths = run_llm_plan_validation(
            llm_response_file_path=Path(os.path.join(current_file_path.parent, "data", "collector", "plan", "long")),
            file_path_without_extension=Path(os.path.join(current_file_path.parent.parent, "output")),
            cache_folder_path=Path(os.path.join(current_file_path.parent.parent, "cache")),
            val_path=None,
        )

        self.assertIsNotNone(output_file_paths)
