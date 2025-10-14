from pydantic import BaseModel

from domain.entities.messages import ChatEntity


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
