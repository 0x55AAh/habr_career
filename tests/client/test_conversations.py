from habr.career.utils import ComplainReason, ResponseErrorType2
from tests.utils import BasicTestCase


class ConversationsTestCase(BasicTestCase):
    username = "test"

    def test_get_conversations(self):
        result = self.client.get_conversations()
        # self.assertIn("conversationObjects", result)
        # self.assertIn("conversationIds", result)
        # self.assertIn("meta", result)

    def test_get_conversation(self):
        result = self.client.get_conversation(self.username)
        # self.assertIn("theme", result)
        # self.assertIn("userId", result)
        # self.assertIn("hasNewMessage", result)
        # self.assertIn("banned", result)
        # self.assertIn("messages", result)

    def test_get_messages(self):
        result = self.client.get_messages(self.username)
        # self.assertIn("data", result)
        # self.assertIn("meta", result)

    def test_get_templates(self):
        result = self.client.get_templates()
        # self.assertIn("templates", result)

    def _test_create_template(self) -> None:
        result = self.client.create_template(title="New title",
                                             body="New body")
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def _test_delete_template(self, id_: int) -> None:
        result = self.client.delete_template(id_)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def _test_update_template(self, id_: int) -> None:
        result = self.client.update_template(id_,
                                             title="Updated title",
                                             body="Updated body")
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_CRUD_template(self):
        # Note: For real CRUD me miss retrieve template by ID.
        def get_template_ids() -> set[int]:
            result = self.client.get_templates()
            return {t.id for t in result.templates}

        ids1 = get_template_ids()
        self._test_create_template()
        ids2 = get_template_ids()

        id_ = next(iter(ids2 - ids1), None)
        self.assertIsNotNone(id_)

        self._test_update_template(id_)
        self._test_delete_template(id_)

    def test_send_message(self):
        with self.assertRaises(ResponseErrorType2):
            result = self.client.send_message(self.username, "Test message")
        # self.assertIn("status", result)
        # self.assertIn("errors", result)

    def test_delete_conversation(self):
        result = self.client.delete_conversation(self.username)
        # self.assertIn("success", result)
        # self.assertTrue(result["success"])

    def test_unread_conversation(self):
        result = self.client.unread_conversation(self.username)
        # self.assertIn("success", result)
        # self.assertTrue(result["success"])

    def test_change_conversation_subject(self):
        result = self.client.change_conversation_subject(self.username,
                                                         "Testing")
        # self.assertIn("success", result)
        # self.assertTrue(result["success"])
        # self.assertIn("newTheme", result)
        # self.assertEqual(result["newTheme"], "Testing")

    def test_complain_conversation(self):
        result = self.client.complain_conversation(self.username,
                                                   ComplainReason.OTHER)
        self.assertIn("status", result)
        self.assertIn("message", result)
        self.assertTrue(result["status"])
        self.assertIn(
            result["message"],
            [
                "Профиль пользователя заблокирован, вы не можете "
                "отправлять ему сообщения.",
                "Переписка заблокирована, потому что вы пожаловались на этого "
                "пользователя"
            ]
        )
