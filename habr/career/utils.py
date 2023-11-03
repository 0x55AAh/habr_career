import json
from collections import UserDict
from enum import Enum, verify, UNIQUE, StrEnum
from urllib.parse import urlencode

from bs4 import BeautifulSoup


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


def bool_to_str(value: bool | None) -> str | None:
    """
    Convert boolean value into string.

    :param value:
    :return:
    """
    if value is not None:
        return str(value).lower()


class QueryParams(UserDict):
    """Query parameters builder."""

    @staticmethod
    def _convert(value, bool_as_str=False):
        if isinstance(value, bool):
            value = str(value).lower() if bool_as_str else int(value)
        elif isinstance(value, Enum):
            value = value.value
        return value

    def query(self, doseq=False, bool_as_str=False):
        """
        Convert current query object into string representation
        for using it as a query part of url.

        :param doseq:
        :param bool_as_str:
        :return:
        """
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
    # prohibited: Профиль содержит запрещенный контент
    # ads: Профиль содержит одну рекламу
    # impersonate: Выдает себя за другого
    PROHIBITED = "prohibited"
    ADS = "ads"
    IMPERSONATE = "impersonate"

    # insult: Ведет себя оскорбительно
    # spam: Рассылает спам
    # other: Другое
    SPAM = "spam"
    INSULT = "insult"
    OTHER = "other"


@verify(UNIQUE)
class CareerSearchField(StrEnum):
    # fio: в имени
    # resume_headline: в специализации
    # experiences: в должностях
    # skills: в навыках профиля
    # social_tags: в навыках сообществ
    FIO = "fio"
    RESUME_HEADLINE = "resume_headline"
    EXPERIENCES = "experiences"
    SKILLS = "skills"
    SOCIAL_TAGS = "social_tags"
