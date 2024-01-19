from enum import StrEnum, verify, UNIQUE
from typing import Any

from habr.career.utils import Currency, Pagination, QualificationID


@verify(UNIQUE)
class VacanciesSort(StrEnum):
    RELEVANCE = "relevance"      # По соответствию (default)
    DATE = "date"                # По дате размещения
    SALARY_DESC = "salary_desc"  # По убыванию зарплаты
    SALARY_ASC = "salary_asc"    # По возрастанию зарплаты


@verify(UNIQUE)
class VacancyType(StrEnum):
    ALL = "all"            # Все вакансии (default)
    SUITABLE = "suitable"  # Подходящие


@verify(UNIQUE)
class EmploymentType(StrEnum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"


# noinspection PyUnresolvedReferences
class HABRCareerVacanciesMixin:
    """Раздел `Вакансии`"""

    def get_vacancies(
            self,
            search: str | None = None,
            sort: VacanciesSort | None = VacanciesSort.RELEVANCE,
            type_: VacancyType | None = VacancyType.ALL,
            specializations: list[int] | None = None,
            locations: list[str] | None = None,
            skills: list[int] | None = None,
            qualification: QualificationID | None = None,
            employment_type: EmploymentType | None = None,
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
        Get vacancies.

        :param per_page:
        :param page:
        :param search:
        :param currency:
        :param specializations:
        :param locations: List of aliases
        :param skills:
        :param qualification:
        :param employment_type:
        :param salary:
        :param company:
        :param with_salary:
        :param remote:
        :param has_accreditation:
        :param exclude_company:
        :param sort:
        :param type_:
        :return: Examples:
            {
                "list": [
                    {
                        "id": 1000135136,
                        "href": "/vacancies/1000135136",
                        "title": "Сисадмин-космонавт ",
                        "isMarked": False,
                        "remoteWork": True,
                        "salaryQualification": None,
                        "publishedDate": {
                            "date": "2023-12-07T06:21:11+03:00",
                            "title": "7 декабря"
                        },
                        "location": None,
                        "company": {
                            "alias_name": "firstvds",
                            "href": "/companies/firstvds",
                            "title": "FirstVDS",
                            "accredited": True,
                            "logo": {
                                "src": "https://habrastorage.org/getpro/moikrug/uploads/company/100/005/799/5/logo/medium_3fc6883f3939415a77757d65ce124334.jpg"
                            },
                            "rating": None
                        },
                        "employment": "full_time",
                        "salary": {
                            "from": None,
                            "to": 600000,
                            "currency": "rur",
                            "formatted": "до 600 000 ₽"
                        },
                        "divisions": [
                            {
                                "title": "Системный администратор",
                                "href": "/vacancies?s%5B%5D=17"
                            }
                        ],
                        "skills": [
                            {
                                "title": "Администрирование серверов",
                                "href": "/vacancies?rel=nofollow&skills%5B%5D=183"
                            }
                        ],
                        "media": None,
                        "locations": None,
                        "favorite": False,
                        "archived": False,
                        "hidden": False,
                        "can_edit": False,
                        "userVacancyBanHref": "/api/frontend/user_vacancy_bans",
                        "quickResponseHref": "/api/frontend/quick_responses",
                        "reactions": {
                            "items": [
                                {
                                    "name": "arrow",
                                    "title": "arrow",
                                    "hasReacted": False,
                                    "count": 0,
                                    "image": "/images/emoji/1f3af.svg"
                                },
                                ...
                            ],
                            "fallbackHref": None
                        }
                    },
                    ...
                ],
                "meta": {
                    "totalResults": 5,
                    "perPage": 25,
                    "currentPage": 1,
                    "totalPages": 1
                },
                "recommendedQuickVacancies": [
                    {
                        "id": 1000129425,
                        "href": "/vacancies/1000129425",
                        "title": "Senior Python developer (МСК)",
                        "isMarked": False,
                        "remoteWork": False,
                        "salaryQualification": {
                            "title": "Старший (Senior)",
                            "href": "/vacancies?qid=5"
                        },
                        "publishedDate": {
                            "date": "2023-11-13T11:34:15+03:00",
                            "title": "13 ноября"
                        },
                        "location": None,
                        "company": {
                            "alias_name": "itgri",
                            "href": "/companies/itgri",
                            "title": "GRI",
                            "accredited": True,
                            "logo": {
                                "src": "https://habrastorage.org/getpro/moikrug/uploads/company/100/007/449/3/logo/medium_248c05681f15ed423104d245fdd9d341.png"
                            },
                            "rating": None
                        },
                        "employment": None,
                        "salary": {
                            "from": None,
                            "to": None,
                            "currency": None,
                            "formatted": ""
                        },
                        "divisions": [
                            {
                                "title": "Бэкенд разработчик",
                                "href": "/vacancies?s%5B%5D=2"
                            }
                        ],
                        "skills": [
                            {
                                "title": "Git",
                                "href": "/vacancies?rel=nofollow&skills%5B%5D=947"
                            },
                            ...
                        ],
                        "media": None,
                        "locations": [
                            {
                                "title": "Москва",
                                "href": "/vacancies?city_id=678"
                            }
                        ],
                        "favorite": None,
                        "archived": False,
                        "hidden": False,
                        "can_edit": False,
                        "userVacancyBanHref": "/api/frontend/user_vacancy_bans",
                        "quickResponseHref": "/api/frontend/quick_responses",
                        "recommendationAccuracyPercent": 65
                    },
                    ...
                ]
            }
        """
        params = {
            "sort": sort,
            "type": type_,
            "currency": currency.upper(),
            "per_page": per_page,
            "page": page,
            "q": search,
            "s[]": specializations,
            "skills[]": skills,
            "qid": qualification,
            "salary": salary,
            "company": company,
            "with_salary": with_salary,
            "remote": remote,
            "has_accreditation": has_accreditation,
            "exclude_company": exclude_company,
            "locations[]": locations,
            "employment_type": employment_type,
        }
        return self.get(
            "frontend/vacancies",
            params=params,
            params_options={
                "bool_as_str": True,
            },
        )

    def get_vacancy(self, id_: int) -> dict[str, Any]:
        """
        Get vacancy details.

        :param id_: Vacancy ID
        :return: Examples:
            {
                "placeholder": {
                    "title": "Авторизуйтесь",
                    "description": "Откликаться на вакансии могут только зарегистрированные пользователи.",
                    "actions": [
                        {
                            "title": "Войдите",
                            "href": "https://career.habr.com/users/auth/tmid",
                            "appearance": "primary",
                            "attrs": {
                                "rel": "nofollow"
                            }
                        },
                        {
                            "title": "Зарегистрируйтесь",
                            "href": "https://career.habr.com/users/auth/tmid/register?ae=vr",
                            "appearance": "primary",
                            "attrs": {
                                "rel": "nofollow"
                            }
                        }
                    ]
                },
                "createResponse": None,
                "responses": None,
                "currencies": [
                    {
                        "title": "₽",
                        "value": "rur"
                    },
                    {
                        "title": "$",
                        "value": "usd"
                    },
                    {
                        "title": "€",
                        "value": "eur"
                    },
                    {
                        "title": "₴",
                        "value": "uah"
                    },
                    {
                        "title": "₸",
                        "value": "kzt"
                    }
                ],
                "favorite": False,
                "vacancy": {
                    "id": 1000135136,
                    "href": "/vacancies/1000135136",
                    "title": "Сисадмин-космонавт ",
                    "isMarked": False,
                    "remoteWork": True,
                    "salaryQualification": None,
                    "publishedDate": {
                        "date": "2023-12-07T06:21:11+03:00",
                        "title": "7 декабря"
                    },
                    "location": None,
                    "company": {
                        "alias_name": "firstvds",
                        "href": "/companies/firstvds",
                        "title": "FirstVDS",
                        "accredited": True,
                        "logo": {
                            "src": "https://habrastorage.org/getpro/moikrug/uploads/company/100/005/799/5/logo/medium_3fc6883f3939415a77757d65ce124334.jpg"
                        },
                        "rating": None
                    },
                    "employment": "full_time",
                    "salary": {
                        "from": None,
                        "to": 600000,
                        "currency": "rur",
                        "formatted": "до 600 000 ₽"
                    },
                    "divisions": [
                        {
                            "title": "Системный администратор",
                            "href": "/vacancies?s%5B%5D=17"
                        }
                    ],
                    "skills": [
                        {
                            "title": "Администрирование серверов",
                            "href": "/vacancies?rel=nofollow&skills%5B%5D=183"
                        }
                    ],
                    "media": None,
                    "locations": None,
                    "favorite": False,
                    "archived": False,
                    "hidden": False,
                    "can_edit": False,
                    "userVacancyBanHref": "/api/frontend/user_vacancy_bans",
                    "quickResponseHref": "/api/frontend/quick_responses",
                    "description": "<p><strong>Условия:</strong><br></p>\n<ul><li>График работы: с 10 до 20 по мск. Ношение скафандра — 24 часа в сутки.</li><li>Зарплата от 600 000 рублей в месяц.</li><li>Молодой и дружный коллектив.</li><li>В офисе пряничные берега, кофейные реки, обеды, завтраки и вообще можно оттуда не выходить.</li><li>Спортзал для поддержания космической формы. По средам — фрукты в тюбиках для поддержания витаминного баланса.</li><li>Отсутствие стрессов. Если любишь свою работу — всё в радость!</li></ul>",
                    "humanCityNames": "",
                    "shortGeo": "",
                    "employmentType": "Полный рабочий день",
                    "bonuses": "",
                    "instructions": "",
                    "bannerDescription": " Условия:  График работы: с 10 до 20 по мск. Ношение скафандра — 24 часа в сутки. Зарплата от 600 000 рублей в месяц. Молодой и дружный коллектив. В офисе пряничные берега, кофейные реки, обеды, завтраки и вообще можно оттуда не выходить. Спортзал для поддержания космической формы. По средам — фрукты в тюбиках для поддержания витаминного баланса. Отсутствие стрессов. Если любишь свою работу — в...",
                    "team": "<p><strong>В детстве мечтали стать космонавтом? Это ваш шанс!</strong></p>\n<p>Хостинг-компании FirstVDS срочно нужен новый космонавт. Если у вас возник вопрос «Куда делся старый?» — вы не одиноки, мы сами хотели бы это знать. Наш самый ценный сотрудник пропал во время празднования дня рождения компании, и пока ещё его не нашли.</p>\n<p><strong>Именно поэтому вы видите эту вакансию. </strong></p>\n<p>Нам не важно, сколько вам лет и какого вы пола — главное, чтобы вы откликались на имя Джон и были готовы носить космический скафандр 24/7. В идеале — вы должны настолько любить ходить в скафандре, чтобы делать это даже бесплатно.   <br><br></p>\n\n",
                    "candidate": "<p><strong>Требования:</strong></p>\n<ul><li>Устойчивость к перегрузкам. Во всех смыслах.</li><li>Наличие справки об отсутствии астрофобии, кометофобии, метеорофобии и любых других фобий, связанных с космосом. </li><li>Улыбчивость. Хоть этого и не будет видно под скафандром, но мы-то будем знать!</li></ul>\n<p><strong>Обязанности:</strong><br></p>\n<ul><li>Вызывать расположение у аудитории. Джона любят все без исключения и вам придётся максимально поддержать его образ.</li><li>Активно взаимодействовать с клиентами компании: махать рукой, писать приветствия в чатах, здороваться на улице.</li><li>Фотографироваться для рекламных кампаний, а также быть 2D-моделью и вдохновением для наших иллюстраторов.</li><li>Вести аккаунты на Хабре и VC. Отвечать на комментарии под статьями.</li><li>Ухаживать за корпоративным котом: кормить, мыть космо-лоток, выслушивать жалобы.</li><li>Напоминать клиентам про важность создания бэкапов.</li><li>Джон — наш самый ценный сотрудник. И пока мы поймём, сколько человек нужно, чтобы его заменить — вам придётся создавать видимость бурной деятельности.</li></ul>\n<p><strong>+ Будет плюсом</strong><br></p>\n<p>+ Знание наизусть текста песни «Трава у дома», группы «Земляне»</p>\n<p>+ Навыки в посадке картошки на марсианской земле</p>\n<p>+ Владение клингонским языком на уровне не ниже 'Itlh</p>\n<p>+ Способность ориентироваться на местности в условиях невесомости</p>\n<p>+ Изучение профильной литературы: Булычёв, Хайнлайн, Азимов и Уэллс</p>"
                },
                "company": {
                    "name": "FirstVDS",
                    "url": {
                        "text": "firstvds.ru",
                        "href": "http://firstvds.ru"
                    },
                    "href": "/companies/firstvds",
                    "logo": "https://habrastorage.org/getpro/moikrug/uploads/company/100/005/799/5/logo/medium_3fc6883f3939415a77757d65ce124334.jpg",
                    "description": "Размещаем сайты клиентов на виртуальных и выделенных серверах в дата-центре в Москве",
                    "habrahabr": "translation missing: ru.companies.shared.sidebar.sidebar_about.habrahabr_hint",
                    "rating": None,
                    "vacancies": {
                        "active": 1,
                        "inactive": 13,
                        "href": "/companies/firstvds/vacancies",
                        "list": []
                    }
                },
                "similar": [
                    {
                        "href": "/vacancies/1000135019",
                        "title": "Системный администратора",
                        "city": {
                            "href": "/vacancies?city_id=679",
                            "title": "Санкт-Петербург"
                        },
                        "salary": "От 70 000 до 80 000 ₽",
                        "company": {
                            "name": "Виталфарм",
                            "href": "/companies/vitalfarm",
                            "logo": "https://habrastorage.org/getpro/moikrug/uploads/company/100/008/688/2/logo/medium_43d9baa5497bedbeaca4eeb42239607f.png"
                        }
                    },
                    ...
                ],
                "landingLinks": []
            }
        """
        # TODO: API endpoint not discovered yet
        return self.get(f"vacancies/{id_}", ssr=True)

    # def add_vacancy_to_favorites(self, id_: int) -> dict[str, Any]:
    #     """
    #     Add vacancy to favorites list.
    #
    #     :param id_: Vacancy ID
    #     :return: Examples:
    #         {"favorite": True}
    #     """
    #     path = f"frontend_v1/vacancies/{id_}/favorite"
    #     return self.post(path, auth_required=True)

    def add_vacancy_to_favorites(self, id_: int) -> dict[str, Any]:
        """
        Add vacancy to favorites list.

        :param id_: Vacancy ID
        :return: Examples:
            {"favorite": True}
        """
        path = f"frontend/vacancies/{id_}/favorite"
        return self.post(path, auth_required=True)

    # def remove_vacancy_from_favorites(self, id_: int) -> dict[str, Any]:
    #     """
    #     Remove vacancy from favorites list.
    #
    #     :param id_: Vacancy ID
    #     :return: Examples:
    #         {"favorite": False}
    #     """
    #     path = f"frontend_v1/vacancies/{id_}/unfavorite"
    #     return self.post(path, auth_required=True)

    def remove_vacancy_from_favorites(self, id_: int) -> dict[str, Any]:
        """
        Remove vacancy from favorites list.

        :param id_: Vacancy ID
        :return: Examples:
            {"favorite": False}
        """
        path = f"frontend/vacancies/{id_}/favorite"
        return self.delete(path, auth_required=True)

    def give_reactions_to_vacancy(
            self,
            id_: int,
            reactions: list[str],
    ) -> dict[str, Any]:
        """
        Give reactions to vacancy.

        :param id_: Vacancy ID
        :param reactions: Reactions aliases
        :return: Examples:
            {"status": "ok"}
        """
        params = {"reactions[]": reactions}
        path = f"frontend/vacancies/{id_}/reactions"
        return self.post(path, auth_required=True, params=params)

    def respond_to_vacancy(self, id_: int) -> dict[str, Any]:
        """
        Respond to vacancy.

        :param id_: Vacancy ID
        :return: Examples:
            {
                "response": {
                    "id": 2117371,
                    "email": None,
                    "message": None,
                    "publishedAt": "25 октября 2023 в 17:43",
                    "messageHtml": None,
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
                            ...
                        ],
                        "lastJob": {
                            "position": "Python Software Engeener",
                            "company": {
                                "title": "NDA",
                                "href": None
                            },
                            "duration": "2 года и 8 месяцев"
                        },
                        "education": None,
                        "additionalEducation": [],
                        "conversations": [],
                        "socials": [],
                        "isExpert": False,
                        "moreUniversityCount": 0
                    }
                }
            },
            {
                "message": "Необходимо заполнить капчу",
                "error": {"type": "captcha"}
            }
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

    def update_response_to_vacancy(
            self,
            vacancy_id: int,
            response_id: int,
            body: str,
    ) -> dict[str, Any]:
        """
        Update existing response to vacancy.

        :param vacancy_id: Vacancy ID
        :param response_id: Response ID
        :param body: Text message
        :return: Examples:
            {
                "response": {
                    "id": 2212628,
                    "email": None,
                    "message": "test",
                    "publishedAt": " 7 декабря 2023 в 12:28",
                    "messageHtml": "<p>test</p>",
                    "isQuick": False,
                    "vacancyRecommendationAccuracyPercent": null,
                    "canUpdate": True,
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
                        "experience": "8 лет и 4 месяца",
                        "skills": [
                            {
                                "title": "Git",
                                "href": "/resumes?skills%5B%5D=947"
                            },
                            ...
                        ],
                        "lastJob": {
                            "position": "Python Software Engeener",
                            "company": {
                                "title": "NDA",
                                "href": None
                            },
                            "duration": "2 года и 10 месяцев"
                        },
                        "education": None,
                        "additionalEducation": [],
                        "conversations": [],
                        "socials": [],
                        "isExpert": False,
                        "moreUniversityCount": 0,
                        "companiesCount": "3 компании",
                        "companiesHistory": [
                            {
                                "companyName": "NDA",
                                "experience": "2 года и 10 месяцев (по настоящее время)"
                            },
                            ...
                        ]
                    }
                }
            }
        """
        path = f"frontend/vacancies/{vacancy_id}/responses/{response_id}"
        return self.patch(
            path,
            json={"body": body},
            auth_required=True,
        )

    def get_vacancy_responses(self, id_: int) -> dict[str, Any]:
        """
        Get responses to vacancy.

        :param id_: Vacancy ID
        :return: Examples:
            {
                "list": [
                    {
                        "id": 2212628,
                        "publishedAt": " 7 декабря 2023 в 12:28",
                        "message": None,
                        "messageHtml": "<p></p>",
                        "author": {
                            "id": "x55aah",
                            "title": "Владимир Лысенко",
                            "href": "/x55aah?source=response&source_id=2212628",
                            "avatar": {
                                "src": "https://habrastorage.org/getpro/moikrug/uploads/user/100/026/547/2/avatar/medium_8f53ae217b54d13eef1e9cee3d0487a4.jpg",
                                "alt": "x55aah"
                            },
                            "moreUniversityCount": 0,
                            "location": "Луганск",
                            "status": "Готов к удалённой работе",
                            "salary": "5000 $",
                            "availability": "Рассмотрю предложения",
                            "skills": [
                                {
                                    "title": "Git",
                                    "href": "/resumes?q=Git"
                                },
                                ...
                            ],
                            "qualification": "Старший (Senior)",
                            "age": "39 лет",
                            "experience": "8 лет и 4 месяца",
                            "companiesCount": "3 компании",
                            "companiesHistory": [
                                {
                                    "companyName": "NDA",
                                    "experience": "2 года и 10 месяцев (по настоящее время)"
                                },
                                ...
                            ],
                            "isExpert": False,
                            "lastJob": {
                                "position": "Python Software Engeener",
                                "company": {
                                    "title": "NDA",
                                    "href": None
                                },
                                "duration": "2 года и 10 месяцев"
                            },
                            "education": None,
                            "additionalEducation": [],
                            "conversations": [],
                            "socials": []
                        },
                        "favorite": False,
                        "archived": False,
                        "hasAnalytics": True,
                        "isQuick": False,
                        "vacancyRecommendationAccuracyPercent": None
                    }
                ],
                "meta": {
                    "totalResults": 1,
                    "perPage": 30,
                    "currentPage": 1,
                    "totalPages": 1
                }
            }
        """
        path = f"frontend/vacancies/{id_}/responses"
        return self.get(path, auth_required=True)

    def get_vacancy_favorite_responses(self, id_: int) -> dict[str, Any]:
        """
        Get responses to vacancy that was marked as favorite.

        :param id_: Vacancy ID
        :return: Examples:
            {
                "list": [
                    {
                        "id": 498608,
                        "publishedAt": "14 января 2020 в 14:00",
                        "message": None,
                        "messageHtml": "<p></p>",
                        "author": {
                            "id": "x55aah",
                            "title": "Владимир Лысенко",
                            "href": "/x55aah?source=response&source_id=498608",
                            "avatar": {
                                "src": "https://habrastorage.org/getpro/moikrug/uploads/user/100/026/547/2/avatar/medium_8f53ae217b54d13eef1e9cee3d0487a4.jpg",
                                "alt": "x55aah"
                            },
                            "moreUniversityCount": 0,
                            "location": "Луганск",
                            "status": "Готов к удалённой работе",
                            "salary": "5000 $",
                            "availability": "Рассмотрю предложения",
                            "skills": [
                                {
                                    "title": "Git",
                                    "href": "/resumes?q=Git"
                                },
                                ...
                            ],
                            "qualification": "Старший (Senior)",
                            "age": "39 лет",
                            "experience": "8 лет и 4 месяца",
                            "companiesCount": "3 компании",
                            "companiesHistory": [
                                {
                                    "companyName": "NDA",
                                    "experience": "2 года и 10 месяцев (по настоящее время)"
                                },
                                ...
                            ],
                            "isExpert": False,
                            "lastJob": {
                                "position": "Python Software Engeener",
                                "company": {
                                    "title": "NDA",
                                    "href": None
                                },
                                "duration": "2 года и 10 месяцев"
                            },
                            "education": None,
                            "additionalEducation": [],
                            "conversations": [],
                            "socials": []
                        },
                        "favorite": True,
                        "archived": False,
                        "hasAnalytics": True,
                        "isQuick": False,
                        "vacancyRecommendationAccuracyPercent": None
                    }
                ],
                "meta": {
                    "totalResults": 1
                }
            }
        """
        path = f"frontend/vacancies/{id_}/responses/favorited"
        return self.get(path, auth_required=True)

    def get_vacancy_archived_responses(self, id_: int) -> dict[str, Any]:
        """
        Get responses to vacancy that was moved to archive.

        :param id_: Vacancy ID
        :return: Examples:
            {
                "list": [
                    {
                        "id": 1907959,
                        "publishedAt": "20 июля 2023 в 16:30",
                        "message": None,
                        "messageHtml": "<p></p>",
                        "author": {
                            "id": "x55aah",
                            "title": "Владимир Лысенко",
                            "href": "/x55aah?source=response&source_id=1907959",
                            "avatar": {
                                "src": "https://habrastorage.org/getpro/moikrug/uploads/user/100/026/547/2/avatar/medium_8f53ae217b54d13eef1e9cee3d0487a4.jpg",
                                "alt": "x55aah"
                            },
                            "moreUniversityCount": 0,
                            "location": "Луганск",
                            "status": "Готов к удалённой работе",
                            "salary": "5000 $",
                            "availability": "Рассмотрю предложения",
                            "skills": [
                                {
                                    "title": "Git",
                                    "href": "/resumes?q=Git"
                                },
                                ...
                            ],
                            "qualification": "Старший (Senior)",
                            "age": "39 лет",
                            "experience": "8 лет и 4 месяца",
                            "companiesCount": "3 компании",
                            "companiesHistory": [
                                {
                                    "companyName": "NDA",
                                    "experience": "2 года и 10 месяцев (по настоящее время)"
                                },
                                ...
                            ],
                            "isExpert": False,
                            "lastJob": {
                                "position": "Python Software Engeener",
                                "company": {
                                    "title": "NDA",
                                    "href": None
                                },
                                "duration": "2 года и 10 месяцев"
                            },
                            "education": None,
                            "additionalEducation": [],
                            "conversations": [],
                            "socials": []
                        },
                        "favorite": False,
                        "archived": True,
                        "hasAnalytics": False,
                        "isQuick": False,
                        "vacancyRecommendationAccuracyPercent": None
                    }
                ],
                "meta": {
                    "totalResults": 1
                }
            }
        """
        path = f"frontend/vacancies/{id_}/responses/archived"
        return self.get(path, auth_required=True)

    # TODO: https://career.habr.com/api/frontend/vacancies/programmist_python
    # TODO: https://career.habr.com/api/frontend/user_vacancy_bans
    # TODO: https://career.habr.com/api/frontend/quick_responses
