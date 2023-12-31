from tests.utils import BasicTestCase


class UsersTestCase(BasicTestCase):
    username = "test"

    def test_get_subscribe_status(self):
        result = self.client.subscribe_status
        # self.assertIn("isHr", result)
        # self.assertIn("isGuest", result)
        # self.assertIn("hasSubscribe", result)
        # self.assertIn("registerHref", result)
        # self.assertIn("notificationsHref", result)

    def test_get_profile(self):
        result = self.client.get_profile(self.username)
        # self.assertIn("user", result)
        # self.assertIn("hasActiveConnection", result)
        # self.assertIn("visibleConnectionFeedback", result)

    def test_get_current_profile(self):
        result = self.client.profile
        # self.assertIn("user", result)
        # self.assertIn("hasActiveConnection", result)
        # self.assertIn("visibleConnectionFeedback", result)

    def test_get_my_skills(self):
        result = self.client.get_my_skills(limit=5)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)

    def test_get_skills_in_my_specialization(self):
        result = self.client.get_skills_in_my_specialization(limit=5)
        self.assertIsInstance(result, list)
        self.assertLessEqual(len(result), 5)

    def test_get_cv(self):
        result = self.client.get_my_cv()
        self.assertIsInstance(result, bytes)
