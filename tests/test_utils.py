import unittest
from time import sleep, time

from parameterized import parameterized

from habr.career.utils import (
    get_ssr_json,
    cleanup_tags,
    bool_to_str,
    ConcurrentJobs,
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

    def test_concurrent_jobs(self) -> None:
        jobs = ConcurrentJobs()

        for _ in range(10):
            jobs.register(sleep, 1)

        t1 = time()
        list(jobs.run())
        dt = time() - t1

        self.assertAlmostEqual(dt, 1, delta=0.01)
