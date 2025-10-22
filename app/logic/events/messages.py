from dataclasses import dataclass

from domain.events.chats import NewMessageReceivedEvent
from infrastructure.message_brokers.converters import convert_event_to_broker_message
from logic.events.base import BaseEventHandler


@dataclass
class NewMessageReceivedEventHandler(BaseEventHandler[NewMessageReceivedEvent, None]):
    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic.format(chat_oid=event.chat_oid),
            value=convert_event_to_broker_message(event=event),
            key=event.chat_oid.encode(),
        )
