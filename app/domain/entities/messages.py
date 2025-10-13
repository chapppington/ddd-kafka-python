from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity
from domain.value_objects.messages import (
    TextValueObject,
    TitleValueObject,
)


@dataclass
class MessageEntity(BaseEntity):
    text: TextValueObject


@dataclass
class ChatEntity(BaseEntity):
    title: TitleValueObject
    messages: list[MessageEntity] = field(default_factory=list, kw_only=True)

    def add_message(self, message: MessageEntity):
        self.messages.append(message)
