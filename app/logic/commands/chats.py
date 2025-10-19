from dataclasses import dataclass

from domain.entities.chats import ChatEntity
from domain.value_objects.chats import TitleValueObject
from infrastructure.repositories.chats.base import BaseChatsRepository
from logic.commands.base import (
    BaseCommand,
    BaseCommandHandler,
)
from logic.exceptions.chats import ChatAlreadyExistsException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class CreateChatCommandHandler(BaseCommandHandler[CreateChatCommand, ChatEntity]):
    chats_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> ChatEntity:
        if await self.chats_repository.check_chat_exists_by_title(command.title):
            raise ChatAlreadyExistsException(command.title)

        title = TitleValueObject(value=command.title)

        new_chat = ChatEntity.create_chat(title=title)

        await self.chats_repository.add_chat(new_chat)
        await self._mediator.publish(new_chat.pull_events())

        return new_chat
