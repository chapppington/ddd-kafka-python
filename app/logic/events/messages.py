from dataclasses import dataclass

from domain.events.chats import NewMessageReceivedEvent
from infrastructure.message_brokers.converters import convert_event_to_broker_message
from logic.events.base import BaseEventHandler


@dataclass
class NewMessageReceivedEventHandler(BaseEventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )
