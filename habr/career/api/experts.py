from typing import Any

from habr.career.utils import QueryParams


# noinspection PyUnresolvedReferences
class HABRCareerExpertsMixin:
    def get_experts(
            self,
            search: str,
            order: str | None = None,
    ) -> dict[str, Any]:
        params = QueryParams({
            "q": search,
            # lastActive: По дате визита
            # rate_desc: Цена по убыванию
            # rate_asc: Цена по возрастанию
            "order": "lastActive",
            "rid": 1,
            "sid": [2],
            "qid": 1,
            "skills": [821],
            "rateFrom": 10000,
            "rate": 50000,
            "currency": "eur",
            "freeOnly": "true",
            "freeIntro": "true",
        })
        path = f"frontend_v1/experts?{params.query(doseq=True)}"
        return self.get(path)
