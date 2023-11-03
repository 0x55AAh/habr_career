from tests.utils import BasicTestCase


class UsersTestCase(BasicTestCase):
    username = "test"

    def test_get_current_user(self):
        result = self.api.user
        self.assertIn("user", result)
        self.assertIn("userCompanies", result)
        self.assertIn("meta", result)

    def test_get_current_username(self):
        self.assertIsInstance(self.api.username, str)

    def test_get_subscribe_status(self):
        result = self.api.subscribe_status
        self.assertIn("isHr", result)
        self.assertIn("isGuest", result)
        self.assertIn("hasSubscribe", result)
        self.assertIn("registerHref", result)
        self.assertIn("notificationsHref", result)

    def test_get_profile(self):
        result = self.api.get_profile(self.username)
        self.assertIn("user", result)
        self.assertIn("hasActiveConnection", result)
        self.assertIn("visibleConnectionFeedback", result)

    def test_get_current_profile(self):
        result = self.api.profile
        self.assertIn("user", result)
        self.assertIn("hasActiveConnection", result)
        self.assertIn("visibleConnectionFeedback", result)
