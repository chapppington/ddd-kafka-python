from datetime import datetime

from pydantic import BaseModel

from domain.entities.chats import ChatEntity
from domain.entities.messages import MessageEntity


class CreateChatRequestSchema(BaseModel):
    title: str


class CreateChatResponseSchema(BaseModel):
    oid: str
    title: str

    @classmethod
    def from_entity(cls, entity: ChatEntity) -> "CreateChatResponseSchema":
        return cls(
            oid=entity.oid,
            title=entity.title.as_generic_type(),
        )


class CreateMessageRequestSchema(BaseModel):
    text: str


class CreateMessageResponseSchema(BaseModel):
    oid: str
    text: str

    @classmethod
    def from_entity(cls, entity: MessageEntity) -> "CreateMessageResponseSchema":
        return cls(
            oid=entity.oid,
            text=entity.text.as_generic_type(),
        )


class MessageDetailSchema(BaseModel):
    oid: str
    text: str
    created_at: datetime


class ChatDetailSchema(BaseModel):
    oid: str
    title: str
    created_at: datetime

    @classmethod
    def from_entity(cls, chat: ChatEntity) -> "ChatDetailSchema":
        return cls(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )
