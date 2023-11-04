from typing import Any

from habr.career.utils import HABRCareerClientError


# noinspection PyUnresolvedReferences
class HABRCareerUsersMixin:
    @property
    def user(self) -> dict[str, Any]:
        """
        Get current (logged in) user data.
        If user is not logged in or using incorrect token we will get an empty
        dict and method will raise HABRCareerAPIError.

        :return: Examples:
            {
                "user": {
                    "avatarUrl": "https://habrastorage.org/getpro/moikrug/uploads/user/100/026/547/2/avatar/8f53ae217b54d13eef1e9cee3d0487a4.jpg",
                    "jobSearchState": 'ready',
                    "alias": 'x55aah',
                    "fullName": 'Владимир Лысенко',
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
        data = self.get("frontend_v1/users/me", auth_required=True)
        if not data:
            raise HABRCareerClientError("Not authorized")
        return data

    @property
    def username(self) -> str:
        """
        Get username (alias) of current (logged in) user.

        :return:
        """
        return self.user["user"]["alias"]

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
