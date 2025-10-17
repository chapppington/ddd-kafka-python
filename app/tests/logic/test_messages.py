import pytest
from faker import Faker

from domain.entities.messages import ChatEntity
from domain.value_objects.messages import TitleValueObject
from infrastructure.repositories.messages.base import BaseChatRepository
from logic.commands.messages import CreateChatCommand
from logic.exceptions.messages import ChatAlreadyExistsException
from logic.mediator import Mediator


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
):
    chat: ChatEntity
    chat, *_ = await mediator.handle_command(CreateChatCommand(title=faker.text()[:50]))

    assert await chat_repository.check_chat_exists_by_title(
        title=chat.title.as_generic_type(),
    )


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
    faker: Faker,
):
    title_text = faker.text()[:50]
    chat = ChatEntity(title=TitleValueObject(value=title_text))
    await chat_repository.add_chat(chat)

    assert chat in chat_repository._saved_chats

    with pytest.raises(ChatAlreadyExistsException):
        await mediator.handle_command(CreateChatCommand(title=title_text))

    assert len(chat_repository._saved_chats) == 1
