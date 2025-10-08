# import unittest
# from ai_profiling.helpers.token_helper.token_helper import get_token_length
# from tests.test_helpers.file_helper import read_str_from_file


# class TestTokenHelper(unittest.TestCase):
#     def test_get_token_length_basic(self):
#         token_length = get_token_length("gpt-4", "Hello World")
#         self.assertEqual(token_length, 2)

#     def test_get_token_length_short_plan(self):
#         short_plan_str = read_str_from_file(
#             "./tests//data/pddl/plan.pddl")
#         token_length = get_token_length("gpt-4", short_plan_str)
#         self.assertEqual(token_length, 12)

#     def test_get_token_length_short_domain(self):
#         short_plan_str = read_str_from_file(
#             "./tests/data/pddl/domain.pddl")
#         token_length = get_token_length("gpt-4", short_plan_str)
#         self.assertEqual(token_length, 1813)
