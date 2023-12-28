from tests.utils import BasicTestCase


class BaseClientTestCase(BasicTestCase):
    def test_get_current_user(self):
        result = self.client.user
        # self.assertIn("user", result)
        # self.assertIn("userCompanies", result)
        # self.assertIn("meta", result)

    def test_get_current_username(self):
        self.assertIsInstance(self.client.username, str)

    def test_get_authenticity_token(self):
        self.assertIsInstance(self.client.authenticity_token, str)
