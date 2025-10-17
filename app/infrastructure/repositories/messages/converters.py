from domain.entities.messages import (
    ChatEntity,
    MessageEntity,
)


def convert_message_to_document(message: MessageEntity) -> dict:
    return {
        "oid": message.oid,
        "text": message.text.as_generic_type(),
    }


def convert_chat_entity_to_document(chat: ChatEntity) -> dict:
    return {
        "oid": chat.oid,
        "title": chat.title.as_generic_type(),
        "created_at": chat.created_at,
        "messages": [convert_message_to_document(message) for message in chat.messages],
    }
