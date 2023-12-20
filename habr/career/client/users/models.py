from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl

type Username = str


class User(BaseModel):
    user: _User
    user_companies: list = Field(alias="userCompanies")  # TODO
    meta: Meta

    class Meta(BaseModel):
        logout_token: str = Field(alias="logoutToken")

    class _User(BaseModel):
        avatar_url: HttpUrl = Field(alias="avatarUrl")
        job_search_state: str = Field(alias="jobSearchState")
        alias: Username
        full_name: str = Field(alias="fullName")
        ga_uid_token: str = Field(alias="gaUidToken")
        can_edit_courses: bool = Field(alias="canEditCourses")
        is_expert: bool = Field(alias="isExpert")
        notification_counters: NotificationCounters = Field(
            alias="notificationCounters")
        salary_range: SalaryRange = Field(alias="salaryRange")

        class NotificationCounters(BaseModel):
            messages: int
            friends: int
            events: int

        class SalaryRange(BaseModel):
            from_: int | None = Field(alias="from")
            to: int
            unit: str
