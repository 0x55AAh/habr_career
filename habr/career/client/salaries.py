from enum import verify, UNIQUE, IntEnum
from typing import Any

from habr.career.utils import QueryParams, bool_to_str, Qualification


@verify(UNIQUE)
class EmploymentType(IntEnum):
    FULL_TIME = 0
    PART_TIME = 1


# noinspection PyUnresolvedReferences
class HABRCareerSalariesMixin:
    """Раздел `Зарплаты`"""

    def my_salary(self) -> dict[str, Any]:
        """
        Get my salary.

        :return: Examples:
            {
                "periods": [
                    {"key": 221, "value": null, "title": "1-е пол. 2022"},
                    {"key": 222, "value": null, "title": "2-е пол. 2022"},
                    {"key": 231, "value": null, "title": "1-е пол. 2023"},
                    {"key": 232, "value": 329800, "title": "2-е пол. 2023"}
                ],
                "lastSalary": {
                    "value": 329800,
                    "qualification": "Senior",
                    "specialization": "backend"
                },
                "currentPeriod": {
                    "value": 329800,
                    "qualification": "Senior",
                    "specialization": "backend"
                },
                "feedbackIsActive": True,
                "leftFeedback": False,
                "hasServices": False
            }
        """
        path = "frontend_v1/salary_calculator/my_salary"
        return self.get(path, auth_required=True)

    def get_suitable_vacancies(
            self,
            specializations: list[str] | None = None,
            qualification: Qualification | None = None,
            remote: bool | None = None,
            employment_type: EmploymentType | None = None,
            company: str | None = None,
            skills: list[str] | None = None,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get suitable vacancies.

        :param specializations: Specializations aliases list
        :param qualification:
        :param remote:
        :param employment_type:
        :param company:
        :param skills:
        :param locations: Locations aliases list
        :param exclude_locations:
        :return: Examples:
            {
                "href": "/vacancies?sort=salary_desc&type=all&with_salary=true",
                "vacancies": [
                    {
                        "id": 412670009,
                        "title": "Ruby Backend Engineer к Злым марсианам (релокация или удаленно)",
                        "specializations": [
                            {
                                "title": "Бэкенд разработчик",
                                "translation": "Backend Developer"
                            }
                        ],
                        "published_at": "2023-12-01T12:15:18.353+03:00",
                        "url": "https://career.habr.com/vacancies/412670009",
                        "qualification": None,
                        "company": {
                            "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/company/300/735/779/logo/9e13486e94ac84f1c8a87e169e49ed2c.png",
                            "title": "Evil Martians",
                            "alias": "evilmartians",
                            "responses": 0,
                            "accredited": True,
                            "rating": "4.33"
                        },
                        "employment_type": "Полный рабочий день",
                        "salary": "от 6 000 до 9 000 $",
                        "remote": True,
                        "skills": [
                            {
                                "alias": "ruby",
                                "title": "Ruby"
                            },
                            {
                                "alias": "ruby-on-rails",
                                "title": "Ruby on Rails"
                            },
                            {
                                "alias": "git",
                                "title": "Git"
                            },
                            {
                                "alias": "postgresql",
                                "title": "PostgreSQL"
                            },
                            {
                                "alias": "golang",
                                "title": "Golang"
                            },
                            {
                                "alias": "docker",
                                "title": "Docker"
                            }
                        ],
                        "locations": [],
                        "favorite": False
                    },
                    ...
                ]
            }
        """
        params = QueryParams({
            "qualification": qualification,  # TODO: Can be `All`
            "spec_aliases[]": specializations,
            "remote": bool_to_str(remote),
            "employment_type": employment_type,
            "company_alias": company,
            "skills[]": skills,
            "locations[]": locations,
            "exclude_locations": exclude_locations,
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/suitable_vacancies?{query}"
        return self.get(path, auth_required=True, key="vacancies")

    def get_suitable_courses(
            self,
            specializations: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get suitable courses.

        :param specializations: Specializations aliases list
        :return: Examples:
            {
                "href": "/courses",
                "courses": [
                    {
                        "title": "Продуктовый маркетинг и аналитика",
                        "alias": "2613-produktovyy-marketing-i-analitika",
                        "startDate": "2024-09-01T00:00:00.000+03:00",
                        "startKind": "date",
                        "installment": True,
                        "scoresCount": 0,
                        "averageRating": None,
                        "educationPlatform": {
                            "title": "Нетология",
                            "alias": "10-netologiya",
                            "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/010/logo/003c92ceabc8f920e17b38b8020063f6.png",
                            "isPartner": True
                        },
                        "specialization": {
                            "title": "Менеджер по маркетингу",
                            "alias": "marketing_manager",
                            "translation": "Marketing Manager",
                            "landingPath": "marketing/marketing_manager"
                        },
                        "currentQualification": None,
                        "resultQualification": None,
                        "duration": {
                            "value": 22,
                            "unit": "month"
                        },
                        "skills": [
                            {
                                "title": "Продуктовый маркетинг",
                                "alias": "produktovyy-marketing"
                            },
                            {
                                "title": "Стратегический маркетинг",
                                "alias": "strategicheskiy-marketing"
                            },
                            {
                                "title": "Математическое моделирование",
                                "alias": "matematicheskoe-modelirovanie"
                            },
                            {
                                "title": "Управление проектами",
                                "alias": "upravlenie-proektami"
                            },
                            {
                                "title": "Бизнес аналитика",
                                "alias": "biznes-analitika"
                            },
                            {
                                "title": "Маркетинговые исследования",
                                "alias": "marketingovye-issledovaniya"
                            }
                        ],
                        "city": None,
                        "price": {
                            "value": 175000,
                            "unit": "rur",
                            "discount": 0,
                            "oldValue": None
                        },
                        "labels": [
                            {
                                "type": "string",
                                "kind": "hasCert"
                            },
                            {
                                "type": "string",
                                "kind": "isOnline"
                            }
                        ],
                        "courseAuthor": None,
                        "url": "https://thevospad.com/g/xtem2fvy7p3ea34e371f69bd3583e1/?erid=LatgBt89N&f_id=25070&ulp=https%3A%2F%2Fnetology.ru%2Fprograms%2Fdigital_marketing_bhe"
                    },
                ]
            }
        """
        # TODO: not sure this is all parameters
        params = QueryParams({
            "spec_aliases[]": specializations,
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/suitable_courses?{query}"
        return self.get(path, auth_required=True, key="courses")

    def get_salary_reports(self) -> list[dict[str, str]]:
        """
        Get salary reports.

        :return: Examples:
            {
                "href": "/journal/salary",
                "posts": [
                    {
                        "publishedAt": "2023-07-05T13:23:08.000+03:00",
                        "preview": "https://habrastorage.org/getpro/habr/upload_files/cd0/f98/9b4/cd0f989b45f90803f55b824b7b939204.png",
                        "href": "https://habr.com/ru/companies/habr_career/articles/746038/",
                        "title": "Зарплатные вилки весной 2023: языки программирования и фреймворки",
                        "tag": "зарплаты в it"
                    },
                    {
                        "publishedAt": "2022-08-04T11:21:10.000+03:00",
                        "preview": "https://habrastorage.org/getpro/habr/upload_files/1f2/13c/ff5/1f213cff52699be7061e11912f6f3d3f.png",
                        "href": "https://habr.com/ru/specials/679698/",
                        "title": "Зарплаты айтишников в первом полугодии 2022: впервые за пять лет средняя зарплата не изменилась",
                        "tag": "зарплаты в it"
                    },
                    {
                        "publishedAt": "2023-07-18T10:00:20.000+03:00",
                        "preview": "https://habrastorage.org/getpro/habr/upload_files/783/acb/641/783acb6412b447e771fbf7a9aced45f5.png",
                        "href": "https://habr.com/ru/specials/748058/",
                        "title": "Зарплаты IT-специалистов в первом полугодии 2023: +10% за счет регионов",
                        "tag": "зарплаты в it"
                    }
                ]
            }
        """
        path = "frontend_v1/salary_calculator/salary_reports"
        return self.get(path, key="posts")

    def get_salary_general_graph(
            self,
            specializations: list[str] | None = None,
            remote: bool | None = None,
            employment_type: EmploymentType | None = None,
            company: str | None = None,
            skills: list[str] | None = None,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
    ) -> dict[str, Any]:
        """
        Get salary general graph.

        :param specializations: Specializations aliases list
        :param remote:
        :param employment_type:
        :param company:
        :param skills:
        :param locations: Locations aliases list
        :param exclude_locations:
        :return: Examples:
            {
                "groups": [
                    {
                        "name": "All",
                        "min": 47500,
                        "max": 376000,
                        "p25": 77500,
                        "p75": 255833,
                        "median": 151666,
                        "total": 30905,
                        "title": "По всем IT-специалистам",
                        "specTitle": None,
                        "seoTitle": None,
                        "salary": {
                            "total": 151666,
                            "value": 135000,
                            "bonus": 16666,
                            "bonusPercent": 39
                        }
                    },
                    {
                        "name": "Middle",
                        "min": 72500,
                        "max": 281966,
                        "p25": 108333,
                        "p75": 227927,
                        "median": 166666,
                        "total": 11101,
                        "title": "По Middle IT-специалистам",
                        "specTitle": None,
                        "seoTitle": [
                            "Middle"
                        ],
                        "salary": {
                            "total": 166666,
                            "value": 150000,
                            "bonus": 16666,
                            "bonusPercent": 40
                        }
                    },
                    {
                        "name": "Intern",
                        "min": 20833,
                        "max": 100000,
                        "p25": 31166,
                        "p75": 68333,
                        "median": 44042,
                        "total": 2222,
                        "title": "По Intern IT-специалистам",
                        "specTitle": None,
                        "seoTitle": [
                            "Intern"
                        ],
                        "salary": {
                            "total": 44042,
                            "value": 40000,
                            "bonus": 4042,
                            "bonusPercent": 25
                        }
                    },
                    {
                        "name": "Senior",
                        "min": 137750,
                        "max": 459000,
                        "p25": 207000,
                        "p75": 360000,
                        "median": 279166,
                        "total": 5247,
                        "title": "По Senior IT-специалистам",
                        "specTitle": None,
                        "seoTitle": [
                            "Senior"
                        ],
                        "salary": {
                            "total": 279166,
                            "value": 250000,
                            "bonus": 29166,
                            "bonusPercent": 46
                        }
                    },
                    {
                        "name": "Junior",
                        "min": 35925,
                        "max": 145000,
                        "p25": 52916,
                        "p75": 103333,
                        "median": 72500,
                        "total": 5800,
                        "title": "По Junior IT-специалистам",
                        "specTitle": None,
                        "seoTitle": [
                            "Junior"
                        ],
                        "salary": {
                            "total": 72500,
                            "value": 65000,
                            "bonus": 7500,
                            "bonusPercent": 28
                        }
                    },
                    {
                        "name": "Lead",
                        "min": 158333,
                        "max": 595000,
                        "p25": 230833,
                        "p75": 458499,
                        "median": 341666,
                        "total": 3367,
                        "title": "По Lead IT-специалистам",
                        "specTitle": None,
                        "seoTitle": [
                            "Lead"
                        ],
                        "salary": {
                            "total": 341666,
                            "value": 300000,
                            "bonus": 41666,
                            "bonusPercent": 54
                        }
                    }
                ]
            }
        """
        params = QueryParams({
            "spec_aliases[]": specializations,
            "remote": bool_to_str(remote),
            "employment_type": employment_type,
            "company_alias": company,
            "skills[]": skills,
            "locations[]": locations,
            "exclude_locations": exclude_locations,
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/general_graph?{query}"
        return self.get(path, auth_required=True)

    def get_salary_dynamic_graph(
            self,
            qualification: Qualification | None = None,
            specializations: list[str] | None = None,
            remote: bool | None = None,
            employment_type: EmploymentType | None = None,
            company: str | None = None,
            skills: list[str] | None = None,
            locations: list[str] | None = None,
            exclude_locations: bool | None = None,
    ) -> dict[str, Any]:
        """
        Get salary dynamic graph.

        :param qualification:
        :param specializations: Specializations aliases list
        :param remote:
        :param employment_type:
        :param company:
        :param skills:
        :param locations: Locations aliases list
        :param exclude_locations:
        :return: Examples:
            {
                "graphs_data": {
                    "title": "Средняя зарплата по рынку",
                    "periods": [
                        {
                            "key": 221,
                            "value": 163333,
                            "title": "1-е пол. 2022"
                        },
                        {
                            "key": 222,
                            "value": 130500,
                            "title": "2-е пол. 2022"
                        },
                        {
                            "key": 231,
                            "value": 152083.0,
                            "title": "1-е пол. 2023"
                        },
                        {
                            "key": 232,
                            "value": 75416.5,
                            "title": "2-е пол. 2023"
                        }
                    ]
                }
            }
        """
        params = QueryParams({
            "qualification": qualification,
            "spec_aliases[]": specializations,
            "remote": bool_to_str(remote),
            "employment_type": employment_type,
            "company_alias": company,
            "skills[]": skills,
            "locations[]": locations,
            "exclude_locations": exclude_locations,
        })
        query = params.query(doseq=True)
        path = f"frontend_v1/salary_calculator/dynamic_graph?{query}"
        return self.get(path, auth_required=True)

    def get_salary_chart(
            self,
            specialization: str | None = None,
    ) -> list[dict[str, str]]:
        """
        Get salary chart.

        :param specialization: Specialization alias
        :return: Examples:
            {
                "title": "бэкенд разработчика",
                "values": [
                    {
                        "title": "Intern",
                        "salary": {
                            "value": 40000,
                            "unit": "rur"
                        },
                        "isUserQualification": False
                    },
                    {
                        "title": "Junior",
                        "salary": {
                            "value": 80000,
                            "unit": "rur"
                        },
                        "isUserQualification": False
                    },
                    {
                        "title": "Middle",
                        "salary": {
                            "value": 180000,
                            "unit": "rur"
                        },
                        "isUserQualification": False
                    },
                    {
                        "title": "Senior",
                        "salary": {
                            "value": 270000,
                            "unit": "rur"
                        },
                        "isUserQualification": True
                    },
                    {
                        "title": "Lead",
                        "salary": {
                            "value": 320000,
                            "unit": "rur"
                        },
                        "isUserQualification": False
                    }
                ],
                "diagramHref": "/salaries?spec_aliases%5B%5D=backend"
            }
        """
        params = QueryParams({"specialization": specialization})
        path = f"frontend_v1/salary_chart?{params.query()}"
        return self.get(path, auth_required=True)

    def get_locations_suggestions(self, search: str) -> list[dict[str, str]]:
        """
        Get locations.

        :param search: Search query
        :return: Examples:
            {
                "locations": [
                    {
                        "title": "Москва",
                        "subtitle": "Россия, Москва и Московская область",
                        "alias": "c_678"
                    },
                    ...
                ]
            }
        """
        path = f"frontend_v1/suggestions/locations?q={search}"
        return self.get(path, key="locations")

    # def get_locations_suggestions(self, search: str) -> list[dict[str, str]]:
    #     """
    #     Get locations.
    #     When search is empty we get list of our own locations.
    #
    #     :param search: Search query
    #     :return: Examples:
    #         {
    #             "list": [
    #                 {
    #                     "value": "c_678",
    #                     "title": "Москва",
    #                     "subtitle": "Россия, Москва и Московская область"
    #                 },
    #                 ...
    #             ]
    #         }
    #     """
    #     path = f"frontend/suggestions/locations?term={search}"
    #     return self.get(path, key="list")

    def get_companies_suggestions(self, search: str) -> list[dict[str, str]]:
        """
        Get companies.

        :param search: Search query.
        :return: Examples:
            {
                "companies": [
                    {
                        "title": "МТС",
                        "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/company/355/898/672/logo/medium_b8623ca7ce06fcc39ac26ccb7c2bafcb.png",
                        "alias": "mts"
                    },
                    ...
                ]
            }
        """
        path = f"frontend_v1/suggestions/companies?term={search}"
        return self.get(path, key="companies")

    # def get_companies_suggestions(self, search: str) -> list[dict[str, Any]]:
    #     """
    #     Get companies.
    #
    #     :param search: Search query.
    #     :return: Examples:
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
