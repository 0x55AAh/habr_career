from typing import Any, TypedDict, Unpack

from requests.status_codes import codes

from habr.career.utils import Pagination, ComplainReason
from .models import (
    Conversations,
    Conversation,
    Messages,
    Message,
    Templates,
)


class TemplateParams(TypedDict):
    title: str
    body: str


class TemplateUpdateParams(TemplateParams, total=False):
    pass


# noinspection PyUnresolvedReferences
class HABRCareerConversationsMixin:
    """Раздел `Переписки`"""

    def get_conversations(
            self,
            search: str | None = None,
            page: int = Pagination.INIT_PAGE,
    ) -> Conversations:
        """
        Get all conversations.

        :param search:
        :param page: Page number
        :return: Example:
            {
                "conversationObjects": {
                    "user123": {
                        "fullName": "Виктория Талалаева",
                        "avatarUrl": "https://habrastorage.org/getpro/moikrug/uploads/user/100/046/467/3/avatar/medium_14bfaf11c39a19f518d861da2af9626a.jpg",
                        "login": "user123",
                        "subtitle": "Королев · Wanted: Profi · IT-рекрутер",
                        "conversation": {
                            "lastMessage": {
                                "body": "<p>Добрый день!<p>",
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
                    "user123",
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
        search_part = "/search" if search else ""
        return self.get(
            f"frontend/conversations{search_part}",
            cls=Conversations,
            auth_required=True,
            params={"page": page, "q": search},
        )

    def get_conversation(
            self,
            username: str,
            page: int = Pagination.INIT_PAGE,
    ) -> Conversation:
        """
        Get or create conversation with a specified user.

        :param username: User alias
        :param page: Page number
        :return: Example:
            {
                "theme": "",
                "userId": "user123",
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
                            "body": "<p>Добрый день!<p>",
                            "authorId": "user123",
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
        return self.get(
            f"frontend/conversations/{username}",
            cls=Conversation,
            auth_required=True,
            params={"valid": True, "page": page},
            params_options={
                "bool_as_str": True,
            },
        )

    connect = get_conversation

    def get_conversation_data(
            self,
            username: str,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """

        :param username: User alias
        :param page: Page number
        :return: Example:
        """
        return self.get(
            f"conversations/{username}",
            base_url="https://career.habr.com",
            auth_required=True,
            ssr=True,
            params={"page": page},
        )

    def get_messages(
            self,
            username: str,
            page: int = Pagination.INIT_PAGE,
    ) -> Messages:
        """
        Get all messages related to a conversation with a specified user.

        :param username: User alias
        :param page: Page number
        :return: Example:
            {
                "data": [
                    {
                        "id": 560968181,
                        "createdAt": 1610697438976,
                        "body": "<p>Рассматриваете предложения о работе?</p>",
                        "authorId": "user123",
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
        return self.get(
            f"frontend/conversations/{username}/messages",
            cls=Messages,
            auth_required=True,
            params={"page": page},
        )

    def get_templates(self) -> Templates:
        """
        Get all created templates.

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
        return self.get(path, cls=Templates, auth_required=True)

    # def create_template(
    #         self,
    #         **data: Unpack[TemplateParams]
    # ) -> dict[str, Any]:
    #     """
    #     Create new template with specified attributes.
    #
    #     :param data:
    #     :return:
    #     """
    #     # TODO: 500 Internal Server Error
    #     # TODO: This creates new template with requested parameters.
    #     # TODO: Failing when getting detail of a new created template.
    #     return self.post(
    #         "frontend/conversations/templates",
    #         json=data,
    #         auth_required=True,
    #     )

    def create_template(
            self,
            **data: Unpack[TemplateParams]
    ) -> dict[str, Any]:
        """
        Create new template with specified attributes.
        TODO: Real API endpoint raise error, so requesting not API
              endpoint here.

        :param data:
        :return:
        """

        self.post(
            "conversation_templates",
            base_url="https://career.habr.com/",
            data={
                f"conversation_template[{k}]": v
                for k, v in data.items()
            },
            auth_required=True,
        )
        return {"success": True}

    # def delete_template(self, id_: int) -> dict[str, Any]:
    #     """
    #     Remove template.
    #
    #     :param id_:
    #     :return:
    #     """
    #     # TODO: 500 Internal Server Error
    #     return self.delete(
    #         f"frontend/conversations/templates/{id_}",
    #         auth_required=True,
    #     )

    def delete_template(self, id_: int) -> dict[str, Any]:
        """
        Remove template.
        TODO: Real API endpoint raise error, so requesting not API
              endpoint here.

        :param id_:
        :return:
        """
        self.post(
            f"conversation_templates/template_{id_}",
            base_url="https://career.habr.com/",
            data={"_method": "delete"},
            auth_required=True,
        )
        return {"success": True}

    # def update_template(
    #         self,
    #         id_: int,
    #         **data: Unpack[TemplateUpdateParams]
    # ) -> dict[str, Any]:
    #     """
    #     Update template with specified attributes.
    #
    #     :param id_:
    #     :param data:
    #     :return:
    #     """
    #     # TODO: 500 Internal Server Error
    #     return self.patch(
    #         f"frontend/conversations/templates/{id_}",
    #         json=data,
    #         auth_required=True,
    #     )

    def update_template(
            self,
            id_: int,
            **data: Unpack[TemplateUpdateParams]
    ) -> dict[str, Any]:
        """
        Update template with specified attributes.
        TODO: Real API endpoint raise error, so requesting not API
              endpoint here.

        :param id_:
        :param data:
        :return:
        """
        _data = {
            f"conversation_template[{k}]": v
            for k, v in data.items()
        }
        self.post(
            f"conversation_templates/template_{id_}",
            base_url="https://career.habr.com/",
            data={"_method": "patch", **_data},
            auth_required=True,
        )
        return {"success": True}

    def delete_conversation(self, username: str) -> dict[str, Any]:
        """
        Remove conversation with specified user.

        :param username: User alias
        :return: Examples:
            {"success": True}
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
        """
        path = f"frontend/conversations/{username}"
        return self.delete(path, auth_required=True)

    disconnect = delete_conversation

    def send_message(self, username: str, message: str) -> Message:
        """
        Send message to specified user.

        :param username: User alias
        :param message:
        :return: Examples:
            {
                "id": 568978437,
                "createdAt": 1697889194624,
                "body": "<p>Я сейчас ищу Python разработчика удаленно.</p>",
                "authorId": "user123",
                "isMine": True
            }
            {
                "status": "error",
                "errors": [
                    {
                        "message": "Профиль пользователя заблокирован, вы не можете отправлять ему сообщения.",
                        "type": "error"
                    }
                ]
            }
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.post(
            f"frontend/conversations/{username}/messages",
            json={"body": message},
            cls=Message,
            auth_required=True,
        )

    def unread_conversation(self, username: str) -> dict[str, Any]:
        """
        Mark conversation with a specified user as unread.

        :param username: User alias
        :return: Examples:
            {"success": True}
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
            {"status": "500", "error": "Internal Server Error"}
        """
        path = f"frontend/conversations/{username}/unread"
        return self.patch(path, auth_required=True)

    def change_conversation_subject(
            self,
            username: str,
            subject: str,
    ) -> dict[str, Any]:
        """
        Change a specified user conversation topic.

        :param username: User alias
        :param subject:
        :return: Examples:
            {"success": True, "newTheme": "test"}
            {"error": "Not found"}
            {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.patch(
            f"frontend/conversations/{username}/change_subject",
            json={"body": subject},
            auth_required=True,
        )

    def complain_conversation(
            self,
            username: str,
            reason: ComplainReason,
    ) -> dict[str, Any]:
        """
        Complain to a specified user.

        :param username: User alias
        :param reason:
        :return: Examples:
             {
                 "status": True,
                 "message": "Переписка заблокирована, потому что вы пожаловались на этого пользователя"
             }
             {
                 "status": True,
                 "message": "Профиль пользователя заблокирован, вы не можете отправлять ему сообщения."
             }
             {"error": "Not found"}
             {"status": "422", "error": "Unprocessable Entity"}
        """
        return self.post(
            f"frontend/conversations/{username}/complaint",
            json={"reasonId": reason.value},
            auth_required=True,
        )
