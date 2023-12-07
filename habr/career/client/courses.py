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
    """Раздел `Образование`"""
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
        Get courses list.

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
        :return: Examples:
            {
                "coursesIds": [
                    1451,
                    ...
                ],
                "coursesRefs": {
                    "1451": {
                        "title": "Python-разработчик плюс",
                        "alias": "1451-python-razrabotchik-plyus",
                        "startDate": None,
                        "startKind": "full",
                        "installment": True,
                        "scoresCount": 7,
                        "averageRating": "4.45",
                        "educationPlatform": {
                            "title": "Яндекс Практикум",
                            "alias": "35-yandeks-praktikum",
                            "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/035/logo/9029ac948c9751ee1ad303e78f4f03c8.png",
                            "isPartner": True
                        },
                        "specialization": {
                            "title": "Бэкенд разработчик",
                            "alias": "backend",
                            "translation": "Backend Developer",
                            "landingPath": "development/backend"
                        },
                        "currentQualification": "intern",
                        "resultQualification": "junior",
                        "duration": {
                            "value": 14,
                            "unit": "month"
                        },
                        "skills": [
                            {
                                "title": "Python",
                                "alias": "python"
                            },
                            {
                                "title": "Django",
                                "alias": "django"
                            },
                            {
                                "title": "Flask",
                                "alias": "flask"
                            },
                            {
                                "title": "Асинхронное программирование",
                                "alias": "asynchrony"
                            },
                            {
                                "title": "Администрирование Linux",
                                "alias": "administrirovanie-linux"
                            },
                            {
                                "title": "Администрирование сетей",
                                "alias": "administrirovanie-setey"
                            },
                            {
                                "title": "SQL",
                                "alias": "sql"
                            },
                            {
                                "title": "Алгоритмы",
                                "alias": "algoritmy"
                            }
                        ],
                        "city": None,
                        "price": {
                            "value": 215600,
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
                                "kind": "hasAssist"
                            },
                            {
                                "type": "string",
                                "kind": "isOnline"
                            }
                        ],
                        "courseAuthor": None,
                        "url": "https://practicum.yandex.ru/python-developer-plus/?utm_campaign=partners_habr-career\u0026utm_medium=habr-career\u0026utm_source=partners"
                    },
                    ...
                },
                "meta": {
                    "total": 3,
                    "totalPages": 1,
                    "perPage": 24,
                    "currentPage": 1
                }
            }
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

            "educationPlatforms[]": education_platforms,
            "cities[]": cities,

            "duration": duration,
            "qualification": qualification,

            "skills[]": skills,
            "specializations[]": specializations,

            "q": search,
        })
        query = params.query(doseq=True)
        return self.get(f"frontend_v1/courses?{query}")

    def get_course(self, alias: str) -> dict[str, Any]:
        """
        Get course detail.

        :param alias: Course alias
        :return: Examples:
            {
                "course": {
                    "startDate": None,
                    "startKind": "full",
                    "courseAuthor": None,
                    "alias": "1451-python-razrabotchik-plyus",
                    "title": "Python-разработчик плюс",
                    "url": "https://practicum.yandex.ru/python-developer-plus/?utm_campaign=partners_habr-career&utm_medium=habr-career&utm_source=partners",
                    "description": "Онлайн-курс «Python-разработчик плюс» с трудоустройством от сервиса Яндекс Практикум. За 14 месяцев обучения по 15 часов в неделю вы освоите навыки профессии разработчика на Python.",
                    "price": {
                        "value": 215600,
                        "unit": "rur",
                        "discount": 0,
                        "oldValue": None
                    },
                    "labels": [
                        {"type": "string", "kind": "hasCert"},
                        {"type": "string", "kind": "hasAssist"},
                        {"type": "string", "kind": "isOnline"}
                    ],
                    "duration": {
                        "value": 14,
                        "unit": "month"
                    },
                    "installment": {
                        "value": 15400,
                        "unit": "rur",
                        "duration": {
                            "value": 14,
                            "unit": "month"
                        }
                    },
                    "promocode": None,
                    "currentQualification": "intern",
                    "resultQualification": "junior",
                    "scoreable": True,
                    "skills": [
                        {
                            "title": "Python",
                            "alias": "python"
                        },
                        {
                            "title": "Django",
                            "alias": "django"
                        },
                        {
                            "title": "Flask",
                            "alias": "flask"
                        },
                        {
                            "title": "Асинхронное программирование",
                            "alias": "asynchrony"
                        },
                        {
                            "title": "Администрирование Linux",
                            "alias": "administrirovanie-linux"
                        },
                        {
                            "title": "Администрирование сетей",
                            "alias": "administrirovanie-setey"
                        },
                        {
                            "title": "SQL",
                            "alias": "sql"
                        },
                        {
                            "title": "Алгоритмы",
                            "alias": "algoritmy"
                        }
                    ],
                    "city": None,
                    "specialization": {
                        "title": "Бэкенд разработчик",
                        "alias": "backend",
                        "translation": "Backend Developer",
                        "landingPath": "development/backend"
                    },
                    "educationPlatform": {
                        "title": "Яндекс Практикум",
                        "alias": "35-yandeks-praktikum",
                        "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/035/logo/9029ac948c9751ee1ad303e78f4f03c8.png",
                        "isPartner": true,
                        "url": "https://practicum.yandex.ru",
                        "coursesCount": 64
                    }
                }
            },
            {
                "httpCode": 404,
                "errorCode": "NOT_FOUND",
                "message": "Not found",
                "data": {}
            }
        """
        return self.get(f"frontend_v1/courses/{alias}")

    def get_course_scores(self, alias: str) -> dict[str, Any]:
        """
        Get course scores.

        :param alias: Course alias
        :return: Examples:
            {
                "scoresCount": 7,
                "commentsCount": 4,
                "averageRating": "4.45",
                "recommendedBy": 86,
                "jobOrPromotionStat": {
                    "ignore": 1,
                    "yes": 3,
                    "no": 3
                },
                "averageScores": {
                    "course_program": "4.57",
                    "employment_assist": "4.00",
                    "platform": "4.71",
                    "practice": "4.29",
                    "price": "4.29",
                    "skills": "4.57",
                    "tutor": "4.71"
                },
                "canRate": true,
                "hasMore": false,
                "scores": [
                    {
                        "id": 761,
                        "createdAt": "2023-10-24T15:22:12.490+03:00",
                        "averageScore": "4.57",
                        "recommendation": 80,
                        "detail": [
                            {
                                "key": "price",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "course_program",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "tutor",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "skills",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "platform",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "practice",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "employment_assist",
                                "value": 4,
                                "title": null
                            }
                        ],
                        "advantages": "<p>Работа с ревьюерами и наставниками. Карьерное сопровождение. </p>",
                        "disadvantages": "<p>Не весь материал внутри курса подавался связно, есть недоработки</p>",
                        "comment": "<p>Рынок очень сильно перегрет, гарантия трудоустройства - совсем не гарантия. Тем не менее, карьерное сопровождение полезное. </p><p>Курс достаточно сложный и насыщенный для новичка, ему нужно будет уделять время и внимание. Возможно, придётся уволиться с основной работы. Я бы посоветовал подготовить финансовую подушку примерно на полгода. </p>",
                        "qualification": "Младший (Junior)",
                        "likes": 0,
                        "liked": false,
                        "canHide": false,
                        "canDelete": false,
                        "canComplain": true,
                        "jobOrPromotion": "yes"
                    },
                    {
                        "id": 204,
                        "createdAt": "2023-06-13T15:44:29.236+03:00",
                        "averageScore": "4.86",
                        "recommendation": 80,
                        "detail": [
                            {
                                "key": "price",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "course_program",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "tutor",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "skills",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "platform",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "practice",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "employment_assist",
                                "value": 5,
                                "title": null
                            }
                        ],
                        "advantages": "<p>В целом понравилось все. Четкая структура того что необходимо изучить и как от простого перейти к сложным вещам Впитывал все что можно было подчерпнуть. Курс уже близиться к завершению. Позже дополню отзыв, когда пройду карьерный трек и уже по результатам трутоустройства будет ясно, стоил ли курс всех тех сил которых были вложены.</p>",
                        "disadvantages": "<p>Много материала, очень много. И достаточно серьезные финальные задания. Попав на курс пришлось жить этим обучением, сдвинув на второстепенный план все остальное. Удивлен как еще с женой не развелся пока учился.</p>",
                        "comment": "<p>Для того что бы вас не отчислили требуется много времени уделить на изучение материалов, а так же серьезно озадачиться с выполнением финальных заданий. Если не уложиться в дедлайны, вы можете 2 раза взять академ, но если еще раз не уложитесь в дедлайн, вас отчислят. Не думайте что раз первые уроки простые, то вы с легкостью и остальное пройдете. У меня, с учетом того что уже был знаком с некоторыми вещами, уходило все свободное время после работы, а так же все выходные, отпуска и праздники, а то и больше.</p>",
                        "qualification": "Младший (Junior)",
                        "likes": 0,
                        "liked": false,
                        "canHide": false,
                        "canDelete": false,
                        "canComplain": true,
                        "jobOrPromotion": "yes"
                    },
                    {
                        "id": 100,
                        "createdAt": "2023-06-03T13:58:23.925+03:00",
                        "averageScore": "4.86",
                        "recommendation": 90,
                        "detail": [
                            {
                                "key": "price",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "course_program",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "tutor",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "skills",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "platform",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "practice",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "employment_assist",
                                "value": 4,
                                "title": null
                            }
                        ],
                        "advantages": "<p>В этом курсе полезно всё. Понятная теория, множество задач, интересная практика</p>",
                        "disadvantages": "<p>В целом всё очень хорошо. Ревьюеры подают много дополнительной информации, наставники быстро отвечают, но вот вебинары довольно монотонные и их тяжело слушать</p>",
                        "comment": "<p>Если не получается - не отчаивайся. На прохождение курса нужно время, по моему опыту это 4-5 часов в день, 4-5 раз в неделю, если вы будете двигаться с хорошим темпом конечно</p>",
                        "qualification": null,
                        "likes": 0,
                        "liked": false,
                        "canHide": false,
                        "canDelete": false,
                        "canComplain": true,
                        "jobOrPromotion": "ignore"
                    },
                    {
                        "id": 56,
                        "createdAt": "2023-05-31T19:48:48.378+03:00",
                        "averageScore": "4.86",
                        "recommendation": 100,
                        "detail": [
                            {
                                "key": "price",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "course_program",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "tutor",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "skills",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "platform",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "practice",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "employment_assist",
                                "value": 5,
                                "title": null
                            }
                        ],
                        "advantages": "<p>Мне понравилась система подачи информации. Теория подается структурированно, от простого к сложному.  Да, в некоторых моментах нужно самому поискать информацию, но это часть обучения. Тренажер очень удобный, за очень редким исключением, работал без сбоев. Куратор наш, Вика Выговская- просто золото! Сплотила нашу когорту, благодаря ей мы с некоторыми ребятами общаемся до сих пор.  Вика всегда поддерживала нас, при необходимости,  решала вопросы индивидуально.  Вебинары наставников Арсена Халилова и Сергея Ивакина проходили оживленно, с вопросами и ответами.  Ревьюеры у некоторых студентов менялись. У меня был постоянный проверяющий, это кстати, очень удобно: он знает, как я пишу код и знает, к чему готовиться))</p>",
                        "disadvantages": "<p>Пару раз отваливался Git Hub от закрепленной страницы курса, приходилось писать в поддержку. Но поддержка 24/7 всегда выручает!</p>",
                        "comment": "<p>Сложно, но можно! Тем, кто с нуля - время на обучение уходит НЕ 2-3 часа в день, а гораздо больше! Учитывайте это при распределении вашего времени. Расслабляйтесь только на каникулах! Один день не кодишь - считай, что забыл половину темы. Будьте активны в обсуждении тем. Появился вопрос - поищи сам сначала, а если не нашел ответа или не понял, задай вопрос в треде. Не бойтесь задавать вопросы! Не думайте, что вы будете выглядеть глупо! Обсуждения сближают ребят, вы получаете ответ и новых приятелей.</p>",
                        "qualification": "Средний (Middle)",
                        "likes": 0,
                        "liked": false,
                        "canHide": false,
                        "canDelete": false,
                        "canComplain": true,
                        "jobOrPromotion": "no"
                    },
                    {
                        "id": 837,
                        "createdAt": "2023-11-18T20:08:09.769+03:00",
                        "averageScore": "5.00",
                        "recommendation": 100,
                        "detail": [
                            {
                                "key": "price",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "course_program",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "tutor",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "skills",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "platform",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "practice",
                                "value": 5,
                                "title": null
                            },
                            {
                                "key": "employment_assist",
                                "value": 5,
                                "title": null
                            }
                        ],
                        "advantages": null,
                        "disadvantages": null,
                        "comment": null,
                        "qualification": "Средний (Middle)",
                        "likes": 0,
                        "liked": false,
                        "canHide": false,
                        "canDelete": false,
                        "canComplain": true,
                        "jobOrPromotion": "yes"
                    },
                    {
                        "id": 830,
                        "createdAt": "2023-11-18T05:04:46.867+03:00",
                        "averageScore": "3.00",
                        "recommendation": 50,
                        "detail": [
                            {
                                "key": "price",
                                "value": 3,
                                "title": null
                            },
                            {
                                "key": "course_program",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "tutor",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "skills",
                                "value": 3,
                                "title": null
                            },
                            {
                                "key": "platform",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "practice",
                                "value": 2,
                                "title": null
                            },
                            {
                                "key": "employment_assist",
                                "value": 1,
                                "title": null
                            }
                        ],
                        "advantages": null,
                        "disadvantages": null,
                        "comment": null,
                        "qualification": "Младший (Junior)",
                        "likes": 0,
                        "liked": false,
                        "canHide": false,
                        "canDelete": false,
                        "canComplain": true,
                        "jobOrPromotion": "no"
                    },
                    {
                        "id": 805,
                        "createdAt": "2023-11-09T15:28:18.540+03:00",
                        "averageScore": "4.00",
                        "recommendation": 100,
                        "detail": [
                            {
                                "key": "price",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "course_program",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "tutor",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "skills",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "platform",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "practice",
                                "value": 4,
                                "title": null
                            },
                            {
                                "key": "employment_assist",
                                "value": 4,
                                "title": null
                            }
                        ],
                        "advantages": null,
                        "disadvantages": null,
                        "comment": null,
                        "qualification": "Младший (Junior)",
                        "likes": 0,
                        "liked": false,
                        "canHide": false,
                        "canDelete": false,
                        "canComplain": true,
                        "jobOrPromotion": "no"
                    }
                ]
            },
            {
                "httpCode": 404,
                "errorCode": "NOT_FOUND",
                "message": "Not found",
                "data": {}
            }
        """
        return self.get(f"frontend_v1/courses/{alias}/scores")

    def get_similar_courses(self, alias: str) -> dict[str, Any]:
        """
        Get courses similar to which was requested by alias.

        :param alias: Course alias
        :return: Examples:
            {
                "similarCoursesIds": [
                    3015,
                    337,
                    1198
                ],
                "similarCoursesRefs": {
                    "337": {
                        "title": "Профессия: Python-разработчик",
                        "alias": "337-professiya-python-razrabotchik",
                        "price": {
                            "value": 134100,
                            "unit": "rur",
                            "discount": 21,
                            "oldValue": 168000
                        },
                        "startDate": None,
                        "startKind": "full",
                        "educationPlatform": {
                            "title": "Хекслет",
                            "alias": "3-hekslet",
                            "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/003/logo/733e8366d5e14ff8539f5fccc8c058da.jpg",
                            "isPartner": True
                        },
                        "duration": {
                            "value": 10,
                            "unit": "month"
                        },
                        "courseAuthor": None
                    },
                    "1198": {
                        "title": "Мидл Python-разработчик",
                        "alias": "1198-midl-python-razrabotchik",
                        "price": {
                            "value": 110000,
                            "unit": "rur",
                            "discount": 0,
                            "oldValue": None
                        },
                        "startDate": None,
                        "startKind": "full",
                        "educationPlatform": {
                            "title": "Яндекс Практикум",
                            "alias": "35-yandeks-praktikum",
                            "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/035/logo/9029ac948c9751ee1ad303e78f4f03c8.png",
                            "isPartner": True
                        },
                        "duration": {
                            "value": 6,
                            "unit": "month"
                        },
                        "courseAuthor": None
                    },
                    "3015": {
                        "title": "Python - программист с нуля",
                        "alias": "3015-python-programmist-s-nulya",
                        "price": {
                            "value": 12150,
                            "unit": "rur",
                            "discount": 10,
                            "oldValue": 13500
                        },
                        "startDate": None,
                        "startKind": "full",
                        "educationPlatform": {
                            "title": "Merion Academy",
                            "alias": "288-merion-academy",
                            "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/288/logo/8b2577ad5291ca5e5ce6ba2273b02e9d.png",
                            "isPartner": True
                        },
                        "duration": {
                            "value": 4,
                            "unit": "month"
                        },
                        "courseAuthor": None
                    }
                },
                "similarCoursesHref": {
                    "landingPath": "development/backend",
                    "titleGenitive": "бэкенд разработчика"
                }
            },
            {
                "httpCode": 404,
                "errorCode": "NOT_FOUND",
                "message": "Not found",
                "data": {}
            }
        """
        return self.get(f"frontend_v1/courses/{alias}/similar_courses")

    def get_popular_education_platforms(
            self,
            limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Get popular education platforms.

        :param limit:
        :return: Examples:
            {
                "popularEducationPlatforms": [
                    {
                        "id": "35",
                        "title": "Яндекс Практикум",
                        "alias": "35-yandeks-praktikum",
                        "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/035/logo/medium_9029ac948c9751ee1ad303e78f4f03c8.png",
                        "isPartner": True,
                        "coursesCount": 41,
                        "graduatesCount": 9843
                    },
                    ...
               ]
            }
        """
        path = f"frontend_v1/education_platforms/popular?limit={limit}"
        return self.get(path, key="popularEducationPlatforms")

    def get_popular_skills(self, limit: int = 10) -> list[dict[str, str]]:
        """
        Get popular skills.

        :param limit:
        :return: Examples:
            {
                "skills": [
                    {
                      "title": "Python",
                      "alias": "python"
                    },
                    {
                      "title": "Java",
                      "alias": "java"
                    },
                    {
                      "title": "Защита информации",
                      "alias": "zaschita-informatsii"
                    },
                    {
                      "title": "JavaScript",
                      "alias": "javascript"
                    },
                    {
                      "title": "Управление проектами",
                      "alias": "upravlenie-proektami"
                    }
                ]
            }
        """
        path = f"frontend_v1/skills/popular?limit={limit}"
        return self.get(path, key="skills")

    def get_educations_suggestions(self, search: str) -> dict[str, Any]:
        """
        Get educations suggestions.

        :param search:
        :return: Examples:
            {
                "skills": [
                    {
                        "title": "TestLink",
                        "alias": "testlink",
                        "logoUrl": None
                    },
                    {
                        "title": "TestNG",
                        "alias": "testng",
                        "logoUrl": None
                    }
                ],
                "specializations": [],
                "courses": [
                    {
                        "title": "Software Testing",
                        "alias": "868-software-testing",
                        "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/029/logo/980525cd33c1f8484b834654cc501c0f.png"
                    },
                    {
                        "title": "Software Testing QA",
                        "alias": "878-software-testing-qa",
                        "logoUrl": "https://habrastorage.org/getpro/moikrug/uploads/education_platform/000/000/142/logo/f4399c9ff8d4f76c73bd58736d39da8d.png"
                    }
                ]
            },
            {
                "status": "500",
                "error": "Internal Server Error"
            }
        """
        return self.get(f"frontend_v1/suggestions/educations?term={search}")

    def get_education_platforms_suggestions(
            self,
            search: str,
    ) -> list[dict[str, str]]:
        """
        Get education platforms suggestions.

        :param search:
        :return: Examples:
            {
                "education_platforms": [
                    {
                        "title": "TestGrow",
                        "alias": "278-testgrow"
                    },
                    {
                        "title": "Software-testing.ru",
                        "alias": "68-software-testing-ru"
                    },
                    {
                        "title": "QATestLab Training Center",
                        "alias": "171-qatestlab-training-center"
                    }
                ]
            }
        """
        path = f"frontend_v1/suggestions/education_platforms?term={search}"
        return self.get(path, key="education_platforms")

    @property
    def courses_count(self) -> int:
        """
        Get the number of currently active courses.

        :return: Examples:
            {"count": 1139}
        """
        return self.get("frontend_v1/courses/total_count", key="count")

    def get_specializations_with_course_counters(self) -> dict[str, Any]:
        """
        Get specializations with courses counters.

        :return: Examples:
            {
                "groups": [
                    {
                        "title": "Искусственный интеллект",
                        "alias": "ai",
                        "translation": "Artificial Intelligence",
                        "items": [
                            {
                                "title": "Ученый по данным",
                                "alias": "data_scientist",
                                "translation": "Data Scientist",
                                "landingPath": "ai/data_scientist",
                                "coursesCount": 17
                            },
                            {
                                "title": "ML разработчик",
                                "alias": "ml-engineer",
                                "translation": "ML Engineer",
                                "landingPath": "ai/ml-engineer",
                                "coursesCount": 7
                            },
                            {
                                "title": "Другое",
                                "alias": "ai-other",
                                "translation": "Other",
                                "landingPath": "ai/ai-other",
                                "coursesCount": 0
                            }
                        ]
                    },
                    ...
                ]
            }
        """
        return self.get("frontend_v1/specializations/with_course_counters")

    def get_specializations(self) -> dict[str, Any]:
        """
        Get specializations.

        :return: Examples:
            {
                "groups": [
                    {
                        "title": "Искусственный интеллект",
                        "alias": "ai",
                        "translation": "Artificial Intelligence",
                        "items": [
                            {
                                "title": "Ученый по данным",
                                "alias": "data_scientist",
                                "translation": "Data Scientist",
                                "landingPath": "ai/data_scientist"
                            },
                            {
                                "title": "ML разработчик",
                                "alias": "ml-engineer",
                                "translation": "ML Engineer",
                                "landingPath": "ai/ml-engineer"
                            },
                            {
                                "title": "Другое",
                                "alias": "ai-other",
                                "translation": "Other",
                                "landingPath": "ai/ai-other"
                            }
                        ]
                    },
                    ...
                ]
            }
        """
        return self.get("frontend_v1/specializations")

    def get_offers(self, specializations: list[str]) -> dict[str, Any]:
        """
        Get offers by specializations list.

        :param specializations:
        :return: Examples:
            {
                "offers": {
                    "lowPrice": 28990,
                    "highPrice": 39990,
                    "priceCurrency": "RUB",
                    "offerCount": 4,
                    "offers": [
                        {
                            "@type": "FinancialProduct",
                            "name": "PROавтовебинарные воронки на GetCourse 2.0 ",
                            "brand": "GetHelpers.ru"
                        },
                        {
                            "@type": "FinancialProduct",
                            "name": "Технический специалист по настройке GetCourse",
                            "brand": "GetHelpers.ru"
                        },
                        {
                            "@type": "FinancialProduct",
                            "name": "PROпроцессы и маркетинг на GetCourse",
                            "brand": "GetHelpers.ru"
                        },
                        {
                            "@type": "FinancialProduct",
                            "name": "Специалист по чат-ботам",
                            "brand": "GetHelpers.ru"
                        }
                    ]
                },
                "aggregateRating": {
                    "bestRating": "5",
                    "worstRating": "1",
                    "ratingCount": 0,
                    "ratingValue": None
                },
                "events": [
                    {
                        "name": "Разработчик C++",
                        "description": "Образовательный курс в «Яндекс Практикум». 9 месяцев, 126 000 ₽. Онлайн обучение. Сертификат. Трудоустройство. Запишитесь на курс прямо сейчас или расскажите о нём своим знакомым.",
                        "startDate": "2023-11-13",
                        "endDate": "2024-08-13",
                        "url": "https://career.habr.com/courses/1200-razrabotchik-c"
                    },
                    {
                        "name": "Инженер данных",
                        "description": "Образовательный курс в «Яндекс Практикум». 6 месяцев, 95 000 ₽. Онлайн обучение. Сертификат. Запишитесь на курс прямо сейчас или расскажите о нём своим знакомым.",
                        "startDate": "2023-11-13",
                        "endDate": "2024-05-13",
                        "url": "https://career.habr.com/courses/2900-inzhener-dannyh"
                    },
                    {
                        "name": "Продакт-менеджер",
                        "description": "Образовательный курс в «Яндекс Практикум». 5 месяцев, 120 000 ₽. Онлайн обучение. Сертификат. Запишитесь на курс прямо сейчас или расскажите о нём своим знакомым.",
                        "startDate": "2023-11-13",
                        "endDate": "2024-04-13",
                        "url": "https://career.habr.com/courses/2936-prodakt-menedzher"
                    }
                ]
            },
            {
                "httpCode": 404,
                "errorCode": "NOT_FOUND",
                "message": "Not found",
                "data": {}
            }
        """
        params = QueryParams({"specializations[]": specializations})
        query = params.query(doseq=True)
        return self.get(f"frontend_v1/courses/ld_json?{query}")
