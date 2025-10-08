from typing import Tuple
import unittest
from tests.test_helpers.file_helper import read_str_from_file, write_str_on_file
from ai_profiling.helpers.api_ai_helper.open_ai_api_helper.open_ai_api_helper import get_response_from_open_ai_model
from ai_profiling.helpers.prompt_helper.planner_prompt_helper import (
    get_prompt_description_to_plan,
    get_prompt_description_to_pddl,
    get_prompt_pddl_to_plan,
    get_prompt_description_to_tarski,
)
from profiler.common_helpers.string_helper import trim_pddl_str
from profiler.test_helpers.profiler_test_helper_variables import (
    pddl_start_key,
)


@unittest.skip("deprecated")
class TestPrompts(unittest.TestCase):
    def get_formatted_pddl_strs(self) -> Tuple[str, str]:
        pddl_domain = read_str_from_file("./tests/data/pddl/domain.pddl")
        pddl_problem = read_str_from_file("./tests/data/pddl/problem.pddl")
        return trim_pddl_str(pddl_domain, pddl_start_key), trim_pddl_str(pddl_problem, pddl_start_key)

    @unittest.skip("Check LLM's response only once")
    def test_do_you_know_pddl_gpt4(self):
        prompt = "Do you know Planning Domain Definition Language (PDDL)? Can you show me an example?"
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=1
        )
        write_str_on_file("do_you_know_pddl_gpt4.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_do_you_know_pddl_gpt35turbo(self):
        prompt = "Do you know Planning Domain Definition Language (PDDL)? Can you show me an example?"
        responses = get_response_from_open_ai_model(
            model_name="gpt-3.5-turbo", prompt=prompt, model_temperature=0.0, num_responses=1
        )
        write_str_on_file("do_you_know_pddl_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_do_you_know_pddl_gpt3(self):
        prompt = "Do you know Planning Domain Definition Language (PDDL)? Can you show me an example?"
        responses = get_response_from_open_ai_model(
            model_name="davinci", prompt=prompt, model_temperature=0.0, num_responses=1
        )
        write_str_on_file("do_you_know_pddl_gpt3.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_python_pddl_library_gpt4(self):
        prompt = "Which python library is the best to generate Planning Domain Definition Language (PDDL) files?"
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=1
        )
        write_str_on_file("python_pddl_conversion_gpt4.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_python_pddl_library_gpt35turbo(self):
        prompt = "Which python library is the best to generate Planning Domain Definition Language (PDDL) files?"
        responses = get_response_from_open_ai_model(
            model_name="gpt-3.5-turbo", prompt=prompt, model_temperature=0.0, num_responses=1
        )
        write_str_on_file("python_pddl_conversion_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_tarski_library_gpt4(self):
        prompt = (
            "Tarski is a python library to generate Planning Domain Definition Language (PDDL)"
            + " files. Show me an example of the use of tarski."
        )
        responses = get_response_from_open_ai_model(
            model_name="gpt4", prompt=prompt, model_temperature=0.0, num_responses=1
        )
        write_str_on_file("python_tarski_example_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_tarski_library_gpt35turbo(self):
        prompt = (
            "Tarski is a python library to generate Planning Domain Definition Language (PDDL) files."
            + " Show me an example of the use of tarski."
        )
        responses = get_response_from_open_ai_model(
            model_name="gpt-3.5-turbo", prompt=prompt, model_temperature=0.0, num_responses=1
        )
        write_str_on_file("python_tarski_example_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_to_tarski_translation_gpt_4(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description.txt")
        prompt = get_prompt_description_to_tarski(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_tarski_translation_response_gpt4.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_to_tarski_translation_gpt35turbo(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description.txt")
        prompt = get_prompt_description_to_tarski(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-3.5-turbo", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_tarski_translation_response_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_no_ask_last_resort_plan_gpt_4(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description_no_ask_last_resort.txt")
        prompt = get_prompt_description_to_plan(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_plan_response.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_cost_plan_gpt_4(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description_cost_planning.txt")
        prompt = get_prompt_description_to_plan(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_plan_response.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_plan_gpt_4(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description.txt")
        prompt = get_prompt_description_to_plan(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_plan_response.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_plan_small_gpt_4(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description_small.txt")
        prompt = get_prompt_description_to_plan(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_plan_response_small_gpt4.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_plan_small_gpt35turbo(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description_small.txt")
        prompt = get_prompt_description_to_plan(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-3.5-turbo", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_plan_response_small_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_plan_small_gpt3(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description_small.txt")
        prompt = get_prompt_description_to_plan(description)
        responses = get_response_from_open_ai_model(
            model_name="davinci", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_plan_response_small_gpt3.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_to_pddl_gpt4(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description.txt")
        prompt = get_prompt_description_to_pddl(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_pddl_translation_response_gpt4.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_to_pddl_gpt35turbo(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description.txt")
        prompt = get_prompt_description_to_pddl(description)
        responses = get_response_from_open_ai_model(
            model_name="gpt-3.5-turbo", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_pddl_translation_response_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_description_to_pddl_gpt3(self):
        num_responses = 1
        description = read_str_from_file("./tests/data/info_generator/descriptions/description_small.txt")
        prompt = get_prompt_description_to_pddl(description)
        responses = get_response_from_open_ai_model(
            model_name="davinci", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("description_to_pddl_translation_response_gpt3.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_pddl_to_plan_gpt4(self):
        pddl_domain, pddl_problem = self.get_formatted_pddl_strs()
        prompt = get_prompt_pddl_to_plan(pddl_domain, pddl_problem)
        num_responses = 1
        responses = get_response_from_open_ai_model(
            model_name="gpt-4", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("pddl_to_plan_response_gpt4.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_pddl_to_plan_gpt35turbo(self):
        pddl_domain, pddl_problem = self.get_formatted_pddl_strs()
        prompt = get_prompt_pddl_to_plan(pddl_domain, pddl_problem)
        num_responses = 1
        responses = get_response_from_open_ai_model(
            model_name="gpt-3.5-turbo", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("pddl_to_plan_response_gpt35turbo.txt", responses[0])

    @unittest.skip("Check LLM's response only once")
    def test_pddl_to_plan_gpt3(self):
        pddl_domain, pddl_problem = self.get_formatted_pddl_strs()
        prompt = get_prompt_pddl_to_plan(pddl_domain, pddl_problem)
        num_responses = 1
        responses = get_response_from_open_ai_model(
            model_name="davinci", prompt=prompt, model_temperature=0.0, num_responses=num_responses
        )
        write_str_on_file("pddl_to_plan_response_gpt3.txt", responses[0])
