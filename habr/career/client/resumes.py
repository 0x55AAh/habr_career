from enum import verify, UNIQUE, StrEnum
from typing import Any

from habr.career.utils import Currency, QueryParams


@verify(UNIQUE)
class CareerSortingCriteria(StrEnum):
    # last_visited: по дате визита
    # relevance: по соответствию
    # salary_desc: по убыванию зарплаты
    # salary_asc: по возрастанию зарплаты
    LAST_VISITED = "last_visited"
    RELEVANCE = "relevance"
    SALARY_DESC = "salary_desc"
    SALARY_ASC = "salary_asc"


@verify(UNIQUE)
class CareerActivityPeriod(StrEnum):
    # two_years: За 2 года
    # year: За год
    # three_months: За 3 месяца
    TWO_YEARS = "two_years"
    YEAR = "year"
    THREE_MONTHS = "three_months"


@verify(UNIQUE)
class CareerWorkState(StrEnum):
    # not_search: Не ищу работу
    # search: Ищу работу
    # ready: Рассмотрю предложения
    NOT_SEARCH = "not_search"
    SEARCH = "search"
    READY = "ready"


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


# noinspection PyUnresolvedReferences
class HABRCareerResumesMixin:
    """Раздел `Специалисты`"""

    def get_resumes(
            self,
            search: str | None = None,
            search_fields: list[str] | None = None,
            sort: CareerSortingCriteria | None = None,
            specializations: list[int] | None = None,
            qualification: int | None = None,
            skills: list[int] | None = None,
            salary: int | None = None,
            currency: Currency | None = Currency.RUR,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
            companies: list[int] | None = None,
            not_companies: bool | None = None,
            current_company: bool | None = None,
            universities: list[int] | None = None,
            not_universities: bool | None = None,
            educations: list[int] | None = None,
            not_educations: bool | None = None,
            work_state: CareerWorkState | None = None,
            relocation: bool | None = None,
            remote: bool | None = None,
            period: CareerActivityPeriod | None = None,
            with_educations: bool | None = None,
            with_extra_educations: bool | None = None,
            with_experiences: bool | None = None,
            with_salary: bool | None = None,
            with_social_ratings: bool | None = None,
    ) -> dict[str, Any]:
        # TODO:
        params = QueryParams({
            "q": search,
            # fio - в имени
            # resume_headline - в специализации
            # experiences - в должностях
            # skills - в навыках профиля
            # social_tags - в навыках сообществ
            "fields": search_fields,
            "s": specializations,
            "order": sort,
            "qid": qualification,
            "skills": skills,
            "salary": salary,
            "currency": currency,  # Case-sensitive? (Default "RUR")
            "locations": locations,
            "exclude_locations": exclude_locations,
            "company_ids": companies,
            "not_companies": not_companies,
            "current_company": current_company,
            "university_ids": universities,
            "not_universities": not_universities,
            "edc_ids": educations,
            "not_edcs": not_educations,
            "work_state": work_state,
            "relocation": relocation,
            "remote": remote,
            "period": period,
            # С высшим образованием
            "with_educations": with_educations,
            # С дополнительным образованием
            "with_add_eds": with_extra_educations,
            # С опытом работы
            "with_experiences": with_experiences,
            # Указана зарплата
            "with_salary": with_salary,
            # Участник ИТ-сообществ
            "with_social_ratings": with_social_ratings,
        })
        query = params.query(doseq=True, bool_as_str=True)
        return self.get(f"frontend/resumes?{query}")

    def get_resumes_data(
            self,
            search: str | None = None,
            search_fields: list[str] | None = None,
            sort: CareerSortingCriteria | None = None,
            specializations: list[int] | None = None,
            qualification: int | None = None,
            skills: list[int] | None = None,
            salary: int | None = None,
            currency: Currency | None = Currency.RUR,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
            companies: list[int] | None = None,
            not_companies: bool | None = None,
            current_company: bool | None = None,
            universities: list[int] | None = None,
            not_universities: bool | None = None,
            educations: list[int] | None = None,
            not_educations: bool | None = None,
            work_state: CareerWorkState | None = None,
            relocation: bool | None = None,
            remote: bool | None = None,
            period: CareerActivityPeriod | None = None,
            with_educations: bool | None = None,
            with_extra_educations: bool | None = None,
            with_experiences: bool | None = None,
            with_salary: bool | None = None,
            with_social_ratings: bool | None = None,
    ) -> dict[str, Any]:
        """
        Returned data contains an extra data including saved filters.
        TODO: API endpoint returning filters not discovered yet.

        :param search:
        :param search_fields:
        :param sort:
        :param specializations:
        :param qualification:
        :param skills:
        :param salary:
        :param currency:
        :param locations:
        :param exclude_locations:
        :param companies:
        :param not_companies:
        :param current_company:
        :param universities:
        :param not_universities:
        :param educations:
        :param not_educations:
        :param work_state:
        :param relocation:
        :param remote:
        :param period:
        :param with_educations:
        :param with_extra_educations:
        :param with_experiences:
        :param with_salary:
        :param with_social_ratings:
        :return:
        """
        # TODO:
        params = QueryParams({
            "q": search,
            # fio - в имени
            # resume_headline - в специализации
            # experiences - в должностях
            # skills - в навыках профиля
            # social_tags - в навыках сообществ
            "fields": search_fields,
            "s": specializations,
            "order": sort,
            "qid": qualification,
            "skills": skills,
            "salary": salary,
            "currency": currency,  # Case-sensitive? (Default "RUR")
            "locations": locations,
            "exclude_locations": exclude_locations,
            "company_ids": companies,
            "not_companies": not_companies,
            "current_company": current_company,
            "university_ids": universities,
            "not_universities": not_universities,
            "edc_ids": educations,
            "not_edcs": not_educations,
            "work_state": work_state,
            "relocation": relocation,
            "remote": remote,
            "period": period,
            # С высшим образованием
            "with_educations": with_educations,
            # С дополнительным образованием
            "with_add_eds": with_extra_educations,
            # С опытом работы
            "with_experiences": with_experiences,
            # Указана зарплата
            "with_salary": with_salary,
            # Участник ИТ-сообществ
            "with_social_ratings": with_social_ratings,
        })
        query = params.query(doseq=True, bool_as_str=True)
        return self.get(f"resumes?{query}", auth_required=True, ssr=True)

    def save_careers_filter(
            self,
            search: str | None = None,
            search_fields: list[str] | None = None,
            sort: CareerSortingCriteria | None = None,
            specializations: list[int] | None = None,
            qualification: int | None = None,
            skills: list[int] | None = None,
            salary: int | None = None,
            currency: Currency | None = Currency.RUR,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
            companies: list[int] | None = None,
            not_companies: bool | None = None,
            current_company: bool | None = None,
            universities: list[int] | None = None,
            not_universities: bool | None = None,
            educations: list[int] | None = None,
            not_educations: bool | None = None,
            work_state: CareerWorkState | None = None,
            relocation: bool | None = None,
            remote: bool | None = None,
            period: CareerActivityPeriod | None = None,
            with_educations: bool | None = None,
            with_extra_educations: bool | None = None,
            with_experiences: bool | None = None,
            with_salary: bool | None = None,
            with_social_ratings: bool | None = None,
    ) -> dict[str, Any]:
        """
        - RESPONSE:
            {
                "status": "ok",
                "savedFilters": [
                    {
                        "id": 71930,
                        "title": "Бэкенд разработчик • до 200 000 ₽ • МТС (не текущее место работы) • ИПК и ПРНО МО (исключить) • Яндекс Практикум (исключить) • Стажёр (Intern) • Готов к удаленной работе • Готов к переезду • С образованием • С доп. образованием • С опытом работы • Указана зарплата • Участник ИТ-сообществ • Заходили на сайт за 3 месяца • Луганск (исключить) • По возрастанию зарплаты • [Анд]",
                        "href": "/resumes?company_ids%5B%5D=355898672\u0026currency=RUR\u0026current_company=true\u0026edc_ids%5B%5D=35\u0026exclude_locations=true\u0026locations%5B%5D=c_909\u0026not_companies=true\u0026not_edcs=true\u0026not_universities=true\u0026order=salary_asc\u0026period=three_months\u0026q=%D0%90%D0%BD%D0%B4\u0026qid=1\u0026relocation=true\u0026remote=true\u0026s%5B%5D=2\u0026salary=200000\u0026university_ids%5B%5D=82038\u0026with_add_eds=true\u0026with_educations=true\u0026with_experiences=true\u0026with_salary=true\u0026with_social_ratings=true",
                        "filters": {
                            "searchFields": [],
                            "qualification": 1,
                            "salary": 200000,
                            "currency": "RUR",
                            "remoteWork": true,
                            "relocation": true,
                            "hasSalary": true,
                            "hasHighEducation": true,
                            "hasExtraEducation": true,
                            "hasExperience": true,
                            "hasSocialRatings": true,
                            "excludeLocation": true,
                            "excludeCompany": true,
                            "excludeUniversity": true,
                            "excludeExtraEducation": true,
                            "isCurrentCompany": true,
                            "activityPeriod": "three_months",
                            "s": [
                                2
                            ],
                            "locations": [
                                "c_909"
                            ],
                            "companies": [
                                355898672
                            ],
                            "universities": [
                                82038
                            ],
                            "extraEducations": [
                                35
                            ]
                        },
                        "query": "Анд",
                        "order": "salary_asc",
                        "filtersData": {
                            "locations": [
                                {
                                    "value": "c_909",
                                    "title": "Луганск"
                                }
                            ],
                            "skills": [],
                            "companies": [
                                {
                                    "value": 355898672,
                                    "title": "МТС"
                                }
                            ],
                            "universities": [
                                {
                                    "value": 82038,
                                    "title": "ИПК и ПРНО МО",
                                    "subtitle": "Москва, Институт повышения квалификации и профессиональной переподготовки работников народного образования Московской области"
                                }
                            ],
                            "extraEducations": [
                                {
                                    "value": 35,
                                    "title": "Яндекс Практикум"
                                }
                            ]
                        }
                    }
                ]
            },
            {
                "status": "error",
                "errors": [
                    {
                        "message": "Вы уже сохранили фильтр с такими параметрами.",
                        "type": "error"
                    }
                ]
            }
        :return:
        """
        # TODO:
        params = QueryParams({
            "q": search,
            # fio - в имени
            # resume_headline - в специализации
            # experiences - в должностях
            # skills - в навыках профиля
            # social_tags - в навыках сообществ
            "fields": search_fields,
            "s": specializations,
            "order": sort,
            "qid": qualification,
            "skills": skills,
            "salary": salary,
            "currency": currency,  # Case-sensitive? (Default "RUR")
            "locations": locations,
            "exclude_locations": exclude_locations,
            "company_ids": companies,
            "not_companies": not_companies,
            "current_company": current_company,
            "university_ids": universities,
            "not_universities": not_universities,
            "edc_ids": educations,
            "not_edcs": not_educations,
            "work_state": work_state,
            "relocation": relocation,
            "remote": remote,
            "period": period,
            # С высшим образованием
            "with_educations": with_educations,
            # С дополнительным образованием
            "with_add_eds": with_extra_educations,
            # С опытом работы
            "with_experiences": with_experiences,
            # Указана зарплата
            "with_salary": with_salary,
            # Участник ИТ-сообществ
            "with_social_ratings": with_social_ratings,
        })
        query = params.query(doseq=True, bool_as_str=True)
        path = f"frontend/user_filters/resumes?{query}"
        return self.post(path, auth_required=True)

    def _career_filter_to_params(self, id_: int) -> QueryParams:
        # {
        #     "id": 71945,
        #     "title": "\u0411\u044d\u043a\u0435\u043d\u0434 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u0447\u0438\u043a \u2022 \u0434\u043e 200 000 \u20bd \u2022 \u041c\u0422\u0421 (\u043d\u0435 \u0442\u0435\u043a\u0443\u0449\u0435\u0435 \u043c\u0435\u0441\u0442\u043e \u0440\u0430\u0431\u043e\u0442\u044b) \u2022 \u0418\u041f\u041a \u0438 \u041f\u0420\u041d\u041e \u041c\u041e (\u0438\u0441\u043a\u043b\u044e\u0447\u0438\u0442\u044c) \u2022 \u042f\u043d\u0434\u0435\u043a\u0441 \u041f\u0440\u0430\u043a\u0442\u0438\u043a\u0443\u043c (\u0438\u0441\u043a\u043b\u044e\u0447\u0438\u0442\u044c) \u2022 \u0421\u0442\u0430\u0436\u0451\u0440 (Intern) \u2022 \u0413\u043e\u0442\u043e\u0432 \u043a \u0443\u0434\u0430\u043b\u0435\u043d\u043d\u043e\u0439 \u0440\u0430\u0431\u043e\u0442\u0435 \u2022 \u0413\u043e\u0442\u043e\u0432 \u043a \u043f\u0435\u0440\u0435\u0435\u0437\u0434\u0443 \u2022 \u0421 \u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435\u043c \u2022 \u0421 \u0434\u043e\u043f. \u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435\u043c \u2022 \u0421 \u043e\u043f\u044b\u0442\u043e\u043c \u0440\u0430\u0431\u043e\u0442\u044b \u2022 \u0423\u043a\u0430\u0437\u0430\u043d\u0430 \u0437\u0430\u0440\u043f\u043b\u0430\u0442\u0430 \u2022 \u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a \u0418\u0422-\u0441\u043e\u043e\u0431\u0449\u0435\u0441\u0442\u0432 \u2022 \u0417\u0430\u0445\u043e\u0434\u0438\u043b\u0438 \u043d\u0430 \u0441\u0430\u0439\u0442 \u0437\u0430 3 \u043c\u0435\u0441\u044f\u0446\u0430 \u2022 \u041b\u0443\u0433\u0430\u043d\u0441\u043a (\u0438\u0441\u043a\u043b\u044e\u0447\u0438\u0442\u044c) \u2022 \u041f\u043e \u0432\u043e\u0437\u0440\u0430\u0441\u0442\u0430\u043d\u0438\u044e \u0437\u0430\u0440\u043f\u043b\u0430\u0442\u044b \u2022 [\u0410\u043d\u0434]",
        #     "href": "/resumes?company_ids%5B%5D=355898672&currency=RUR&current_company=true&edc_ids%5B%5D=35&exclude_locations=true&locations%5B%5D=c_909&not_companies=true&not_edcs=true&not_universities=true&order=salary_asc&period=three_months&q=%D0%90%D0%BD%D0%B4&qid=1&relocation=true&remote=true&s%5B%5D=2&salary=200000&university_ids%5B%5D=82038&with_add_eds=true&with_educations=true&with_experiences=true&with_salary=true&with_social_ratings=true",
        #     "filters": {
        #         "searchFields": [],
        #         "qualification": 1,
        #         "salary": 200000,
        #         "currency": "RUR",
        #         "remoteWork": true,
        #         "relocation": true,
        #         "hasSalary": true,
        #         "hasHighEducation": true,
        #         "hasExtraEducation": true,
        #         "hasExperience": true,
        #         "hasSocialRatings": true,
        #         "excludeLocation": true,
        #         "excludeCompany": true,
        #         "excludeUniversity": true,
        #         "excludeExtraEducation": true,
        #         "isCurrentCompany": true,
        #         "activityPeriod": "three_months",
        #         "s": [
        #             2
        #         ],
        #         "locations": [
        #             "c_909"
        #         ],
        #         "companies": [
        #             355898672
        #         ],
        #         "universities": [
        #             82038
        #         ],
        #         "extraEducations": [
        #             35
        #         ]
        #     },
        #     "query": "\u0410\u043d\u0434",
        #     "order": "salary_asc",
        #     "filtersData": {
        #         "locations": [
        #             {
        #                 "value": "c_909",
        #                 "title": "\u041b\u0443\u0433\u0430\u043d\u0441\u043a"
        #             }
        #         ],
        #         "skills": [],
        #         "companies": [
        #             {
        #                 "value": 355898672,
        #                 "title": "\u041c\u0422\u0421"
        #             }
        #         ],
        #         "universities": [
        #             {
        #                 "value": 82038,
        #                 "title": "\u0418\u041f\u041a \u0438 \u041f\u0420\u041d\u041e \u041c\u041e",
        #                 "subtitle": "\u041c\u043e\u0441\u043a\u0432\u0430, \u0418\u043d\u0441\u0442\u0438\u0442\u0443\u0442 \u043f\u043e\u0432\u044b\u0448\u0435\u043d\u0438\u044f \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0438 \u043f\u0440\u043e\u0444\u0435\u0441\u0441\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u043e\u0439 \u043f\u0435\u0440\u0435\u043f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0438 \u0440\u0430\u0431\u043e\u0442\u043d\u0438\u043a\u043e\u0432 \u043d\u0430\u0440\u043e\u0434\u043d\u043e\u0433\u043e \u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u044f \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438"
        #             }
        #         ],
        #         "extraEducations": [
        #             {
        #                 "value": 35,
        #                 "title": "\u042f\u043d\u0434\u0435\u043a\u0441 \u041f\u0440\u0430\u043a\u0442\u0438\u043a\u0443\u043c"
        #             }
        #         ]
        #     }
        # }
        filters = {
            f["id"]: f for f
            in self.get_resumes_data()["search"]["savedFilters"]
        }
        filter_data = filters[id_]
        # TODO:
        return QueryParams({
            "q": filter_data["query"],
            "order": filter_data["order"],

            "fields": filter_data["filters"]["searchFields"],
            "s": filter_data["filters"]["s"],
            "qid": filter_data["filters"]["qualification"],
            "skills": filter_data["filters"]["skills"],
            "salary": filter_data["filters"]["salary"],
            "currency": filter_data["filters"]["currency"],  # Case-sensitive? (Default "RUR")
            "locations": filter_data["filters"]["locations"],
            "exclude_locations": filter_data["filters"]["excludeLocation"],
            "company_ids": filter_data["filters"]["companies"],
            "not_companies": filter_data["filters"]["excludeCompany"],
            "not_universities": filter_data["filters"]["excludeUniversity"],
            "not_edcs": filter_data["filters"]["excludeExtraEducation"],

            # TODO: Not working, availability is always null
            # TODO: "work_state": filter_data["filters"]["availability"],

            "edc_ids": filter_data["filters"]["extraEducations"],
            "university_ids": filter_data["filters"]["universities"],
            "current_company": filter_data["filters"]["isCurrentCompany"],
            "relocation": filter_data["filters"]["relocation"],
            "remote": filter_data["filters"]["remoteWork"],
            "period": filter_data["filters"]["activityPeriod"],
            # С высшим образованием
            "with_educations": filter_data["filters"]["hasHighEducation"],
            # С дополнительным образованием
            "with_add_eds": filter_data["filters"]["hasExtraEducation"],
            # С опытом работы
            "with_experiences": filter_data["filters"]["hasExperience"],
            # Указана зарплата
            "with_salary": filter_data["filters"]["hasSalary"],
            # Участник ИТ-сообществ
            "with_social_ratings": filter_data["filters"]["hasSocialRatings"],
        })

    def apply_career_filter(self, id_: int) -> dict[str, Any]:
        """
        Apply saved filer on server side.
        NOTE: It might be a bit slower as it needs an extra request to get all
        filters.

        :param id_: Filter ID
        :return:
        """
        params = self._career_filter_to_params(id_)
        query = params.query(doseq=True, bool_as_str=True)
        return self.get(f"frontend/resumes?{query}")

    def delete_careers_filter(self, id_: int) -> dict[str, Any]:
        """

        :param id_: Filter ID
        :return: Example:
            {"status": "ok", "id": 71930}
        """
        path = f"frontend/user_filters/resumes/{id_}"
        return self.delete(path, auth_required=True)

    def get_universities_suggestions(
            self,
            search: str,
    ) -> list[dict[str, Any]]:
        """

        :param search:
        :return: Example:
            {
                "list": [
                    {
                        "value": 82038,
                        "title": "ИПК и ПРНО МО",
                        "subtitle": "Москва, Институт повышения квалифик..."
                    },
                    ...
                ]
            }
        """
        path = f"frontend/suggestions/universities?term={search}"
        return self.get(path, key="list")

    def get_education_centers_suggestions(
            self,
            search: str,
    ) -> list[dict[str, str | int]]:
        """

        :param search:
        :return: Example:
            {
                "list": [
                    {
                        "value": 35,
                        "title": "Яндекс Практикум"
                    },
                    ...
                ]
            }
        """
        path = f"frontend/suggestions/education_centers?term={search}"
        return self.get(path, key="list")
