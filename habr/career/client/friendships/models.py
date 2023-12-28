from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from habr.career.utils import Username


class FriendshipBase(BaseModel):
    list: list[Friends]
    meta: Meta

    class Friends(BaseModel):
        id: Username
        title: str
        subtitle: str | None
        href: str
        friendship: Literal["accepted", "incoming"]
        avatar: Avatar
        is_expert: bool = Field(alias="isExpert")

        class Avatar(BaseModel):
            alt: Username
            src: HttpUrl
            src2x: HttpUrl

    class Meta(BaseModel):
        current_page: int = Field(alias="currentPage")
        total_pages: int = Field(alias="totalPages")
        per_page: int = Field(alias="perPage")


class Friends(FriendshipBase):
    pass


class FriendshipRequests(FriendshipBase):
    pass


class Result(BaseModel):
    status: Literal["accepted", "cancelled", "pending", "none"]
