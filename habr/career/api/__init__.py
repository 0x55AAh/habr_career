from abc import ABC, abstractmethod
from functools import partialmethod
from typing import Any

from requests import Request, Session, Response, JSONDecodeError

from habr.career.api.companies import (
    HABRCareerCompaniesMixin,
    HABRCareerCompaniesRatingsMixin,
)
from habr.career.api.conversations import HABRCareerConversationsMixin
from habr.career.api.courses import HABRCareerCoursesMixin
from habr.career.api.experts import HABRCareerExpertsMixin
from habr.career.api.friendships import HABRCareerFriendshipsMixin
from habr.career.api.journal import HABRCareerJournalMixin
from habr.career.api.resumes import HABRCareerResumesMixin
from habr.career.api.salaries import HABRCareerSalariesMixin
from habr.career.api.tools import HABRCareerToolsMixin
from habr.career.api.users import HABRCareerUsersMixin
from habr.career.api.vacancies import HABRCareerVacanciesMixin
from habr.career.utils import get_ssr_json

__all__ = [
    "Authenticator",
    "TokenAuthenticator",

    "HABRCareerToolsMixin",
    "HABRCareerUsersMixin",
    "HABRCareerFriendshipsMixin",
    "HABRCareerConversationsMixin",
    "HABRCareerVacanciesMixin",
    "HABRCareerResumesMixin",
    "HABRCareerExpertsMixin",
    "HABRCareerCompaniesMixin",
    "HABRCareerCompaniesRatingsMixin",
    "HABRCareerSalariesMixin",
    "HABRCareerCoursesMixin",
    "HABRCareerJournalMixin",

    "HABRCareerBaseAPI",
    "HABRCareerAPI",

    "HABRCareerAPIError",
]


class Authenticator(ABC):
    def __init__(self):
        self._token: str | None = None
        self.api = None

    @property
    def token(self) -> str | None:
        return self._token

    @token.setter
    def token(self, value) -> None:
        self._token = value

    def is_authenticated(self) -> bool:
        return self.token is not None

    @abstractmethod
    def login(self) -> None:
        pass

    def logout(self) -> None:
        self._token = None

    def before_request(self, request: Request, **kwargs) -> None:
        pass

    def after_response(self, response: Response) -> None:
        pass


class TokenAuthenticator(Authenticator):
    def __init__(self, token_: str):
        super().__init__()
        self._token = token_
        self._sess: str | None = None

    def login(self) -> None:
        """Nothing to do here as token has already configured."""

    def before_request(
            self,
            request: Request,
            auth_required: bool = False,
    ) -> None:
        if auth_required:
            # if request.method in ("POST", "PUT", "PATCH", "DELETE"):
            #     request.headers["X-Csrf-Token"] = self.api.csrf_token
            request.cookies["remember_user_token"] = self.token
            request.cookies["_career_session"] = self._sess

    def after_response(self, response: Response) -> None:
        sess = response.cookies.get("_career_session")
        if sess:
            self._sess = sess


class HABRCareerAPIError(Exception):
    pass


class HABRCareerBaseAPI:
    BASE_URL: str = "https://career.habr.com/api/"
    BASE_GENERAL_URL: str = "https://career.habr.com/"

    def __init__(self, auth: Authenticator):
        self.auth = auth
        if not auth.is_authenticated():
            self.auth.login()

    @property
    def auth(self) -> Authenticator:
        return self._auth

    @auth.setter
    def auth(self, value: Authenticator) -> None:
        self._auth = value
        self._auth.api = self

    def request(
            self,
            path: str,
            method: str,
            auth_required: bool = False,
            key: str | None = None,
            base_url: str | None = None,
            ssr: bool = False,
            **kwargs
    ) -> Response | dict[str, Any]:
        """

        :param path:
        :param method:
        :param auth_required:
        :param key:
        :param base_url:
        :param ssr:
        :param kwargs:
        :return:
        """
        url = self.make_url(path, base_url, ssr)

        kwargs["cookies"] = kwargs.get("cookies") or {}

        session = Session()
        request = Request(method, url, **kwargs)

        self.auth.before_request(request, auth_required=auth_required)
        response = session.send(request.prepare())
        self.auth.after_response(response)

        try:
            data = response.json()
        except JSONDecodeError:
            if ssr:
                data = get_ssr_json(response.text)
            else:
                return response

        return data[key] if key else data

    def make_url(
            self,
            path: str,
            base_url: str | None = None,
            ssr: bool = False,
    ) -> str:
        """

        :param path:
        :param base_url:
        :param ssr:
        :return:
        """
        preconfigured_base = self.BASE_GENERAL_URL if ssr else self.BASE_URL
        base_url = (base_url or preconfigured_base).rstrip("/")
        return f"{base_url}/{path}"

    # Methods shortcuts
    get = partialmethod(request, method="GET")
    post = partialmethod(request, method="POST")
    put = partialmethod(request, method="PUT")
    patch = partialmethod(request, method="PATCH")
    delete = partialmethod(request, method="DELETE")

    @property
    def user(self) -> dict[str, Any]:
        """

        :return:
        """
        data = self.get("frontend_v1/users/me", auth_required=True)
        if not data:
            raise HABRCareerAPIError("Not authorized")
        return data

    @property
    def username(self) -> str:
        """

        :return:
        """
        return self.user["user"]["alias"]

    @property
    def authenticity_token(self) -> str:
        """

        :return:
        """
        path = "frontend_v1/users/authenticity_token"
        return self.get(path, key="token")

    csrf_token = authenticity_token

    @property
    def subscribe_status(self) -> dict[str, Any]:
        """

        :return:
        """
        path = "frontend_v1/users/notification_subscribe_data"
        return self.get(path, key="subscribeInfo")

    @property
    def profile(self) -> dict[str, Any]:
        """

        :return:
        """
        # TODO: API request not discovered yet
        return self.get(self.username, auth_required=True, ssr=True)


class HABRCareerAPI(
    HABRCareerToolsMixin,
    HABRCareerUsersMixin,
    HABRCareerFriendshipsMixin,
    HABRCareerConversationsMixin,
    HABRCareerVacanciesMixin,
    HABRCareerResumesMixin,
    HABRCareerExpertsMixin,
    HABRCareerCompaniesMixin,
    HABRCareerCompaniesRatingsMixin,
    HABRCareerSalariesMixin,
    HABRCareerCoursesMixin,
    HABRCareerJournalMixin,
    HABRCareerBaseAPI
):
    pass
