from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)

from domain.events.base import BaseEvent
from logic.commands.base import (
    BaseCommand,
    BaseCommandHandler,
    CommandResultType,
    CommandType,
)
from logic.events.base import (
    BaseEventHandler,
    EventResultType,
    EventType,
)
from logic.exceptions.mediator import CommandHandlersNotRegisteredException
from logic.mediator.command import CommandMediator
from logic.mediator.event import EventMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QueryResultType,
    QueryType,
)


@dataclass(eq=False)
class Mediator(EventMediator, QueryMediator, CommandMediator):
    events_map: dict[EventType, BaseEventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CommandType, BaseCommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[QueryType, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(
        self,
        event: EventType,
        event_handlers: Iterable[BaseEventHandler[EventType, EventResultType]],
    ):
        self.events_map[event].extend(event_handlers)

    def register_command(
        self,
        command: CommandType,
        command_handlers: Iterable[BaseCommandHandler[CommandType, CommandResultType]],
    ):
        self.events_map[command].extend(command_handlers)

    def register_query(
        self,
        query: QueryType,
        query_handler: BaseQueryHandler[QueryType, QueryResultType],
    ) -> QueryResultType:
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[EventResultType]:
        result = []

        for event in events:
            handlers: Iterable[BaseEventHandler[EventType, EventResultType]] = (
                self.events_map[event.__class__]
            )

            for handler in handlers:
                result.append(await handler.handle(event=event))

            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CommandResultType]:
        command_type = command.__class__
        handlers = self.events_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QueryResultType:
        return await self.queries_map[query.__class__].handle(query=query)
