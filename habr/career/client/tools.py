# noinspection PyUnresolvedReferences
class HABRCareerToolsMixin:
    def get_cities_suggestions(self, search: str) -> list[dict[str, str]]:
        """
        Get cities list.
        Working different when logged in. This is not a big deal, so we do not
        pass auth data on the request.

        :param search: Search query
        :return: Examples:
            {
                "cities": [
                    {
                        "title": "Moscow",
                        "regionTitle": "Айдахо",
                        "countryTitle": "США",
                        "alias": "moscow-idaho"
                    }
                ]
            }
        """
        path = "frontend_v1/suggestions/cities"
        return self.get(path, key="cities", params={"q": search})

    def get_skills_alias_suggestions(
            self, search: str) -> list[dict[str, str]]:
        """
        Get skills list.
        Alias is passed as unique key.
        Used in filters.

        :param search: Search query
        :return: Examples:
            {
                "skills": [
                    {"title": "Python", "alias": "python"},
                    {"title": "PyTorch", "alias": "pytorch"},
                    {"title": "Falcon", "alias": "falcon"},
                    {"title": "Keras", "alias": "keras"},
                    {"title": "FastAPI", "alias": "fastapi"},
                    {"title": "Boo", "alias": "boo"}
                ]
            }
        """
        path = "frontend_v1/suggestions/skills"
        return self.get(path, key="skills", params={"q": search})

    def get_skills_ids_suggestions(
            self, search: str) -> list[dict[str, int | str]]:
        """
        Get skills list.
        ID is passed as unique key.
        Used in filters.

        :param search: Search query
        :return: Examples:
            {
                "list": [
                    {"value": 446, "title": "Python"},
                    {"value": 1241, "title": "PyTorch"},
                    {"value": 1217, "title": "Falcon"},
                    {"value": 1216, "title": "Keras"},
                    {"value": 1349, "title": "FastAPI"},
                    {"value": 1625, "title": "Boo"}
                ]
            }
        """
        path = "frontend/suggestions/skills"
        return self.get(path, key="list", params={"term": search})

    def get_qualifications(self) -> list[dict[str, str | int]]:
        """
        Get qualifications list.
        Used in filters.

        :return: Examples:
            {
                "qualifications": [
                    {"title": "Стажёр", "position": 0, "alias": "Intern"},
                    {"title": "Младший", "position": 2, "alias": "Junior"},
                    {"title": "Средний", "position": 3, "alias": "Middle"},
                    {"title": "Старший", "position": 4, "alias": "Senior"},
                    {"title": "Ведущий", "position": 5, "alias": "Lead"}
                ]
            }
        """
        return self.get("frontend_v1/qualifications", key="qualifications")

    def get_currencies(self) -> list[str]:
        """
        Get currencies list.
        Used in filters.

        :return: Examples:
            {
                "currencies": [
                    {"currency": "rur"},
                    {"currency": "eur"},
                    {"currency": "usd"},
                    {"currency": "uah"},
                    {"currency": "kzt"}
                ]
            }
        """
        res = self.get("frontend_v1/currencies", key="currencies")
        return [r["currency"] for r in res]

    def get_similar_skills(self) -> list[dict[str, str | int]]:
        """
        Get similar skills.

        :return: Examples:
            {
                "list": [
                    {"value": 947, "title": "Git"},
                    {"value": 264, "title": "JavaScript"},
                    {"value": 322, "title": "SQL"},
                    {"value": 1017, "title": "HTML"},
                    {"value": 446, "title": "Python"},
                    ...
                ]
            }
        """
        return self.get("frontend/suggestions/similar_skills", key="list")

    def get_similar_skills_extended(self) -> list[dict[str, str | int]]:
        """
        Get similar skills with additional data.

        :return: Examples:
            [
                {
                    "id": 947,
                    "created_at": "2015-06-06T15:12:56.079+03:00",
                    "updated_at": "2015-07-11T23:21:58.587+03:00",
                    "alias_name": "git",
                    "title": "Git",
                    "users_count": 133284,
                    "synonyms": "гит",
                    "bs_id": 14328,
                    "popularity": 133068,
                    "division_id": 2,
                    "reports_title": "Git",
                    "axis_title": "Git",
                    "title_en": "Git"
                },
                ...
            ]
        """
        path = "suggest/skills/similar"
        return self.get(path, base_url="https://career.habr.com/")

    # TODO: https://career.habr.com/api/frontend_v1/specializations/group_dative?q=development
    # TODO: https://career.habr.com/api/frontend_v1/specializations/spec_genitive?q=zerocoder&group=no-code
    # TODO: https://career.habr.com/api/frontend_v1/skills/python
    # TODO: https://career.habr.com/api/frontend_v1/suggestions/skills?aliases[]=python&q
