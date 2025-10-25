from dataclasses import dataclass

from infrastructure.message_brokers.converters import convert_event_to_broker_message

from domain.events.chats import NewChatCreatedEvent
from logic.events.base import BaseEventHandler


@dataclass
class NewChatCreatedEventHandler(BaseEventHandler[NewChatCreatedEvent, None]):
    async def handle(self, event: NewChatCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )
