from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity
from domain.entities.messages import MessageEntity
from domain.events.chats import (
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from domain.value_objects.chats import TitleValueObject


@dataclass(eq=False)
class ChatEntity(BaseEntity):
    title: TitleValueObject
    messages: set[MessageEntity] = field(
        default_factory=set,
        kw_only=True,
    )

    @classmethod
    def create_chat(cls, title: TitleValueObject) -> "ChatEntity":
        new_chat = cls(title=title)
        new_chat.register_event(
            NewChatCreatedEvent(
                chat_oid=new_chat.oid,
                chat_title=new_chat.title.as_generic_type(),
            ),
        )

        return new_chat

    def add_message(self, message: MessageEntity):
        self.messages.add(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                chat_oid=self.oid,
                message_oid=message.oid,
            ),
        )
