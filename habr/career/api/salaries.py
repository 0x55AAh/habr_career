from typing import Any

from habr.career.utils import EmploymentType, QueryParams, bool_to_str


# noinspection PyUnresolvedReferences
class HABRCareerSalariesMixin:
    @property
    def my_salary(self) -> dict[str, Any]:
        """

        :return:
        """
        path = "frontend_v1/salary_calculator/my_salary"
        return self.get(path, auth_required=True)

    def get_suitable_vacancies(
            self,
            specializations: list[str] | None = None,
            qualification: str | None = None,
            remote: bool | None = None,
            employment_type: EmploymentType | None = None,
            company: str | None = None,
            skills: list[str] | None = None,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
    ) -> list[dict[str, Any]]:
        """

        :param specializations:
        :param qualification:
        :param remote:
        :param employment_type:
        :param company:
        :param skills:
        :param locations:
        :param exclude_locations:
        :return:
        """
        params = QueryParams({
            "qualification": qualification,   # ["Senior", "All"]
            "spec_aliases": specializations,  # ["backend"]
            "remote": bool_to_str(remote),    # ["true", "false"]
            "employment_type": employment_type,
            "company_alias": company,         # "makediff"
            "skills": skills,                 # ["TCP"]
            "locations": locations,           # ["ct_444"]
            "exclude_locations": exclude_locations,  # [0, 1]
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/suitable_vacancies?{query}"
        return self.get(path, auth_required=True, key="vacancies")

    def get_suitable_courses(
            self,
            specializations: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """

        :param specializations:
        :return:
        """
        # TODO: All parameters?
        params = QueryParams({
            "spec_aliases": specializations,  # ["backend"]
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/suitable_courses?{query}"
        return self.get(path, auth_required=True, key="courses")

    def get_salary_reports(self) -> list[dict[str, str]]:
        path = "frontend_v1/salary_calculator/salary_reports"
        return self.get(path, key="posts")

    def get_salary_general_graph(
            self,
            # qualification: str | None = None,
            specializations: list[str] | None = None,
            remote: bool | None = None,
            employment_type: EmploymentType | None = None,
            company: str | None = None,
            skills: list[str] | None = None,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
    ) -> dict[str, Any]:
        params = QueryParams({
            # TODO: check qualification
            # "qualification": qualification,          # "Senior"
            "spec_aliases": specializations,         # ["backend"],
            "remote": bool_to_str(remote),           # ["true", "false"]
            "employment_type": employment_type,      # [0, 1]
            "company_alias": company,                # "makediff"
            "skills": skills,                        # ["TCP"]
            "locations": locations,                  # ["ct_444"]
            "exclude_locations": exclude_locations,  # [0, 1]
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/general_graph?{query}"
        return self.get(path, auth_required=True)

    def get_salary_dynamic_graph(
            self,
            qualification: str | None = None,
            specializations: list[str] | None = None,
            remote: bool | None = None,
            employment_type: EmploymentType | None = None,
            company: str | None = None,
            skills: list[str] | None = None,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
    ) -> dict[str, Any]:
        """

        :param qualification:
        :param specializations:
        :param remote:
        :param employment_type:
        :param company:
        :param skills:
        :param locations:
        :param exclude_locations:
        :return:
        """
        params = QueryParams({
            "qualification": qualification,          # "Senior"
            "spec_aliases": specializations,         # ["backend"],
            "remote": bool_to_str(remote),           # ["true", "false"]
            "employment_type": employment_type,      # [0, 1]
            "company_alias": company,                # "makediff"
            "skills": skills,                        # ["TCP"]
            "locations": locations,                  # ["ct_444"]
            "exclude_locations": exclude_locations,  # [0, 1]
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/dynamic_graph?{query}"
        return self.get(path, auth_required=True)

    def get_locations_suggestions(self, search: str) -> list[dict[str, str]]:
        path = f"frontend_v1/suggestions/locations?q={search}"
        return self.get(path, key="locations")

    # def get_locations_suggestions(self, search: str) -> list[dict[str, str]]:
    #     # when search is empty we get list of our own locations
    #     path = f"frontend/suggestions/locations?term={search}"
    #     return self.get(path, key="list")

    def get_companies_suggestions(self, search: str) -> list[dict[str, str]]:
        path = f"frontend_v1/suggestions/companies?term={search}"
        return self.get(path, key="companies")

    # def get_companies_suggestions(self, search: str) -> list[dict[str, Any]]:
    #     """
    #
    #     :param search:
    #     :return: Example:
    #         {
    #             "list": [
    #                 {
    #                     "value": 1000080155,
    #                     "title": "MTS Digital",
    #                     "image": {
    #                         "src": "https://habrastorage.org/getpro/moikrug/uploads/company/100/008/015/5/logo/medium_a7e9f2a19e0220bcc8975f5dd57b1107.png",
    #                         "src2x": null,
    #                         "alt": "MTS Digital"
    #                     }
    #                 },
    #                 ...
    #             ]
    #         }
    #     """
    #     path = f"frontend/suggestions/companies?term={search}"
    #     return self.get(path, key="list")
