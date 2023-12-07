from tests.utils import BasicTestCase


class CompaniesTestCase(BasicTestCase):
    def test_get_companies_ratings(self):
        result = self.client.get_companies_ratings()
        self.assertIn("list", result)
        self.assertIn("meta", result)
