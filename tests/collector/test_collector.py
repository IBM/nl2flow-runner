import os
import unittest

from ai_profiling.helpers.prompt_helper.planner_prompt_helper import get_planning_prompt
from ai_profiling.pipeline.llm_planning_pipeline import retrieve_llm_plans


class TestCollector(unittest.TestCase):
    async def test_collector_plan(self) -> None:
        llm_plan_file_path = await retrieve_llm_plans(
            planning_source_file_path="/Users/jungkookang/Downloads/nl2flow_test/output/generator",
            file_path_without_extension="/Users/jungkookang/Downloads/nl2flow_test/output/",
            api_key=os.environ.get("LLM_SERVICE_API_KEY"),
            max_token=1500,
            min_new_tokens=1,
            temperature=0.0,
            time_limit=480,
            num_generations=1,
            llm_model_ids=["Qwen/Qwen2.5-72B-Instruct"],
            prompt_function=get_planning_prompt,
            is_concise=False,
            start_index=0,
        )

        assert len(llm_plan_file_path) > 0
