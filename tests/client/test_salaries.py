from tests.utils import BasicTestCase


class SalariesTestCase(BasicTestCase):
    def test_my_salary(self):
        result = self.client.my_salary()
        self.assertIn("periods", result)
        self.assertIn("lastSalary", result)
        self.assertIn("currentPeriod", result)
        self.assertIn("feedbackIsActive", result)
        self.assertIn("leftFeedback", result)
        self.assertIn("hasServices", result)

    def test_get_suitable_vacancies(self):
        result = self.client.get_suitable_vacancies()
        self.assertIsInstance(result, list)

    def test_get_suitable_courses(self):
        result = self.client.get_suitable_courses()
        self.assertIsInstance(result, list)

    def test_get_salary_reports(self):
        result = self.client.get_salary_reports()
        self.assertIsInstance(result, list)

    def test_get_salary_general_graph(self):
        result = self.client.get_salary_general_graph()
        self.assertIn("groups", result)
        self.assertEqual(len(result["groups"]), 6)

    def test_get_salary_dynamic_graph(self):
        result = self.client.get_salary_dynamic_graph()
        self.assertIn("graphs_data", result)

    def test_get_salary_chart(self):
        result = self.client.get_salary_chart()
        self.assertIn("title", result)
        self.assertIn("values", result)
        self.assertIn("diagramHref", result)

    def test_get_locations_suggestions(self):
        result = self.client.get_locations_suggestions("test")
        self.assertIsInstance(result, list)

    def test_get_companies_suggestions(self):
        result = self.client.get_companies_suggestions("test")
        self.assertIsInstance(result, list)
