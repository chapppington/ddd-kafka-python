from infrastructure.repositories.chats.base import BaseChatsRepository
from infrastructure.repositories.chats.memory import DummyInMemoryChatsRepository
from punq import (
    Container,
    Scope,
)

from logic.init import _init_container


def init_dummy_container() -> Container:
    container = _init_container()

    container.register(
        BaseChatsRepository,
        DummyInMemoryChatsRepository,
        scope=Scope.singleton,
    )

    return container
