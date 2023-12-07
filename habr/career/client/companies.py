from datetime import datetime
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
            year: int | None = None,
            size: CompanySize = CompanySize.HUGE,
            sort: CompanyRatingCriteria = CompanyRatingCriteria.AV,
            search: str | None = None,
            page: int = Pagination.INIT_PAGE,
    ) -> dict[str, Any]:
        """
        Get companies ratings.

        :param year: Covers last previous 5 years.
        :param size:
        :param sort:
        :param search:
        :param page:
        :return: Examples:
            {
                "list": [
                    {
                        "summary": {
                            "visible_summary": True,
                            "href": "/companies/aston/scores",
                            "title": "Средняя оценка компании в 2023 году",
                            "value": "4.15"
                        },
                        "scores": {
                            "featured": {
                                "title": "Средняя оценка",
                                "value": "4.81"
                            },
                            "items": [
                                {
                                    "title": "Интересные задачи",
                                    "value": "4.78",
                                    "level": "average"
                                },
                                {
                                    "title": "Современные технологии",
                                    "value": "4.86",
                                    "level": "good"
                                },
                                {
                                    "title": "Адекватная зарплата",
                                    "value": "4.83",
                                    "level": "average"
                                },
                                {
                                    "title": "Социальный пакет",
                                    "value": "4.73",
                                    "level": "average"
                                },
                                {
                                    "title": "Комфортные условия труда",
                                    "value": "4.85",
                                    "level": "average"
                                },
                                {
                                    "title": "Профессиональный рост",
                                    "value": "4.86",
                                    "level": "good"
                                },
                                {
                                    "title": "Карьерный рост",
                                    "value": "4.84",
                                    "level": "average"
                                },
                                {
                                    "title": "Отношения с коллегами",
                                    "value": "4.86",
                                    "level": "good"
                                },
                                {
                                    "title": "Признание результатов труда",
                                    "value": "4.76",
                                    "level": "average"
                                },
                                {
                                    "title": "Грамотность менеджмента",
                                    "value": "4.77",
                                    "level": "average"
                                },
                                {
                                    "title": "Связь с топ-менеджментом",
                                    "value": "4.78",
                                    "level": "average"
                                },
                                {
                                    "title": "Компания делает мир лучше",
                                    "value": "4.79",
                                    "level": "average"
                                }
                            ]
                        },
                        "review": {
                            "shouldCollapse": True,
                            "summary": "\u003cp\u003eВ целом все устраивает, зп конкурентная. Когда захотел по личным причинам уехать в Грузию - предоставили возможность работать удаленно.\u003cbr\u003e\u003c/p\u003e",
                            "positives": "\u003cp\u003eГибкая удаленка\u003c/p\u003e\n\u003cp\u003eХорошие процессы\u003c/p\u003e\n\u003cp\u003eКрутые ребята\u003c/p\u003e",
                            "negatives": "\u003cp\u003eДМС оформляется только после испытательного\u003c/p\u003e\n\u003cp\u003eНе хватает тимбилдинга для удаленщиков\u003c/p\u003e"
                        },
                        "position": 1,
                        "company": {
                            "title": "Aston (ex. Andersen)",
                            "description": "Аутсорсинговая компания, ориентированная на разработку ПО",
                            "href": "/companies/aston",
                            "avatar": {
                                "src": "https://habrastorage.org/getpro/moikrug/uploads/company/100/005/141/5/logo/medium_f9256456483c3c02a7a9eb56c48ba5a1.jpg",
                                "src2x": "https://habrastorage.org/getpro/moikrug/uploads/company/100/005/141/5/logo/medium_f9256456483c3c02a7a9eb56c48ba5a1.jpg",
                                "alt": "Aston (ex. Andersen)"
                            },
                            "rateHref": None,
                            "location": {
                                "title": "Москва",
                                "href": "/companies/ratings?city_id=678"
                            },
                            "vacancies": {
                                "title": "4 вакансии",
                                "href": "/companies/aston/vacancies"
                            },
                            "awards": [
                                {
                                    "title": "Средняя оценка #1",
                                    "image": {
                                        "src": "/images/medals/rating.svg"
                                    },
                                    "href": "/companies/ratings?sz=4\u0026y=2022"
                                },
                                ...
                            ],
                            "accredited": True
                        }
                    }
                ],
                "meta": {
                    "perPage": 25,
                    "currentPage": 1,
                    "totalPages": 1,
                    "totalResults": 1,
                    "counterDescription": "медианная общая средняя оценка 4.81"
                }
            }
        """
        params = QueryParams({
            "sort": sort,
            "y": year or datetime.now().year - 1,
            "sz": size,
            "page": page,
            "q": search,
        })
        return self.get(f"frontend/companies/ratings?{params.query()}")

    def rate_company(self):
        # TODO:
        pass
