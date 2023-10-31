from typing import Any

from habr.career.utils import Pagination, QueryParams, ComplainReason


# noinspection PyUnresolvedReferences
class HABRCareerConversationsMixin:
    def get_conversations(
            self,
            search: str | None = None,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """

        :param search:
        :param page:
        :return: Example:
            {
                "conversationObjects": {
                    "marbulaewa": {
                        "fullName": "Марина Булаева",
                        "avatarUrl": "https://habrastorage.org/getpro/moikrug/uploads/user/100/046/467/3/avatar/medium_14bfaf11c39a19f518d861da2af9626a.jpg",
                        "login": "marbulaewa",
                        "subtitle": "Королев · Wanted: Profi · IT-рекрутер",
                        "conversation": {
                            "lastMessage": {
                                "body": "<p>Добрый день! Владимир, тогда, к сожалению, не получится отправить ваше резюме, т.к. в компании оформление только по ТК РФ.<p>",
                                "createdAt": 1698073349923,
                                "isMine": False,
                                "isRead": True
                            }
                        },
                        "banned": {
                            "status": False,
                            "message": None
                        },
                        "isExpert": False
                    },
                    ...
                },
                "conversationIds": [
                    "marbulaewa",
                    ...
                ],
                "meta": {
                    "totalCount": 241,
                    "total": 13,
                    "unread": 1,
                    "page": 1,
                    "perPage": 20
                }
            }
            {"status": "500", "error": "Internal Server Error"}
        """
        path = "frontend/conversations"
        params = QueryParams({"page": page, "q": search})
        if search:
            path += "/search"
        path += f"?{params.query()}"
        return self.get(path, auth_required=True)

    def get_conversation(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return: Example:
            {
                "theme": "",
                "userId": "devakant",
                "hasNewMessage": False,
                "banned": {
                    "status": False,
                    "message": None
                },
                "messages": {
                    "data": [
                        {
                            "id": 560968181,
                            "createdAt": 1610697438976,
                            "body": "<p>Добрый день! Я сейчас ищу Python разработчика удаленно. Рассматриваете предложения о работе?<p>",
                            "authorId": "elenpavlova",
                            "isMine": False
                        },
                        ...
                    ],
                    "meta": {
                        "page": 1,
                        "perPage": 25,
                        "total": 5
                    }
                }
            }
            {"error": "Not found"}
            {"status": "500", "error": "Internal Server Error"}
        """
        path = f"frontend/conversations/{username}?valid=true"
        return self.get(path, auth_required=True)

    connect = get_conversation

    def get_messages(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return: Example:
            {
                "data": [
                    {
                        "id": 560968181,
                        "createdAt": 1610697438976,
                        "body": "<p>Добрый день! Я сейчас ищу Python разработчика удаленно. Рассматриваете предложения о работе?</p>",
                        "authorId": "elenpavlova",
                        "isMine": False
                    },
                    ...
                ],
                "meta": {
                    "total": 5,
                    "page": 1,
                    "perPage": 25
                }
            }
            {"error": "Not found"}
            {"error": "Войдите, прежде чем продолжить."}
        """
        path = f"frontend/conversations/{username}/messages"
        return self.get(path, auth_required=True)

    def get_templates(self) -> dict[str, Any]:
        """

        :return: Examples:
            {
                "templates": [
                    {"id": 17325, "title": "test", "body": "test"},
                    ...
                ]
            }
            {"error": "Войдите, прежде чем продолжить."}
        """
        path = "frontend/conversations/templates"
        return self.get(path, auth_required=True)

    def create_template(self, title: str, body: str) -> dict[str, Any]:
        """

        :param title:
        :param body:
        :return:
        """
        # TODO: 500 Internal Server Error
        # TODO: This creates new template with requested parameters.
        # TODO: Failing when getting detail of a new created template.
        return self.post(
            path="frontend/conversations/templates",
            auth_required=True,
            json={"title": title, "body": body},
            headers={"X-Csrf-Token": self.csrf_token},
        )

    def delete_template(self, id_: int) -> dict[str, Any]:
        """

        :param id_:
        :return:
        """
        # TODO: 500 Internal Server Error
        return self.delete(
            path=f"frontend/conversations/templates/{id_}",
            auth_required=True,
            headers={"X-Csrf-Token": self.csrf_token},
        )

    def update_template(
            self,
            id_: int,
            title: str | None = None,
            body: str | None = None,
    ) -> dict[str, Any]:
        """

        :param id_:
        :param title:
        :param body:
        :return:
        """
        # TODO: 500 Internal Server Error
        data = {}
        title and data.update(title=title)
        body and data.update(title=body)
        return self.patch(
            path=f"frontend/conversations/templates/{id_}",
            auth_required=True,
            json=data,
            headers={"X-Csrf-Token": self.csrf_token},
        )

    def delete_conversation(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return: Examples:
            {"success": True}
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.delete(
            path=f"frontend/conversations/{username}",
            auth_required=True,
            headers={"X-Csrf-Token": self.csrf_token},
        )

    disconnect = delete_conversation

    def send_message(self, username: str, message: str) -> dict[str, Any]:
        """

        :param username: User alias
        :param message:
        :return: Examples:
            {
                "id": 568978437,
                "createdAt": 1697889194624,
                "body": "<p>One more test</p>",
                "authorId": "x55aah",
                "isMine": True
            }
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.post(
            path=f"frontend/conversations/{username}/messages",
            auth_required=True,
            json={"body": message},
            headers={"X-Csrf-Token": self.csrf_token},
        )

    def unread_conversation(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return: Examples:
            {"success": True}
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.patch(
            path=f"frontend/conversations/{username}/unread",
            auth_required=True,
            headers={"X-Csrf-Token": self.csrf_token},
        )

    def change_conversation_subject(
            self,
            username: str,
            subject: str,
    ) -> dict[str, Any]:
        """

        :param username: User alias
        :param subject:
        :return: Examples:
            {"success": True, "newTheme": "test"}
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.patch(
            path=f"frontend/conversations/{username}/change_subject",
            auth_required=True,
            json={"body": subject},
            headers={"X-Csrf-Token": self.csrf_token},
        )

    def complain_conversation(
            self,
            username: str,
            reason: ComplainReason,
    ) -> dict[str, Any]:
        """

        :param username: User alias
        :param reason:
        :return: Examples:
             {
                 "status": True,
                 "message": "Переписка заблокирована, потому что вы пожаловались на этого пользователя"
             }
             {"error": "Not found"}
             {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.post(
            path=f"frontend/conversations/{username}/complaint",
            auth_required=True,
            json={"reasonId": reason.value},
            headers={"X-Csrf-Token": self.csrf_token},
        )
