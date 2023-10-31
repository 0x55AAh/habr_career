import json
from collections import UserDict
from enum import Enum, verify, UNIQUE, StrEnum, IntEnum
from typing import NamedTuple
from urllib.parse import urlencode

from bs4 import BeautifulSoup


def get_ssr_json(html_code: str) -> dict:
    """

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

    :param value:
    :return:
    """
    if value is not None:
        return str(value).lower()


class QueryParams(UserDict):
    @staticmethod
    def _convert(value, bool_as_str=False):
        if isinstance(value, bool):
            value = str(value).lower() if bool_as_str else int(value)
        elif isinstance(value, Enum):
            value = value.value
        return value

    def query(self, doseq=False, bool_as_str=False):
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
class CourseDuration(StrEnum):
    QUARTER = "quarter"
    LESS_HALF = "lessHalf"
    MORE_HALF = "moreHalf"
    MORE_YEAR = "moreYear"


@verify(UNIQUE)
class CourseSortField(StrEnum):
    START_DATE = "startDate"
    PRICE = "price"
    AVERAGE_RATING = "averageRating"


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
class CompanySize(IntEnum):
    HUGE = 5    # > 5000
    BIG = 4     # 1000 - 5000
    MEDIUM = 3  # 100 - 1000
    SMALL = 2   # 10 - 100


@verify(UNIQUE)
class EmploymentType(IntEnum):
    FULL_TIME = 0
    PART_TIME = 1


@verify(UNIQUE)
class ComplainReason(StrEnum):
    # TODO: Ensure it fits both conversations and users
    # - prohibited: Профиль содержит запрещенный контент
    # - ads: Профиль содержит одну рекламу
    # - impersonate: Выдает себя за другого
    PROHIBITED = "prohibited"
    ADS = "ads"
    IMPERSONATE = "impersonate"

    # - insult: Ведет себя оскорбительно
    # - spam: Рассылает спам
    # - other: Другое
    SPAM = "spam"
    INSULT = "insult"
    OTHER = "other"


@verify(UNIQUE)
class CompanyRatingCriteria(StrEnum):
    AV = "av"     # Общая оценка
    S2 = "s_2"    # Интересные задачи
    S16 = "s_16"  # Современные технологии
    S3 = "s_3"    # Адекватная зарплата
    S4 = "s_4"    # Социальный пакет
    S5 = "s_5"    # Комфортные условия труда
    S6 = "s_6"    # Профессиональный рост
    S7 = "s_7"    # Карьерный рост
    S8 = "s_8"    # Отношения с коллегами
    S9 = "s_9"    # Признание результатов труда
    S10 = "s_10"  # Грамотность менеджмента
    S11 = "s_11"  # Связь с топ-менеджментом
    S12 = "s_12"  # Компания делает мир лучше


@verify(UNIQUE)
class CareerSearchField(StrEnum):
    # fio - в имени
    # resume_headline - в специализации
    # experiences - в должностях
    # skills - в навыках профиля
    # social_tags - в навыках сообществ
    FIO = "fio"
    RESUME_HEADLINE = "resume_headline"
    EXPERIENCES = "experiences"
    SKILLS = "skills"
    SOCIAL_TAGS = "social_tags"


@verify(UNIQUE)
class CareerSortingCriteria(StrEnum):
    # last_visited - по дате визита
    # relevance - по соответствию
    # salary_desc - по убыванию зарплаты
    # salary_asc - по возрастанию зарплаты
    LAST_VISITED = "last_visited"
    RELEVANCE = "relevance"
    SALARY_DESC = "salary_desc"
    SALARY_ASC = "salary_asc"


@verify(UNIQUE)
class CareerWorkState(StrEnum):
    # not_search: Не ищу работу
    # search: Ищу работу
    # ready: Рассмотрю предложения
    NOT_SEARCH = "not_search"
    SEARCH = "search"
    READY = "ready"


@verify(UNIQUE)
class CareerActivityPeriod(StrEnum):
    # two_years: За 2 года
    # year: За год
    # three_months: За 3 месяца
    TWO_YEARS = "two_years"
    YEAR = "year"
    THREE_MONTHS = "three_months"


class Sort(NamedTuple):
    field: CourseSortField
    direction: SortDirection
