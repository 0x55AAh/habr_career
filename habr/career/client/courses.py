from enum import verify, UNIQUE, StrEnum
from typing import Any, NamedTuple

from habr.career.utils import (
    Currency,
    Pagination,
    Qualification,
    SortDirection,
    QueryParams,
)


@verify(UNIQUE)
class CourseSortField(StrEnum):
    START_DATE = "startDate"
    PRICE = "price"
    AVERAGE_RATING = "averageRating"


@verify(UNIQUE)
class CourseDuration(StrEnum):
    QUARTER = "quarter"
    LESS_HALF = "lessHalf"
    MORE_HALF = "moreHalf"
    MORE_YEAR = "moreYear"


class Sort(NamedTuple):
    field: CourseSortField
    direction: SortDirection


# noinspection PyUnresolvedReferences
class HABRCareerCoursesMixin:
    """Раздел `Образование`"""
    # TODO: API not discovered for education_centers and universities

    def get_courses(
            self,
            currency: Currency = Currency.RUR,
            search: str | None = None,
            page: int = Pagination.INIT_PAGE,
            per_page: int = Pagination.PER_PAGE,
            sort: Sort | None = None,
            price: int | None = None,
            free_only: bool | None = None,
            online_only: bool | None = None,
            with_assist: bool | None = None,
            with_cert: bool | None = None,
            education_platforms: list[str] | None = None,
            cities: list[str] | None = None,
            skills: list[str] | None = None,
            specializations: list[str] | None = None,
            duration: CourseDuration | None = None,
            qualification: Qualification | None = None,
    ) -> dict[str, Any]:
        """

        :param currency:
        :param search:
        :param page:
        :param per_page:
        :param sort:
        :param price:
        :param free_only:
        :param online_only:
        :param with_assist:
        :param with_cert:
        :param education_platforms:
        :param cities:
        :param skills:
        :param specializations:
        :param duration:
        :param qualification:
        :return:
        """
        sort = sort or Sort(CourseSortField.PRICE, SortDirection.ASC)
        params = QueryParams({
            "priceCurrency": currency,
            "page": page,
            "perPage": per_page,
            "sortBy": sort.field,
            "dir": sort.direction,

            "priceValue": price,

            "freeOnly": free_only,
            "onlineOnly": online_only,
            "withAssist": with_assist,
            "withCert": with_cert,

            "educationPlatforms[]": education_platforms,
            "cities[]": cities,

            "duration": duration,
            "qualification": qualification,

            "skills[]": skills,
            "specializations[]": specializations,

            "q": search,
        })
        query = params.query(doseq=True)
        return self.get(f"frontend_v1/courses?{query}")

    def get_course(self, alias: str) -> dict[str, Any]:
        """
        Get course detail.

        :param alias: Course alias
        :return:
        """
        return self.get(f"frontend_v1/courses/{alias}")

    def get_course_scores(self, alias: str) -> dict[str, Any]:
        """
        Get course scores.

        :param alias: Course alias
        :return:
        """
        return self.get(f"frontend_v1/courses/{alias}/scores")

    def get_similar_courses(self, alias: str) -> dict[str, Any]:
        """
        Get courses similar to which was requested by alias.

        :param alias: Course alias
        :return:
        """
        return self.get(f"frontend_v1/courses/{alias}/similar_courses")

    def get_popular_education_platforms(
            self,
            limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Get popular education platforms.

        :param limit:
        :return: Examples:
            {
                "popularEducationPlatforms": [
                    {
                        "id": "35",
                        "title": "Яндекс Практикум",
                        "alias": "35-yandeks-praktikum",
                        "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/035/logo/medium_9029ac948c9751ee1ad303e78f4f03c8.png",
                        "isPartner": true,
                        "coursesCount": 41,
                        "graduatesCount": 9843
                    }
               ]
            }
        """
        path = f"frontend_v1/education_platforms/popular?limit={limit}"
        return self.get(path, key="popularEducationPlatforms")

    def get_popular_skills(self, limit: int = 10) -> dict[str, Any]:
        """
        Get popular skills.

        :param limit:
        :return: Examples:
            {
                "skills": [
                    {
                      "title": "Python",
                      "alias": "python"
                    },
                    {
                      "title": "Java",
                      "alias": "java"
                    },
                    {
                      "title": "Защита информации",
                      "alias": "zaschita-informatsii"
                    },
                    {
                      "title": "JavaScript",
                      "alias": "javascript"
                    },
                    {
                      "title": "Управление проектами",
                      "alias": "upravlenie-proektami"
                    }
                ]
            }
        """
        path = f"frontend_v1/skills/popular?limit={limit}"
        return self.get(path, key="skills")

    def get_educations_suggestions(self, search: str) -> dict[str, Any]:
        """

        :param search:
        :return:
        """
        return self.get(f"frontend_v1/suggestions/educations?term={search}")

    def get_education_platforms_suggestions(
            self,
            search: str,
    ) -> list[dict[str, str]]:
        """

        :param search:
        :return:
        """
        path = f"frontend_v1/suggestions/education_platforms?term={search}"
        return self.get(path, key="education_platforms")

    @property
    def courses_count(self) -> int:
        """
        Get the number of currently active courses.

        :return: Examples:
            {"count": 1139}
        """
        return self.get("frontend_v1/courses/total_count", key="count")

    def get_specializations_with_course_counters(self) -> dict[str, Any]:
        """

        :return:
        """
        return self.get("frontend_v1/specializations/with_course_counters")

    def get_specializations(self) -> dict[str, Any]:
        """

        :return:
        """
        return self.get("frontend_v1/specializations")

    def get_offers(self, specializations: list[str]) -> dict[str, Any]:
        """

        :param specializations:
        :return: Examples:
            {
                "offers": {
                    "lowPrice": 28990,
                    "highPrice": 39990,
                    "priceCurrency": "RUB",
                    "offerCount": 4,
                    "offers": [
                        {
                            "@type": "FinancialProduct",
                            "name": "PROавтовебинарные воронки на GetCourse 2.0 ",
                            "brand": "GetHelpers.ru"
                        },
                        {
                            "@type": "FinancialProduct",
                            "name": "Технический специалист по настройке GetCourse",
                            "brand": "GetHelpers.ru"
                        },
                        {
                            "@type": "FinancialProduct",
                            "name": "PROпроцессы и маркетинг на GetCourse",
                            "brand": "GetHelpers.ru"
                        },
                        {
                            "@type": "FinancialProduct",
                            "name": "Специалист по чат-ботам",
                            "brand": "GetHelpers.ru"
                        }
                    ]
                },
                "aggregateRating": {
                    "bestRating": "5",
                    "worstRating": "1",
                    "ratingCount": 0,
                    "ratingValue": null
                },
                "events": [
                    {
                        "name": "Разработчик C++",
                        "description": "Образовательный курс в «Яндекс Практикум». 9 месяцев, 126 000 ₽. Онлайн обучение. Сертификат. Трудоустройство. Запишитесь на курс прямо сейчас или расскажите о нём своим знакомым.",
                        "startDate": "2023-11-13",
                        "endDate": "2024-08-13",
                        "url": "https://career.habr.com/courses/1200-razrabotchik-c"
                    },
                    {
                        "name": "Инженер данных",
                        "description": "Образовательный курс в «Яндекс Практикум». 6 месяцев, 95 000 ₽. Онлайн обучение. Сертификат. Запишитесь на курс прямо сейчас или расскажите о нём своим знакомым.",
                        "startDate": "2023-11-13",
                        "endDate": "2024-05-13",
                        "url": "https://career.habr.com/courses/2900-inzhener-dannyh"
                    },
                    {
                        "name": "Продакт-менеджер",
                        "description": "Образовательный курс в «Яндекс Практикум». 5 месяцев, 120 000 ₽. Онлайн обучение. Сертификат. Запишитесь на курс прямо сейчас или расскажите о нём своим знакомым.",
                        "startDate": "2023-11-13",
                        "endDate": "2024-04-13",
                        "url": "https://career.habr.com/courses/2936-prodakt-menedzher"
                    }
                ]
            },
            {
                "httpCode": 404,
                "errorCode": "NOT_FOUND",
                "message": "Not found",
                "data": {}
            }
        """
        params = QueryParams({"specializations[]": specializations})
        query = params.query(doseq=True)
        return self.get(f"frontend_v1/courses/ld_json?{query}")
