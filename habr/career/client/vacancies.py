from typing import Any
from urllib.parse import urlencode

from habr.career.utils import Currency, Pagination, QueryParams


# noinspection PyUnresolvedReferences
class HABRCareerVacanciesMixin:
    """Раздел `Вакансии`"""

    def get_vacancies(
            self,
            search: str | None = None,
            sort: str | None = None,
            type_: str | None = None,
            specializations: list[int] | None = None,
            locations: list[str] | None = None,
            skills: list[int] | None = None,
            qualification: int | None = None,
            employment_type: str | None = None,
            salary: int | None = None,
            company: int | None = None,
            with_salary: bool | None = None,
            remote: bool | None = None,
            has_accreditation: bool | None = None,
            exclude_company: bool | None = None,
            currency: Currency | None = Currency.RUR,
            page: int = Pagination.INIT_PAGE,
            per_page: int = Pagination.PER_PAGE,
    ) -> dict[str, Any]:
        """

        :param per_page:
        :param page:
        :param search:
        :param currency:
        :param specializations:
        :param locations: List of aliases
        :param skills:
        :param qualification:
        :param employment_type: ["full_time", "part_time"]
        :param salary:
        :param company:
        :param with_salary:
        :param remote:
        :param has_accreditation:
        :param exclude_company:
        :param sort:
             - relevance: По соответствию (default)
             - date: По дате размещения
             - salary_desc: По убыванию зарплаты
             - salary_asc: По возрастанию зарплаты
        :param type_:
             - all: Все вакансии (default)
             - suitable: Подходящие
        :return:
        """
        params = QueryParams({
            "sort": sort,
            "type": type_,
            "currency": currency,  # Case-sensitive? (Default "RUR")
            "per_page": per_page,
            "page": page,
            "q": search,
            "s": specializations,
            "skills": skills,
            "qid": qualification,
            "salary": salary,
            "company": company,
            "with_salary": with_salary,
            "remote": remote,
            "has_accreditation": has_accreditation,
            "exclude_company": exclude_company,
            "locations": locations,
            "employment_type": employment_type,
        })
        query = params.query(doseq=True, bool_as_str=True)
        return self.get(f"frontend/vacancies?{query}")

    def get_vacancy(self, id_: int) -> dict[str, Any]:
        """

        :param id_: Vacancy ID
        :return:
        """
        # TODO: API endpoint not discovered yet
        return self.get(f"vacancies/{id_}", ssr=True)

    # def add_vacancy_to_favorites(self, id_: int) -> dict[str, Any]:
    #     """
    #
    #     :param id_:
    #     :return: Example: {"favorite": True}
    #     """
    #     path = f"frontend_v1/vacancies/{id_}/favorite"
    #     return self.post(path, auth_required=True)

    def add_vacancy_to_favorites(self, id_: int) -> dict[str, Any]:
        """

        :param id_:
        :return: Example: {"favorite": True}
        """
        path = f"frontend/vacancies/{id_}/favorite"
        return self.post(path, auth_required=True)

    # def remove_vacancy_from_favorites(self, id_: int) -> dict[str, Any]:
    #     """
    #
    #     :param id_: Vacancy ID
    #     :return: Example: {"favorite": False}
    #     """
    #     path = f"frontend_v1/vacancies/{id_}/unfavorite"
    #     return self.post(path, auth_required=True)

    def remove_vacancy_from_favorites(self, id_: int) -> dict[str, Any]:
        """

        :param id_:
        :return: Example: {"favorite": False}
        """
        path = f"frontend/vacancies/{id_}/favorite"
        return self.delete(path, auth_required=True)

    def give_reactions_to_vacancy(
            self,
            id_: int,
            reactions: list[str],
    ) -> dict[str, Any]:
        """

        :param id_: Vacancy ID
        :param reactions:
        :return: Example: {"status": "ok"}
        """
        params = {"reactions": reactions}
        query = urlencode(params, doseq=True)
        path = f"frontend/vacancies/{id_}/reactions?{query}"

        return self.post(path, auth_required=True)

    def respond_to_vacancy(self, id_: int) -> dict[str, Any]:
        """
        - Method: POST
        - URL: https://career.habr.com/api/frontend/vacancies/1000125310/responses
        - RESPONSE:
        {
            "response": {
                "id": 2117371,
                "email": null,
                "message": null,
                "publishedAt": "25 октября 2023 в 17:43",
                "messageHtml": null,
                "author": {
                    "title": "Владимир Лысенко",
                    "href": "/x55aah",
                    "avatar": {
                        "src": "https://habrastorage.org/getpro/moikrug/uploads/user/100/026/547/2/avatar/medium_8f53ae217b54d13eef1e9cee3d0487a4.jpg",
                        "alt": "x55aah"
                    },
                    "location": "Луганск",
                    "status": "Готов к удалённой работе",
                    "salary": "От 5000 $",
                    "availability": "Рассмотрю предложения",
                    "specialization": [
                        "Бэкенд разработчик",
                        "Веб-разработчик"
                    ],
                    "qualification": "Старший (Senior)",
                    "age": "39 лет",
                    "experience": "8 лет и 1 месяц",
                    "skills": [
                        {
                            "title": "Git",
                            "href": "/resumes?skills%5B%5D=947"
                        },
                        {
                            "title": "Python",
                            "href": "/resumes?skills%5B%5D=446"
                        },
                        {
                            "title": "Django",
                            "href": "/resumes?skills%5B%5D=1075"
                        },
                        {
                            "title": "Linux",
                            "href": "/resumes?skills%5B%5D=821"
                        },
                        {
                            "title": "Docker",
                            "href": "/resumes?skills%5B%5D=1067"
                        },
                        {
                            "title": "MongoDB",
                            "href": "/resumes?skills%5B%5D=229"
                        },
                        {
                            "title": "RabbitMQ",
                            "href": "/resumes?skills%5B%5D=184"
                        },
                        {
                            "title": "Apache Kafka",
                            "href": "/resumes?skills%5B%5D=1187"
                        },
                        {
                            "title": "AWS",
                            "href": "/resumes?skills%5B%5D=197"
                        },
                        {
                            "title": "PostgreSQL",
                            "href": "/resumes?skills%5B%5D=537"
                        }
                    ],
                    "lastJob": {
                        "position": "Python Software Engeener",
                        "company": {
                            "title": "NDA",
                            "href": null
                        },
                        "duration": "2 года и 8 месяцев"
                    },
                    "education": null,
                    "additionalEducation": [],
                    "conversations": [],
                    "socials": [],
                    "isExpert": false,
                    "moreUniversityCount": 0
                }
            }
        }
        - RESPONSE: {"message":"Необходимо заполнить капчу","error":{"type":"captcha"}}

        :param id_: Vacancy ID
        :return:
        """
        # TODO: captcha
        path = f"frontend/vacancies/{id_}/responses"
        return self.post(path, auth_required=True)

    def revoke_response_to_vacancy(
            self,
            vacancy_id: int,
            response_id: int,
    ) -> dict[str, str]:
        """
        Revoke existing response to vacancy.

        :param vacancy_id: Vacancy ID
        :param response_id: Response ID
        :return: Examples:
            {"status": "success"}
        """
        path = f"frontend/vacancies/{vacancy_id}/responses/{response_id}"
        return self.delete(path, auth_required=True)

    def get_vacancy_responses(self, id_: int) -> dict[str, Any]:
        """

        :param id_: Vacancy ID
        :return:
        """
        path = f"frontend/vacancies/{id_}/responses"
        return self.get(path, auth_required=True)

    def get_vacancy_favorite_responses(self, id_: int) -> dict[str, Any]:
        """

        :param id_: Vacancy ID
        :return:
        """
        path = f"frontend/vacancies/{id_}/responses/favorited"
        return self.get(path, auth_required=True)

    def get_vacancy_archived_responses(self, id_: int) -> dict[str, Any]:
        """

        :param id_: Vacancy ID
        :return:
        """
        path = f"frontend/vacancies/{id_}/responses/archived"
        return self.get(path, auth_required=True)

    # TODO: https://career.habr.com/api/frontend/vacancies/programmist_python
