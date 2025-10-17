from typing import (
    Any,
    Mapping,
)

from domain.entities.chats import ChatEntity
from domain.entities.messages import MessageEntity


def convert_message_entity_to_document(message: MessageEntity) -> dict:
    return {
        "oid": message.oid,
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
        "messages": [
            convert_message_entity_to_document(message) for message in chat.messages
        ],
    }


def convert_message_document_to_entity(
    message_document: Mapping[str, Any],
) -> MessageEntity:
    return MessageEntity(
        text=message_document["text"],
        oid=message_document["oid"],
        created_at=message_document["created_at"],
        updated_at=message_document["updated_at"],
    )


def convert_chat_document_to_entity(chat_document: Mapping[str, Any]) -> ChatEntity:
    return ChatEntity(
        title=chat_document["title"],
        oid=chat_document["oid"],
        created_at=chat_document["created_at"],
        messages={
            convert_message_document_to_entity(message_document)
            for message_document in chat_document["messages"]
        },
    )
