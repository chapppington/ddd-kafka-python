from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)

from domain.events.base import BaseEvent
from infrastructure.message_brokers.base import BaseMessageBroker


EventType = TypeVar("EventType", bound=BaseEvent)
EventResultType = TypeVar("EventResultType", bound=Any)


@dataclass
class BaseEventHandler(ABC, Generic[EventType, EventResultType]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = None

    @abstractmethod
    def handle(self, event: EventType) -> EventResultType: ...
