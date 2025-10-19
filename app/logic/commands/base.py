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

from logic.mediator.event import EventMediator


@dataclass(frozen=True)
class BaseCommand(ABC): ...


CommandType = TypeVar("CommandType", bound=BaseCommand)
CommandResultType = TypeVar("CommandResultType", bound=Any)


@dataclass(frozen=True)
class BaseCommandHandler(ABC, Generic[CommandType, CommandResultType]):
    _mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CommandType) -> CommandResultType: ...
