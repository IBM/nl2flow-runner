import unittest
from ai_profiling.helpers.hash_helper.hash_helper import get_list_hash, format_plan, get_plan_hash


class TestHashHelper(unittest.TestCase):
    def test_get_list_hash(self):
        lst_0 = ["c", "d", "e"]
        hash_0 = get_list_hash(lst_0)
        lst_1 = ["c", "d", "f"]
        hash_1 = get_list_hash(lst_1)
        self.assertNotEqual(hash_0, hash_1)

    def test_format_plan(self):
        plan = ["(n b a)", "(c j b a)"]
        formatted_plan = format_plan(plan)
        self.assertEqual(2, len(formatted_plan))
        self.assertEqual("(n a b)", formatted_plan[0])
        self.assertEqual("(c a b j)", formatted_plan[1])

    def test_get_plan_hash(self):
        plan = ["(n b a)", "(c j b a)"]
        plan_hash = get_plan_hash(plan)
        self.assertGreater(len(plan_hash), 0)
