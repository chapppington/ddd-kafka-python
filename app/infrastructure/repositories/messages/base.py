from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.messages import MessageEntity


@dataclass
class BaseMessagesRepository(ABC):
    @abstractmethod
    async def add_message(self, message: MessageEntity): ...
