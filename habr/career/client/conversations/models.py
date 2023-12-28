from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from habr.career.utils import Username


class Conversations(BaseModel):
    objects: dict[Username, Item] = Field(alias="conversationObjects")
    ids: list[Username] = Field(alias="conversationIds")
    meta: Meta

    class Meta(BaseModel):
        total_count: int | None = Field(None, alias="totalCount")
        total: int
        unread: int | None = None
        page: int
        per_page: int = Field(alias="perPage")

    class Item(BaseModel):
        full_name: str = Field(alias="fullName")
        avatar_url: HttpUrl = Field(alias="avatarUrl")
        login: Username
        subtitle: str | None
        conversation: Conversation
        banned: Banned
        is_expert: bool = Field(alias="isExpert")

        class Banned(BaseModel):
            status: bool
            message: str | None

        class Conversation(BaseModel):
            last_message: LastMessage | None = Field(alias="lastMessage")

            class LastMessage(BaseModel):
                body: str
                created_at: datetime = Field(alias="createdAt")
                is_mine: bool = Field(alias="isMine")
                is_read: bool = Field(alias="isRead")


class Message(BaseModel):
    id: int
    created_at: datetime = Field(alias="createdAt")
    body: str
    author_id: Username = Field(alias="authorId")
    is_mine: bool = Field(alias="isMine")


class Messages(BaseModel):
    data: list[Message]
    meta: Meta

    class Meta(BaseModel):
        total: int
        page: int
        per_page: int = Field(alias="perPage")


class Conversation(BaseModel):
    theme: str
    user_id: Username = Field(alias="userId")
    has_new_message: bool = Field(alias="hasNewMessage")
    banned: Banned
    messages: Messages

    class Banned(BaseModel):
        status: bool
        message: str | None


class Template(BaseModel):
    id: int
    title: str
    body: str


class Templates(BaseModel):
    templates: list[Template]


class Success(BaseModel):
    success: bool


class ChangeConversationSubjectSuccess(Success):
    new_theme: str = Field(alias="newTheme")


class ComplainConversationSuccess(BaseModel):
    status: bool
    message: str
