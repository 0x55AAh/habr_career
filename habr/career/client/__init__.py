from abc import ABC, abstractmethod
from functools import partialmethod
from typing import Any

from requests import Request, Session, Response, JSONDecodeError

from habr.career.client.companies import (
    HABRCareerCompaniesMixin,
    HABRCareerCompaniesRatingsMixin,
)
from habr.career.client.conversations import HABRCareerConversationsMixin
from habr.career.client.courses import HABRCareerCoursesMixin
from habr.career.client.experts import HABRCareerExpertsMixin
from habr.career.client.friendships import HABRCareerFriendshipsMixin
from habr.career.client.journal import HABRCareerJournalMixin
from habr.career.client.resumes import HABRCareerResumesMixin
from habr.career.client.salaries import HABRCareerSalariesMixin
from habr.career.client.tools import HABRCareerToolsMixin
from habr.career.client.users import HABRCareerUsersMixin
from habr.career.client.vacancies import HABRCareerVacanciesMixin
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

    "HABRCareerBaseClient",
    "HABRCareerClient",
]


class Authenticator(ABC):
    """
    Provides basic authentication functionality.
    Used by client for being able to make requests on behalf of logged-in user.
    """

    def __init__(self):
        self.token: str | None = None
        self.client = None

    def is_authenticated(self) -> bool:
        return self.token is not None

    @abstractmethod
    def login(self) -> None:
        """
        Perform login operation.
        This is the main operation for making current user authorized.
        In most cases the method will take credentials saved when instantiating
        authenticator and receive auth token based on these credentials.
        Run this method before using client.

        :return:
        """
        pass

    def logout(self) -> None:
        """
        Perform logout operation.
        Used for cleaning up the results of previous logging in.

        :return:
        """
        self.token = None


class TokenAuthenticator(Authenticator):
    """
    Authenticator uses already received token.
    This is for those cases when you are unable to perform login operation.
    This might be the case, for example, due to re-captcha.
    In such situation you should log in using other clients, for example
    web browser. And then use the received token when creating authenticator.
    """

    def __init__(self, token: str):
        super().__init__()
        self.token = token

    def login(self) -> None:
        """Nothing to do here as token has already configured."""


class HABRCareerBaseClient:
    BASE_URL = "https://career.habr.com/api/"
    GENERAL_BASE_URL = "https://career.habr.com/"
    CSRF_PROTECTED_HTTP_METHODS = ("POST", "PUT", "PATCH", "DELETE")

    def __init__(self, auth: Authenticator):
        self.auth = auth
        if not auth.is_authenticated():
            self.auth.login()
        self._sess: str | None = None

    @property
    def auth(self) -> Authenticator:
        return self._auth

    @auth.setter
    def auth(self, value: Authenticator) -> None:
        self._auth = value
        self._auth.client = self

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
        Basic request method.

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

        if auth_required:
            if method in self.CSRF_PROTECTED_HTTP_METHODS:
                request.headers["X-Csrf-Token"] = self.csrf_token
            request.cookies["remember_user_token"] = self.auth.token
            request.cookies["_career_session"] = self._sess

        response = session.send(request.prepare())

        self._sess = response.cookies.get("_career_session")

        if ssr:
            data = get_ssr_json(response.text)
        else:
            try:
                data = response.json()
            except JSONDecodeError:
                return response

        return data[key] if key else data

    def make_url(
            self,
            path: str,
            base_url: str | None = None,
            ssr: bool = False,
    ) -> str:
        """
        Build url for client requests.

        :param path:
        :param base_url:
        :param ssr:
        :return:
        """
        preconfigured_base = self.GENERAL_BASE_URL if ssr else self.BASE_URL
        base_url = (base_url or preconfigured_base).rstrip("/")
        return f"{base_url}/{path}"

    # Methods shortcuts
    get = partialmethod(request, method="GET")
    post = partialmethod(request, method="POST")
    put = partialmethod(request, method="PUT")
    patch = partialmethod(request, method="PATCH")
    delete = partialmethod(request, method="DELETE")

    @property
    def authenticity_token(self) -> str:
        """
        Get authenticity token used as a token on different operations.
        For example this token is being used as a CSRF token in conjunction
        with HTTP methods POST, PATCH, DELETE, etc.
        This is not require you to be logged in.

        :return:
        """
        path = "frontend_v1/users/authenticity_token"
        return self.get(path, key="token")

    csrf_token = authenticity_token


class HABRCareerClient(
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
    HABRCareerToolsMixin,
    HABRCareerUsersMixin,
    HABRCareerBaseClient
):
    """Fully featured client."""
