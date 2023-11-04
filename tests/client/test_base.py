from tests.utils import BasicTestCase


class BaseClientTestCase(BasicTestCase):
    def test_get_authenticity_token(self):
        self.assertIsInstance(self.client.authenticity_token, str)
