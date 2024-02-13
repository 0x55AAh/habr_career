from parameterized import parameterized

from habr.career.client.resumes import CareerWorkState
from habr.career.utils import QualificationID
from tests.utils import BasicTestCase


class ResumesTestCase(BasicTestCase):
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


class GetResumesTestCase(BasicTestCase):
    # TODO:
    #  search: str | None = None,
    #  search_fields: list[CareerSearchField] | None = None,
    #  sort: CareerSortingCriteria | None = None,
    #  salary: int | None = None,
    #  currency: Currency | None = Currency.RUR,
    #  period: CareerActivityPeriod | None = None,
    def test_get_resumes(self):
        result = self.client.get_resumes()
        # self.assertIn("list", result)
        # self.assertIn("meta", result)
        # self.assertIn("limitedAccess", result)

    @parameterized.expand([
        (2, 7),
    ])
    def test_pagination(self, page, per_page):
        result = self.client.get_resumes(page=page, per_page=per_page)
        self.assertEqual(result.meta.per_page, per_page)
        self.assertEqual(result.meta.current_page, page)

    def test_filtering_by_relocation(self):
        result = self.client.get_resumes(relocation=True)
        self.assertTrue(all([x.relocation for x in result.objects]))

    def test_filtering_by_remote(self):
        result = self.client.get_resumes(remote=True)
        self.assertTrue(all([x.remote_work for x in result.objects]))

    @parameterized.expand([
        (QualificationID.INTERN, "Intern"),
        (QualificationID.JUNIOR, "Junior"),
        (QualificationID.MIDDLE, "Middle"),
        (QualificationID.SENIOR, "Senior"),
        (QualificationID.LEAD, "Lead"),
    ])
    def test_filtering_by_qualification(self, qualification, label):
        result = self.client.get_resumes(qualification=qualification)
        self.assertTrue(all(
            [x.qualification.title == label for x in result.objects]))

    @parameterized.expand([
        (CareerWorkState.NOT_SEARCH, "Не ищу работу"),
        (CareerWorkState.SEARCH, "Ищу работу"),
        (CareerWorkState.READY, "Рассмотрю предложения"),
    ])
    def test_filtering_by_work_state(self, work_state, label):
        result = self.client.get_resumes(work_state=work_state)
        self.assertTrue(all(
            [x.availability.title == label for x in result.objects]))

    @parameterized.expand([
        ("c_707", "Краснодар"),
    ])
    def test_filtering_by_locations(self, location, label):
        # TODO: exclude_locations: bool | None = None,
        result = self.client.get_resumes(locations=[location])
        self.assertTrue(all(
            [x.location.title == label for x in result.objects]))

    @parameterized.expand([
        (446, "Python"),
    ])
    def test_filtering_by_skills(self, skill, label):
        result = self.client.get_resumes(skills=[skill])
        self.assertTrue(all([
            label in [z.title for z in x.skills]
            for x in result.objects
        ]))

    @parameterized.expand([
        (35, {"Яндекс.Практикум", "Яндекс Практикум"}),
    ])
    def test_filtering_by_educations(self, education, labels):
        # Additional education
        # TODO: not_educations: bool | None = None,
        result = self.client.get_resumes(educations=[education])
        self.assertTrue(all([
            {e.title for e in x.additional_education} & labels
            for x in result.objects
        ]))

    # @parameterized.expand([
    #     (1894, "ННГУ им. Н.И. Лобачевского"),
    # ])
    # def test_filtering_by_universities(self, university, label):
    #     # TODO: not_universities: bool | None = None,
    #     result = self.client.get_resumes(universities=[university])
    #     self.assertTrue(all([
    #         # TODO: Указанный университет может и не быть в данном поле,
    #         #  но при этом быть в списке университетов в профиле
    #         x.education.university.title == label
    #         for x in result.objects
    #     ]))

    # @parameterized.expand([
    #     (87191269, "Онлайн-кинотеатр Иви"),
    # ])
    # def test_filtering_by_companies(self, company, label):
    #     # TODO: not_companies: bool | None = None,
    #     result = self.client.get_resumes(companies=[company])
    #     # TODO: Компания может и не быть lastJob, поэтому нужно смотреть
    #     #  в профиле

    # @parameterized.expand([
    #     (87191269, "Онлайн-кинотеатр Иви"),
    # ])
    # def test_filtering_by_companies_with_current_company(self, company,
    #                                                      label):
    #     result = self.client.get_resumes(companies=[company],
    #                                      current_company=True)
    #     # TODO: Попадаются левые компании
    #     self.assertTrue(all([
    #         x.last_job.company.title == label for x in result.objects]))

    @parameterized.expand([
        (2, "Бэкенд разработчик"),
    ])
    def test_filtering_by_specializations(self, specialization, label):
        result = self.client.get_resumes(specializations=[specialization])
        self.assertTrue(all([
            label in [z.title for z in x.specializations]
            for x in result.objects
        ]))

    def test_filtering_by_with_salary(self):
        # Указана зарплата
        result = self.client.get_resumes(with_salary=True)
        self.assertTrue(all([x.salary is not None for x in result.objects]))

    # def test_filtering_by_with_social_ratings(self):
    #     # Участник ИТ-сообществ
    #     # TODO: Фильтр отрабатывает с ошибками, пропуская тех у кого
    #     #  список сообществ пустой
    #     result = self.client.get_resumes(with_social_ratings=True)
    #     self.assertTrue(all([x.communities for x in result.objects]))

    def test_filtering_by_with_experiences(self):
        # С опытом работы
        result = self.client.get_resumes(with_experiences=True)
        self.assertTrue(all([
            x.experience is not None for x in result.objects]))

    def test_filtering_by_with_educations(self):
        # С высшим образованием
        result = self.client.get_resumes(with_educations=True)
        self.assertTrue(all([
            x.education is not None for x in result.objects]))

    def test_filtering_by_with_extra_educations(self):
        # С дополнительным образованием
        result = self.client.get_resumes(with_extra_educations=True)
        self.assertTrue(all([
            x.additional_education for x in result.objects]))