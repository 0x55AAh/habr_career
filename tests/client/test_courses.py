from habr.career.utils import ResponseErrorType1
from tests.utils import BasicTestCase


class CoursesTestCase(BasicTestCase):
    def test_get_courses(self):
        result = self.client.get_courses()
        self.assertIn("coursesIds", result)
        self.assertIn("coursesRefs", result)
        self.assertIn("meta", result)

    def test_get_course(self):
        with self.assertRaises(ResponseErrorType1):
            result = self.client.get_course("test")
        # self.assertIn("httpCode", result)
        # self.assertIn("errorCode", result)
        # self.assertIn("message", result)
        # self.assertIn("data", result)

    def test_get_course_scores(self):
        with self.assertRaises(ResponseErrorType1):
            result = self.client.get_course_scores("test")
        # self.assertIn("httpCode", result)
        # self.assertIn("errorCode", result)
        # self.assertIn("message", result)
        # self.assertIn("data", result)

    def test_get_similar_courses(self):
        with self.assertRaises(ResponseErrorType1):
            result = self.client.get_similar_courses("test")
        # self.assertIn("httpCode", result)
        # self.assertIn("errorCode", result)
        # self.assertIn("message", result)
        # self.assertIn("data", result)

    def test_get_popular_education_platforms(self):
        result = self.client.get_popular_education_platforms()
        self.assertIsInstance(result, list)

    def test_get_popular_skills(self):
        result = self.client.get_popular_skills()
        self.assertIsInstance(result, list)

    def test_get_educations_suggestions(self):
        result = self.client.get_educations_suggestions("test")
        self.assertIn("skills", result)
        self.assertIn("specializations", result)
        self.assertIn("courses", result)

    def test_get_education_platforms_suggestions(self):
        result = self.client.get_education_platforms_suggestions("test")
        self.assertIsInstance(result, list)

    def test_courses_count(self):
        self.assertIsInstance(self.client.courses_count, int)

    def test_get_specializations_with_course_counters(self):
        result = self.client.get_specializations_with_course_counters()
        self.assertIn("groups", result)

    def test_get_specializations(self):
        result = self.client.get_specializations()
        self.assertIn("groups", result)

    def test_get_offers(self):
        result = self.client.get_offers(specializations=["backend"])
        self.assertIn("offers", result)
        self.assertIn("aggregateRating", result)
        self.assertIn("events", result)
