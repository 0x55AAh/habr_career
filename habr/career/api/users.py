from typing import Any


# noinspection PyUnresolvedReferences
class HABRCareerUsersMixin:
    def get_profile(self, username: str) -> dict[str, Any]:
        """

        :param username: User alias
        :return:
        """
        # TODO: API request not discovered yet
        return self.get(username, auth_required=True, ssr=True)
