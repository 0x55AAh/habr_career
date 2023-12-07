import unittest

from parameterized import parameterized

from habr.career.utils import (
    get_ssr_json,
    cleanup_tags,
    bool_to_str,
    QueryParams,
)


class UtilsTestCase(unittest.TestCase):
    def test_get_ssr_json(self) -> None:
        with open("tests/data/file_with_ssr_data.html") as f:
            data = get_ssr_json(f.read())
        self.assertEqual(data, {"value": "Testing"})

    def test_clean_tags(self):
        cleaned_text = "Test message"
        html_code = f"<p>{cleaned_text}</p>"
        self.assertEqual(cleanup_tags(html_code), cleaned_text)

    @parameterized.expand([
        (True, "true"),
        (False, "false"),
        (None, None),
    ])
    def test_bool_to_str(
            self,
            input_: bool | None,
            output_: str | None,
    ) -> None:
        self.assertEqual(bool_to_str(input_), output_)

    @parameterized.expand([
        (False, False, "t1=Test+1&t2=%5B%27Test+2%27%5D&t3=1"),
        (True, False, "t1=Test+1&t2=Test+2&t3=1"),
        (False, True, "t1=Test+1&t2=%5B%27Test+2%27%5D&t3=true"),
    ])
    def test_query_parameters(
            self,
            doseq: bool,
            bool_as_str: bool,
            expected_query: str,
    ) -> None:
        params = QueryParams({
            "t1": "Test 1",
            "t2": ["Test 2"],
            "t3": True,
            "t4": None,
        })
        query = params.query(doseq, bool_as_str)
        self.assertEqual(query, expected_query)
