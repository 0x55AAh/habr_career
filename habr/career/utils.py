from __future__ import annotations

import json
from collections import UserDict
from enum import Enum, verify, UNIQUE, StrEnum, IntEnum
from typing import Any, Self, Iterator

from bs4 import BeautifulSoup
from pydantic import BaseModel, ValidationError

type PydanticModel = BaseModel

registered_errors: list[type[ResponseError]] = []


def register_error(cls):
    registered_errors.append(cls)
    return cls


class HABRCareerClientError(Exception):
    pass


class NotAuthorizedError(HABRCareerClientError):
    pass


class LogoutError(HABRCareerClientError):
    pass


class BaseResponseError(HABRCareerClientError):
    schema: type[PydanticModel] = None

    def __init__(self, **kwargs):
        super().__init__(self.get_reason())
        self.data = kwargs

    def get_reason(self) -> str:
        raise NotImplementedError

    @classmethod
    def check_data(cls, data: dict) -> None:
        try:
            cls.schema(**data)
        except ValidationError:
            return
        raise cls(**data)


@register_error
class ResponseError(BaseResponseError):
    """
    Standard error response.
    Examples:
        {"status": "500", "error": "Internal Server Error"}
        {"error": "Not found"}
        {"status": "422", "error": "Unprocessable Entity"}
    """

    class Schema(BaseModel):
        status: int | None = None
        error: str

    schema = Schema

    def get_reason(self):
        return self.data["error"]


class ConcurrentJobs:
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers
        self.items = []

    def register(self, func, *args, **kwargs) -> Self:
        self.items.append((func, args, kwargs))
        return self

    def run(self) -> Iterator[Any]:
        from concurrent.futures import ThreadPoolExecutor

        fs = []
        with ThreadPoolExecutor(self.max_workers) as executor:
            for job in self.items:
                func, args, kwargs = job
                f = executor.submit(func, *args, **kwargs)
                fs.append(f)

        for f in fs:
            yield f.result()


def get_ssr_json(html_code: str) -> dict:
    """
    Retrieve server side rendered json put into text/html page.
    Use it in case if you do not have corresponding API endpoint that can
    provide JSON data directly.

    :param html_code:
    :return:
    """
    soup = BeautifulSoup(html_code, features="html.parser")
    search_params = {
        "name": "script",
        "type": "application/json",
        "attrs": {"data-ssr-state": "true"},
    }
    el = soup.find(**search_params)
    return json.loads(el.get_text())


def cleanup_tags(html_code: str, **kwargs) -> str:
    """
    Remove HTML tags from input string.

    :param html_code:
    :return:
    """
    soup = BeautifulSoup(html_code, features="html.parser")
    return soup.get_text(**kwargs)


def bool_to_str(value: bool | None) -> str | None:
    """
    Convert boolean value into string.

    :param value:
    :return:
    """
    if value is not None:
        return str(value).lower()


class Convertor:
    @classmethod
    def _convert(cls, value, **options):
        options = options or {}
        bool_as_str: bool = options.get("bool_as_str", False)
        if isinstance(value, bool):
            value = str(value).lower() if bool_as_str else int(value)
        elif isinstance(value, Enum):
            value = value.value
        return value

    def map(self, data: dict, **options) -> dict:
        return {
            key: self._convert(value, **options)
            for key, value in data.items()
        }


class QueryParams(UserDict):
    """Query parameters builder."""

    @staticmethod
    def _convert(value: Any, bool_as_str: bool = False) -> Any:
        if isinstance(value, bool):
            value = str(value).lower() if bool_as_str else int(value)
        elif isinstance(value, Enum):
            value = value.value
        return value

    def query(
            self,
            doseq: bool = False,
            bool_as_str: bool = False,
    ) -> str:
        """
        Convert current query object into string representation
        for using it as a query part of url.

        :param doseq:
        :param bool_as_str:
        :return:
        """
        from urllib.parse import urlencode

        data = {
            k: self._convert(v, bool_as_str)
            for k, v in self.data.items()
            if v is not None
        }
        return urlencode(data, doseq)


@verify(UNIQUE)
class Qualification(StrEnum):
    INTERN = "Intern"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
    LEAD = "Lead"


@verify(UNIQUE)
class QualificationID(IntEnum):
    INTERN = 1
    JUNIOR = 3
    MIDDLE = 4
    SENIOR = 5
    LEAD = 6


@verify(UNIQUE)
class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


@verify(UNIQUE)
class Currency(StrEnum):
    RUR = "rur"
    EUR = "eur"
    USD = "usd"
    UAH = "uah"
    KZT = "kzt"


class Pagination:
    PER_PAGE = 15
    INIT_PAGE = 1


@verify(UNIQUE)
class ComplainReason(StrEnum):
    # TODO: Ensure it fits both conversations and users
    PROHIBITED = "prohibited"    # Профиль содержит запрещенный контент
    ADS = "ads"                  # Профиль содержит одну рекламу
    IMPERSONATE = "impersonate"  # Выдает себя за другого

    SPAM = "spam"                # Рассылает спам
    INSULT = "insult"            # Ведет себя оскорбительно
    OTHER = "other"              # Другое
