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


EventType = TypeVar("EventType", bound=BaseEvent)
EventResultType = TypeVar("EventResultType", bound=Any)


@dataclass(frozen=True)
class BaseEventHandler(ABC, Generic[EventType, EventResultType]):
    @abstractmethod
    def handle(self, event: EventType) -> EventResultType: ...
