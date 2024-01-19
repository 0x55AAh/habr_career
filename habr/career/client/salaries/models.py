from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl

from habr.career.utils import Qualification


class SalaryGeneralGraph(BaseModel):
    groups: list[Group]

    class Group(BaseModel):
        name: Qualification
        min: int
        max: int
        p25: int
        p75: int
        median: int
        total: int
        title: str
        spec_title: str | None = Field(alias="specTitle")
        seo_title: list[str] | None = Field(alias="seoTitle")
        salary: Salary

        class Salary(BaseModel):
            total: int
            value: int
            bonus: int
            bonus_percent: int = Field(alias="bonusPercent")


class SalaryDynamicGraph(BaseModel):
    graphs_data: GraphsData

    class GraphsData(BaseModel):
        title: str
        periods: list[Period]

        class Period(BaseModel):
            key: int
            value: float
            title: str


class SalaryChart(BaseModel):
    title: str
    values: list[Value]
    diagram_href: str = Field(alias="diagramHref")

    class Value(BaseModel):
        title: str
        salary: Salary
        is_user_qualification: bool = Field(alias="isUserQualification")

        class Salary(BaseModel):
            value: int
            unit: str


class Locations(BaseModel):
    locations: list[Location]

    class Location(BaseModel):
        title: str
        subtitle: str
        alias: str


class Companies(BaseModel):
    companies: list[Company]

    class Company(BaseModel):
        title: str
        logoUrl: HttpUrl = Field(alias="logoUrl")
        alias: str


class MySalary(BaseModel):
    periods: list[Period]
    last_salary: LastSalary = Field(alias="lastSalary")
    current_period: CurrentPeriod | Empty = Field(alias="currentPeriod")
    feedback_is_active: bool = Field(alias="feedbackIsActive")
    left_feedback: bool = Field(alias="leftFeedback")
    has_services: bool = Field(alias="hasServices")

    class Period(BaseModel):
        key: int
        value: int | None
        title: str

    class LastSalary(BaseModel):
        value: int
        qualification: str
        specialization: str

    class CurrentPeriod(BaseModel):
        value: int
        qualification: str
        specialization: str

    class Empty(BaseModel):
        pass

