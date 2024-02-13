from enum import StrEnum, verify, UNIQUE, IntEnum

from habr.career.utils import QualificationID, Currency, Pagination
from .models import Experts


@verify(UNIQUE)
class ExpertsOrder(StrEnum):
    LAST_ACTIVE = "lastActive"  # По дате визита
    RATE_DESC = "rate_desc"     # Цена по убыванию
    RATE_ASC = "rate_asc"       # Цена по возрастанию


@verify(UNIQUE)
class RequestID(StrEnum):
    RQ1 = "1"  # Начало карьеры или смена профессии
    RQ2 = "2"  # Развитие навыков
    RQ3 = "3"  # Оценка
    RQ4 = "4"  # Смена работы
    RQ5 = "5"  # Карьерный рост
    RQ6 = "6"  # Помощь с задачей
    RQ7 = "7"  # Поддержка и коучинг
    RQ8 = "8"  # Карьера за рубежом


# noinspection PyUnresolvedReferences
class HABRCareerExpertsMixin:
    """Раздел `Эксперты`"""

    def get_experts(
            self,
            *,
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
            page: int = Pagination.INIT_PAGE,
            per_page: int = Pagination.PER_PAGE,
    ) -> Experts:
        """
        Get experts list.

        :param search: Поиск по навыкам, целям, имени.
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
        :param page:
        :param per_page:
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
                            ...
                        ],
                        "specializations": [
                            {
                                "title": "Фронтенд разработчик",
                                "href": "/experts?sid%5B%5D=3"
                            },
                            ...
                        ],
                        "skills": [
                            {
                                "title": "Node.js",
                                "href": "/experts?skills%5B%5D=12"
                            },
                            ...
                        ],
                        "requests": [
                            {
                                "title": "Начало карьеры или смена профессии",
                                "items": [
                                    {
                                        "title": "Войти в IT",
                                        "href": "/experts?rid=1"
                                    },
                                    ...
                                ]
                            },
                            ...
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
            "page": page,
            "perPage": per_page,
        }
        return self.get(
            "frontend_v1/experts",
            params=params,
            params_options={
                "bool_as_str": True,
            },
            cls=Experts,
        )
