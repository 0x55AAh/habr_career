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

            "educationPlatforms": education_platforms,
            "cities": cities,

            "duration": duration,
            "qualification": qualification,

            "skills": skills,
            "specializations": specializations,

            "q": search,
        })
        return self.get(f"frontend_v1/courses?{params.query(doseq=True)}")

    def get_course(self, alias: str) -> dict[str, Any]:
        """

        :param alias: Course alias
        :return:
        """
        return self.get(f"frontend_v1/courses/{alias}")

    def get_course_scores(self, alias: str) -> dict[str, Any]:
        """

        :param alias: Course alias
        :return:
        """
        return self.get(f"frontend_v1/courses/{alias}/scores")

    def get_similar_courses(self, alias: str) -> dict[str, Any]:
        """

        :param alias: Course alias
        :return:
        """
        return self.get(f"frontend_v1/courses/{alias}/similar_courses")

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

    def get_cities_suggestions(self, search: str) -> list[dict[str, str]]:
        """

        :param search:
        :return:
        """
        path = f"frontend_v1/suggestions/cities?q={search}"
        return self.get(path, key="cities")

    def get_skills_suggestions(self, search: str) -> list[dict[str, str]]:
        """

        :param search:
        :return:
        """
        path = f"frontend_v1/suggestions/skills?q={search}"
        return self.get(path, key="skills")

    # def get_skills_suggestions(self, search: str) -> list[dict[str, Any]]:
    #     """
    #
    #     :param search:
    #     :return:
    #     """
    #     path = f"frontend/suggestions/skills?term={search}"
    #     return self.get(path, key="list")

    @property
    def courses_count(self) -> int:
        """

        :return:
        """
        return self.get("frontend_v1/courses/total_count", key="count")

    @property
    def qualifications(self) -> list[dict[str, str | int]]:
        """
        {
            "qualifications": [
                {
                    "title": "Стажёр",
                    "position": 0,
                    "alias": "Intern"
                },
                {
                    "title": "Младший",
                    "position": 2,
                    "alias": "Junior"
                },
                {
                    "title": "Средний",
                    "position": 3,
                    "alias": "Middle"
                },
                {
                    "title": "Старший",
                    "position": 4,
                    "alias": "Senior"
                },
                {
                    "title": "Ведущий",
                    "position": 5,
                    "alias": "Lead"
                }
            ]
        }
        :return:
        """
        return self.get("frontend_v1/qualifications", key="qualifications")

    @property
    def currencies(self) -> list[str]:
        """
        {
            "currencies": [
                {
                    "currency": "rur"
                },
                {
                    "currency": "eur"
                },
                {
                    "currency": "usd"
                },
                {
                    "currency": "uah"
                },
                {
                    "currency": "kzt"
                }
            ]
        }
        :return:
        """
        res = self.get("frontend_v1/currencies", key="currencies")
        return [r["currency"] for r in res]

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
