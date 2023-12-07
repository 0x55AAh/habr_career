from tests.utils import BasicTestCase


class VacanciesTestCase(BasicTestCase):
    def test_get_vacancies(self):
        result = self.client.get_vacancies()
        self.assertIn("list", result)
        self.assertIn("meta", result)
        self.assertIn("recommendedQuickVacancies", result)

    # def test_get_vacancy(self):
    #     result = self.client.get_vacancy(1000135136)
    #     self.assertIn("placeholder", result)
    #     self.assertIn("createResponse", result)
    #     self.assertIn("responses", result)
    #     self.assertIn("currencies", result)
    #     self.assertIn("favorite", result)
    #     self.assertIn("vacancy", result)
    #     self.assertIn("company", result)
    #     self.assertIn("similar", result)
    #     self.assertIn("landingLinks", result)

    # def test_get_vacancy_responses(self):
    #     result = self.client.get_vacancy_responses(1000135136)
    #     self.assertIn("list", result)
    #     self.assertIn("meta", result)
