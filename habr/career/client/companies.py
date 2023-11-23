from enum import verify, UNIQUE, IntEnum, StrEnum
from typing import Any

from habr.career.utils import Pagination, QueryParams


@verify(UNIQUE)
class CompanySize(IntEnum):
    HUGE = 5    # > 5000
    BIG = 4     # 1000 - 5000
    MEDIUM = 3  # 100 - 1000
    SMALL = 2   # 10 - 100


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


# noinspection PyUnresolvedReferences
class HABRCareerCompaniesMixin:
    """Раздел `Компании`"""

    # TODO: No API endpoints found for the chapter
    pass


# noinspection PyUnresolvedReferences
class HABRCareerCompaniesRatingsMixin:
    """Раздел `Рейтинг`"""

    def get_companies_ratings(
            self,
            year: str,
            size: CompanySize,
            sort: CompanyRatingCriteria = CompanyRatingCriteria.AV,
            search: str | None = None,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """

        :param year: Covers last 5 years
        :param size:
        :param sort:
        :param search:
        :param page:
        :return:
        """
        params = QueryParams({
            "sort": sort,
            "y": year,
            "sz": size,
            "page": page,
            "q": search,
        })
        return self.get(f"frontend/companies/ratings?{params.query()}")

    def rate_company(self):
        # TODO:
        pass
