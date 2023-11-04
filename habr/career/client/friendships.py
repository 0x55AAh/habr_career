from typing import Any

from habr.career.utils import Pagination, ComplainReason


# noinspection PyUnresolvedReferences
class HABRCareerFriendshipsMixin:
    def get_friends(
            self,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """

        :param page:
        :return:
        """
        path = f"frontend/users/{self.username}/friendships?page={page}"
        return self.get(path, auth_required=True)

    def get_friendship_requests(
            self,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """

        :param page:
        :return: Examples:
            {
                "list": [
                ],
                "meta": {
                    "currentPage": 1,
                    "totalPages": 0,
                    "perPage": 25
                }
            }
        """
        path = f"frontend/users/{self.username}/friendship_requests?page={page}"
        return self.get(path, auth_required=True)

    def cancel_add_friend(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return:
        """
        path = f"frontend/users/{username}/friendships?status=pending"
        return self.post(path, auth_required=True)

    def accept_friend(self, username: str) -> dict[str, Any]:
        """
        Accept adding to friends:
        - Method: ?
        - URL: ?

        :param username: User alias
        :return:
        """
        return self.post(  # TODO: ensure method
            path=f"frontend/users/{username}/friendships?status=none",  # TODO:
            auth_required=True,
        )

    def reject_friend(self, username: str) -> dict[str, Any]:
        """
        Reject adding to friends:
        - Method: ?
        - URL: ?

        :param username: User alias
        :return:
        """
        return self.post(  # TODO: ensure method
            path=f"frontend/users/{username}/friendships?status=none",  # TODO:
            auth_required=True,
        )

    def request_add_friend(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return:
        """
        path = f"frontend/users/{username}/friendships?status=none"
        return self.post(path, auth_required=True)

    def delete_friend(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return:
        """
        path = f"frontend/users/{username}/friendships?status=accepted"
        return self.post(path, auth_required=True)

    def complain_user(
            self,
            username: str,
            reason: ComplainReason,
    ) -> dict[str, Any]:
        """

        :param username: User alias
        :param reason:
        :return:
        """
        return self.post(  # TODO: ensure method
            path=f"frontend/users/{username}/complaints",
            auth_required=True,
            json={"reason": reason.value},  # TODO: Query parameters?
        )
