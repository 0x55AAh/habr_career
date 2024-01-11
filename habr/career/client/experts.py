from enum import StrEnum, verify, UNIQUE, IntEnum
from typing import Any

from habr.career.utils import QualificationID, Currency


@verify(UNIQUE)
class ExpertsOrder(StrEnum):
    LAST_ACTIVE = "lastActive"  # По дате визита
    RATE_DESC = "rate_desc"     # Цена по убыванию
    RATE_ASC = "rate_asc"       # Цена по возрастанию


@verify(UNIQUE)
class RequestID(IntEnum):
    RQ1 = 1  # Начало карьеры или смена профессии
    RQ2 = 2  # Развитие навыков
    RQ3 = 3  # Оценка
    RQ4 = 4  # Смена работы
    RQ5 = 5  # Карьерный рост
    RQ6 = 6  # Помощь с задачей
    RQ7 = 7  # Поддержка и коучинг
    RQ8 = 8  # Карьера за рубежом


# noinspection PyUnresolvedReferences
class HABRCareerExpertsMixin:
    """Раздел `Эксперты`"""

    def get_experts(
            self,
            search: str | None = None,
            order: str | None = ExpertsOrder.LAST_ACTIVE,
            free_only: bool | None = None,
            free_intro: bool | None = None,
            skills: list[int] | None = None,
            specializations: list[int] | None = None,
            qualification: QualificationID | None = None,
            currency: Currency | None = Currency.RUR,
            rate_from: int | None = None,
            rate_to: int | None = None,
            request: RequestID | None = None,
    ) -> dict[str, Any]:
        """
        Get experts data.

        :param search:
        :param order:
        :param free_only:
        :param free_intro:
        :param skills:
        :param specializations:
        :param qualification:
        :param currency:
        :param rate_from:
        :param rate_to:
        :param request:
        :return: Examples:
            {
                "list": [
                    {
                        "title": "Evgeny Shmakov",
                        "login": "sjs-master",
                        "alias": "sjs-master",
                        "avatar": {
                            "src": "https://habrastorage.org/getpro/moikrug/uploads/user/100/020/228/1/avatar/medium_799bad5a3b514f096e69bbc4a7896cd9.jpg",
                            "src2x": "https://habrastorage.org/getpro/moikrug/uploads/user/100/020/228/1/avatar/medium_799bad5a3b514f096e69bbc4a7896cd9.jpg"
                        },
                        "age": {
                            "title": "34 года",
                            "value": 34
                        },
                        "experience": {
                            "title": "11 лет и 11 месяцев",
                            "value": 143
                        },
                        "lastJob": {
                            "position": "React native developer",
                            "company": {
                                "title": "QVEDO",
                                "accredited": False,
                                "href": "/companies/qvedo"
                            },
                            "duration": {
                                "title": "1 год и 6 месяцев",
                                "value": 18
                            }
                        },
                        "lastVisited": {
                            "title": "сегодня",
                            "date": "2023-11-24T17:24:01+03:00"
                        },
                        "score": {
                            "connections": 1,
                            "averageScore": 5.0,
                            "scoresCount": 1
                        },
                        "qualifications": [
                            {
                                "title": "Стажёр",
                                "position": 0,
                                "href": "/experts?qid=1"
                            },
                            {
                                "title": "Младший",
                                "position": 2,
                                "href": "/experts?qid=3"
                            },
                            {
                                "title": "Средний",
                                "position": 3,
                                "href": "/experts?qid=4"
                            },
                            {
                                "title": "Старший",
                                "position": 4,
                                "href": "/experts?qid=5"
                            },
                            {
                                "title": "Ведущий",
                                "position": 5,
                                "href": "/experts?qid=6"
                            }
                        ],
                        "specializations": [
                            {
                                "title": "Фронтенд разработчик",
                                "href": "/experts?sid%5B%5D=3"
                            },
                            {
                                "title": "Разработчик мобильных приложений",
                                "href": "/experts?sid%5B%5D=5"
                            }
                        ],
                        "skills": [
                            {
                                "title": "Node.js",
                                "href": "/experts?skills%5B%5D=12"
                            },
                            {
                                "title": "CSS",
                                "href": "/experts?skills%5B%5D=32"
                            },
                            {
                                "title": "TypeScript",
                                "href": "/experts?skills%5B%5D=245"
                            },
                            {
                                "title": "JavaScript",
                                "href": "/experts?skills%5B%5D=264"
                            },
                            {
                                "title": "HTML",
                                "href": "/experts?skills%5B%5D=1017"
                            },
                            {
                                "title": "React",
                                "href": "/experts?skills%5B%5D=1070"
                            },
                            {
                                "title": "React Native",
                                "href": "/experts?skills%5B%5D=1104"
                            },
                            {
                                "title": "Redux",
                                "href": "/experts?skills%5B%5D=1106"
                            },
                            {
                                "title": "GraphQL",
                                "href": "/experts?skills%5B%5D=1198"
                            },
                            {
                                "title": "Next.js",
                                "href": "/experts?skills%5B%5D=1313"
                            }
                        ],
                        "requests": [
                            {
                                "title": "Начало карьеры или смена профессии",
                                "items": [
                                    {
                                        "title": "Войти в IT",
                                        "href": "/experts?rid=1"
                                    },
                                    {
                                        "title": "Смена IT-профессии",
                                        "href": "/experts?rid=2"
                                    }
                                ]
                            },
                            {
                                "title": "Развитие навыков",
                                "items": [
                                    {
                                        "title": "Учебный план",
                                        "href": "/experts?rid=3"
                                    },
                                    {
                                        "title": "Развитие навыков",
                                        "href": "/experts?rid=4"
                                    }
                                ]
                            },
                            {
                                "title": "Оценка",
                                "items": [
                                    {
                                        "title": "Оценка навыков",
                                        "href": "/experts?rid=5"
                                    },
                                    {
                                        "title": "Оценка портфолио",
                                        "href": "/experts?rid=6"
                                    },
                                    {
                                        "title": "Проверка резюме",
                                        "href": "/experts?rid=7"
                                    },
                                    {
                                        "title": "Сколько я стою",
                                        "href": "/experts?rid=8"
                                    }
                                ]
                            },
                            {
                                "title": "Смена работы",
                                "items": [
                                    {
                                        "title": "Резюме для российского рынка",
                                        "href": "/experts?rid=9"
                                    },
                                    {
                                        "title": "Резюме для иностранного рынка",
                                        "href": "/experts?rid=10"
                                    },
                                    {
                                        "title": "Подготовка к собеседованию",
                                        "href": "/experts?rid=11"
                                    },
                                    {
                                        "title": "Тестовое собеседование",
                                        "href": "/experts?rid=12"
                                    }
                                ]
                            },
                            {
                                "title": "Карьерный рост",
                                "items": [
                                    {
                                        "title": "Карьерная консультация",
                                        "href": "/experts?rid=13"
                                    },
                                    {
                                        "title": "План карьерного роста",
                                        "href": "/experts?rid=14"
                                    },
                                    {
                                        "title": "Личный бренд",
                                        "href": "/experts?rid=15"
                                    }
                                ]
                            },
                            {
                                "title": "Помощь с задачей",
                                "items": [
                                    {
                                        "title": "Помощь с тестовым заданием",
                                        "href": "/experts?rid=16"
                                    },
                                    {
                                        "title": "Помощь с рабочей задачей",
                                        "href": "/experts?rid=17"
                                    },
                                    {
                                        "title": "Помощь с проектом",
                                        "href": "/experts?rid=18"
                                    }
                                ]
                            },
                            {
                                "title": "Карьера за рубежом",
                                "items": [
                                    {
                                        "title": "Резюме для иностранного рынка",
                                        "href": "/experts?rid=22"
                                    },
                                    {
                                        "title": "Построение карьеры за рубежом",
                                        "href": "/experts?rid=23"
                                    }
                                ]
                            }
                        ],
                        "rate": {
                            "amount": 3000,
                            "currency": "rur",
                            "freeIntro": True
                        },
                        "connectHref": "/experts/sjs-master/connect",
                        "hasDialog": False
                    },
                    ...
                ],
                "meta": {
                    "currentPage": 1,
                    "perPage": 25,
                    "total": 3,
                    "totalPages": 1
                }
            }
        """
        params = {
            "q": search,
            "order": order,
            "rid": request,
            "sid[]": specializations,
            "qid": qualification,
            "skills[]": skills,
            "rateFrom": rate_from,
            "rate": rate_to,
            "currency": currency,
            "freeOnly": free_only,
            "freeIntro": free_intro,
        }
        return self.get(
            "frontend_v1/experts",
            params=params,
            params_options={
                "bool_as_str": True,
            },
        )
