from parameterized import parameterized

from habr.career.client.vacancies import (
    VacanciesSort,
    VacancyType,
    EmploymentType,
)
from habr.career.utils import Currency, QualificationID
from tests.utils import BasicTestCase


class VacanciesTestCase(BasicTestCase):
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
    pass


class GetVacanciesTestCase(BasicTestCase):
    def test_get_vacancies(self):
        result = self.client.get_vacancies()
        self.assertIn("list", result)
        self.assertIn("meta", result)
        self.assertIn("recommendedQuickVacancies", result)

    @parameterized.expand([
        (2, 7),
    ])
    def test_pagination(self, page, per_page):
        result = self.client.get_vacancies(page=page, per_page=per_page)
        self.assertEqual(result["meta"]["perPage"], per_page)
        self.assertEqual(result["meta"]["currentPage"], page)

    # def test_sorting(self):
    #     result = self.client.get_vacancies(sort=VacanciesSort.RELEVANCE)
    #
    # def test_filtering_by_type(self):
    #     result = self.client.get_vacancies(type_=VacancyType.ALL)
    #
    # def test_filtering_by_query(self):
    #     result = self.client.get_vacancies(search="test")

    @parameterized.expand([
        (2, "Бэкенд разработчик"),
    ])
    def test_filtering_by_specializations(self, specialization, label):
        result = self.client.get_vacancies(specializations=[specialization])
        self.assertTrue(all([
            label in [z["title"] for z in x["divisions"]]
            for x in result["list"]
        ]))

    @parameterized.expand([
        (QualificationID.INTERN, "Стажёр (Intern)"),
        (QualificationID.JUNIOR, "Младший (Junior)"),
        (QualificationID.MIDDLE, "Средний (Middle)"),
        (QualificationID.SENIOR, "Старший (Senior)"),
        (QualificationID.LEAD, "Ведущий (Lead)"),
    ])
    def test_filtering_by_qualification(self, qualification, label):
        result = self.client.get_vacancies(qualification=qualification)
        self.assertTrue([
            x["salaryQualification"]["title"] == label
            for x in result["list"]
        ])

    @parameterized.expand([
        (446, "Python"),
    ])
    def test_filtering_by_skills(self, skill, label):
        result = self.client.get_vacancies(skills=[skill])
        self.assertTrue(all([
            label in [z["title"] for z in x["skills"]]
            for x in result["list"]
        ]))

    # def test_filtering_by_salary(self):
    #     result = self.client.get_vacancies(
    #         salary=400000, currency=Currency.RUR)

    # def test_filtering_by_with_salary(self):
    #     result = self.client.get_vacancies(with_salary=True)

    @parameterized.expand([
        (87191269, "Онлайн-кинотеатр Иви"),
    ])
    def test_filtering_by_company(self, company, label):
        result = self.client.get_vacancies(company=company,
                                           exclude_company=None)
        self.assertTrue(all([
            x["company"]["title"] == label
            for x in result["list"]])
        )

    def test_filtering_by_remote(self):
        result = self.client.get_vacancies(remote=True)
        self.assertTrue(all([
            x["remoteWork"] for x in result["list"]])
        )

    def test_filtering_by_has_accreditation(self):
        result = self.client.get_vacancies(has_accreditation=True)
        self.assertTrue(all([
            x["company"]["accredited"] for x in result["list"]])
        )

    @parameterized.expand([
        ("c_707", "Краснодар"),
    ])
    def test_filtering_by_locations(self, location, label):
        result = self.client.get_vacancies(locations=[location])
        self.assertTrue(all([
            label in [
                z["title"] for z in x["locations"]]
            for x in result["list"]
        ]))

    @parameterized.expand([
        (EmploymentType.FULL_TIME,),
        (EmploymentType.PART_TIME,),
    ])
    def test_filtering_by_employment_type(self, employment_type):
        result = self.client.get_vacancies(employment_type=employment_type)
        self.assertTrue(all([
            x["employment"] == str(employment_type)
            for x in result["list"]])
        )
