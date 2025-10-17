from dataclasses import dataclass

from domain.entities.messages import MessageEntity
from infrastructure.repositories.base.mongo import BaseMongoDBRepository
from infrastructure.repositories.converters import convert_message_entity_to_document
from infrastructure.repositories.messages.base import BaseMessagesRepository


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, chat_oid: str, message: MessageEntity) -> None:
        await self._collection.update_one(
            filter={"oid": chat_oid},
            update={
                "$push": {
                    "messages": convert_message_entity_to_document(message),
                },
            },
        )
