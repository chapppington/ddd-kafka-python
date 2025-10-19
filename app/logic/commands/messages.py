from dataclasses import dataclass

from domain.entities.chats import ChatEntity
from domain.entities.messages import MessageEntity
from domain.value_objects.messages import TextValueObject
from infrastructure.repositories.chats.base import BaseChatsRepository
from infrastructure.repositories.messages.base import BaseMessagesRepository
from logic.commands.base import (
    BaseCommand,
    BaseCommandHandler,
)
from logic.exceptions.chats import ChatNotFoundException


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    text: str
    chat_oid: str


@dataclass(frozen=True)
class CreateMessageCommandHandler(BaseCommandHandler[CreateMessageCommand, ChatEntity]):
    messages_repository: BaseMessagesRepository
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateMessageCommand) -> MessageEntity:
        chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)

        if not chat:
            raise ChatNotFoundException(chat_oid=command.chat_oid)

        message = MessageEntity(
            chat_oid=command.chat_oid,
            text=TextValueObject(value=command.text),
        )
        chat.add_message(message)
        await self.messages_repository.add_message(
            message=message,
        )
        await self._mediator.publish(chat.pull_events())

        return message
