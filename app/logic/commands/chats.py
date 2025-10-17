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
    chat_repository: BaseChatsRepository

    async def handle(self, command: CreateChatCommand) -> ChatEntity:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise ChatAlreadyExistsException(command.title)

        title = TitleValueObject(value=command.title)

        new_chat = ChatEntity.create_chat(title=title)

        # TODO считать ивенты
        await self.chat_repository.add_chat(new_chat)

        return new_chat
