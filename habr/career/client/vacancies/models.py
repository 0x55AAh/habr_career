from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, HttpUrl

from habr.career.utils import Username


class Response(BaseModel):
    id: int
    published_at: str = Field(alias="publishedAt")
    message: str
    message_html: str = Field(alias="messageHtml")
    author: Author
    favorite: bool
    archived: bool
    has_analytics: bool = Field(alias="hasAnalytics")
    is_quick: bool = Field(alias="isQuick")
    vacancy_recommendation_accuracy_percent: Any | None = Field(alias="vacancyRecommendationAccuracyPercent")  # TODO

    class Author(BaseModel):
        id: Username
        title: str
        href: str
        avatar: Avatar
        more_university_count: int = Field(alias="moreUniversityCount")
        location: str
        status: str
        salary: str
        availability: str
        skills: list[Skill]
        qualification: str
        age: str
        experience: str
        companies_count: str = Field(alias="companiesCount")
        companies_history: list[Company] = Field(alias="companiesHistory")
        is_expert: bool = Field(alias="isExpert")
        last_job: LastJob = Field(alias="lastJob")
        education: Any | None  # TODO: undefined type
        additional_education: list = Field(alias="additionalEducation")  # TODO: undefined structure
        conversations: list  # TODO: undefined structure
        socials: list  # TODO: undefined structure

        class Avatar(BaseModel):
            src: HttpUrl
            alt: str

        class Skill(BaseModel):
            title: str
            href: str

        class Company(BaseModel):
            company_name: str = Field(alias="companyName")
            experience: str

        class LastJob(BaseModel):
            position: str
            company: Company
            duration: str

            class Company(BaseModel):
                title: str
                href: str | None


class Responses(BaseModel):
    objects: list[Response] = Field(alias="list")
    meta: Meta

    class Meta(BaseModel):
        total_results: int = Field(alias="totalResults")
        per_page: int = Field(alias="perPage")
        current_page: int = Field(alias="currentPage")
        total_pages: int = Field(alias="totalPages")


class ResponsesArchived(BaseModel):
    objects: list[Response] = Field(alias="list")
    meta: Meta

    class Meta(BaseModel):
        total_results: int = Field(alias="totalResults")


class ResponsesFavorite(ResponsesArchived):
    pass
