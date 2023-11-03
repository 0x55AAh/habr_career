from tests.utils import BasicTestCase


class BaseAPITestCase(BasicTestCase):
    def test_get_authenticity_token(self):
        self.assertIsInstance(self.api.authenticity_token, str)
