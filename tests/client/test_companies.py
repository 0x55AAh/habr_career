from tests.utils import BasicTestCase


class CompaniesTestCase(BasicTestCase):
    test_company = "ivi"

    def test_get_companies_ratings(self):
        result = self.client.get_companies_ratings()
        # self.assertIn("list", result)
        # self.assertIn("meta", result)

    def test_subscribe_company(self):
        result = self.client.subscribe_company(self.test_company)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_unsubscribe_company(self):
        result = self.client.unsubscribe_company(self.test_company)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_favorite_company(self):
        result = self.client.favorite_company(self.test_company)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_unfavorite_company(self):
        result = self.client.unfavorite_company(self.test_company)
        self.assertIn("success", result)
        self.assertTrue(result["success"])
