from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from habr.career.utils import Username


class Experts(BaseModel):
    objects: list[Expert] = Field(alias="list")
    meta: Meta

    class Expert(BaseModel):
        title: str
        login: Username
        alias: Username
        avatar: Avatar
        age: Age | None
        experience: Experience
        last_job: LastJob | None = Field(alias="lastJob")
        last_visited: LastVisited = Field(alias="lastVisited")
        score: Score
        qualifications: list[Qualification]
        specializations: list[Specialization]
        skills: list[Skill]
        requests: list[Request]
        rate: Rate | None
        connect_href: str = Field(alias="connectHref")
        has_dialog: bool = Field(alias="hasDialog")

        class Avatar(BaseModel):
            src: HttpUrl
            src2x: HttpUrl

        class Age(BaseModel):
            title: str
            value: int

        class Experience(BaseModel):
            title: str
            value: int

        class LastJob(BaseModel):
            position: str
            company: Company
            duration: Duration

            class Company(BaseModel):
                title: str
                accredited: bool = False
                href: str | None

            class Duration(BaseModel):
                title: str
                value: int

        class LastVisited(BaseModel):
            title: str
            date: datetime

        class Score(BaseModel):
            connections: int
            average_score: float = Field(alias="averageScore")
            scores_count: int = Field(alias="scoresCount")

        class Qualification(BaseModel):
            title: str
            position: int
            href: str

        class Specialization(BaseModel):
            title: str
            href: str

        class Skill(BaseModel):
            title: str
            href: str

        class Request(BaseModel):
            title: str
            items: list[Item]

            class Item(BaseModel):
                title: str
                href: str

        class Rate(BaseModel):
            amount: int
            currency: str
            free_intro: bool | None = Field(alias="freeIntro")

    class Meta(BaseModel):
        current_page: int = Field(alias="currentPage")
        total_pages: int = Field(alias="totalPages")
        per_page: int = Field(alias="perPage")
        total: int
