import os
import unittest

from habr.career.client import HABRCareerClient, TokenAuthenticator


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        token = os.getenv("HABR_CAREER_TOKEN")
        session_id = os.getenv("HABR_CAREER_SESSION_ID")
        auth = TokenAuthenticator(token=token)
        self.client = HABRCareerClient(auth=auth, session_id=session_id)
