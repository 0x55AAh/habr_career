from enum import verify, UNIQUE, StrEnum
from typing import Any

from habr.career.utils import Currency


@verify(UNIQUE)
class CareerSortingCriteria(StrEnum):
    LAST_VISITED = "last_visited"  # по дате визита
    RELEVANCE = "relevance"        # по соответствию
    SALARY_DESC = "salary_desc"    # по убыванию зарплаты
    SALARY_ASC = "salary_asc"      # по возрастанию зарплаты


@verify(UNIQUE)
class CareerActivityPeriod(StrEnum):
    TWO_YEARS = "two_years"        # За 2 года
    YEAR = "year"                  # За 1 год
    THREE_MONTHS = "three_months"  # За 3 месяца


@verify(UNIQUE)
class CareerWorkState(StrEnum):
    NOT_SEARCH = "not_search"  # Не ищу работу
    SEARCH = "search"          # Ищу работу
    READY = "ready"            # Рассмотрю предложения


@verify(UNIQUE)
class CareerSearchField(StrEnum):
    FIO = "fio"                          # в имени
    RESUME_HEADLINE = "resume_headline"  # в специализации
    EXPERIENCES = "experiences"          # в должностях
    SKILLS = "skills"                    # в навыках профиля
    SOCIAL_TAGS = "social_tags"          # в навыках сообществ


# noinspection PyUnresolvedReferences
class HABRCareerResumesMixin:
    """Раздел `Специалисты`"""

    def get_resumes(
            self,
            search: str | None = None,
            search_fields: list[CareerSearchField] | None = None,
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
        Get resumes.

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
        :param with_educations: С высшим образованием
        :param with_extra_educations: С дополнительным образованием
        :param with_experiences: С опытом работы
        :param with_salary: Указана зарплата
        :param with_social_ratings: Участник ИТ-сообществ
        :return: Examples:
            {
                "list": [
                    {
                        "id": "elenatyurinait",
                        "title": "Елена Тюрина",
                        "href": "/elenatyurinait",
                        "conversationHref": "/elenatyurinait/connect",
                        "avatar": {
                            "src": "https://habrastorage.org/getpro/moikrug/uploads/user/100/052/265/2/avatar/medium_676c50ea9b78a738009bc2940ccf2822.jpg",
                            "src2x": "https://habrastorage.org/getpro/moikrug/uploads/user/100/052/265/2/avatar/medium_676c50ea9b78a738009bc2940ccf2822.jpg"
                        },
                        "lastVisited": {
                            "title": "сегодня",
                            "date": "2023-12-03T18:51:01+03:00"
                        },
                        "specialization": "",
                        "qualification": {
                            "title": "Middle",
                            "value": 4
                        },
                        "salary": {
                            "title": "От 150 000 ₽",
                            "value": 150000,
                            "currency": "rur"
                        },
                        "availability": {
                            "title": "Не ищу работу",
                            "value": "unavailable"
                        },
                        "location": {
                            "title": "Саратов",
                            "name": "",
                            "href": "/resumes?city_ids%5B%5D=729",
                            "value": 729
                        },
                        "remoteWork": True,
                        "relocation": False,
                        "skills": [
                            {
                                "title": "Подбор специалистов",
                                "href": "/resumes?skills%5B%5D=352",
                                "value": 352
                            },
                            {
                                "title": "Проведение интервью",
                                "href": "/resumes?skills%5B%5D=71",
                                "value": 71
                            },
                            {
                                "title": "Работа в команде",
                                "href": "/resumes?skills%5B%5D=638",
                                "value": 638
                            },
                            {
                                "title": "Консультирование",
                                "href": "/resumes?skills%5B%5D=884",
                                "value": 884
                            },
                            {
                                "title": "Подбор руководителей",
                                "href": "/resumes?skills%5B%5D=882",
                                "value": 882
                            },
                            {
                                "title": "Консультирование по подбору персонала",
                                "href": "/resumes?skills%5B%5D=790",
                                "value": 790
                            },
                            {
                                "title": "Обучение персонала",
                                "href": "/resumes?skills%5B%5D=518",
                                "value": 518
                            }
                        ],
                        "age": {
                            "title": "35 лет",
                            "value": 35
                        },
                        "experience": {
                            "title": "2 года и 5 месяцев",
                            "value": 29
                        },
                        "lastJob": {
                            "position": "it рекрутер",
                            "company": {
                                "title": "Selecty",
                                "accredited": false,
                                "href": "/companies/selecty"
                            },
                            "duration": {
                                "title": "2 года и 4 месяца",
                                "value": 28
                            }
                        },
                        "education": {
                            "university": {
                                "title": "СГУ им. Н.Г. Чернышевского",
                                "href": "/universities/1718"
                            },
                            "faculty": "Механико-математический",
                            "duration": {
                                "title": "4 года и 9 месяцев",
                                "value": 57
                            }
                        },
                        "additionalEducation": [],
                        "communities": [],
                        "coworkers": [],
                        "specializations": [
                            {
                                "title": "Менеджер по персоналу"
                            },
                            {
                                "title": "Менеджер по найму"
                            }
                        ],
                        "gender": 1,
                        "isExpert": False,
                        "moreUniversityCount": 0
                    },
                ],
                "meta": {
                    "totalResults": 494923,
                    "perPage": 25,
                    "currentPage": 1,
                    "totalPages": 19797
                },
                "limitedAccess": {
                    "type": "noCompany",
                    "newCompanyHref": "https://career.habr.com/companies/new"
                }
            }
        """
        params = {
            "q": search,
            "fields[]": search_fields,
            "s[]": specializations,
            "order": sort,
            "qid": qualification,
            "skills[]": skills,
            "salary": salary,
            "currency": currency.upper(),
            "locations[]": locations,
            "exclude_locations": exclude_locations,
            "company_ids[]": companies,
            "not_companies": not_companies,
            "current_company": current_company,
            "university_ids[]": universities,
            "not_universities": not_universities,
            "edc_ids[]": educations,
            "not_edcs": not_educations,
            "work_state": work_state,
            "relocation": relocation,
            "remote": remote,
            "period": period,
            "with_educations": with_educations,
            "with_add_eds": with_extra_educations,
            "with_experiences": with_experiences,
            "with_salary": with_salary,
            "with_social_ratings": with_social_ratings,
        }
        return self.get(
            "frontend/resumes",
            params=params,
            params_options={
                "bool_as_str": True,
            },
        )

    def get_resumes_data(
            self,
            search: str | None = None,
            search_fields: list[CareerSearchField] | None = None,
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
        :param with_educations: С высшим образованием
        :param with_extra_educations: С дополнительным образованием
        :param with_experiences: С опытом работы
        :param with_salary: Указана зарплата
        :param with_social_ratings: Участник ИТ-сообществ
        :return: Examples:
            {
                "isGuest": True,
                "tabs": [
                    {
                        "title": "Хабр Карьера",
                        "href": "/resumes",
                        "active": True
                    },
                    ...
                ],
                "search": {
                    "query": "",
                    "order": "last_visited",
                    "filters": {
                        "qualification": None,
                        "currency": "RUR",
                        "companies": [],
                        "salary": None,
                        "divisions": [],
                        "skills": [],
                        "locations": [],
                        "availability": None,
                        "searchFields": [],
                        "universities": [],
                        "extraEducations": [],
                        "excludeLocation": False,
                        "excludeCompany": False,
                        "excludeUniversity": False,
                        "excludeExtraEducation": False,
                        "isCurrentCompany": False,
                        "relocation": False,
                        "remoteWork": False,
                        "hasHighEducation": False,
                        "hasExtraEducation": False,
                        "hasExperience": False,
                        "hasSalary": False,
                        "hasSocialRatings": False,
                        "hasVisitedLastYear": False,
                        "activityPeriod": None,
                        "s": []
                    },
                    "groups": [
                        ...
                    ],
                    "savedFilters": []
                },
                "options": {
                    "order": [
                        {
                            "value": "relevance",
                            "title": "По соответствию"
                        },
                        ...
                    ],
                    "searchFields": [
                        {
                            "title": "в имени",
                            "value": "fio"
                        },
                        ...
                    ],
                    "divisions": [
                        {
                            "value": "backend",
                            "title": "Бэкенд"
                        },
                        ...
                    ],
                    "qualification": [
                        {
                            "value": None,
                            "title": "Любая"
                        },
                        ...
                    ],
                    "currency": [
                        {
                            "value": "RUR",
                            "title": "₽"
                        },
                        ...
                    ],
                    "availability": [
                        {
                            "title": "Любая",
                            "value": None
                        },
                        ...
                    ],
                    "activityPeriod": [
                        {
                            "title": "Любая",
                            "value": None
                        },
                        ...
                    ],
                    "s": [
                        {
                            "value": 1,
                            "title": "Десктоп разработчик",
                            "parent_id": 1
                        },
                        ...
                    ]
                },
                "filtersData": {
                    "skills": [],
                    "companies": [],
                    "locations": [],
                    "universities": [],
                    "extraEducations": []
                },
                "resumes": {
                    "list": [
                        {
                            "id": "dima-onischuk",
                            "title": "Дима Онищук",
                            "href": "/dima-onischuk",
                            "conversationHref": None,
                            "avatar": {
                                "src": "https://career.habr.com/assets/defaults/avatars/user-4ae9deaab7da70ad824797029541e20765d74e4d1707ec8708d05d2a61eee32b.png",
                                "src2x": "https://career.habr.com/assets/defaults/avatars/user-4ae9deaab7da70ad824797029541e20765d74e4d1707ec8708d05d2a61eee32b.png"
                            },
                            "lastVisited": {
                                "title": "сегодня",
                                "date": "2023-12-03T19:24:01+03:00"
                            },
                            "specialization": "С++ программист",
                            "qualification": {
                                "title": "Middle",
                                "value": 4
                            },
                            "salary": None,
                            "availability": {
                                "title": "Не ищу работу",
                                "value": "unavailable"
                            },
                            "location": {
                                "title": "Санкт-Петербург",
                                "name": "saint-petersburg",
                                "href": "/resumes?city_ids%5B%5D=679",
                                "value": 679
                            },
                            "remoteWork": True,
                            "relocation": True,
                            "skills": [
                                {
                                    "title": "C++",
                                    "href": "/resumes?skills%5B%5D=172",
                                    "value": 172
                                },
                                ...
                            ],
                            "age": {
                                "title": "23 года",
                                "value": 23
                            },
                            "experience": {
                                "title": "3 года и 6 месяцев",
                                "value": 42
                            },
                            "lastJob": {
                                "position": "Разработчик функциональности товарного поиска",
                                "company": {
                                    "title": "Яндекс",
                                    "accredited": False,
                                    "href": "/companies/yandex"
                                },
                                "duration": {
                                    "title": "10 месяцев",
                                    "value": 10
                                }
                            },
                            "education": {
                                "university": {
                                    "title": "НГУ",
                                    "href": "/universities/1691"
                                },
                                "faculty": "Факультет информационных технологий (ФИТ)",
                                "duration": {
                                    "title": "3 года и 9 месяцев",
                                    "value": 45
                                }
                            },
                            "additionalEducation": [],
                            "communities": [],
                            "coworkers": [],
                            "specializations": [
                                {
                                    "title": "Бэкенд разработчик"
                                }
                            ],
                            "gender": 0,
                            "isExpert": False,
                            "moreUniversityCount": 0
                        },
                    ],
                    "meta": {
                        "totalResults": 259411,
                        "perPage": 25,
                        "currentPage": 1,
                        "totalPages": 10377
                    },
                    "limitedAccess": {
                        "type": "guest",
                        "registerHref": "https://career.habr.com/users/auth/tmid/register",
                        "loginHref": "https://career.habr.com/users/auth/tmid"
                    }
                },
                "vacancyBanners": []
            }
        """
        params = {
            "q": search,
            "fields[]": search_fields,
            "s[]": specializations,
            "order": sort,
            "qid": qualification,
            "skills[]": skills,
            "salary": salary,
            "currency": currency.upper(),
            "locations[]": locations,
            "exclude_locations": exclude_locations,
            "company_ids[]": companies,
            "not_companies": not_companies,
            "current_company": current_company,
            "university_ids[]": universities,
            "not_universities": not_universities,
            "edc_ids[]": educations,
            "not_edcs": not_educations,
            "work_state": work_state,
            "relocation": relocation,
            "remote": remote,
            "period": period,
            "with_educations": with_educations,
            "with_add_eds": with_extra_educations,
            "with_experiences": with_experiences,
            "with_salary": with_salary,
            "with_social_ratings": with_social_ratings,
        }
        return self.get(
            "resumes",
            auth_required=True,
            ssr=True,
            params=params,
            params_options={
                "bool_as_str": True,
            },
        )

    def save_careers_filter(
            self,
            search: str | None = None,
            search_fields: list[CareerSearchField] | None = None,
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
        Save filter.

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
        :param with_educations: С высшим образованием
        :param with_extra_educations: С дополнительным образованием
        :param with_experiences: С опытом работы
        :param with_salary: Указана зарплата
        :param with_social_ratings: Участник ИТ-сообществ
        :return: Examples:
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
                            "remoteWork": True,
                            "relocation": True,
                            "hasSalary": True,
                            "hasHighEducation": True,
                            "hasExtraEducation": True,
                            "hasExperience": True,
                            "hasSocialRatings": True,
                            "excludeLocation": True,
                            "excludeCompany": True,
                            "excludeUniversity": True,
                            "excludeExtraEducation": True,
                            "isCurrentCompany": True,
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
        """
        params = {
            "q": search,
            "fields[]": search_fields,
            "s[]": specializations,
            "order": sort,
            "qid": qualification,
            "skills[]": skills,
            "salary": salary,
            "currency": currency.upper(),
            "locations[]": locations,
            "exclude_locations": exclude_locations,
            "company_ids[]": companies,
            "not_companies": not_companies,
            "current_company": current_company,
            "university_ids[]": universities,
            "not_universities": not_universities,
            "edc_ids[]": educations,
            "not_edcs": not_educations,
            "work_state": work_state,
            "relocation": relocation,
            "remote": remote,
            "period": period,
            "with_educations": with_educations,
            "with_add_eds": with_extra_educations,
            "with_experiences": with_experiences,
            "with_salary": with_salary,
            "with_social_ratings": with_social_ratings,
        }
        return self.post(
            "frontend/user_filters/resumes",
            auth_required=True,
            params=params,
            params_options={
                "bool_as_str": True,
            },
        )

    @staticmethod
    def _career_filter_data_to_params(filter_data: dict) -> dict:
        """
        Converts filter data into query params.

        :param filter_data: Expected structure:
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
        :return:
        """
        filters = filter_data["filters"]
        return {
            "q": filter_data.get("query"),
            "order": filter_data.get("order"),

            "fields[]": filters.get("searchFields"),
            "s[]": filters.get("s"),
            "qid": filters.get("qualification"),
            "skills[]": filters.get("skills"),
            "salary": filters.get("salary"),
            "currency": filters.get("currency"),
            "locations[]": filters.get("locations"),
            "exclude_locations": filters.get("excludeLocation"),
            "company_ids[]": filters.get("companies"),
            "not_companies": filters.get("excludeCompany"),
            "not_universities": filters.get("excludeUniversity"),
            "not_edcs": filters.get("excludeExtraEducation"),

            # TODO: Not working, availability is always null
            "work_state": filters.get("availability"),

            "edc_ids[]": filters.get("extraEducations"),
            "university_ids[]": filters.get("universities"),
            "current_company": filters.get("isCurrentCompany"),
            "relocation": filters.get("relocation"),
            "remote": filters.get("remoteWork"),
            "period": filters.get("activityPeriod"),

            "with_educations": filters.get("hasHighEducation"),
            "with_add_eds": filters.get("hasExtraEducation"),
            "with_experiences": filters.get("hasExperience"),
            "with_salary": filters.get("hasSalary"),
            "with_social_ratings": filters.get("hasSocialRatings"),
        }

    def _career_filter_to_params(self, id_: int) -> dict:
        """
        Converts filter into query params.

        :param id_: Filter ID
        :return:
        """
        _filters = {
            f["id"]: f for f
            in self.get_resumes_data()["search"]["savedFilters"]
        }
        filter_data = _filters[id_]
        return self._career_filter_data_to_params(filter_data)

    def apply_career_filter(self, id_: int) -> dict[str, Any]:
        """
        Apply saved filer by filter ID.

        :param id_: Filter ID
        :return:
        """
        params = self._career_filter_to_params(id_)
        return self.get(
            "frontend/resumes",
            params=params,
            params_options={
                "bool_as_str": True,
            },
        )

    def apply_career_filter_data(self, filter_data: dict) -> dict[str, Any]:
        """
        Apply saved filer by filter data.

        :param filter_data:
        :return:
        """
        params = self._career_filter_data_to_params(filter_data)
        return self.get(
            "frontend/resumes",
            params=params,
            params_options={
                "bool_as_str": True,
            },
        )

    def delete_careers_filter(self, id_: int) -> dict[str, str | int]:
        """
        Delete filter.

        :param id_: Filter ID
        :return: Examples:
            {"status": "ok", "id": 71930}
        """
        path = f"frontend/user_filters/resumes/{id_}"
        return self.delete(path, auth_required=True)

    def get_universities_suggestions(
            self,
            search: str,
    ) -> list[dict[str, str | int]]:
        """
        Find universities by text query.
        Util method used in filters.

        :param search: Search query
        :return: Examples:
            {
                "list": [
                    {
                        "value": 1683,
                        "title": "МГУ им. Ломоносова",
                        "subtitle": "Москва, Московский государственный университет имени М.В. Ломоносова"
                    },
                    ...
                ]
            }
        """
        path = "frontend/suggestions/universities"
        return self.get(path, key="list", params={"term": search})

    def get_education_centers_suggestions(
            self,
            search: str,
    ) -> list[dict[str, str | int]]:
        """
        Find education centers by text query.
        Util method used in filters.

        :param search: Search query
        :return: Examples:
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
        path = "frontend/suggestions/education_centers"
        return self.get(path, key="list", params={"term": search})
