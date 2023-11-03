import unittest

from habr.career.utils import get_ssr_json, bool_to_str, QueryParams


class UtilsTestCase(unittest.TestCase):
    def test_get_ssr_json(self):
        with open("tests/data/file_with_ssr_data.html") as f:
            data = get_ssr_json(f.read())
        self.assertEqual(data, {"value": "Testing"})

    def test_bool_to_str(self):
        self.assertEqual(bool_to_str(True), "true")
        self.assertEqual(bool_to_str(False), "false")
        self.assertEqual(bool_to_str(None), None)


class QueryParamsTestCase(unittest.TestCase):
    params = QueryParams({
        "t1": "Test 1",
        "t2": ["Test 2"],
        "t3": True,
        "t4": None,
    })

    def test_query_parameters(self):
        query = self.params.query()
        self.assertEqual(query, "t1=Test+1&t2=%5B%27Test+2%27%5D&t3=1")

    def test_doseq_true(self):
        query = self.params.query(doseq=True)
        self.assertEqual(query, "t1=Test+1&t2=Test+2&t3=1")

    def test_bool_as_str_true(self):
        query = self.params.query(bool_as_str=True)
        self.assertEqual(query, "t1=Test+1&t2=%5B%27Test+2%27%5D&t3=true")
