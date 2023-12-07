from tests.utils import BasicTestCase


class FriendshipsTestCase(BasicTestCase):
    def test_get_friends(self):
        result = self.client.get_friends()
        self.assertIn("list", result)
        self.assertIn("meta", result)

    def test_get_friendship_requests(self):
        result = self.client.get_friendship_requests()
        self.assertIn("list", result)
        self.assertIn("meta", result)
