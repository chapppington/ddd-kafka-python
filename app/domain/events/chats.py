from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewChatCreatedEvent(BaseEvent):
    chat_oid: str
    chat_title: str
