import os
import unittest

from habr.career import HABRCareerAPI, TokenAuthenticator


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        token = os.getenv("HABR_CAREER_TOKEN")
        self.api = HABRCareerAPI(auth=TokenAuthenticator(token=token))
