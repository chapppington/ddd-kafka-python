from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity
from domain.events.messages import NewMessageReceivedEvent
from domain.value_objects.messages import (
    TextValueObject,
    TitleValueObject,
)


@dataclass(eq=False)
class MessageEntity(BaseEntity):
    text: TextValueObject


@dataclass(eq=False)
class ChatEntity(BaseEntity):
    title: TitleValueObject
    messages: list[MessageEntity] = field(default_factory=list, kw_only=True)

    def add_message(self, message: MessageEntity):
        self.messages.append(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                message_oid=message.oid,
                chat_oid=self.oid,
            ),
        )
