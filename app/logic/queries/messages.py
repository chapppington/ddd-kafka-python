from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import MessageEntity
from infrastructure.repositories.filters.messages import GetMessagesFilters
from infrastructure.repositories.messages.base import BaseMessagesRepository
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilters


@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    messages_repository: BaseMessagesRepository

    async def handle(self, query: GetMessagesQuery) -> Iterable[MessageEntity]:
        return await self.messages_repository.get_messages(
            chat_oid=query.chat_oid,
            filters=query.filters,
        )
