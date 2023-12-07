from typing import Any

from habr.career.utils import Pagination


# noinspection PyUnresolvedReferences
class HABRCareerFriendshipsMixin:
    """Раздел `Друзья`"""

    def get_friends(
            self,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """
        Get friends list.

        :param page: Page number
        :return: Examples:
            {
                "list": [
                    {
                        "id": "v_angelina",
                        "title": "Ангелина Ващенко",
                        "subtitle": "сорсер в консалтинге",
                        "href": "/v_angelina",
                        "avatar": {
                            "alt": "v_angelina",
                            "src": "https://habrastorage.org/getpro/moikrug/uploads/user/100/048/355/2/avatar/medium_edd6cd305a56a3f4a23dbf6a108762a0.jpg",
                            "src2x": "https://habrastorage.org/getpro/moikrug/uploads/user/100/048/355/2/avatar/medium_edd6cd305a56a3f4a23dbf6a108762a0.jpg"
                        },
                        "friendship": "accepted",
                        "isExpert": True
                    },
                    ...
                ],
                "meta": {
                    "currentPage": 1,
                    "totalPages": 3,
                    "perPage": 25
                }
            }
        """
        path = f"frontend/users/{self.username}/friendships?page={page}"
        return self.get(path, auth_required=True)

    def get_friendship_requests(
            self,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """
        Get friendship requests.

        :param page: Page number
        :return: Examples:
            {
                "list": [
                    {
                        "id": "annasytnik",
                        "title": "Анна Сытник",
                        "subtitle": None,
                        "href": "/annasytnik",
                        "avatar": {
                            "alt": "annasytnik",
                            "src": "https://career.habr.com/assets/defaults/avatars/user-4ae9deaab7da70ad824797029541e20765d74e4d1707ec8708d05d2a61eee32b.png",
                            "src2x": "https://career.habr.com/assets/defaults/avatars/user-4ae9deaab7da70ad824797029541e20765d74e4d1707ec8708d05d2a61eee32b.png"
                        },
                        "friendship": "incoming",
                        "isExpert": False
                    },
                    ...
                ],
                "meta": {
                    "currentPage": 1,
                    "totalPages": 1,
                    "perPage": 25
                }
            }
        """
        query = f"page={page}"
        path = f"frontend/users/{self.username}/friendship_requests?{query}"
        return self.get(path, auth_required=True)

    def approve_friend(self, username: str) -> dict[str, str]:
        """
        Approve friendship request.

        :param username: User alias
        :return: Examples:
            {"status": "accepted"}
        """
        path = f"frontend/users/{username}/friendship_requests/approve"
        return self.patch(path, auth_required=True)

    def reject_friend(self, username: str) -> dict[str, str]:
        """
        Reject friendship request.

        :param username: User alias
        :return: Examples:
            {"status": "cancelled"}
        """
        path = f"frontend/users/{username}/friendship_requests/reject"
        return self.patch(path, auth_required=True)

    def request_new_friendship(self, username: str) -> dict[str, str]:
        """
        Make request for a new friendship to be established.

        :param username: User alias
        :return: Examples:
            {"status": "pending"}
        """
        path = f"frontend/users/{username}/friendships?status=none"
        return self.post(path, auth_required=True)

    def cancel_pending_friendship(self, username: str) -> dict[str, str]:
        """
        Make request for pending friendship to be canceled.

        :param username: User alias
        :return: Examples:
            {"status": "none"}
        """
        path = f"frontend/users/{username}/friendships?status=pending"
        return self.post(path, auth_required=True)

    def delete_friend(self, username: str) -> dict[str, str]:
        """
        Make request for friendship to be deleted.

        :param username: User alias
        :return: Examples:
            {"status": "none"}
        """
        path = f"frontend/users/{username}/friendships?status=accepted"
        return self.post(path, auth_required=True)
