from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl


class Ratings(BaseModel):
    list_: list[Rating] = Field(alias="list")
    meta: Meta

    class Rating(BaseModel):
        summary: Summary
        scores: Scores
        review: Review
        position: int
        company: Company

        class Summary(BaseModel):
            visible_summary: bool
            href: str
            title: str
            value: str

        class Scores(BaseModel):
            featured: Featured
            items: list[Item]

            class Item(BaseModel):
                title: str
                value: str
                level: str

            class Featured(BaseModel):
                title: str
                value: str

        class Review(BaseModel):
            should_collapse: bool = Field(alias="shouldCollapse")
            summary: str
            positives: str
            negatives: str

        class Company(BaseModel):
            title: str
            description: str
            href: str
            avatar: Avatar
            rate_href: str | None = Field(alias="rateHref")
            location: Location | None
            vacancies: Vacancies | None
            awards: list[Award]
            accredited: bool

            class Avatar(BaseModel):
                src: HttpUrl
                src2x: HttpUrl
                alt: str

            class Location(BaseModel):
                title: str
                href: str

            class Vacancies(BaseModel):
                title: str
                href: str

            class Award(BaseModel):
                title: str
                image: Image
                href: str

                class Image(BaseModel):
                    src: str

    class Meta(BaseModel):
        per_page: int = Field(alias="perPage")
        current_page: int = Field(alias="currentPage")
        total_pages: int = Field(alias="totalPages")
        total_results: int = Field(alias="totalResults")
        counter_description: str = Field(alias="counterDescription")
