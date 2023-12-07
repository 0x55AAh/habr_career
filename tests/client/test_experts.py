from tests.utils import BasicTestCase


class ExpertsTestCase(BasicTestCase):
    def test_get_experts(self):
        result = self.client.get_experts()
        self.assertIn("list", result)
        self.assertIn("meta", result)
