from tests.utils import BasicTestCase


class ResumesTestCase(BasicTestCase):
    def test_get_friends(self):
        result = self.client.get_resumes()
        self.assertIn("list", result)
        self.assertIn("meta", result)
        self.assertIn("limitedAccess", result)

    def test_get_resumes_data(self):
        result = self.client.get_resumes_data()
        self.assertIn("isGuest", result)
        self.assertIn("tabs", result)
        self.assertIn("search", result)
        self.assertIn("options", result)
        self.assertIn("filtersData", result)
        self.assertIn("resumes", result)
        self.assertIn("vacancyBanners", result)

    def test_get_universities_suggestions(self):
        result = self.client.get_universities_suggestions("test")
        self.assertIsInstance(result, list)

    def test_get_education_centers_suggestions(self):
        result = self.client.get_education_centers_suggestions("test")
        self.assertIsInstance(result, list)
