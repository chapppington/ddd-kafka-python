from dataclasses import dataclass
from typing import Generic

from infrastructure.repositories.chats.base import BaseChatsRepository
from infrastructure.repositories.messages.base import BaseMessagesRepository

from domain.entities.chats import ChatEntity
from logic.exceptions.chats import ChatNotFoundException
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QueryResultType,
    QueryType,
)


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetChatDetailQueryHandler(
    BaseQueryHandler,
    Generic[QueryResultType, QueryType],
):
    chats_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository  # TODO: забирать сообщения отдельно

    async def handle(self, query: GetChatDetailQuery) -> ChatEntity:
        chat = await self.chats_repository.get_chat_by_oid(oid=query.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat
