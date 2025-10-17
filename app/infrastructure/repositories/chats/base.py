from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities.chats import ChatEntity


@dataclass
class BaseChatsRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool: ...

    @abstractmethod
    async def add_chat(self, chat: ChatEntity): ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> ChatEntity | None: ...
