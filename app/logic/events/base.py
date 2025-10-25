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

from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.websockets.managers import BaseConnectionManager

from domain.events.base import BaseEvent


EventType = TypeVar("EventType", bound=BaseEvent)
EventResultType = TypeVar("EventResultType", bound=Any)


@dataclass
class IntegrationEvent(BaseEvent, ABC): ...


@dataclass
class BaseEventHandler(ABC, Generic[EventType, EventResultType]):
    message_broker: BaseMessageBroker
    connection_manager: BaseConnectionManager
    broker_topic: str | None = None

    @abstractmethod
    def handle(self, event: EventType) -> EventResultType: ...
