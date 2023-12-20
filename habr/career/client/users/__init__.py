from enum import StrEnum, verify, UNIQUE
from functools import cached_property
from typing import Any

from habr.career.utils import NotAuthorizedError, ComplainReason
from .models import User


@verify(UNIQUE)
class CVFormat(StrEnum):
    HTML = "html"
    PDF = "pdf"
    DOC = "docx"


# noinspection PyUnresolvedReferences
class HABRCareerUsersMixin:
    @property
    def user(self) -> User:
        """
        Get current (logged in) user data.
        If user is not logged in or using incorrect token we will get an empty
        dict and method will raise HABRCareerClientError.

        :return: Examples:
            {
                "user": {
                    "avatarUrl": "https://habrastorage.org/getpro/moikrug/uploads/user/100/026/547/2/avatar/8f53ae217b54d13eef1e9cee3d0487a4.jpg",
                    "jobSearchState": "ready",
                    "alias": "x55aah",
                    "fullName": "Владимир Лысенко",
                    "gaUidToken": "BAhpBADXnjs%3D--cbbac35334343f49901ad07235cdaf57fdf51171",
                    "canEditCourses": False,
                    "isExpert": False,
                    "notificationCounters": {
                        "messages": 0,
                        "friends": 0,
                        "events": 0
                    },
                    "salaryRange": {
                        "from": None,
                        "to": 5000,
                        "unit": "usd"
                    }
                },
                "userCompanies": [],
                "meta": {
                    "logoutToken": "oEW1OgPK1wgzMeAMV+qVOSCt8MQ1bB726gZo66Chyn6qXAwG0VloPUW9+7YC86BkzCjyTBsB7j+VEEa/O6K+2A=="
                }
            }
        """
        path = "frontend_v1/users/me"
        data = self.get(path, auth_required=True)
        if not data:
            raise NotAuthorizedError
        return User(**data)

    @cached_property
    def username(self) -> str:
        """
        Get username (alias) of current (logged in) user.

        :return:
        """
        return self.user.user.alias

    @property
    def logout_token(self) -> str:
        """
        Get user token for performing logout operation.
        Note: this is not the same as authenticity_token but can be used
              as a csrf_token.

        :return:
        """
        return self.user.meta.logout_token

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