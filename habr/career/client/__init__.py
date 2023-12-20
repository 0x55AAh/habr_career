from abc import ABC, abstractmethod
from functools import partialmethod
from typing import Any
from urllib.parse import urlparse, parse_qsl

from pydantic import ValidationError
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
from habr.career.utils import (
    get_ssr_json,
    LogoutError,
    NotAuthorizedError,
    ResponseError,
    Convertor,
    PydanticModel,
    registered_errors,
    HABRCareerClientError,
)

# TODO
# import logging
# log = logging.getLogger("urllib3")
#
# log.setLevel(logging.DEBUG)
# from http.client import HTTPConnection
# HTTPConnection.debuglevel = 1

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

    "logout",
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
        """

    def logout(self) -> None:
        """
        Perform logout operation.
        Used for cleaning up the results of previous logging in.
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

    def logout(self) -> None:
        """Invalidates auth token."""

        # TODO: API endpoint not discovered yet
        response = self.client.post(
            "users/sign_out",
            base_url="https://career.habr.com/",
            data={"_method": "delete"},
            headers={"X-Csrf-Token": self.client.logout_token},
            auth_required=True,
        )

        params = dict(parse_qsl(urlparse(response.url).query))

        if not all([response.ok, "token" in params]):
            raise LogoutError

        # TODO:
        #   In web client we have a number of other sign out operations
        #   here performed by token got from previous request.
        #   Skipping for now. Feel free to add if you want to.

        # Ensure the token is no longer valid
        try:
            self.client.user
        except NotAuthorizedError:
            self.token = None
        else:
            raise LogoutError


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
            cls: type[PydanticModel] = None,
            params_options: dict[str, Any] | None = None,
            data_options: dict[str, Any] | None = None,
            **kwargs
    ) -> Response | dict[str, Any] | PydanticModel:
        """
        Basic request method.

        :param path:
        :param method:
        :param auth_required:
        :param key:
        :param base_url:
        :param ssr:
        :param cls: Pydantic model
        :param params_options:
        :param data_options:
        :param kwargs:
        :return:
        """
        url = self.make_url(path, base_url, ssr)

        params_options = params_options or {}
        data_options = data_options or {}

        convertor = Convertor()

        params = kwargs.get("params")
        if params is not None:
            kwargs["params"] = convertor.map(params, **params_options)

        data = kwargs.get("data")
        if data is not None:
            kwargs["data"] = convertor.map(data, **data_options)

        json = kwargs.get("json")
        if json is not None:
            kwargs["json"] = convertor.map(json, **data_options)

        kwargs["cookies"] = kwargs.get("cookies") or {}

        session = Session()
        request = Request(method, url, **kwargs)

        if auth_required:
            if method in self.CSRF_PROTECTED_HTTP_METHODS:
                self.set_header(request,
                                "X-Csrf-Token", lambda: self.csrf_token)
            self.set_cookie(request, "remember_user_token", self.auth.token)
            self.set_cookie(request, "_career_session", self._sess)

        response = session.send(request.prepare())

        self._sess = response.cookies.get("_career_session")

        if not response.ok:
            raise ResponseError(
                status=response.status_code,
                error=response.reason
            )

        # JSON data or Response
        if ssr:
            data = get_ssr_json(response.text)
        else:
            try:
                data = response.json()
            except JSONDecodeError:
                return response

        # Make sure response data is not error
        # Validate data against registered errors
        for cls in registered_errors:
            cls.check_data(data)

        # JSON data processing
        if cls is not None:
            try:
                obj = cls(**data)
                return getattr(obj, key) if key else obj
            except ValidationError:
                raise HABRCareerClientError

        return data[key] if key else data

    @staticmethod
    def _set_request_data(
            field: str,
            request: Request,
            name: str,
            value: Any,
    ) -> None:
        data = getattr(request, field)
        if name not in data:
            if callable(value):
                value = value()
            data[name] = value

    @classmethod
    def set_cookie(cls, request: Request, name: str, value: Any) -> None:
        cls._set_request_data("cookies", request, name, value)

    @classmethod
    def set_header(cls, request: Request, name: str, value: Any) -> None:
        cls._set_request_data("headers", request, name, value)

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
        """
        path = "frontend_v1/users/authenticity_token"
        return self.get(path, key="token")

    csrf_token = authenticity_token

    def logout(self) -> None:
        """Invalidates auth token."""
        self.auth.logout()
        self._sess = None


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


def logout(token: str) -> None:
    """
    Invalidates auth token.

    :param token:
    :return:
    """
    client = HABRCareerClient(auth=TokenAuthenticator(token=token))
    client.logout()
