from dataclasses import dataclass

from infrastructure.repositories.base.mongo import BaseMongoDBRepository
from infrastructure.repositories.chats.base import BaseChatsRepository
from infrastructure.repositories.converters import (
    convert_chat_document_to_entity,
    convert_chat_entity_to_document,
)

from domain.entities.chats import ChatEntity


@dataclass
class MongoDBChatsRepository(BaseChatsRepository, BaseMongoDBRepository):
    async def get_chat_by_oid(self, oid: str) -> ChatEntity | None:
        chat_document = await self._collection.find_one(filter={"oid": oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={"title": title}))

    async def add_chat(self, chat: ChatEntity) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))
