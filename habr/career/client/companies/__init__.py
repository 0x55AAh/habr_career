from datetime import datetime
from enum import verify, UNIQUE, IntEnum, StrEnum

from habr.career.utils import Pagination
from .models import Ratings


@verify(UNIQUE)
class CompanySize(IntEnum):
    """
    HUGE:   Over 5000
    BIG:    1000 - 5000
    MEDIUM: 100 - 1000
    SMALL:  10 - 100
    """
    HUGE = 5    # > 5000
    BIG = 4     # 1000 - 5000
    MEDIUM = 3  # 100 - 1000
    SMALL = 2   # 10 - 100


@verify(UNIQUE)
class CompanyRatingCriteria(StrEnum):
    """
    AV: Общая оценка
    S2: Интересные задачи
    S3: Адекватная зарплата
    S4: Социальный пакет
    S5: Комфортные условия труда
    S6: Профессиональный рост
    S7: Карьерный рост
    S8: Отношения с коллегами
    S9: Признание результатов труда
    S10: Грамотность менеджмента
    S11: Связь с топ-менеджментом
    S12: Компания делает мир лучше
    S16: Современные технологии
    """
    AV = "av"     # Общая оценка
    S2 = "s_2"    # Интересные задачи
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
    S16 = "s_16"  # Современные технологии


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
            year: int | None = datetime.now().year - 1,
            size: CompanySize | None = CompanySize.HUGE,
            sort: CompanyRatingCriteria | None = CompanyRatingCriteria.AV,
            search: str | None = None,
            page: int | None = Pagination.INIT_PAGE,
    ) -> Ratings:
        """
        Get companies ratings.

        :param year: Covers last previous 5 years.
        :param size: Company size.
        :param sort:
        :param search: Search query.
        :param page: Page number.
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
                                ...
                            ]
                        },
                        "review": {
                            "shouldCollapse": True,
                            "summary": "<p>В целом все устраивает, зп конкурентная. Когда захотел по личным причинам уехать в Грузию - предоставили возможность работать удаленно.<br></p>",
                            "positives": "<p>Гибкая удаленка</p>\n<p>Хорошие процессы</p>\n<p>Крутые ребята</p>",
                            "negatives": "<p>ДМС оформляется только после испытательного</p>\n<p>Не хватает тимбилдинга для удаленщиков</p>"
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
                    },
                    ...
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
        return self.get(
            "frontend/companies/ratings",
            params={
                "sort": sort,
                "y": year,
                "sz": size,
                "page": page,
                "q": search,
            },
            cls=Ratings,
        )

    def rate_company(self):
        # TODO:
        pass

    def subscribe_company(self, company_id: str) -> dict[str, bool]:
        """
        Subscribe company.

        :param company_id: Company ID
        :return:
        """
        self.post(
            "profile/company_connections",
            base_url="https://career.habr.com",
            params={"company_id": company_id},
            headers={"Accept": "application/javascript"},
            auth_required=True,
        )
        return {"success": True}

    def unsubscribe_company(self, company_id: str) -> dict[str, bool]:
        """
        Unsubscribe company.

        :param company_id: Company ID
        :return:
        """
        self.delete(
            "profile/company_connections",
            base_url="https://career.habr.com",
            params={"company_id": company_id},
            headers={"Accept": "application/javascript"},
            auth_required=True,
        )
        return {"success": True}

    def favorite_company(self, company_id: str) -> dict[str, bool]:
        """
        Add company to favorites list.

        :param company_id: Company ID
        :return:
        """
        self.post(
            "profile/fav_companies",
            base_url="https://career.habr.com",
            params={"company_id": company_id},
            headers={"Accept": "application/javascript"},
            auth_required=True,
        )
        return {"success": True}

    def unfavorite_company(self, company_id: str) -> dict[str, bool]:
        """
        Remove company from favorites list.

        :param company_id: Company ID
        :return:
        """
        self.delete(
            "profile/fav_companies",
            base_url="https://career.habr.com",
            params={"company_id": company_id},
            headers={"Accept": "application/javascript"},
            auth_required=True,
        )
        return {"success": True}
