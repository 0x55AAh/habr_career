from parameterized import parameterized

from habr.career.client.experts import RequestID
from habr.career.utils import Currency, QualificationID
from tests.utils import BasicTestCase


class ExpertsTestCase(BasicTestCase):
    pass


class GetExpertsTestCase(BasicTestCase):
    @parameterized.expand([
        (2, 7),
    ])
    def test_pagination(self, page, per_page):
        result = self.client.get_experts(page=page, per_page=per_page)
        self.assertEqual(result.meta.per_page, per_page)
        self.assertEqual(result.meta.current_page, page)

    # def test_ordering(self):
    #     result = self.client.get_experts(order=ExpertsOrder.LAST_ACTIVE)
    #
    # def test_filtering_by_query(self):
    #     result = self.client.get_experts(search="test")
    #
    # def test_filtering_by_rates(self):
    #     result = self.client.get_experts(
    #         rate_from=123, rate_to=456, currency=Currency.RUR)

    @parameterized.expand([
        (RequestID.RQ1, "Начало карьеры или смена профессии"),
        (RequestID.RQ2, "Развитие навыков"),
        (RequestID.RQ3, "Оценка"),
        (RequestID.RQ4, "Смена работы"),
        (RequestID.RQ5, "Карьерный рост"),
        (RequestID.RQ6, "Помощь с задачей"),
        (RequestID.RQ7, "Поддержка и коучинг"),
        (RequestID.RQ8, "Карьера за рубежом"),
    ])
    def test_filtering_by_request(self, request, label):
        result = self.client.get_experts(request=request)
        self.assertTrue(all([
            label in [
                r.title for r in x.requests
            ] for x in result.objects])
        )

    @parameterized.expand([
        (QualificationID.INTERN, "Стажёр"),
        (QualificationID.JUNIOR, "Младший"),
        (QualificationID.MIDDLE, "Средний"),
        (QualificationID.SENIOR, "Старший"),
        (QualificationID.LEAD, "Ведущий"),
    ])
    def test_filtering_by_qualification(self, qualification, label):
        result = self.client.get_experts(qualification=qualification)
        self.assertTrue(all([
            label in [
                q.title for q in x.qualifications
            ] for x in result.objects])
        )

    @parameterized.expand([
        (2, "Бэкенд разработчик"),
    ])
    def test_filtering_by_specializations(self, specialization, label):
        result = self.client.get_experts(specializations=[specialization])
        self.assertTrue(all([
            label in [
                s.title for s in x.specializations
            ] for x in result.objects])
        )

    @parameterized.expand([
        (446, "Python"),
    ])
    def test_filtering_by_skills(self, skill, label):
        result = self.client.get_experts(skills=[skill])
        self.assertTrue(all([
            label in [
                s.title for s in x.skills
            ] for x in result.objects])
        )

    def test_filtering_by_free_intro(self):
        result = self.client.get_experts(free_intro=True)
        self.assertTrue(
            all([x.rate.free_intro for x in result.objects]))

    def test_filtering_by_free_only(self):
        result = self.client.get_experts(free_only=True)
        self.assertTrue(
            all([x.rate is None for x in result.objects]))
