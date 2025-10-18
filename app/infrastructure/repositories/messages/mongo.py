from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import MessageEntity
from infrastructure.repositories.base.mongo import BaseMongoDBRepository
from infrastructure.repositories.converters import (
    convert_message_document_to_entity,
    convert_message_entity_to_document,
)
from infrastructure.repositories.filters.messages import GetMessagesFilters
from infrastructure.repositories.messages.base import BaseMessagesRepository


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, message: MessageEntity) -> None:
        await self._collection.insert_one(convert_message_entity_to_document(message))

    async def get_messages(
        self,
        chat_oid: str,
        filters: GetMessagesFilters,
    ) -> tuple[Iterable[MessageEntity], int]:
        find = {"chat_oid": chat_oid}

        cursor = self._collection.find(find).limit(filters.limit).skip(filters.offset)

        messages = [
            convert_message_document_to_entity(message) async for message in cursor
        ]

        total = await self._collection.count_documents(find)

        return messages, total
