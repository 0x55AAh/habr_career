from typing import Any

from habr.career.utils import (
    CompanySize,
    CompanyRatingCriteria,
    Pagination,
    QueryParams,
)


# noinspection PyUnresolvedReferences
class HABRCareerCompaniesMixin:
    # TODO: No API endpoints found for the chapter
    pass


# noinspection PyUnresolvedReferences
class HABRCareerCompaniesRatingsMixin:
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
