from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import MessageEntity
from infrastructure.repositories.filters.messages import GetMessagesFilters


@dataclass
class BaseMessagesRepository(ABC):
    @abstractmethod
    async def add_message(self, message: MessageEntity): ...

    @abstractmethod
    async def get_messages(
        self,
        filters: GetMessagesFilters,
    ) -> Iterable[MessageEntity]: ...
