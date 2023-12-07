from tests.utils import BasicTestCase


class ToolsTestCase(BasicTestCase):
    def test_get_cities_suggestions(self):
        result = self.client.get_cities_suggestions(search="Moscow")
        self.assertIsInstance(result, list)

    def test_get_skills_alias_suggestions(self):
        result = self.client.get_skills_alias_suggestions(search="python")
        self.assertIsInstance(result, list)

    def test_get_skills_ids_suggestions(self):
        result = self.client.get_skills_ids_suggestions(search="python")
        self.assertIsInstance(result, list)

    def test_get_qualifications(self):
        result = self.client.get_qualifications()
        self.assertIsInstance(result, list)

    def test_get_currencies(self):
        result = self.client.get_currencies()
        self.assertIsInstance(result, list)

    def test_get_similar_skills(self):
        result = self.client.get_similar_skills()
        self.assertIsInstance(result, list)

    def test_get_similar_skills_extended(self):
        result = self.client.get_similar_skills_extended()
        self.assertIsInstance(result, list)
