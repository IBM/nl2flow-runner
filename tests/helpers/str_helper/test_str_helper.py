import unittest
from tests.test_helpers.file_helper import read_str_from_file
from ai_profiling.helpers.str_helper.str_helper import get_pddl_strs
from ai_profiling.helpers.str_helper.str_helper_variables import pddl_domain_start_key, pddl_problem_start_key


class TestStrHelper(unittest.TestCase):
    @unittest.skip("deprecated")
    def test_get_pddl_strs(self):
        response = read_str_from_file("./tests/data/responses/description_to_pddl_translation_response.txt")
        pddl_domain_str, pddl_problem_str = get_pddl_strs(response)
        assert pddl_domain_start_key in pddl_domain_str
        assert pddl_problem_start_key in pddl_problem_str
