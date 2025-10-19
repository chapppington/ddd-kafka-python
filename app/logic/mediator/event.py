from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from domain.events.base import BaseEvent
from logic.events.base import (
    BaseEventHandler,
    EventResultType,
    EventType,
)


@dataclass(eq=False)
class EventMediator(ABC):
    events_map: dict[EventType, BaseEventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(
        self,
        event: EventType,
        event_handlers: Iterable[BaseEventHandler[EventType, EventResultType]],
    ): ...

    @abstractmethod
    async def publish(
        self,
        events: Iterable[BaseEvent],
    ) -> Iterable[EventResultType]: ...
