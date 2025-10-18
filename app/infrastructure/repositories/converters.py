from typing import (
    Any,
    Mapping,
)

from domain.entities.chats import ChatEntity
from domain.entities.messages import MessageEntity
from domain.value_objects.chats import TitleValueObject
from domain.value_objects.messages import TextValueObject


def convert_message_entity_to_document(message: MessageEntity) -> dict:
    return {
        "oid": message.oid,
        "chat_oid": message.chat_oid,
        "text": message.text.as_generic_type(),
        "created_at": message.created_at,
        "updated_at": message.updated_at,
    }


def convert_chat_entity_to_document(chat: ChatEntity) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
        "updated_at": chat.updated_at,
    }


def convert_message_document_to_entity(
    message_document: Mapping[str, Any],
) -> MessageEntity:
    return MessageEntity(
        oid=message_document["oid"],
        chat_oid=message_document["chat_oid"],
        text=TextValueObject(value=message_document["text"]),
        created_at=message_document["created_at"],
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> ChatEntity:
    return ChatEntity(
        oid=chat_document["oid"],
        title=TitleValueObject(value=chat_document["title"]),
        created_at=chat_document["created_at"],
    )
