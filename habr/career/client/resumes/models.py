from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from habr.career.utils import Username


class Resumes(BaseModel):
    objects: list[Resume] = Field(alias="list")
    meta: Meta
    limited_access: (
            LimitedAccessForLoggedIn
            | LimitedAccessForNotLoggedIn
            | None
    ) = Field(alias="limitedAccess")

    class Resume(BaseModel):
        id: Username
        title: str  # Full name
        href: str
        conversation_href: str | None = Field(alias="conversationHref")
        avatar: Avatar
        last_visited: LastVisited = Field(alias="lastVisited")
        specialization: str | None
        qualification: Qualification | None
        salary: Salary | None
        availability: Availability
        location: Location | None
        remote_work: bool = Field(alias="remoteWork")
        relocation: bool
        skills: list[Skill]
        age: Age | None
        experience: Experience | None
        last_job: LastJob | None = Field(alias="lastJob")
        education: Education | None
        additional_education: list[AdditionalEducation] = Field(alias="additionalEducation")
        communities: list[Community]
        coworkers: list  # TODO: Items format unknown so far
        specializations: list[Specialization]
        gender: int
        is_expert: bool = Field(alias="isExpert")
        more_university_count: int = Field(alias="moreUniversityCount")
        companies_count: str = Field(alias="companiesCount")
        # TODO: Items format unknown so far
        companies_history: list = Field(alias="companiesHistory")

        class Avatar(BaseModel):
            src: HttpUrl
            src2x: HttpUrl

        class LastVisited(BaseModel):
            title: str
            date: datetime

        class Qualification(BaseModel):
            title: str  # TODO: Enum?
            value: int

        class Salary(BaseModel):
            title: str
            value: int
            currency: str  # TODO: Enum?

        class Availability(BaseModel):
            title: str
            value: str

        class Location(BaseModel):
            title: str
            name: str
            href: str
            value: int

        class Skill(BaseModel):
            title: str
            href: str
            value: int

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

        class Education(BaseModel):
            university: University
            faculty: str | None
            duration: Duration

            class Duration(BaseModel):
                title: str
                value: int

            class University(BaseModel):
                title: str
                href: str

        class Specialization(BaseModel):
            title: str

        class AdditionalEducation(BaseModel):
            title: str
            href: str | None = None

        class Community(BaseModel):
            title: str
            name: str
            icon: str
            href: HttpUrl

    class LimitedAccessForLoggedIn(BaseModel):
        type: str
        new_company_href: HttpUrl = Field(alias="newCompanyHref")

    class LimitedAccessForNotLoggedIn(BaseModel):
        type: str
        register_href: HttpUrl = Field(alias="registerHref")
        login_href: HttpUrl = Field(alias="loginHref")

    class Meta(BaseModel):
        total_results: int = Field(alias="totalResults")
        per_page: int = Field(alias="perPage")
        current_page: int = Field(alias="currentPage")
        total_pages: int = Field(alias="totalPages")
