from dataclasses import (
    dataclass,
    field,
)

from domain.entities.chats import ChatEntity
from infrastructure.repositories.chats.base import BaseChatsRepository


@dataclass
class DummyInMemoryChatsRepository(BaseChatsRepository):
    _saved_chats: list[ChatEntity] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return (
                next(
                    chat
                    for chat in self._saved_chats
                    if chat.title.as_generic_type() == title
                )
                is not None
            )
        except StopIteration:
            return False

    async def add_chat(self, chat: ChatEntity):
        self._saved_chats.append(chat)

    async def get_chat_by_oid(self, oid: str) -> ChatEntity | None:
        try:
            return next(chat for chat in self._saved_chats if chat.oid == oid)
        except StopIteration:
            return None
