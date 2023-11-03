from habr.career.utils import ComplainReason
from tests.utils import BasicTestCase


class ConversationsTestCase(BasicTestCase):
    username = "test"

    def test_get_conversations(self):
        result = self.api.get_conversations()
        self.assertIn("conversationObjects", result)
        self.assertIn("conversationIds", result)
        self.assertIn("meta", result)

    def test_get_conversation(self):
        result = self.api.get_conversation(self.username)
        self.assertIn("theme", result)
        self.assertIn("userId", result)
        self.assertIn("hasNewMessage", result)
        self.assertIn("banned", result)
        self.assertIn("messages", result)

    def test_get_messages(self):
        result = self.api.get_messages(self.username)
        self.assertIn("data", result)
        self.assertIn("meta", result)

    def test_get_templates(self):
        result = self.api.get_templates()
        self.assertIn("templates", result)

    def test_create_template(self):
        # result = self.api.create_template(title="New title", body="New body")
        # self.assertIn("success", result)
        # self.assertTrue(result["success"])
        # TODO
        pass

    def test_delete_template(self):
        # result = self.api.delete_template(17435)
        # self.assertIn("success", result)
        # self.assertTrue(result["success"])
        # TODO
        pass

    def test_update_template(self):
        # result = self.api.update_template(17393,
        #                                   title="Updated title",
        #                                   body="Updated body")
        # self.assertIn("success", result)
        # self.assertTrue(result["success"])
        # TODO
        pass

    def test_send_message(self):
        result = self.api.send_message(self.username, "Test message")
        self.assertIn("status", result)
        self.assertIn("errors", result)

    def test_delete_conversation(self):
        result = self.api.delete_conversation(self.username)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_unread_conversation(self):
        result = self.api.unread_conversation(self.username)
        self.assertIn("success", result)
        self.assertTrue(result["success"])

    def test_change_conversation_subject(self):
        result = self.api.change_conversation_subject(self.username, "Testing")
        self.assertIn("success", result)
        self.assertIn("newTheme", result)
        self.assertTrue(result["success"])
        self.assertEqual(result["newTheme"], "Testing")

    def test_complain_conversation(self):
        result = self.api.complain_conversation(self.username,
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
