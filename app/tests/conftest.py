from pytest import fixture

from infrastructure.repositories.messages import (
    BaseChatRepository,
    DummyInMemoryChatRepository,
)
from logic.init import init_mediator
from logic.mediator import Mediator


@fixture(scope="package")
def chat_repository() -> DummyInMemoryChatRepository:
    return DummyInMemoryChatRepository()


@fixture(scope="package")
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
    return mediator
