from dataclasses import dataclass
from typing import ClassVar

from infrastructure.message_brokers.converters import convert_event_to_broker_message

from domain.events.chats import NewMessageReceivedEvent
from logic.events.base import (
    BaseEventHandler,
    IntegrationEvent,
)


@dataclass
class NewMessageReceivedEventHandler(BaseEventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic.format(chat_oid=event.chat_oid),
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )


@dataclass
class NewMessageReceivedFromBrokerEvent(IntegrationEvent):
    event_title: ClassVar[str] = "New Message From Broker Received"

    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewMessageReceivedFromBrokerEventHandler(
    BaseEventHandler[NewMessageReceivedFromBrokerEvent, None],
):
    async def handle(self, event: NewMessageReceivedFromBrokerEvent) -> None:
        await self.connection_manager.send_all(
            key=event.chat_oid,
            bytes_=convert_event_to_broker_message(event=event),
        )
