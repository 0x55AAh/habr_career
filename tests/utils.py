import os
import unittest

from habr.career import HABRCareerClient, TokenAuthenticator


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        token = os.getenv("HABR_CAREER_TOKEN")
        self.client = HABRCareerClient(auth=TokenAuthenticator(token=token))

    def assertSuccessTrue(self, result):
        self.assertIn("success", result)
        self.assertTrue(result["success"])
