from enum import StrEnum, verify, UNIQUE
from typing import Any

from habr.career.utils import ComplainReason


@verify(UNIQUE)
class CVFormat(StrEnum):
    HTML = "html"
    PDF = "pdf"
    DOC = "docx"


# noinspection PyUnresolvedReferences
class HABRCareerUsersMixin:
    @property
    def subscribe_status(self) -> dict[str, Any]:
        """
        Get general statuses of current user.

        :return: Examples:
            {
                "subscribeInfo": {
                    "isHr": False,
                    "isGuest": True,
                    "hasSubscribe": None,
                    "registerHref": "/users/auth/tmid/register",
                    "notificationsHref": "/preferences/notifications"
                }
            }
        """
        path = "frontend_v1/users/notification_subscribe_data"
        return self.get(path, auth_required=True, key="subscribeInfo")

    def get_profile(self, username: str) -> dict[str, Any]:
        """
        Get arbitrary user profile data.

        :param username: User alias
        :return:
        """
        # TODO: API endpoint not discovered yet
        return self.get(username, auth_required=True, ssr=True)

    @property
    def profile(self) -> dict[str, Any]:
        """
        Get current (logged in) user profile data.

        :return:
        """
        # TODO: API endpoint not discovered yet
        return self.get(self.username, auth_required=True, ssr=True)

    def get_my_skills(self, limit: int = 10) -> list[dict[str, str]]:
        """
        Get skills list of current (logged in) user.
        Empty list if not logged in.

        :param limit:
        :return: Examples:
            {
                "skills": [
                    {"title": "Python", "alias": "python"},
                    {"title": "Git", "alias": "git"},
                    {"title": "Linux", "alias": "linux"},
                    {"title": "Docker", "alias": "docker"},
                    {"title": "PostgreSQL", "alias": "postgresql"},
                    {"title": "Django", "alias": "django"},
                    {"title": "MongoDB", "alias": "mongodb"},
                    {"title": "Apache Kafka", "alias": "kafka"},
                    {"title": "RabbitMQ", "alias": "rabbitmq"},
                    {"title": "AWS", "alias": "amazon-aws"}
                ]
            }
        """
        return self.get(
            "frontend_v1/skills/my",
            auth_required=True,
            key="skills",
            params={"limit": limit},
        )

    def get_skills_in_my_specialization(
            self,
            limit: int = 10,
    ) -> list[dict[str, str]]:
        """
        Get skills list from specialization of current (logged in) user.
        Empty list if not logged in.

        :param limit:
        :return: Examples:
            {
                "skills": [
                    {"title": "Python", "alias": "python"},
                    {"title": "Java", "alias": "java"},
                    {"title": "ООП", "alias": "oop"},
                    {"title": "SQL", "alias": "sql"},
                    {"title": "Django", "alias": "django"},
                    {"title": "MySQL", "alias": "mysql"},
                    {"title": "Базы данных", "alias": "bazy-dannyh"},
                    {"title": "Java Spring Framework", "alias": "java-spring-framework"},
                    {"title": "PostgreSQL", "alias": "postgresql"},
                    {"title": "Docker", "alias": "docker"}
                ]
            }
        """
        return self.get(
            "frontend_v1/skills/my_specialization",
            auth_required=True,
            key="skills",
            params={"limit": limit},
        )

    def get_cv(self, username: str, fmt: CVFormat = CVFormat.PDF) -> bytes:
        """
        Get CV for the requested user.

        :param username: User alias
        :param fmt: Content format
        :return:
        """
        # TODO: API endpoint not discovered yet
        response = self.get(
            f"{username}/print.{fmt}",
            base_url="https://career.habr.com/",
            auth_required=True,
        )
        return response.content

    def get_my_cv(self, fmt: CVFormat = CVFormat.PDF) -> bytes:
        """
        Get CV for the current (logged in) user.

        :param fmt: Content format
        :return:
        """
        return self.get_cv(self.username, fmt)

    def complain_on_user(
            self,
            username: str,
            reason: ComplainReason,
    ) -> dict[str, str]:
        """
        Complain on user.

        :param username: User alias
        :param reason: Complaint reason
        :return: Examples:
            {"status": "accepted"}
        """
        return self.post(
            f"frontend/users/{username}/complaints",
            json={"reason": reason.value},
            auth_required=True,
        )

    # TODO: send opinions
    #  https://career.habr.com/nikolskaya-maria-05/opinions/new
