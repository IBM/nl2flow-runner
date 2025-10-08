import json
import unittest
from ai_profiling.datatypes.database_datatype import LlmRecord


class TestConversion(unittest.TestCase):
    @unittest.skip("deprecated")
    def test_pydantic_data_conversion(self):
        test_dict = {"_id": "abc", "query_txt": "", "response_str": "", "query_source_hash": ""}
        json_bin = json.dumps(test_dict)
        res = LlmRecord.parse_obj(test_dict)  # dict -> BaseModel
        res_json = LlmRecord.parse_raw(json_bin)  # json -> BaseModel
        self.assertIsNotNone(res)
        self.assertIsNotNone(res_json)
